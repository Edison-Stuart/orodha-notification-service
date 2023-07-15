from application import create_app
import pytest
import json

def test_get_main_namespace():
    flask_app = create_app()
    flask_app.testing = True
    
    with flask_app.test_client() as test_client:
        json_response = test_client.get(
            "/api/v1/main/hello"
		)
        
        assert json_response.status_code == 200
