import ast
# Relative import works when run as a module (python -m server.app) or from local package context
# This might show an error in some IDEs if the root content is not set correctly.
from analyzer.rules import get_rules_for_language  # type: ignore

class VulnVisitor(ast.NodeVisitor):
    def __init__(self, code):
        self.code_lines = code.split('\n')
        self.vulnerabilities = []
    
    def visit_Call(self, node):
        # Check for function calls that match vulnerabilities
        func_name = self._get_func_name(node.func)
        
        # Checking for specific dangerous functions via AST (more accurate than regex)
        if func_name == 'eval':
             self._add_vuln("P06", "Use of eval()", "Critical", node.lineno, "Use ast.literal_eval instead.")
        elif func_name == 'exec':
             self._add_vuln("P05", "Use of exec()", "High", node.lineno, "Avoid execution of dynamic code.")
        elif func_name == 'pickle.loads':
             self._add_vuln("P04", "Insecure Deserialization", "Critical", node.lineno, "Do not unpickle untrusted data.")
        elif func_name in ['os.system', 'subprocess.call', 'subprocess.Popen']:
             self._add_vuln("P02", "Command Injection", "Critical", node.lineno, "Use subprocess.run with shell=False.")
        
        self.generic_visit(node)

    def visit_Import(self, node):
        for alias in node.names:
            if alias.name == 'telnetlib':
                self._add_vuln("P16", "Insecure Protocol (Telnet)", "Medium", node.lineno, "Use SSH instead.")
            elif alias.name == 'ftplib':
                self._add_vuln("P15", "Insecure Protocol (FTP)", "Medium", node.lineno, "Use SFTP instead.")
        self.generic_visit(node)

    def visit_Assign(self, node):
        # Heuristic for Hardcoded Credentials
        # Looking for variables named 'password', 'key', etc. assigned to string literals
        for target in node.targets:
            if isinstance(target, ast.Name):
                if any(x in target.id.lower() for x in ['password', 'secret', 'api_key', 'token']):
                    if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                        self._add_vuln("P03", "Hardcoded Credential", "High", node.lineno, "Use env vars.")
        self.generic_visit(node)

    def _get_func_name(self, node):
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{self._get_func_name(node.value)}.{node.attr}"
        return ""

    def _add_vuln(self, id, name, severity, line, fix):
        self.vulnerabilities.append({
            "id": id,
            "type": name,
            "severity": severity,
            "line": line,
            "description": f"Detected {name}",
            "suggested_fix": fix,
            "confidence": "High"  # AST based is usually high confidence
        })

def analyze_python_ast(code):
    try:
        tree = ast.parse(code)
        visitor = VulnVisitor(code)
        visitor.visit(tree)
        return visitor.vulnerabilities
    except SyntaxError:
        # If AST parsing fails (syntax error in user code), return empty or partial
        return []
    except Exception as e:
        print(f"AST Analysis failed: {e}")
        return []
