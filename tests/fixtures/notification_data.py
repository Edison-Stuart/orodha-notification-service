"""Fixture file which contains mock request body which is used to create a notification."""
from uuid import uuid4
from copy import deepcopy
from application.namespaces.notifications.exceptions import OrodhaBadRequestError

MOCK_USER_ID = str(uuid4())
MOCK_KEYCLOAK_ID = str(uuid4())
MOCK_LIST_ID = str(uuid4())

INVITE_PAYLOAD = {
    "targets": [{
        "user_id": MOCK_USER_ID,
        "keycloak_id": MOCK_KEYCLOAK_ID
    }],
    "list_id": MOCK_LIST_ID,
    "notification_type": "list-invite"
}

POST_WITH_USER_ID = {
    "targets": [{
        "user_id": MOCK_USER_ID,
        "keycloak_id": None
    }],
    "list_id": MOCK_LIST_ID,
    "notification_type": "list-invite"
}

POST_WITH_KEYCLOAK_ID = {
    "targets": [{
        "user_id": None,
        "keycloak_id": MOCK_KEYCLOAK_ID
    }],
    "list_id": MOCK_LIST_ID,
    "notification_type": "list-invite"
}

POST_NO_TARGETS = {
    "list_id": MOCK_LIST_ID,
    "notification_type": "list-invite"
}

POST_EMPTY_TARGETS = {
    "targets": [{
        "user_id": None,
        "keycloak_id": None
    }],
    "list_id": MOCK_LIST_ID,
    "notification_type": "list-invite"
}

GET_RESPONSE = [{
    # NOTE: Unused in testing. Here for consist data representation.
    'id': 'SOME_RANDOM_ID',
    'last_accessed': 'SOME_DATETIME',

    'list_id': MOCK_LIST_ID,
    'targets': [{
        'keycloak_id': MOCK_KEYCLOAK_ID,
        'user_id': MOCK_USER_ID
    }]
}]

MOCK_GET_ID_DATA = {
    "user_id": MOCK_USER_ID,
    "keycloak_id": MOCK_KEYCLOAK_ID
}
