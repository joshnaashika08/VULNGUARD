from .language_detector import LanguageDetector
from .ast_engine import analyze_python_ast
from .regex_engine import analyze_regex
from .scoring import calculate_scores
from .rules import get_rules_for_language

class Analyzer:
    def __init__(self):
        self.detector = LanguageDetector()

    def analyze(self, code, specified_language=None):
        language = specified_language
        if not language:
            language = self.detector.detect(code)

        vulnerabilities = []
        
        # Select Analysis Engine
        if language == 'python':
            # Hybrid approach for Python: AST + Regex
            ast_vulns = analyze_python_ast(code)
            regex_vulns = analyze_regex(code, language) # Regex can catch things AST might miss or code pattern issues
            vulnerabilities = ast_vulns + regex_vulns
        elif language in ['c', 'cpp', 'java']:
            # Regex based analysis for others
            vulnerabilities = analyze_regex(code, language)
        else:
            # Fallback or error for unsupported
            pass

        # Calculate Scores
        scores = calculate_scores(vulnerabilities, code)

        return {
            "language": language,
            "vulnerabilities": vulnerabilities,
            "code_quality_score": scores["quality_score"],
            "security_score": scores["security_score"],
            "overall_confidence": scores["confidence_score"],
            "metadata": {
                "loc": len(code.split('\n')),
                "vuln_count": len(vulnerabilities)
            }
        }
