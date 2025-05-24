from dataclasses import dataclass
from typing import Optional, Dict, Any
import requests


@dataclass
class PBXConfig:
    """Configuration for PBX API access."""
    organization_id: str
    api_key: str
    base_url: str = "https://etw-pbx-cloud1.websprix.com/api/v2"


class SipMiddleware:
    """Simple middleware for interacting with the PBX API."""

    def __init__(self, config: PBXConfig):
        self.config = config

    def _headers(self) -> Dict[str, str]:
        return {"x-api-key": self.config.api_key}

    def get_connection_details(self, extension: str) -> Dict[str, Any]:
        """Fetch SIP connection details for the given extension."""
        url = (
            f"{self.config.base_url}/onboard//get_ip_info/"
            f"{self.config.organization_id}/{extension}/1"
        )
        response = requests.get(url, headers=self._headers())
        response.raise_for_status()
        return response.json()

    def add_to_queue(self, queue_name: str, extension: str) -> Dict[str, Any]:
        interface = f"{self.config.organization_id}S{extension}"
        url = f"{self.config.base_url}/member/{self.config.organization_id}/add"
        payload = {"queue_name": queue_name, "interface": interface}
        response = requests.post(url, json=payload, headers=self._headers())
        response.raise_for_status()
        return response.json()

    def remove_from_queue(self, queue_name: str, extension: str) -> Dict[str, Any]:
        interface = f"{self.config.organization_id}S{extension}"
        url = f"{self.config.base_url}/member/{self.config.organization_id}/remove"
        payload = {"queue_name": queue_name, "interface": interface}
        response = requests.delete(url, json=payload, headers=self._headers())
        response.raise_for_status()
        return response.json()

    def get_queue_status(self, extension: str) -> Dict[str, Any]:
        interface = f"{self.config.organization_id}S{extension}"
        url = (
            f"{self.config.base_url}/member/{self.config.organization_id}/"
            f"queues_for_agent?interface={interface}"
        )
        response = requests.get(url, headers=self._headers())
        response.raise_for_status()
        return response.json()

    def fetch_call_logs(self, extension: str, direction: str = "in") -> Dict[str, Any]:
        url = (
            f"{self.config.base_url}/cust_ext/{self.config.organization_id}/"
            f"call_logs/{extension}?dir={direction}"
        )
        response = requests.get(url, headers=self._headers())
        response.raise_for_status()
        return response.json()

    def fetch_offhour_callers(self, queue_name: str) -> Dict[str, Any]:
        url = (
            f"{self.config.base_url}/new-report/{self.config.organization_id}/"
            f"{queue_name}/off-hour-callers?page=1&per_page=100"
        )
        response = requests.get(url, headers=self._headers())
        response.raise_for_status()
        return response.json()

    def fetch_users_for_transfer(self) -> Dict[str, Any]:
        url = f"{self.config.base_url}/cust_ext/{self.config.organization_id}/cust"
        response = requests.get(url, headers=self._headers())
        response.raise_for_status()
        return response.json()
