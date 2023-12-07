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
    EnumField
)
from application.namespaces.notifications.exceptions import NotificationTypeError


class NotificationTypes(Enum):
    """
    Simple class which inherits from Enum and defines our available notification types.
    """
    BASE = "base"
    LIST_INVITE = "list_invite"


class Notification(Document):
    """
    A base document used for defining future notification types with varying behavior.
    """
    notificationType = EnumField(
        NotificationTypes, default=NotificationTypes.BASE)
    targets = ListField(StringField(), required=True)
    lastAccessed = DateTimeField(default=None)

    meta = {"allow_inheritance": True}


class ListInviteNotification(Notification):
    """
    A list invite notification. Contains the listId of the target list
    """
    notificationType = EnumField(
        NotificationTypes, default=NotificationTypes.LIST_INVITE)
    listId = StringField(required=True)


def notification_factory(payload: dict):
    """
    Factory function which takes the payload from the post request
    and creates a notification Document of a type defined in the payload.

    Args:
        payload(dict): The payload passed in from the route functions.

    Returns:
        return_notification: The newly created notification document which
            contains the data sent in from the payload.

    Raises:
        NotificationTypeError: When there is a missing or improper notification type.
    """
    notification_type = payload.get("notification_type")
    return_notification = None
    if notification_type is not None:
        notification_type = notification_type.lower()

    if notification_type == NotificationTypes.BASE.value:
        notification_data = {"targets": payload.get("targets")}
        return_notification = Notification(**notification_data)

    elif notification_type == NotificationTypes.LIST_INVITE.value:
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
