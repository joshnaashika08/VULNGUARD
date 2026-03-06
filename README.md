🔐 VulnGuard – AI Powered Code Vulnerability Analyzer

VulnGuard is a full-stack security analysis platform that detects security vulnerabilities and code quality issues in multiple programming languages including C, C++, Java, and Python.

It provides developers with a modern web interface to scan code, detect security flaws, and receive actionable remediation suggestions.

🚀 Features
🔎 Multi-Language Detection

Automatically detects and analyzes source code written in:

C

C++

Java

Python

🧠 Hybrid Vulnerability Detection

VulGuard combines multiple analysis techniques for accurate detection.

Regex Engine

Detects known vulnerability signatures

Used for C, C++, and Java

AST Analysis (Python)

Parses Python code into Abstract Syntax Trees

Detects logical vulnerabilities such as:

Unsafe imports

Dangerous system calls

Command injections

🛡️ 50+ Security Vulnerability Rules

The analyzer detects critical vulnerabilities such as:

SQL Injection

Cross-Site Scripting (XSS)

Buffer Overflow

Command Injection

Hardcoded Credentials

Path Traversal

Weak Cryptography

Insecure Deserialization

Each detection includes:

Severity level

Vulnerability explanation

Suggested remediation

📊 Security Scoring System

Each scan generates three metrics:

Security Score

Measures severity of vulnerabilities

Code Quality Score

Evaluates coding practices

Confidence Score

Indicates reliability of detection

🌐 Modern Interactive UI

The frontend is designed for a smooth and professional developer experience.

Features include:

Animated UI using Framer Motion

Responsive design with Bootstrap 5

Clean modern icons using Lucide React

🛠️ Tech Stack
Backend

Python

Flask

Python AST

Regex Pattern Engine

Frontend

React (Vite)

Bootstrap 5

Custom CSS

Framer Motion

⚙️ Installation & Running
Prerequisites

Make sure the following tools are installed:

Python 3.8+

Node.js 16+

npm

🚀 One-Click Execution (Windows)

Simply run:

run_project.bat

This script will automatically:

1️⃣ Install backend dependencies
2️⃣ Install frontend dependencies
3️⃣ Start both servers

🔧 Manual Setup
1️⃣ Backend Setup

Install dependencies:

pip install -r server/requirements.txt

Start the Flask server:

python server/app.py

Backend will run at:

http://localhost:5000
2️⃣ Frontend Setup

Navigate to the client directory:

cd client

Install dependencies:

npm install

Run the frontend server:

npm run dev

Frontend will run at:

http://localhost:3000
🧑‍💻 Usage

1️⃣ Open the web application in your browser
2️⃣ Paste your source code into the editor
3️⃣ Click Analyze Code
4️⃣ View detected vulnerabilities and suggested fixes

The application will generate a security analysis report for the submitted code.

📂 Project Structure
VulGuard
│
├── client/                 # React Frontend
│   └── src/
│       └── components/     # UI Components
│
├── server/                 # Flask Backend
│   └── analyzer/           # Core Analysis Engine
│       ├── ast_engine.py
│       ├── regex_engine.py
│       ├── rules.py
│
├── run_project.bat         # One-click project runner
└── README.md
📚 API Documentation

The backend includes interactive Swagger API documentation.

After starting the server, open:

http://localhost:5000/apidocs/

This allows developers to test API endpoints directly from the browser.

🧪 Testing

Run backend tests using:

pytest
🎯 Future Improvements

LLM-based vulnerability explanation (GPT/Gemini)

CI/CD pipeline integration

Support for additional languages (JavaScript, Go, Rust)

IDE plugins (VS Code extension)
