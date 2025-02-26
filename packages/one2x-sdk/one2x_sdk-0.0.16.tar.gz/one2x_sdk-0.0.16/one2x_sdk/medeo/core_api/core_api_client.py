import os
import requests
from one2x_sdk.utils.logger import get_default_logger


class CoreApiClient:
    def __init__(self, base_url=None, token=None, enable_requests=None, logger=None):
        self.base_url = base_url or os.getenv(
            "MEDEO_CORE_API_BASE_URL", "http://localhost:3000"
        )
        self.token = token or os.getenv("MEDEO_CORE_API_AUTH_TOKEN", "default-token")
        self.logger = logger
        self.enable_requests = (
            enable_requests
            if enable_requests is not None
            else os.getenv("MEDEO_CORE_API_ENABLE_REQUESTS", "false").lower() in "true"
        )

        self.logger = logger or get_default_logger('CoreApiClient')
        self.session = requests.Session()

    def _build_headers(self):
        headers = {"Content-Type": "application/json", "Cookie": f"medeo-service-auth-token={self.token}"}
        return headers

    def request(self, method, api_path, params=None, data=None, json=None):
        if not self.enable_requests:
            self.logger.info(
                f"Skipping request to {api_path} in non-production environment"
            )
            return None

        url = f"{self.base_url}/{api_path.strip('/')}"
        headers = self._build_headers()

        result = self.session.request(
            method=method.upper(),
            url=url,
            params=params,
            data=data,
            json=json,
            headers=headers,
            timeout=10,
        )

        if result.status_code in [429, 502]:
            error_msg = {
                429: "Rate limit exceeded",
                502: "Bad Gateway error"
            }[result.status_code]
            self.logger.warning(f"{error_msg} for {url}")
            return None

        result.raise_for_status()

        if not result.text.strip():
            return None
        return result.json()