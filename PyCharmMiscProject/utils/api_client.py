import requests
from utils.config import API_BASE_URL


class APIClient:
    def __init__(self):
        self.base_url = API_BASE_URL
        self.headers = {
            "Content-Type": "application/json",
            "User-Agent": "api-tests/1.0",
        }

    def get_users(self):
        return requests.get(
            f"{self.base_url}/users",
            headers=self.headers,
            timeout=10,
        )

    def get_single_user(self, user_id):
        return requests.get(
            f"{self.base_url}/users/{user_id}",
            headers=self.headers,
            timeout=10,
        )

    def create_user(self, name, job):
        payload = {"name": name, "job": job}
        return requests.post(
            f"{self.base_url}/users",
            json=payload,
            headers=self.headers,
            timeout=10,
        )

    def update_user(self, user_id, name, job):
        payload = {"id": user_id, "name": name, "job": job}
        return requests.put(
            f"{self.base_url}/users/{user_id}",
            json=payload,
            headers=self.headers,
            timeout=10,
        )

    def delete_user(self, user_id):
        return requests.delete(
            f"{self.base_url}/users/{user_id}",
            headers=self.headers,
            timeout=10,
        )