def calculate_scores(vulnerabilities, code):
    """
    Calculates Security Score, Code Quality Score, and Overall Confidence.
    """
    
    # 1. Security Score (0-100)
    # Start at 100. Deduct points based on vulnerability severity.
    security_score = 100
    severity_weights = {
        "Critical": 40,
        "High": 20,
        "Medium": 10,
        "Low": 5
    }
    
    for vuln in vulnerabilities:
        deduction = severity_weights.get(vuln['severity'], 5)
        security_score -= deduction
    
    security_score = max(0, security_score) # Clamp to 0

    # 2. Code Quality Score (0-100)
    # Simple heuristic: heavily penalized by "bad practice" vulnerabilities 
    # and maybe length/complexity (not fully implemented here, using placeholder logic)
    quality_score = 100
    loc = len(code.split('\n'))
    
    # Penalize for critical security flaws as they are also quality flaws
    quality_score -= (100 - security_score) * 0.5 
    
    # Cap quality score
    quality_score = max(0, int(quality_score))

    # 3. Overall Confidence Score (0-100)
    # Base confidence depends on the language and analysis method. 
    # If we found vulnerabilities, we are fairly confident. 
    # If we didn't, we are less confident that there are NONE, but confident in our scan.
    confidence_score = 85 # Base confidence for static analysis
    
    if vulnerabilities:
        # If we found specific patterns, confidence increases
        unique_vulns = len(set(v['type'] for v in vulnerabilities))
        confidence_score += min(10, unique_vulns * 2)
    
    confidence_score = min(99, confidence_score)

    return {
        "security_score": str(security_score),
        "quality_score": str(quality_score),
        "confidence_score": str(confidence_score) + "%"
    }
