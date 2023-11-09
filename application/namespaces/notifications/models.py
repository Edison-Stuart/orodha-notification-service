"""
Module which contains the Mongoengine document definitions as well as helper functions
related to Notifications.
"""
from enum import Enum
from mongoengine import (
    Document,
    ListField,
    StringField,
    DateTimeField,
)
from application.namespaces.notifications.exceptions import NotificationTypeError
import application.namespaces.notifications.utils


class NotificationTypes(Enum):
    BASE_NOTIFICATION = 0
    LIST_INVITE_NOTIFICATION = 1

    def __contains__(self, other):
        try:
            self(other)
        except ValueError:
            return False
        else:
            return True


class Notification(Document):
    """
    A base document used for defining future notification types with varying behavior.
    """
    notificationType = NotificationTypes.BASE_NOTIFICATION
    targets = ListField(StringField, required=True)
    lastAccessed = DateTimeField(default=None)

    meta = {"allow_inheritance": True}


class ListInviteNotification(Notification):
    """
    A list invite notification. Contains the listId of the target list
    """
    notificationType = NotificationTypes.LIST_INVITE_NOTIFICATION
    listId = StringField(required=True)


AVAILABLE_NOTIFICATION_TYPES = {
    # NOTE: Constant has to be declared after class definitions
    #   of Notification types in order to reference them.
    "base": Notification,
    "list-invite": ListInviteNotification
}


def create_target_list(targets: list) -> list:
    """
    Function which takes the targets from our notification factory
    and creates an embedded target document for each target in the given list.

    Args:
        targets(list): Our request target data.

    Returns:
        response(list): A list of NotificationTargetDocuments containing our target id values.
    """
    targets_out = []

    for target in targets:
        target_document = application.namespaces.notifications.utils.obtain_target_document(
            target,
            NotificationTargetDocument
        )
        targets_out.append(target_document)

    return targets_out


def notification_factory(payload: dict):
    """
    Factory function which takes the payload from the post request
    and creates a notification Document of a type defined in the payload.

    Args:
        payload(dict): The payload passed in from the route functions.

    Returns:
        notification_type(**notification_data): The newly created notification document which
            contains the data sent in from the payload.

    Raises:
        NotificationTypeError: When there is a missing or improper notification type.
    """
    notification_type = payload.get("notification_type")

    if notification_type not in AVAILABLE_NOTIFICATION_TYPES.keys():
        raise NotificationTypeError(
            message=f"notification_type: {notification_type} is not supported."
        )
    notification_data = {
        "targets": create_target_list(payload.get("targets")),
        "list_id": payload.get("list_id"),
    }
    return AVAILABLE_NOTIFICATION_TYPES[notification_type](**notification_data)
