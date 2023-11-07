import pytest
import mongomock
from mongoengine import connect
from tests.fixtures.notification_data import INVITE_PAYLOAD
from tests.fixtures.keycloak_response import KEYCLOAK_GET_USER_RESPONSE
from application import create_base_app
import application.namespaces.notifications.models as notification_models


@pytest.fixture
def mock_app_client():
    app = create_base_app()
    connect(mongo_client_class=mongomock.MongoClient)
    yield app.test_client()


@pytest.fixture
def mock_notification():
    notification = notification_models.notification_factory(INVITE_PAYLOAD)
    notification.save()


class MockOrodhaKeycloakClient:
    """Mock OrodhaKeycloakConnection object to return keycloak fixture functions in testing."""

    def get_user(self, *args, **kwargs):
        return KEYCLOAK_GET_USER_RESPONSE


@pytest.fixture
def mock_create_keycloak_connection(mocker):
    """
    Fixture which patches our create_client_connection function to return our mocked client.
    """
    mocker.patch(
        "application.namespaces.notifications.controllers._create_keycloak_client",
        return_value=MockOrodhaKeycloakClient(),
    )
