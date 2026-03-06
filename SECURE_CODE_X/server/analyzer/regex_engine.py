import re
# Relative import for package context
# This might show an error in some IDEs if the root content is not set correctly.
from analyzer.rules import get_rules_for_language  # type: ignore

def analyze_regex(code, language):
    vulnerabilities = []
    lines = code.split('\n')
    rules = get_rules_for_language(language)

    for i, line in enumerate(lines):
        line_num = i + 1
        for rule in rules:
            # Check pattern
            if re.search(rule['pattern'], line):
                # Simple check: ignore comments?
                # A robust parser would strip comments, but for regex-only:
                if language in ['c', 'cpp', 'java'] and line.strip().startswith('//'):
                    continue
                if language == 'python' and line.strip().startswith('#'):
                    continue

                vulnerabilities.append({
                    "id": rule['id'],
                    "type": rule['name'],
                    "severity": rule['severity'],
                    "line": line_num,
                    "description": f"Match found for {rule['name']}",
                    "suggested_fix": rule['fix'],
                    "confidence": "Medium" 
                })
    
    return vulnerabilities
