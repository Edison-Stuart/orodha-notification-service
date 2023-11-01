import pytest
from tests.fixtures.notification_data import MOCK_USER_ID, GET_RESPONSE

BASE_URL = "/api/v1/notifications"


def test_get_notifications(mock_app_client, mock_notification, mock_create_keycloak_connection):
    api_response = mock_app_client.get(
        f"{BASE_URL}?user_id={MOCK_USER_ID}", headers={"Content-Type": "application/json"}
    )
    notification = api_response.json[0]
    mock_response = GET_RESPONSE[0]

    assert notification["targets"] == mock_response["targets"]
    assert notification["list_id"] == mock_response["list_id"]
