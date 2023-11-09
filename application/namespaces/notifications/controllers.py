"""Module which contains controller functions that create, obtain, and delete notifications."""
from datetime import datetime
import orodha_keycloak
from mongoengine import (
    InvalidQueryError,
    ValidationError,
    FieldDoesNotExist,
    OperationError,
    DoesNotExist,
)
from application.config import obtain_config
from application.namespaces.notifications.models import (
    Notification,
    notification_factory,
)
from application.namespaces.notifications.exceptions import (
    OrodhaForbiddenError,
    OrodhaBadRequestError,
    OrodhaInternalError,
    OrodhaNotFoundError
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


def get_notifications(token: str, target_user: str):
    """
    Function which obtains a list of notifications related to a target user.

    Args:
        token(str): A JWT token obtained through keycloak that we use to ensure
            that a user is registered with keycloak
        target_user(str): A user_id that is related to the user we want to get
            notifications for.

    Returns:
        notifications(list[Notification]): A list of our notification documents that contained the
            user_id in their targets list.

    Raises:
        OrodhaInternalError: If there was a problem with the mongoengine query
            or updating our lastAccessed field.
        OrodhaForbiddenError: If the JWT token does not contain a valid user id.
        OrodhaBadRequestError: If the value of target_user is None.
    """
    try:
        keycloak_client = _create_keycloak_client()
        if keycloak_client.get_user(token=token).get("id") is None:
            raise OrodhaForbiddenError()
        if target_user is None:
            raise OrodhaBadRequestError("target_user must be a value.")

        Notification.objects(targets=target_user).modify(
            lastAccessed=datetime.now())

        notifications = [
            x.to_mongo() for x in Notification.objects(
                targets=target_user
            )
        ]

    except (
        OperationError,
        InvalidQueryError
    ) as err:
        raise OrodhaInternalError(
            message=f"There was an internal service error: {err}"
        )
    return notifications


def delete_notifications(token: str, notification_id: str):
    """
    Function which makes a query to the database with a given notification_id
    and deletes any returned notification from the database.

    Args:
        token(str): A JWT token obtained through keycloak that we use to ensure
            that a user is registered with keycloak
        notification_id(str): A string id that is associated with a certain notification.

    Raises:
        OrodhaForbiddenError: If the JWT token does not contain a valid user id.
        OrodhaNotFoundError: If there was not a unique notification found with the specific
            notification_id that was sent in.
        OrodhaBadRequestError: If the notification_id was set to None.
        OrodhaInternalError: If there was a problem with the deletion of the notification from
            the database.
    """
    try:
        keycloak_client = _create_keycloak_client()
        if keycloak_client.get_user(token=token).get("id") is None:
            raise OrodhaForbiddenError()
        if notification_id is None:
            raise OrodhaBadRequestError("notification_id must be a value.")

        notification = Notification.objects.get(id=notification_id)
        notification.delete()
    except DoesNotExist as err:
        raise OrodhaNotFoundError(
            f"Unable to find unique notification_id: {notification_id}"
        )
    except (ValidationError, OperationError) as err:
        raise OrodhaInternalError(
            f"Unable to delete notification {notification_id}: {err}")


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
        notification = notification_factory(payload)
        notification.save()
    except (
        ValidationError,
        FieldDoesNotExist
    ) as err:
        raise OrodhaBadRequestError(
            message=f"There was an issue creating notification: {err}"
        )
