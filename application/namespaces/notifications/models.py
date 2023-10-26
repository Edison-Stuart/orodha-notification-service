"""Module which contains the Mongoengine document definitions for Notifications."""
from mongoengine import Document, StringField, ListField, DateTimeField

class Notification(Document):
    """
    A base document used for defining future notification types with varying behavior.
    Contains targets which is a listField meant to contain user_id values.
    """
    targets = ListField(StringField(), required=True)
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
