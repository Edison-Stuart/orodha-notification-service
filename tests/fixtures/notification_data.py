"""Fixture file which contains mock request body which is used to create a notification."""
from uuid import uuid4

MOCK_USER_ID = str(uuid4())
MOCK_LIST_ID = str(uuid4())

INVITE_PAYLOAD = {
    "targets": [
        MOCK_USER_ID,
    ],
    "list_id": MOCK_LIST_ID,
    "notification_type": 1
}

POST_NO_TARGETS = {
    "list_id": MOCK_LIST_ID,
    "notification_type": 1
}

GET_RESPONSE = [{
    # NOTE: Unused in testing. Here for consist data representation.
    'id': 'SOME_RANDOM_ID',
    'lastAccessed': 'SOME_DATETIME',

    'listId': MOCK_LIST_ID,
    'targets': [MOCK_USER_ID]
}]
