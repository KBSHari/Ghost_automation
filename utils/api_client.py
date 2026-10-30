"""Thin HTTP client used only for test setup and teardown (users, settings, seed data).

The assertions in the UI tests are made through the browser, not through this client.
"""
from dataclasses import dataclass

import requests

from config import settings

DEFAULT_PARAMETERS = {
    "allowFractional": True,
    "allowSells": True,
    "cashReserveAmount": 0,
    "cashReservePercentage": 0,
    "driftThreshold": 0,
    "flatFee": 0,
    "minTradeValue": 0,
    "percentageFee": 0,
}


@dataclass
class TestUser:
    __test__ = False  # not a pytest class

    access_token: str
    auth_token: str
    role: str


class ApiClient:
    def __init__(self, base_url: str = settings.API_URL):
        self.base_url = f"{base_url}/api/v1"

    def _headers(self, auth_token: str) -> dict:
        return {"Authorization": f"Bearer {auth_token}"}

    def signup(self) -> TestUser:
        response = requests.post(f"{self.base_url}/user", json={}, timeout=30)
        response.raise_for_status()
        body = response.json()
        return TestUser(body["accessToken"], body["authToken"], body["role"])

    def set_experimental_features(self, auth_token: str, enabled: bool) -> None:
        response = requests.put(
            f"{self.base_url}/user/setting",
            json={"isExperimentalFeatures": enabled},
            headers=self._headers(auth_token),
            timeout=30,
        )
        response.raise_for_status()

    def list_models(self, auth_token: str) -> requests.Response:
        return requests.get(
            f"{self.base_url}/rebalancing/models",
            headers=self._headers(auth_token),
            timeout=30,
        )

    def create_model(self, auth_token: str, name: str, asset_classes: list[dict]) -> dict:
        response = requests.post(
            f"{self.base_url}/rebalancing/models",
            json={
                "name": name,
                "parameters": DEFAULT_PARAMETERS,
                "targets": {"assetClasses": asset_classes},
            },
            headers=self._headers(auth_token),
            timeout=30,
        )
        response.raise_for_status()
        return response.json()

    def delete_user(self, user: TestUser) -> None:
        # Best effort clean-up; ignore failures so a teardown never hides a test result
        try:
            requests.delete(
                f"{self.base_url}/user",
                json={"accessToken": user.access_token},
                headers=self._headers(user.auth_token),
                timeout=30,
            )
        except requests.RequestException:
            pass
