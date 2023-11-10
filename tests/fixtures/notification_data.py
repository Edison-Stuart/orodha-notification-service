"""Fixture file which contains mock request body which is used to create a notification."""
from uuid import uuid4

MOCK_USER_ID = str(uuid4())
MOCK_LIST_ID = str(uuid4())

INVITE_PAYLOAD = {
    "targets": [
        MOCK_USER_ID,
    ],
    "list_id": MOCK_LIST_ID,
    "notification_type": "LIST_INVITE"
}


POST_NO_TARGETS = {
    "list_id": MOCK_LIST_ID,
    "notification_type": "LIST_INVITE"
}

GET_RESPONSE = [{
    # NOTE: Some values are unused in testing. Here for consistent data representation.
    'id': 'SOME_RANDOM_ID',
    'targets': [MOCK_USER_ID],
    "notificationType": "list_invite",
    'lastAccessed': 'SOME_DATETIME',
    'listId': MOCK_LIST_ID,
}]
