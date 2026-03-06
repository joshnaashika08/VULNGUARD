import pytest
import sys
import os
import json

# Add server to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'server'))

from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    rv = client.get('/health')
    assert rv.status_code == 200
    assert b"healthy" in rv.data

def test_analyze_python_vulnerability(client):
    code = """
import os
def run(cmd):
    os.system(cmd)
    """
    rv = client.post('/analyze', json={'code': code})
    data = json.loads(rv.data)
    
    assert rv.status_code == 200
    assert data['language'] == 'python'
    assert len(data['vulnerabilities']) > 0
    assert any(v['type'] == 'Command Injection' for v in data['vulnerabilities'])

def test_analyze_c_vulnerability(client):
    code = """
#include <string.h>
void func() {
    char buf[10];
    strcpy(buf, "long");
}
    """
    rv = client.post('/analyze', json={'code': code})
    data = json.loads(rv.data)
    
    assert rv.status_code == 200
    assert data['language'] in ['c', 'cpp']
    assert any(v['type'] == 'Buffer Overflow (strcpy)' for v in data['vulnerabilities'])
