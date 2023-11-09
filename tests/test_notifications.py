import pytest
from bson import objectid
from http import HTTPStatus
from tests.fixtures.notification_data import (
    MOCK_USER_ID,
    GET_RESPONSE,
    INVITE_PAYLOAD,
    POST_NO_TARGETS,
)

BAD_ID = objectid.ObjectId()
BASE_NOTIFICATIONS_URL = "/api/v1/notifications"


def test_get_notifications(
        mock_app_client,
        mock_notification,
        mock_create_keycloak_connection):
    api_response = mock_app_client.get(
        f"{BASE_NOTIFICATIONS_URL}?user_id={MOCK_USER_ID}", headers={"Content-Type": "application/json"}
    )
    notification = api_response.json[0]
    mock_response = GET_RESPONSE[0]

    assert notification["targets"] == mock_response["targets"]
    assert notification["listId"] == mock_response["listId"]


def test_get_notifications_bad_request(
        mock_app_client,
        mock_notification,
        mock_create_keycloak_connection):
    api_response = mock_app_client.get(
        BASE_NOTIFICATIONS_URL, headers={"Content-Type": "application/json"}
    )
    assert api_response.json == {'message': 'target_user must be a value.'}
    assert api_response.status_code == HTTPStatus.BAD_REQUEST


def test_delete_notifications(
        mock_app_client,
        mock_notification,
        mock_create_keycloak_connection):
    notification_id = mock_notification.id
    api_response = mock_app_client.delete(
        f"{BASE_NOTIFICATIONS_URL}?notification_id={notification_id}",
        headers={"Content-Type": "application/json"}
    )
    assert api_response.status_code == HTTPStatus.OK


def test_delete_notifications_not_found(
        mock_app_client,
        mock_notification,
        mock_create_keycloak_connection):
    api_response = mock_app_client.delete(
        f"{BASE_NOTIFICATIONS_URL}?notification_id={BAD_ID}",
        headers={"Content-Type": "application/json"}
    )
    assert api_response.status_code == HTTPStatus.NOT_FOUND
    assert api_response.json == {
        'message': f'Unable to find unique notification_id: {BAD_ID}. You have' +
        f' requested this URI [{BASE_NOTIFICATIONS_URL}] but did you mean {BASE_NOTIFICATIONS_URL} ?'
    }


def test_delete_notifications_bad_request(
        mock_app_client,
        mock_notification,
        mock_create_keycloak_connection):
    api_response = mock_app_client.delete(
        f"{BASE_NOTIFICATIONS_URL}",
        headers={"Content-Type": "application/json"}
    )
    assert api_response.status_code == HTTPStatus.BAD_REQUEST
    assert api_response.json == {'message': 'notification_id must be a value.'}


def test_post_notifications(
        mock_app_client,
        mock_create_keycloak_connection,
):
    api_response = mock_app_client.post(
        BASE_NOTIFICATIONS_URL,
        json=INVITE_PAYLOAD
    )
    assert api_response.json == {"status_code": HTTPStatus.OK}


def test_post_notifications_no_targets(mock_app_client, mock_create_keycloak_connection):
    api_response = mock_app_client.post(
        BASE_NOTIFICATIONS_URL,
        json=POST_NO_TARGETS
    )
    assert api_response.json == {'errors': {
        'targets': "'targets' is a required property"}, 'message': 'Input payload validation failed'}
    assert api_response.status_code == HTTPStatus.BAD_REQUEST
