from ddeutil.observe.app import app
from fastapi.testclient import TestClient


def test_app():
    test_client = TestClient(app=app)
    print(test_client)
