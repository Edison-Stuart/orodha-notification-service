import orodha_keycloak
from mongoengine import (
    MultipleObjectsReturned,
    ValidationError,
    FieldDoesNotExist,
    DoesNotExist,
    OperationError,
)
from application.config import obtain_config
from application.namespaces.notifications.models import AVAILABLE_NOTIFICATION_TYPES
from application.namespaces.notifications.exceptions import (
    OrodhaForbiddenError,
    NotificationTypeError,
    OrodhaBadRequestError
)

APPCONFIG = obtain_config()

def _create_keycloak_client() -> orodha_keycloak.OrodhaKeycloakClient:
    """
    Helper function which creates our keycloak client from config data
    for use in our main controller functions.

    Returns:
        OrodhaKeycloakClient: A facade client used by Orodha in order to make interactions with
            keycloak more uniform for the service.
    """
    return orodha_keycloak.OrodhaKeycloakClient(
        server_url=APPCONFIG["keycloak_config"]["keycloak_server_url"],
        realm_name=APPCONFIG["keycloak_config"]["keycloak_realm_name"],
        client_id=APPCONFIG["keycloak_config"]["keycloak_client_id"],
        client_secret_key=APPCONFIG["keycloak_config"]["keycloak_client_secret_key"],
    )

def _obtain_notification_type(payload: dict):
    """
    Helper function which takes the payload from the post request
    and obtains the notification type for Document creation.

    Args:
        payload(dict): The payload passed in from the route functions.
            contains String(notification_type).

    Returns:
        notification_type(AVAILABLE_NOTIFICATION_TYPES): The class of Document
            which matches the notification_type indicator sent in with the request body.

    Raises:
        NotificationTypeError: When there is a missing or improper notification type.
    """
    notification_type = payload.get("notification_type")
    if notification_type not in AVAILABLE_NOTIFICATION_TYPES.keys():
        raise NotificationTypeError(
            message=f"notification_type: {notification_type} is not supported."
        )
    return AVAILABLE_NOTIFICATION_TYPES[notification_type]

def get_notifications(token: str):
    pass

def delete_notifications(token: str):
    pass

def post_notifications(token: str, payload: dict):
    """
    Function which takes the payload from a POST request, then creates
    the correct Notification Document with the data based on the notification_type.

    Args:
        token(str): The JWT token taken from the header of the request.
            Used to ensure the request was made by a user connected to the
            keycloak client.
        payload(dict): The payload sent from the POST route. Contains data
            necessary for determining the type of, as well as creating a Notification.

    Raises:
        OrodhaBadRequestError: If the request is made with extra, or missing data.
        OrodhaForbiddenError: If the JWT token sent through did not contain a valid
            keycloak id.
    """
    try:
        keycloak_client = _create_keycloak_client()
        if keycloak_client.get_user(token=token).get("id") is None:
            raise OrodhaForbiddenError()
        notification = _obtain_notification_type(payload)(**payload)
        notification.save()
    except (
        ValidationError,
        FieldDoesNotExist
    ) as err:
        raise OrodhaBadRequestError(
            message=f"There was an issue creating notification: {err}"
        )
