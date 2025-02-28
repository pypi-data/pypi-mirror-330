import os
import tempfile
import time
from abc import ABC, abstractmethod
from minio import Minio
import pika

from airosentris import Config
from airosentris.client.APIClient import APIClient
from airosentris.config.ConfigFetcher import get_config
from airosentris.logger.Logger import Logger
from airosentris.message.Comment import Comment


class BaseRunner(ABC):

    def __init__(self):
        self.rabbitmq_config = get_config()
        self.rabbitmq_connection = None
        self.rabbitmq_channel = None
        self.api_client = APIClient()
        self.logger = Logger(__name__)

    def download_model(self, run_id: str):
        """Download the model associated with a specific run_id."""
        try:
            import airosentris
            config = airosentris.Config
            minio_client = Minio(
                config.MINIO_ENDPOINT.replace("http://", "").replace("https://", ""),
                access_key=config.MINIO_ACCESS_KEY,
                secret_key=config.MINIO_SECRET_KEY,
                secure=False,
            )
            with tempfile.TemporaryDirectory() as tmp_dir:
                download_path = os.path.join(tmp_dir, f"{run_id}.zip")
                model_path = f"artifacts/models/{run_id}/"
                minio_client.fget_object(config.MINIO_BUCKET, f"model/{run_id}.zip", download_path)
                os.system(f"unzip -o {download_path} -d {model_path}")
                self.logger.info(f"Model downloaded for {run_id} at {model_path}")
                return model_path
        except Exception as e:
            self.logger.error(f"Error downloading model for {run_id}: {e}")
        return None
        
    @abstractmethod
    def evaluate(self, comment: Comment):
        pass

    @abstractmethod
    def load_model(self, scope_code, model_path):
        pass

    def send_tag_to_api(self, comment_id, scope_code, scope_label_code):
        """ Method to send the tag to the API """

        endpoint = "api/v1/comment/tag/agent"        

        payload = {
            "comment_id": comment_id,
            "scopes_code": scope_code,
            "scopes_label_code": scope_label_code
        }

        try:
            response = self.api_client.post_data(endpoint=endpoint, data=payload)
            if response.status_code == 200:
                self.logger.info(f"Successfully tagged comment {comment_id} with {scope_code}: {scope_label_code}")
            else:
                self.logger.error(f"Failed to tag comment {comment_id} with {scope_code}: {scope_label_code}, Response: {response.text}")
        except Exception as e:
            self.logger.error(f"Error sending tag to API: {e}")