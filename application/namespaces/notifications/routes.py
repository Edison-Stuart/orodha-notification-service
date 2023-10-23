from flask_restx import Namespace, Resource
from flask import request
import application.namespaces.notifications.controllers

notification_ns = Namespace(
    "notifications",
    description='Notification related operations'
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

    def post(self):
        try:
            request_token = get_token_from_header(request.headers)
            response = application.namespaces.notifications.controllers.post_notifications(
                request_token, notification_ns.payload
            )
#NOTE       Exception will be made more specific
        except Exception as err:
            notification_ns.abort(err.status_code, err.message)
        
        return response


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
