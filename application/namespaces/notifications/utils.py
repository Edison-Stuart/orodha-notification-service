"""
Utility module which contains functions that assist the model and controller in obtaining data
for our embedded NotificationTargetDocument.
"""
from sys import modules
from application.namespaces.notifications.exceptions import OrodhaBadRequestError

def obtain_target_document(target: dict, DocumentType):
    """
    Helper function which takes a target dictionary as well as
    a document type and creates a document with the target data.

    Args:
        target(dict): A dictionary with id values related to our
            notification target.
        DocumentType(Document): A document definition that will be used to
            create a document object with the target data.

    Returns:
        response(DocumentType): A newly created DocumentType object containing
            the target data.
    """
    valid_id_key = check_for_valid_id(target)
    response = None

    if valid_id_key is None:
        response = DocumentType(**target)
    else:
        id_data = getattr(
            modules[__name__],
            f"get_id_data_from_{valid_id_key}"
        )(target[valid_id_key])
        response = DocumentType(**id_data)

    return response

def check_for_valid_id(target: dict) -> str:
    """
    Helper function which takes a dictionary of targets and ensures that there is
    at least one id type for obtaining the others.

    Args:
        targets(dict): A dictionary of id values related to the target. Contains values
            for user_id and keycloak_id.

    Returns:
        response(str): A string representation of the id type available for search.
            Set to None if both values exist.

    Raises:
        OrodhaBadRequestError: If neither id is present in target dictionary.
    """
    user_id = target.get("user_id")
    keycloak_id = target.get("keycloak_id")
    response = None

    if user_id is None and keycloak_id is None:
        raise OrodhaBadRequestError(
            message="Payload.targets must contain at least user_id or keycloak_id"
        )
    if user_id is None:
        response = "keycloak_id"
    elif keycloak_id is None:
        response = "user_id"
    return response

def get_id_data_from_keycloak_id(keycloak_id: str) -> dict:
    """
    Utility function which takes an existing keycloak_id and uses it
    to obtain the related user_id from the user service.

    Args:
        keycloak_id(str): The keycloak id related to our target user. Used to obtain
            the user_id related to the same target.

    Returns:
        response(dict): A dictionary containing both the keycloak_id and the user_id
            of our target user.
    """
    pass

def get_id_data_from_user_id(user_id: str) -> dict:
    """
    Utility function which takes an existing user_id and uses it to
    obtain the related keycloak_id from the user service.

    Args:
        user_id(str): The user id related to our target user. Used to obtain
            the keycloak_id related to the same target.

    Returns:
        response(dict): A dictionary containing both the keycloak_id and the user_id
            of our target user.
    """
    pass
