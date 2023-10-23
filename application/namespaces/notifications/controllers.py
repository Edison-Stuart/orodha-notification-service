import orodha_keycloak
from application.config import obtain_config
from application.namespaces.notifications.models import Notification

APPCONFIG = obtain_config()

def _create_keycloak_client() -> orodha_keycloak.OrodhaKeycloakClient:
    """
    Helper function which creates our keycloak client from config data
    for use in our main controller functions.

    Returns:
        OrodhaKeycloakClient: A facade client used by Orodha in order to make interactions with
            keycloak more uniform for the service.
    """
    return orodha_keycloak.OrodhaKeycloakClient(
        server_url=APPCONFIG["keycloak_config"]["keycloak_server_url"],
        realm_name=APPCONFIG["keycloak_config"]["keycloak_realm_name"],
        client_id=APPCONFIG["keycloak_config"]["keycloak_client_id"],
        client_secret_key=APPCONFIG["keycloak_config"]["keycloak_client_secret_key"],
    )

def get_notifications(token: str):
    pass

def delete_notifications(token: str):
    pass

def post_notifications(token: str, payload: dict):
    pass
