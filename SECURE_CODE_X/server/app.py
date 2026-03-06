import os
import sys

# Ensure the server directory is in path for relative/package imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, request, jsonify, send_file, render_template
from flask_cors import CORS
from flasgger import Swagger
from analyzer.core import Analyzer
from analyzer.repo_analyzer import RepoAnalyzer
from analyzer.pdf_generator import generate_pdf_report
import traceback
import requests
import zipfile
import io
import shutil

app = Flask(__name__)
CORS(app)
swagger = Swagger(app)

analyzer = Analyzer()
repo_analyzer = RepoAnalyzer()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "version": "1.0.0"}), 200

@app.route('/analyze', methods=['POST'])
def analyze_code():
    """
    Analyze source code for vulnerabilities
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            code:
              type: string
              example: "import os\nos.system('ls')"
            language:
              type: string
              example: "python"
    responses:
      200:
        description: Analysis results
        schema:
          type: object
          properties:
            vulnerabilities:
              type: array
              items:
                type: object
            security_score:
              type: string
            code_quality_score:
              type: string
            overall_confidence:
              type: string
    """
    try:
        data = request.get_json()
        if not data or 'code' not in data:
            return jsonify({"error": "No code provided"}), 400

        source_code = data['code']
        # Optional: Allow user to specify language, otherwise detect it
        specified_language = data.get('language')

        results = analyzer.analyze(source_code, specified_language)
        
        return jsonify(results), 200

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@app.route('/analyze/local', methods=['POST'])
def analyze_local_folder():
    try:
        data = request.get_json()
        path = data.get('path', '.')
        if not os.path.exists(path):
            return jsonify({"error": "Path does not exist"}), 400
        
        results = repo_analyzer.scan_directory(path)
        return jsonify(results), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route('/analyze/github', methods=['POST'])
def analyze_github_repo():
    try:
        data = request.get_json()
        repo_url = data.get('url')
        if not repo_url:
            return jsonify({"error": "No URL provided"}), 400
        
        # Simple extraction of owner/repo from URL
        # e.g., https://github.com/owner/repo
        parts = repo_url.strip('/').split('/')
        if len(parts) < 2:
             return jsonify({"error": "Invalid GitHub URL"}), 400
        
        owner, repo = parts[-2], parts[-1]
        zip_url = f"https://github.com/{owner}/{repo}/archive/refs/heads/main.zip"
        
        # Download and extract
        resp = requests.get(zip_url)
        if resp.status_code != 200:
             # Try 'master' if 'main' fails
             zip_url = f"https://github.com/{owner}/{repo}/archive/refs/heads/master.zip"
             resp = requests.get(zip_url)
             if resp.status_code != 200:
                 return jsonify({"error": f"Could not fetch repo: {resp.status_code}"}), 400
        
        temp_dir = f"temp_scan_{repo}"
        with zipfile.ZipFile(io.BytesIO(resp.content)) as z:
            z.extractall(temp_dir)
        
        # Scan the extracted dir
        results = repo_analyzer.scan_directory(temp_dir)
        
        # Cleanup
        shutil.rmtree(temp_dir)
        
        return jsonify(results), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route('/ai/fix', methods=['POST'])
def get_ai_fix():
    """
    Simulated AI Fix suggestion.
    In a real app, this would call GPT-4 or Gemini.
    """
    try:
        data = request.get_json()
        vuln_type = data.get('type')
        
        # Enhanced simulated AI fixes
        fixes = {
            "SQL Injection": {
                "suggestion": "Use parameterized queries (e.g., cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))) instead of string formatting.",
                "explained": "String interpolation allows attackers to inject malicious SQL commands. Parameterized queries treat user input as data only, never as executable code."
            },
            "Command Injection": {
                "suggestion": "Avoid os.system() or shell=True. Use subprocess.run(['cmd', 'arg']) with lists to prevent shell interpretation.",
                "explained": "Shell-based execution can be hijacked with delimiters like ';' or '&'. Using lists prevents the shell from interpreting user-supplied command parts."
            },
            "Buffer Overflow (strcpy)": {
                "suggestion": "Replace strcpy() with strncpy() or better, use std::string in C++ or safe bounds-checked alternatives in C.",
                "explained": "strcpy does not check the destination buffer size, leading to memory corruption. Bounds checking prevents memory being overwritten beyond the buffer limit."
            }
        }
        
        fix_data = fixes.get(vuln_type, {
            "suggestion": "Review the code and implement bounds checking or input validation.",
            "explained": "This vulnerability is caused by untrusted input reaching a sink. Always validate or sanitize data from external sources."
        })
        
        return jsonify(fix_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/report/pdf', methods=['POST'])
def get_pdf_report():
    """
    Generate PDF Report
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          description: The analysis result object returned by /analyze
    responses:
      200:
        description: PDF Report file
        content:
          application/pdf:
            schema:
              type: string
              format: binary
    """
    try:
        data = request.get_json()
        if not data:
             return jsonify({"error": "No data provided"}), 400
             
        pdf_buffer = generate_pdf_report(data)
        
        return send_file(
            pdf_buffer,
            as_attachment=True,
            download_name='vulnerability_report.pdf',
            mimetype='application/pdf'
        )
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
