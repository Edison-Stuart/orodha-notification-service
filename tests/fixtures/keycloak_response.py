"""Fixture file which contains response data relating to the OrodhaKeycloakClient"""
from uuid import uuid4

TEST_KEYCLOAK_USER_ID = uuid4()

KEYCLOAK_GET_USER_RESPONSE = {
    'id': str(TEST_KEYCLOAK_USER_ID), 'createdTimestamp': 1695143223350,
    'username': 'someuser', 'enabled': True, 'totp': False,
    'emailVerified': False, 'disableableCredentialTypes': [],
    'requiredActions': [], 'notBefore': 0,
    'access': {
        'manageGroupMembership': True,
        'view': True, 'mapRoles': True,
        'impersonate': True, 'manage': True
    }
}