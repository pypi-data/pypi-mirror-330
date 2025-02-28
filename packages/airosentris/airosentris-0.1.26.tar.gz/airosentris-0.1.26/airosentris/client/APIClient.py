import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from airosentris import Config
from airosentris.logger.Logger import Logger


class APIClient:
    """A reusable API client for interacting with the main application."""

    def __init__(self):
        if not Config.API_URL or not Config.API_TOKEN:
            raise ValueError("❌ API_URL or API_TOKEN is missing. Please initialize the airosentris package with valid config.")

        self.api_url = Config.API_URL
        self.api_token = Config.API_TOKEN
        self.session = requests.Session()
        self.logger = Logger(__name__)

        self._setup_session()

        self.logger.info(f"✅ [APIClient Initialized]")

    def _setup_session(self):
        """Set up the session with retries and logging."""
        retries = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retries)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def _build_url(self, endpoint):
        """Construct the full URL for the API endpoint."""
        return f"{self.api_url}/{endpoint}"

    def _build_headers(self):
        """Build the headers for API requests."""
        return {"Authorization": f"Bearer {self.api_token}"}

    def fetch_data(self, endpoint, timeout=10):
        """Fetch data from the specified API endpoint."""
        url = self._build_url(endpoint)
        headers = self._build_headers()

        self.logger.info(f"📡 [GET] Fetching data from {url}")

        try:
            response = self.session.get(url, headers=headers, timeout=timeout)
            response.raise_for_status()
            response_data = response.json()

            if not response_data.get("success", True):
                error_message = response_data.get("message", "Unknown error")
                self.logger.error(f"❌ [GET] Fetch failed: {error_message}")
                raise Exception(error_message)

            self.logger.info(f"✅ [GET] Data fetched successfully from {url}")
            return response_data
        except requests.RequestException as e:
            self.logger.error(f"❌ [GET] Request failed: {e}")
            raise

    def post_data(self, endpoint, data, files=None, timeout=10):
        """Post data to the specified API endpoint."""
        url = self._build_url(endpoint)
        headers = self._build_headers()

        self.logger.info(f"📡 [POST] Sending data to {url}")

        try:
            response = self.session.post(url, headers=headers, json=data, files=files, timeout=timeout)
            response.raise_for_status()
            response_data = response.json()

            if not response_data.get("success", True):
                error_message = response_data.get("message", "Unknown error")
                self.logger.error(f"❌ [POST] Upload failed: {error_message}")
                raise Exception(error_message)

            self.logger.info(f"✅ [POST] Data uploaded successfully to {url}")
            return response_data
        except requests.RequestException as e:
            self.logger.error(f"❌ [POST] Request failed: {e}")
            raise

    def delete_data(self, endpoint, timeout=10):
        """Send a DELETE request to the specified API endpoint."""
        url = self._build_url(endpoint)
        headers = self._build_headers()

        self.logger.info(f"📡 [DELETE] Removing data at {url}")

        try:
            response = self.session.delete(url, headers=headers, timeout=timeout)
            response.raise_for_status()
            response_data = response.json()

            if not response_data.get("success", True):
                error_message = response_data.get("message", "Unknown error")
                self.logger.error(f"❌ [DELETE] Failed: {error_message}")
                raise Exception(error_message)

            self.logger.info(f"✅ [DELETE] Data removed successfully from {url}")
            return response_data
        except requests.RequestException as e:
            self.logger.error(f"❌ [DELETE] Request failed: {e}")
            raise

    def put_data(self, endpoint, data, timeout=10):
        """Send a PUT request to the specified API endpoint."""
        url = self._build_url(endpoint)
        headers = self._build_headers()

        self.logger.info(f"📡 [PUT] Updating data at {url}")

        try:
            response = self.session.put(url, headers=headers, json=data, timeout=timeout)
            response.raise_for_status()
            response_data = response.json()

            if not response_data.get("success", True):
                error_message = response_data.get("message", "Unknown error")
                self.logger.error(f"❌ [PUT] Update failed: {error_message}")
                raise Exception(error_message)

            self.logger.info(f"✅ [PUT] Data updated successfully at {url}")
            return response_data
        except requests.RequestException as e:
            self.logger.error(f"❌ [PUT] Request failed: {e}")
            raise
