from application.namespaces.notifications.exceptions import OrodhaBadRequestError
def check_missing_data(targets: dict) -> str:
    """
    Helper function which takes a dictionary of targets and ensures that there is
    at least one id type for obtaining the others.

    Args:
        targets(dict): A dictionary of targets obtained from the payload. Contains values
            for user_id and keycloak_id.

    Returns:
        response(str): A string representation of the id type available for search.
            Set to None if both values exist.

    Raises:
        OrodhaBadRequestError: If neither id is present in targets dictionary.
    """
    user_id = targets.get("user_id")
    keycloak_id = targets.get("keycloak_id")
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

def get_target_data_from_keycloak_id(keycloak_id: str) -> dict:
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

def get_target_data_from_user_id(user_id: str) -> dict:
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
