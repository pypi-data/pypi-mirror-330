from threading import Lock, Thread
import time
import json
from datetime import datetime
from airosentris.client.RabbitMQClient import RabbitMQClient
from airosentris.config.ConfigFetcher import get_config
from airosentris.logger.Logger import Logger


class TrainerLogger:
    """
    TrainerLogger is responsible for logging training activity to RabbitMQ.
    It ensures that training-related logs such as commands, metrics, and statuses
    are published reliably.
    """

    _instance = None
    _lock = Lock()

    def __new__(cls, *args, **kwargs):
        """
        Ensure only one instance of TrainerLogger is created.
        """
        if not cls._instance:
            with cls._lock:  # Thread-safe initialization
                if not cls._instance:  # Double-checked locking
                    cls._instance = super(TrainerLogger, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """
        Initializes the RabbitMQ client and logger.
        """
        if not hasattr(self, "initialized"):
            self.logger = Logger(__name__)
            self.logger.info("🚀 Initializing TrainerLogger...")

            config = get_config()
            self.rabbitmq_client = RabbitMQClient(config=config, name="trainer_logger")
            self.setup_rabbitmq_client()
            self.exchange_name = "airosentris.status"
            self.initialized = True

            self.current_status = None
            self.prev_status = None
            self.status_thread = None
            self.status_thread_stop = False 

            self.logger.info("✅ TrainerLogger initialized successfully.")

    def setup_rabbitmq_client(self):
        """
        Sets up the RabbitMQ connection, declares the exchange, and binds the queue.
        """
        try:
            self.rabbitmq_client.connect()
            self.rabbitmq_client.declare_exchange("airosentris.status")
            self.rabbitmq_client.declare_queue("airosentris.status.queue")
            self.rabbitmq_client.bind_queue("airosentris.agent", "airosentris.status.queue", "")
            self.logger.info("✅ RabbitMQ setup complete for TrainerLogger.")
        except Exception as e:
            self.logger.error(f"❌ Error setting up RabbitMQ: {e}")

    def _prepare_log_message(self, project_id: str, run_id: str, log_type: str, data: dict | str) -> str:
        """
        Prepares a structured log message in JSON format.

        Args:
            project_id (str): Project ID associated with the log.
            run_id (str): Training run ID.
            log_type (str): Type of log (command, metric, status).
            data (dict | str): Log content.

        Returns:
            str: JSON formatted log message.
        """
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return json.dumps({
            "project_id": project_id,
            "run_id": run_id,
            "type": log_type,
            "time": current_time,
            "data": data if isinstance(data, str) else json.dumps(data)
        })
    
    def log_command(self, project_id: str, run_id: str, command: str) -> None:
        """
        Logs a command executed during training.

        Args:
            project_id (str): The ID of the project.
            run_id (str): The ID of the training run.
            command (str): The command executed.
        """
        try:
            message = self._prepare_log_message(project_id, run_id, "command", command)
            self.rabbitmq_client.publish_message(self.exchange_name, "", message)
            self.logger.info(f"📜 Command log sent: {command}")
        except Exception as e:
            self.logger.error(f"❌ Failed to log command: {e}")
    
    def log_metric(self, project_id: str, run_id: str, metrics: dict) -> None:
        """
        Mencatat metrik hasil pelatihan.

        Args:
            project_id (str): ID proyek.
            run_id (str): ID pelatihan atau proses.
            metrics (dict): Data metrik pelatihan.
        """
        message = self._prepare_log_message(project_id, run_id, "metric", metrics)
        self.rabbitmq_client.publish_message(self.exchange_name, "", message)
        self.logger.info(f"📈 Metric log sent")

    def log_status(self, project_id: str, run_id: str, status: str) -> None:
        """
        Logs training status updates (e.g., 'Started', 'In Progress', 'Completed').

        - Stops the previous status update thread when a new status is received.
        - Starts a new thread that continuously sends the latest status at 1-second intervals.

        Args:
            project_id (str): ID of the project.
            run_id (str): Training run ID.
            status (str): Training status.
        """
        with self._lock:
            if self.current_status == status:
                self.logger.debug(f"🔄 Status unchanged ({status}). No new thread started.")
                return

            # Stop the previous status thread
            if self.status_thread and self.status_thread.is_alive():
                self.logger.info(f"🛑 Stopping previous status thread for {run_id}...")
                self.status_thread_stop = True
                self.status_thread.join()  # Wait for thread to stop

            # Update the current status
            self.current_status = status
            self.status_thread_stop = False
            self.logger.info(f"🚦 Status changed: {status}")

            # Define function for status logging in a separate thread
            def status_logging():
                """
                Runs in a separate thread to send status logs at 1-second intervals.
                """
                thread_rmq_client = RabbitMQClient(config=get_config(), name="trainer_logger_thread")
                thread_rmq_client.connect()
                self.logger.info(f"📡 Starting status update thread for {run_id}...")

                while not self.status_thread_stop:
                    try:
                        
                        message = self._prepare_log_message(project_id, run_id, "status", self.current_status)
                        thread_rmq_client.publish_message(self.exchange_name, "", message)
                        if self.current_status != self.prev_status:
                            self.logger.info(f"🚦 Status changed: {self.prev_status} ➝ {self.current_status}")
                            self.prev_status = self.current_status  # Update the previous status

                        if self.current_status == "End":
                            self.logger.info(f"✅ Status thread for {run_id} completed.")
                            break
                        time.sleep(1)
                    except Exception as e:
                        self.logger.error(f"❌ Error logging status: {e}")
                        break

                thread_rmq_client.close()
                self.logger.info(f"🛑 Status thread for {run_id} stopped.")

            # Start a new thread for continuous status logging
            self.status_thread = Thread(target=status_logging, daemon=True)
            self.status_thread.start()
