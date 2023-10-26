"""
Module which contains route functions for interacting with notifications
that direct incoming requests to the correct controllers.
"""
from http import HTTPStatus
from flask_restx import Namespace, Resource, fields
from flask import request
import application.namespaces.notifications.controllers
from application.namespaces.notifications.exceptions import (
    OrodhaBadRequestError,
    OrodhaForbiddenError,
    NotificationTypeError,
)

notification_ns = Namespace(
    "notifications",
    description='Notification related operations'
)

list_invite_creation_model = notification_ns.model(
    "Notification input, includes optional list_id for ListInviteNotification type",
    {
        "targets": fields.List(required=True),
        "list_id": fields.String(required=False),
        "notification_type": fields.String(default="list-invite")
    },
)

def get_token_from_header(headers: dict) -> str:
    """
    Accepts a request header and gets the auth token from it.

    Args:
        headers(request.headers): A dictionary containing information including our JWT token.

    Returns:
        token(str): Our token string which can be decoded via keycloak to get our user info.
    """
    token = headers.get("Authorization", "").lstrip("Bearer").strip()
    return token

@notification_ns.route("")
class NotificationsApi(Resource):
    """
    Class that contains routes for GET, POST, and DELETE requests interacting
    with notifications.
    """
    def get(self):
        try:
            request_token = get_token_from_header(request.headers)
            response = application.namespaces.notifications.controllers.get_notifications(
                request_token
            )
#NOTE       Exception will be made more specific
        except Exception as err:
            notification_ns.abort(err.status_code, err.message)

        return response

    @notification_ns.expect(list_invite_creation_model, validate=True)
    def post(self):
        """
        Function which accepts POST requests and initiates the creation of
        a Notification based on the payload.

        Args(Arguments are expected on the request body):
            targets(list): A list of user_id values used to connect notifications
                to their recipients.
            notification_type(str): A value that determines which Notification type
                should be created with the incoming data. Needs to be a key
                of AVAILABLE_NOTIFICATION_TYPES, which is defined in the models module.
            list_id(str): An optional list_id which connects the targets to a the list
                via the ListInviteNotification.

        Returns:
            status_code(dict): dictionary containing a status code of 200, OK.

        Raises:
            OrodhaBadRequestError: If the payload contained incorrect data.
            OrodhaForbiddenError: If the JWT token from the request header
                did not contain a valid keycloak user.
            NotificationTypeError: If the notification_type value in the payload
                was not included in AVAILABLE_NOTIFICATION_TYPES.
        """
        try:
            request_token = get_token_from_header(request.headers)
            application.namespaces.notifications.controllers.post_notifications(
                request_token, notification_ns.payload
            )
        except (
            OrodhaBadRequestError,
            OrodhaForbiddenError,
            NotificationTypeError
        ) as err:
            notification_ns.abort(err.status_code, err.message)

        return {"status_code": HTTPStatus.OK}

    def delete(self):
        try:
            request_token = get_token_from_header(request.headers)
            response = application.namespaces.notifications.controllers.delete_notifications(
                request_token
            )
#NOTE       Exception will be made more specific
        except Exception as err:
            notification_ns.abort(err.status_code, err.message)
        
        return response
