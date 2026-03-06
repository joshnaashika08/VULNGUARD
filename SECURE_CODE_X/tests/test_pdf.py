import sys
import os
import io

# Add server to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'server')))

# Import from server module (dynamic path setup)
# This may show a lint error in some IDEs, but it works at runtime.
from analyzer.pdf_generator import generate_pdf_report  # type: ignore

def test_pdf_generation():
    mock_data = {
        "language": "python",
        "security_score": "80",
        "code_quality_score": "90",
        "overall_confidence": "High",
        "vulnerabilities": [
            {
                "type": "SQL Injection",
                "severity": "High",
                "line": 10,
                "description": "Detected SQL Injection",
                "suggested_fix": "Use parameterized queries"
            }
        ]
    }
    
    pdf_buffer = generate_pdf_report(mock_data)
    assert isinstance(pdf_buffer, io.BytesIO)
    content = pdf_buffer.getvalue()
    assert len(content) > 0
    assert b"%PDF" in content
    print("PDF Generation Test Passed!")

if __name__ == "__main__":
    test_pdf_generation()
