import pytest
import allure
import os
from utils.api_client import APIClient
from utils.data_loader import load_json

api_data = load_json("api_users.json")
create_user_data = api_data["create_user"]
update_user_data = api_data["update_user"]

@pytest.fixture
def api_client():
    return APIClient()


# Helper to ensure a valid ReqRes API key is configured
def require_reqres_api_key():
    api_key = os.getenv("REQRES_API_KEY")
    if not api_key or api_key.startswith("paste_") or api_key.startswith("actual_"):
        pytest.skip(
            "Valid ReqRes API key not configured. Set REQRES_API_KEY to a real key from app.reqres.in/api-keys and rerun pytest -m api."
        )


@pytest.mark.api
@allure.feature("Users API")
@allure.story("Get users list")
def test_get_users(api_client):
    require_reqres_api_key()
    with allure.step("Send GET request for users list"):
        response = api_client.get_users()

    with allure.step("Verify status code is 200"):
        assert response.status_code == 200

    with allure.step("Verify response contains user data"):
        body = response.json()
        assert isinstance(body, list)
        assert len(body) > 0
        assert "id" in body[0]
        assert "name" in body[0]


@pytest.mark.api
@allure.feature("Users API")
@allure.story("Get single user")
def test_get_single_user(api_client):
    require_reqres_api_key()
    with allure.step("Send GET request for single user"):
        response = api_client.get_single_user(2)

    with allure.step("Verify status code is 200"):
        assert response.status_code == 200

    with allure.step("Verify returned user id is 2"):
        body = response.json()
        assert body["id"] == 2


@pytest.mark.api
@allure.feature("Users API")
@allure.story("Create user")
def test_create_user(api_client):
    require_reqres_api_key()
    with allure.step("Send POST request to create user"):
        response = api_client.create_user(
            create_user_data["name"],
            create_user_data["job"]
        )

    with allure.step("Verify status code is 201"):
        assert response.status_code == 201

    with allure.step("Verify created user payload"):
        body = response.json()
        assert body["name"] == create_user_data["name"]
        assert body["job"] == create_user_data["job"]


@pytest.mark.api
@allure.feature("Users API")
@allure.story("Update user")
def test_update_user(api_client):
    require_reqres_api_key()
    with allure.step("Send PUT request to update user"):
        response = api_client.update_user(
            update_user_data["id"],
            update_user_data["name"],
            update_user_data["job"]
        )

    with allure.step("Verify status code is 200"):
        assert response.status_code == 200

    with allure.step("Verify updated payload"):
        body = response.json()
        assert body["id"] == update_user_data["id"]
        assert body["name"] == update_user_data["name"]
        assert body["job"] == update_user_data["job"]


@pytest.mark.api
@allure.feature("Users API")
@allure.story("Delete user")
def test_delete_user(api_client):
    require_reqres_api_key()
    with allure.step("Send DELETE request"):
        response = api_client.delete_user(2)

    with allure.step("Verify delete response status code"):
        assert response.status_code in (200, 204)