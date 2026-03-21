import logging
import os
import requests
from utils.config import API_BASE_URL

logger = logging.getLogger(__name__)


class APIClient:
    def __init__(self):
        self.base_url = API_BASE_URL
        self.headers = {
            "Content-Type": "application/json",
            "User-Agent": "api-tests/1.0",
        }
        api_key = os.getenv("REQRES_API_KEY")
        if api_key:
            self.headers["x-api-key"] = api_key

    def get_users(self):
        logger.info("GET %s/users", self.base_url)
        return requests.get(f"{self.base_url}/users", headers=self.headers, timeout=10)

    def get_single_user(self, user_id):
        logger.info("GET %s/users/%s", self.base_url, user_id)
        return requests.get(f"{self.base_url}/users/{user_id}", headers=self.headers, timeout=10)

    def create_user(self, name, job):
        logger.info("POST %s/users name=%s job=%s", self.base_url, name, job)
        return requests.post(
            f"{self.base_url}/users",
            json={"name": name, "job": job},
            headers=self.headers,
            timeout=10,
        )

    def update_user(self, user_id, name, job):
        logger.info("PUT %s/users/%s name=%s job=%s", self.base_url, user_id, name, job)
        return requests.put(
            f"{self.base_url}/users/{user_id}",
            json={"name": name, "job": job},
            headers=self.headers,
            timeout=10,
        )

    def delete_user(self, user_id):
        logger.info("DELETE %s/users/%s", self.base_url, user_id)
        return requests.delete(f"{self.base_url}/users/{user_id}", headers=self.headers, timeout=10)
