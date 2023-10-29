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
    OrodhaInternalError,
    OrodhaNotFoundError
)

notification_ns = Namespace(
    "notifications",
    description='Notification related operations'
)

request_target_model = notification_ns.model(
    "Model for the targets field",
    {
        "user_id": fields.String(),
        "keycloak_id": fields.String()
    }
)

list_invite_creation_model = notification_ns.model(
    "Notification input, includes optional list_id for ListInviteNotification type",
    {
        "targets": fields.List(fields.Nested(request_target_model), required=True),
        "list_id": fields.String(required=False),
        "notification_type": fields.String(default="base")
    },
)

notification_response_model = notification_ns.model(
    "Notification Response",
    {
        "id": fields.String(required=True),
        "targets": fields.List(required=True),
        "last_accessed": fields.DateTime(required=False),
        "list_id": fields.String(required=False),
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
    @notification_ns.marshal_with(notification_response_model, as_list=True)
    def get(self):
        """
        Function which accepts GET requests to the notifications route, expecting a query parameter
        which defines the target user_id, and returns a list of
        Notifications associated with the user_id.

        Args(expected as query parameter):
            user_id(str): The user_id that is associated with the user we inted to
                obtain the notifications for.

        Returns:
            response(list): A list containing the notifications associated with the user_id.
                Contains:
                    id(str): The notification id.
                    list_id(str): The optional id of the associated list.
                    targets(list): A list of user_id values which this notification is meant for.
                    last_accessed(datetime): A datetime object of the date this notification
                        was last accessed.

        Raises:
            OrodhaForbiddenError: If the JWT token from the request header
                did not contain a valid keycloak user.
            OrodhaInternalError: If there was an internal server error during get process.
            OrodhaBadRequestError: If the expected query parameter was not passed in.
        """
        try:
            request_token = get_token_from_header(request.headers)
            target_user = request.args.get("user_id")
            response = application.namespaces.notifications.controllers.get_notifications(
                request_token, target_user
            )

        except (
            OrodhaForbiddenError,
            OrodhaInternalError,
            OrodhaBadRequestError
        ) as err:
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
        """
        Function which accepts DELETE request to the /notifications endpoint.

        Args(Excpected as query parameters):
            notification_id(str): A document id for a notification object. Used to query
                and delete notifications.

        Returns:
            status_code(dict): dictionary containing a status code of 200, OK.

        Raises:
            OrodhaForbiddenError: If the JWT token from the request header
                did not contain a valid keycloak user.

            OrodhaNotFoundError: If there was not a unique notification found with the specific
            notification_id that was sent in.

            OrodhaBadRequestError: If notification_id was not passed to route.

            OrodhaInternalError: If there was a problem with the deletion of the notification from
            the database.
        """
        try:
            request_token = get_token_from_header(request.headers)
            target_notification = request.args.get("notification_id")
            application.namespaces.notifications.controllers.delete_notifications(
                request_token, target_notification
            )

        except (
            OrodhaForbiddenError,
            OrodhaNotFoundError,
            OrodhaBadRequestError,
            OrodhaInternalError
        ) as err:
            notification_ns.abort(err.status_code, err.message)

        return {"status_code": HTTPStatus.OK}
