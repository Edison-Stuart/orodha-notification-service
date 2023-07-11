from flask_restx import Api

from .notifications import ns as notification_ns

api = Api(
    title="Orodha Notification Api",
    version="0.1",
    description='A collection of namespaces relating to the Orodha notification service.'
)

api.add_namespace(notification_ns, path='/')
