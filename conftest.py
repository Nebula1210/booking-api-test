import pytest
from lib.api_client import APIClient


@pytest.fixture(scope="session")
def api_client():
    """
    session 级别共享API客户端

    """
    return APIClient()


@pytest.fixture(scope="session")
def auth_token(api_client: APIClient):
    """
    获取认证token的fixture
    :param api_client:
    :return:
    """
    auth_payload = {
        "username": "admin",
        "password": "password123"
    }
    response = api_client.post("/auth", json=auth_payload)
    assert response.status_code == 200, f"Auth failed: {response.text}"
    token = response.json().get("token")
    assert token is not None, "Token not found in auth response"
    return token
