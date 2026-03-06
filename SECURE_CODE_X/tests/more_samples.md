# Vulnerable Code Samples for Testing

Here are some additional code snippets to test the Vulnerability Analyzer.

### 1. Java: SQL Injection & Weak Cryptography

```java
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.Statement;
import java.security.MessageDigest;

public class VulnerableApp {
    public void getUser(String username) {
        try {
            Connection conn = DriverManager.getConnection("jdbc:mysql://localhost:3306/db", "root", "password");
            Statement stmt = conn.createStatement();
            
            // Vulnerability: SQL Injection
            String query = "SELECT * FROM users WHERE username = '" + username + "'";
            stmt.executeQuery(query);
            
            // Vulnerability: Weak Cryptography (MD5)
            MessageDigest md = MessageDigest.getInstance("MD5");
            byte[] hash = md.digest(username.getBytes());
            
            // Vulnerability: Hardcoded Credential
            String apiKey = "1234567890-SECRET";
            
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

### 2. C++: Memory Safety Issues

```cpp
#include <iostream>
#include <cstring>

void process_input(char* user_input) {
    char buffer[10];
    
    // Vulnerability: Buffer Overflow
    strcpy(buffer, user_input);
    
    // Vulnerability: Memory Leak
    int* data = new int[100];
    data[0] = 5;
    // Missing delete[] data;
    
    // Vulnerability: Use After Free
    int* ptr = new int(10);
    delete ptr;
    *ptr = 20; // Writing to freed memory
}

int main() {
    process_input("This string is definitely too long for the buffer");
    return 0;
}
```

### 3. Python: Advanced Web Vulnerabilities

```python
from flask import Flask, request
import subprocess

app = Flask(__name__)

@app.route('/cmd')
def command():
    cmd = request.args.get('cmd')
    
    # Vulnerability: Command Injection
    subprocess.call(cmd, shell=True)
    return "Executed"

@app.route('/read')
def read_file():
    filename = request.args.get('file')
    
    # Vulnerability: Path Traversal
    with open("/var/www/" + filename, "r") as f:
        return f.read()

@app.route('/login')
def login():
    # Vulnerability: Hardcoded Secret
    if request.args.get('password') == "admin123":
        return "Logged in"
    return "Failed"
```
