from flask_restx import Namespace, Resource

ns = Namespace(
    "main",
    description="The main namespace"
)

@ns.route('/hello')
class HelloWorld(Resource):
    def get(self):
	    return "Hello World"
