from flask_restx import Namespace, Resource

notification_ns = Namespace(
    "notifications",
    description='Notification related operations',
    url_prefix="/notification"
    )

# class SomeResource(Resource):
