
# Detailed Vulnerability Rules for Static Analysis
# Each rule contains: id, name, description, pattern (regex), severity, remediation

COMMON_RULES = {
    # C/C++ Rules
    "c": [
        {"id": "C01", "name": "Buffer Overflow (strcpy)", "pattern": r"strcpy\(", "severity": "Critical", "fix": "Use strncpy_s or strlcpy instead.", "cwe": "CWE-120"},
        {"id": "C02", "name": "Buffer Overflow (strcat)", "pattern": r"strcat\(", "severity": "Critical", "fix": "Use strncat_s or strlcat instead.", "cwe": "CWE-120"},
        {"id": "C03", "name": "Format String Vulnerability", "pattern": r"printf\([^\"]*\);", "severity": "High", "fix": "Ensure format string is constant or use specific format specifiers.", "cwe": "CWE-134"},
        {"id": "C04", "name": "Command Injection (system)", "pattern": r"system\(", "severity": "Critical", "fix": "Avoid system(). Use execve() family functions.", "cwe": "CWE-78"},
        {"id": "C05", "name": "Hardcoded Credentials", "pattern": r"(password|passwd|pwd|secret|token)\s*=\s*['\"].+['\"]", "severity": "High", "fix": "Use environment variables or a secrets manager.", "cwe": "CWE-798"},
        {"id": "C06", "name": "Insecure Randomness", "pattern": r"rand\(", "severity": "Medium", "fix": "Use logic from <random> or cryptographic PRNGs.", "cwe": "CWE-338"},
        {"id": "C07", "name": "Integer Overflow", "pattern": r"(short|int)\s+[a-zA-Z_]\w*\s*=\s*.*\*.*", "severity": "Medium", "fix": "Check for overflow before arithmetic operations.", "cwe": "CWE-190"},
        {"id": "C08", "name": "Use of gets()", "pattern": r"gets\(", "severity": "Critical", "fix": "Never use gets(). Use fgets().", "cwe": "CWE-242"},
        {"id": "C09", "name": "Race Condition (vfork)", "pattern": r"vfork\(", "severity": "High", "fix": "Use fork() instead of vfork() to avoid race conditions.", "cwe": "CWE-362"},
        {"id": "C10", "name": "Double Free", "pattern": r"free\(.*\);.*free\(.*\);", "severity": "High", "fix": "Ensure pointers are set to NULL after freeing.", "cwe": "CWE-415"},
        {"id": "C11", "name": "Memory Leak (malloc no free)", "pattern": r"malloc\(", "severity": "Medium", "fix": "Ensure allocated memory is freed.", "cwe": "CWE-401"},
        {"id": "C12", "name": "Uninitialized Variable", "pattern": r"(int|char|float|double)\s+[a-zA-Z_]\w*;", "severity": "Low", "fix": "Initialize variables on declaration.", "cwe": "CWE-457"},
        {"id": "C13", "name": "Null Pointer Dereference", "pattern": r"\*\w+\s*=\s*", "severity": "High", "fix": "Check for NULL before dereferencing.", "cwe": "CWE-476"},
        {"id": "C14", "name": "Unsafe Temporary File", "pattern": r"tmpnam\(", "severity": "Medium", "fix": "Use mkstemp() instead.", "cwe": "CWE-377"},
        {"id": "C15", "name": "Chroot Jail Break", "pattern": r"chroot\(", "severity": "High", "fix": "Ensure chroot is used securely and drops privileges.", "cwe": "CWE-243"},
        {"id": "C16", "name": "Weak Cryptography (DES)", "pattern": r"DES_", "severity": "High", "fix": "Use AES-256 or ChaCha20.", "cwe": "CWE-327"},
        {"id": "C17", "name": "Weak Cryptography (MD5)", "pattern": r"MD5\(", "severity": "Medium", "fix": "Use SHA-256 or SHA-3.", "cwe": "CWE-327"},
        {"id": "C18", "name": "Improper Exception Handling", "pattern": r"catch\(\.\.\.\)", "severity": "Low", "fix": "Catch specific exceptions.", "cwe": "CWE-755"},
    ],
    
    # C++ Rules (Inherits C rules generally, adding specific C++ ones)
    "cpp": [
         {"id": "CPP01", "name": "Use of auto_ptr", "pattern": r"std::auto_ptr", "severity": "Medium", "fix": "Use std::unique_ptr instead.", "cwe": "CWE-404"},
         {"id": "CPP02", "name": "Unprotected Member Access", "pattern": r"public:\s*\w+\s+\w+;", "severity": "Low", "fix": "Make data members private and use accessors.", "cwe": "CWE-494"},
         # ... include C rules as well in logic
    ],

    # Java Rules
    "java": [
        {"id": "J01", "name": "SQL Injection", "pattern": r"Statement\s+\w+\s*=\s*.*create(Statement|PreparedStatement)", "severity": "High", "fix": "Use PreparedStatement with placeholders.", "cwe": "CWE-89"},
        {"id": "J02", "name": "Command Injection", "pattern": r"Runtime\.getRuntime\(\)\.exec\(", "severity": "Critical", "fix": "Validate and sanitize inputs before execution.", "cwe": "CWE-78"},
        {"id": "J03", "name": "Weak Cryptography (MD5/SHA1)", "pattern": r"MessageDigest\.getInstance\(\"(MD5|SHA-1)\"\)", "severity": "Medium", "fix": "Use SHA-256 or stronger.", "cwe": "CWE-327"},
        {"id": "J04", "name": "Hardcoded Credentials", "pattern": r"String\s+(password|pwd|secret)\s*=\s*\"[^\"]+\"", "severity": "High", "fix": "Store secrets in secure config or vault.", "cwe": "CWE-798"},
        {"id": "J05", "name": "Insecure Randomness", "pattern": r"new\s+Random\(", "severity": "Low", "fix": "Use SecureRandom instead.", "cwe": "CWE-338"},
        {"id": "J06", "name": "XSS in JSP", "pattern": r"out\.print\(request\.getParameter", "severity": "High", "fix": "Encode output patterns.", "cwe": "CWE-79"},
        {"id": "J07", "name": "Insecure Deserialization", "pattern": r"ObjectInputStream", "severity": "Critical", "fix": "Validate class before deserializing.", "cwe": "CWE-502"},
        {"id": "J08", "name": "System.out.println finding", "pattern": r"System\.out\.println", "severity": "Low", "fix": "Use a logger (SLF4J, Log4j) instead.", "cwe": "CWE-532"},
        {"id": "J09", "name": "Thread.stop()", "pattern": r"Thread\.stop\(", "severity": "Medium", "fix": "Do not use deprecated Thread.stop().", "cwe": "CWE-676"},
        {"id": "J10", "name": "Empty Catch Block", "pattern": r"catch\s*\(\w+\s+\w+\)\s*\{\s*\}", "severity": "Low", "fix": "Log the exception.", "cwe": "CWE-390"},
        {"id": "J11", "name": "Public Mutable Field", "pattern": r"public\s+(?!final)\w+\s+\w+;", "severity": "Low", "fix": "Make fields private.", "cwe": "CWE-493"},
        {"id": "J12", "name": "File Inclusion", "pattern": r"new\s+File\(request\.getParameter", "severity": "High", "fix": "Validate filenames against an allowlist.", "cwe": "CWE-73"},
        {"id": "J13", "name": "LDAP Injection", "pattern": r"DirContext", "severity": "High", "fix": "Sanitize LDAP queries.", "cwe": "CWE-90"},
        {"id": "J14", "name": "XPath Injection", "pattern": r"XPath\.compile", "severity": "Medium", "fix": "Sanitize inputs to XPath.", "cwe": "CWE-643"},
        {"id": "J15", "name": "Unsafe Reflection", "pattern": r"Class\.forName", "severity": "Medium", "fix": "Validate class names.", "cwe": "CWE-470"}
    ],

    # Python Rules
    "python": [
        {"id": "P01", "name": "SQL Injection", "pattern": r"execute\(\s*[\"'].*\%s", "severity": "High", "fix": "Use parameterized queries (e.g. `execute(query, params)`).", "cwe": "CWE-89"},
        {"id": "P02", "name": "Command Injection", "pattern": r"(os\.system|subprocess\.call|subprocess\.Popen)\(", "severity": "Critical", "fix": "Use `subprocess.run` with `shell=False`.", "cwe": "CWE-78"},
        {"id": "P03", "name": "Hardcoded Credentials", "pattern": r"(password|secret|key|token)\s*=\s*['\"].+['\"]", "severity": "High", "fix": "Use environment variables.", "cwe": "CWE-798"},
        {"id": "P04", "name": "Insecure Deserialization", "pattern": r"pickle\.loads\(", "severity": "Critical", "fix": "Avoid `pickle` for untrusted data. Use JSON.", "cwe": "CWE-502"},
        {"id": "P05", "name": "Use of exec()", "pattern": r"exec\(", "severity": "High", "fix": "Avoid dynamic code execution.", "cwe": "CWE-94"},
        {"id": "P06", "name": "Use of eval()", "pattern": r"eval\(", "severity": "High", "fix": "Avoid `eval()`. Use `ast.literal_eval` safely.", "cwe": "CWE-95"},
        {"id": "P07", "name": "Weak Cryptography (MD5)", "pattern": r"hashlib\.md5", "severity": "Medium", "fix": "Use `hashlib.sha256`.", "cwe": "CWE-327"},
        {"id": "P08", "name": "Debug Mode Enabled", "pattern": r"debug\s*=\s*True", "severity": "High", "fix": "Disable debug mode in production.", "cwe": "CWE-489"},
        {"id": "P09", "name": "Binding to All Interfaces", "pattern": r"host\s*=\s*['\"]0\.0\.0\.0['\"]", "severity": "Medium", "fix": "Bind to specific internal IPs.", "cwe": "CWE-1327"},
        {"id": "P10", "name": "Django Secret Key", "pattern": r"SECRET_KEY\s*=\s*['\"].+['\"]", "severity": "High", "fix": "Load SECRET_KEY from env.", "cwe": "CWE-798"},
        {"id": "P11", "name": "Unsafe YAML Load", "pattern": r"yaml\.load\(", "severity": "High", "fix": "Use `yaml.safe_load()`.", "cwe": "CWE-502"},
        {"id": "P12", "name": "Requests with verify=False", "pattern": r"requests\.\w+\(.*\s*verify\s*=\s*False", "severity": "High", "fix": "Enable SSL verification.", "cwe": "CWE-295"},
        {"id": "P13", "name": "Temporary File Creation", "pattern": r"tempfile\.mktemp", "severity": "Medium", "fix": "Use `tempfile.mkstemp`.", "cwe": "CWE-377"},
        {"id": "P14", "name": "Assert Used in Security Check", "pattern": r"assert\s+.+", "severity": "Low", "fix": "Do not use assert for security, checks are optimized out.", "cwe": "CWE-703"},
        {"id": "P15", "name": "FTP Usage", "pattern": r"ftplib\.FTP", "severity": "Medium", "fix": "Use SFTP or HTTPS.", "cwe": "CWE-319"},
        {"id": "P16", "name": "Telnet Usage", "pattern": r"telnetlib\.Telnet", "severity": "Medium", "fix": "Use SSH.", "cwe": "CWE-319"},
        {"id": "P17", "name": "XML External Entity (XXE)", "pattern": r"etree\.parse", "severity": "High", "fix": "Disable external entities in XML parser.", "cwe": "CWE-611"},
        {"id": "P18", "name": "Flask Send File Issue", "pattern": r"send_file\(.*filename=.*\)", "severity": "Medium", "fix": "Ensure filename is validated.", "cwe": "CWE-22"},
        {"id": "P19", "name": "Pseudo-Random Number Generator", "pattern": r"random\.random", "severity": "Low", "fix": "Use `secrets` module.", "cwe": "CWE-338"},
        {"id": "P20", "name": "Generic Exception Catch", "pattern": r"except\s+Exception\s*:", "severity": "Low", "fix": "Catch specific exceptions.", "cwe": "CWE-703"}
    ]
}

def get_rules_for_language(language):
    rules = COMMON_RULES.get(language, [])
    if language == 'cpp':
        rules.extend(COMMON_RULES.get('c', []))
    return rules
