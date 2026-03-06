import os
try:
    from analyzer.core import Analyzer
except ImportError:
    from core import Analyzer

class RepoAnalyzer:
    def __init__(self):
        self.analyzer = Analyzer()
        self.supported_extensions = ['.py', '.c', '.cpp', '.java']

    def scan_directory(self, root_dir):
        """
        Recursively scan a directory for vulnerabilities.
        """
        vulnerabilities = []
        files_scanned = 0
        total_security_score = 0
        total_quality_score = 0

        for root, dirs, files in os.walk(root_dir):
            for file in files:
                if any(file.endswith(ext) for ext in self.supported_extensions):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            code = f.read()
                        
                        file_results = self.analyzer.analyze(code)
                        
                        # Add file context to vulnerabilities
                        for vuln in file_results['vulnerabilities']:
                            vuln_copy = vuln.copy()
                            vuln_copy['file'] = os.path.relpath(file_path, root_dir)
                            vulnerabilities.append(vuln_copy)
                        
                        files_scanned += 1
                        total_security_score += int(file_results['security_score'])
                        total_quality_score += int(file_results['code_quality_score'])
                        
                    except Exception as e:
                        print(f"Error scanning {file_path}: {e}")

        security_score = "0"
        code_quality_score = "0"
        if files_scanned > 0:
            security_score = str(int(total_security_score) // int(files_scanned))
            code_quality_score = str(int(total_quality_score) // int(files_scanned))
        
        return {
            "vulnerabilities": vulnerabilities,
            "files_scanned": files_scanned,
            "security_score": security_score,
            "code_quality_score": code_quality_score,
            "overall_confidence": "High",
            "language": "Mixed"
        }
