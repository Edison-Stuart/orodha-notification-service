"""Module that contains custom exceptions for the Orodha notification service."""
from http import HTTPStatus

class OrodhaForbiddenError(Exception):
    """
    Exception for when a request is made with a token not containing proper auth.
    Returns a 403 FORBIDDEN status code.
    """
    status_code = HTTPStatus.FORBIDDEN

    def __init__(self, message: str = "You don't have permission to access this resource"):
        self.message = message
        super().__init__(self.message)

class NotificationTypeError(Exception):
    """
    Exception for when a post request is made with a notification_type that does not exist.
    """
    status_code = HTTPStatus.BAD_REQUEST

    def __init__(self, message: str = None):
        self.message = message
        super().__init__(self.message)

class OrodhaBadRequestError(Exception):
    """
    Exception for when there is a problem with either keycloak or mongo when
    trying to post user data. Could either be called when you are missing fields
    or when you have extra fields in your request. Returns a 400 BAD REQUEST status code.
    """
    status_code = HTTPStatus.BAD_REQUEST

    def __init__(self, message: str = None):
        self.message = message
        super().__init__(self.message)

class OrodhaNotFoundError(Exception):
    """
    Exception for when a search for a specific object in either our database or
    the keycloak database is not found. Returns a 404 NOT FOUND status code.
    """
    status_code = HTTPStatus.NOT_FOUND

    def __init__(self, message: str = None):
        self.message = message
        super().__init__(self.message)

class OrodhaInternalError(Exception):
    """
    Exception for when there is an internal server error.
    """
    status_code = HTTPStatus.INTERNAL_SERVER_ERROR

    def __init__(self, message: str = None):
        self.message = message
        super().__init__(self.message)
