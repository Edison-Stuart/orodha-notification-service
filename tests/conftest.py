import pytest
import mongomock
import os
from mongoengine import connect
import application.namespaces.notifications.models as notification_models
from application import create_base_app
from tests.fixtures.notification_data import INVITE_PAYLOAD, MOCK_GET_ID_DATA
from tests.fixtures.keycloak_response import KEYCLOAK_GET_USER_RESPONSE


@pytest.fixture
def mock_app_client():
    app = create_base_app()
    connect(mongo_client_class=mongomock.MongoClient)
    yield app.test_client()


@pytest.fixture
def mock_notification():
    notification = notification_models.notification_factory(INVITE_PAYLOAD)
    notification.save()
    yield notification


class MockOrodhaKeycloakClient:
    """Mock OrodhaKeycloakConnection object to return keycloak fixture functions in testing."""

    def get_user(self, *args, **kwargs):
        return KEYCLOAK_GET_USER_RESPONSE


@pytest.fixture
def mock_create_keycloak_connection(mocker):
    """
    Fixture function which patches our _create_keycloak_client function to return our mocked client.
    """
    mocker.patch(
        "application.namespaces.notifications.controllers._create_keycloak_client",
        return_value=MockOrodhaKeycloakClient(),
    )


@pytest.fixture
def mock_get_id_from_keycloak_id(mocker):
    """
    Fixture function which patches our get_id_data_from_keycloak_id util
    function to return fixture data.
    """
    mocker.patch(
        "application.namespaces.notifications.utils.get_id_data_from_keycloak_id",
        return_value=MOCK_GET_ID_DATA
    )


@pytest.fixture
def mock_get_id_from_user_id(mocker):
    """
    Fixture function which patches our get_id_data_from_user_id util
    function to return fixture data.
    """
    mocker.patch(
        "application.namespaces.notifications.utils.get_id_data_from_user_id",
        return_value=MOCK_GET_ID_DATA
    )
