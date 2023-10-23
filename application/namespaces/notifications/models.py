"""Module which contains the Mongoengine document definitions."""
from mongoengine import Document, StringField, ListField

class BaseNotification(Document):
    """
    A base document used for defining future notification types with varying behavior.
    Contains targets which is a listField meant to contain user_id values.
    """
    targets = ListField(required=True)

class ListInviteNotification(BaseNotification):
    """
    A list invite notification. Contains the list_id of the target list
    """
    list_id = StringField(required=True)
