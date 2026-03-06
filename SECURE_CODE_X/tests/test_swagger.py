import pytest
import sys
import os

# Add server to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'server'))

from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_swagger_docs(client):
    rv = client.get('/apidocs/')
    # Flasgger usually redirects or returns 200
    assert rv.status_code in [200, 302, 308]
    if rv.status_code == 200:
        assert b"Swagger" in rv.data or b"flasgger" in rv.data

if __name__ == "__main__":
    # Manual run support
    try:
        test_swagger_docs(app.test_client())
        print("Swagger Docs Test Passed!")
    except Exception as e:
        print(f"Swagger Docs Test Failed: {e}")
        exit(1)
