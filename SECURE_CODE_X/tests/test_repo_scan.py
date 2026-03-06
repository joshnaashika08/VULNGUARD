import pytest
import sys
import os
import json
import shutil
import tempfile

# Add server to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'server'))

try:
    from analyzer.repo_analyzer import RepoAnalyzer
    from app import app
except ImportError:
    # Fallback for environments where server/ isn't a package
    from backend.server.analyzer.repo_analyzer import RepoAnalyzer
    from backend.server.app import app

@pytest.fixture
def repo_analyzer():
    return RepoAnalyzer()

@pytest.fixture
def temp_repo():
    # Create a temporary directory with some vulnerable files
    tmpdir = tempfile.mkdtemp()
    
    # Vulnerable Python file
    py_path = os.path.join(tmpdir, "vuln.py")
    with open(py_path, "w") as f:
        f.write("import os\ndef run(c): os.system(c)")
    
    # Vulnerable C file
    c_path = os.path.join(tmpdir, "vuln.c")
    with open(c_path, "w") as f:
        f.write("#include <string.h>\nvoid f(char* s) { char b[10]; strcpy(b, s); }")
    
    yield tmpdir
    shutil.rmtree(tmpdir)

def test_repo_analyzer_scan(repo_analyzer, temp_repo):
    results = repo_analyzer.scan_directory(temp_repo)
    
    assert results['files_scanned'] == 2
    assert len(results['vulnerabilities']) >= 2
    assert int(results['security_score']) < 50  # Should be low due to high severity vulns
    assert results['language'] == 'Mixed'

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_local_analyze_endpoint(client, temp_repo):
    rv = client.post('/analyze/local', json={'path': temp_repo})
    data = json.loads(rv.data)
    
    assert rv.status_code == 200
    assert data['files_scanned'] == 2
    assert 'vulnerabilities' in data
