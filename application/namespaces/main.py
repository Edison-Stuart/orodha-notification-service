from flask_restx import Namespace, Resource

main_ns = Namespace(
    "main",
    description="The main namespace"
)

@main_ns.route('/hello')
class HelloWorld(Resource):
    def get(self):
	    return "Hello World"
