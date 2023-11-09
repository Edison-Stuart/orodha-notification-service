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


class NotificationTypes(Enum):
    BASE_NOTIFICATION = 0
    LIST_INVITE_NOTIFICATION = 1


class Notification(Document):
    """
    A base document used for defining future notification types with varying behavior.
    """
    notificationType = NotificationTypes.BASE_NOTIFICATION
    targets = ListField(StringField(), required=True)
    lastAccessed = DateTimeField(default=None)

    meta = {"allow_inheritance": True}


class ListInviteNotification(Notification):
    """
    A list invite notification. Contains the listId of the target list
    """
    notificationType = NotificationTypes.LIST_INVITE_NOTIFICATION
    listId = StringField(required=True)


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
    return_notification = None

    if notification_type is NotificationTypes.BASE_NOTIFICATION.value:
        notification_data = {"targets": payload.get("targets")}
        return_notification = Notification(**notification_data)

    elif notification_type is NotificationTypes.LIST_INVITE_NOTIFICATION.value:
        notification_data = {
            "targets": payload.get("targets"),
            "listId": payload.get("list_id"),
        }
        return_notification = ListInviteNotification(**notification_data)

    else:
        raise NotificationTypeError(
            message=f"notification_type: {notification_type} is not supported."
        )
    return return_notification
