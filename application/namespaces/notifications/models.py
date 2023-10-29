"""
Module which contains the Mongoengine document definitions as well as helper functions
related to Notifications.
"""
from copy import deepcopy
from mongoengine import (
    Document,
    EmbeddedDocument,
    EmbeddedDocumentListField,
    StringField,
    DateTimeField,
)
from application.namespaces.notifications.exceptions import NotificationTypeError
import application.namespaces.notifications.utils as utils

class NotificationTargetDocument(EmbeddedDocument):
    """
    An EmbeddedDocument which contains identity information about our notification target.
    """
    user_id = StringField()
    keycloak_id = StringField()

class Notification(Document):
    """
    A base document used for defining future notification types with varying behavior.
    """
    targets = EmbeddedDocumentListField(NotificationTargetDocument(), required=True)
    last_accessed = DateTimeField(default=None)

    meta = {"allow_inheritance": True}

class ListInviteNotification(Notification):
    """
    A list invite notification. Contains the list_id of the target list
    """
    list_id = StringField(required=True)

AVAILABLE_NOTIFICATION_TYPES = {
    "base": Notification,
    "list-invite": ListInviteNotification
}

def target_document_factory(payload: dict) -> dict:
    """
    Factory function which takes the payload from our notification factory
    and creates an embedded target document from our target info.
    If target data is missing, function will call util functions to obtain missing
    data from existing data.

    Args:
        payload(dict): Our full post request payload which contains our request target data.

    Returns:
        response(dict): A copy of our payload dictionary with targets replaced with a
            NotificationTargetDocument containing our target id values.
    """
    targets = payload.get("targets")
    available_target_data = utils.check_missing_data(targets)
    response = deepcopy(payload)

    if available_target_data is not None:
        target_data = getattr(
            utils,
            f"get_target_data_from_{available_target_data}"
        )(targets[available_target_data])
        response["targets"] = NotificationTargetDocument(**target_data)
    else:
        response["targets"] = NotificationTargetDocument(**targets)

    return response

def notification_factory(payload: dict):
    """
    Factory function which takes the payload from the post request
    and creates a notification Document of a type defined in the payload.

    Args:
        payload(dict): The payload passed in from the route functions.

    Returns:
        notification_type(**notification_data): The newly created notification document which contains
            the data sent in from the payload.

    Raises:
        NotificationTypeError: When there is a missing or improper notification type.
    """
    notification_type = payload.get("notification_type")
    if notification_type not in AVAILABLE_NOTIFICATION_TYPES.keys():
        raise NotificationTypeError(
            message=f"notification_type: {notification_type} is not supported."
        )
    notification_data = target_document_factory(payload)
    return AVAILABLE_NOTIFICATION_TYPES[notification_type](**notification_data)
