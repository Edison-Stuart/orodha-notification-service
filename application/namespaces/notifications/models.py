from mongoengine import Document, DictField

class Notification(Document):
    data = DictField(required=True)
