# AI-Powered Code Vulnerability Analyzer

A full-stack web application that detects security vulnerabilities and code quality issues in C, C++, Java, and Python source code.

## Features
- **Multi-Language Support**: Auto-detects C, C++, Java, and Python.
- **Deep Analysis**: Uses AST (Abstract Syntax Tree) for Python and advanced Regex patterns for other languages.
- **50+ Vulnerability Rules**: Detects SQL Injection, Buffer Overflows, XSS, Command Injection, and more.
- **Modern UI**: Built with React, Vite, and Framer Motion for a smooth, animated experience.
- **Scoring System**: Provides Security Score, Code Quality Score, and Confidence levels.

## Tech Stack
- **Backend**: Python (Flask)
- **Frontend**: React (Vite)
- **Styling**: Bootstrap 5, Custom CSS, Framer Motion
- **Analysis**: Python AST, Regex

## Installation & Running

### Prerequisites
- Python 3.8+
- Node.js & npm

### One-Click Execution (Windows)
Simply double-click `run_project.bat` in the root directory.
This script will:
1. Install backend dependencies.
2. Install frontend dependencies.
3. Start both servers automatically.

### Manual Setup
### 1. Backend Setup
Navigate to the project root and install Python dependencies:
```bash
pip install -r server/requirements.txt
```

Run the Flask server:
```bash
python server/app.py
```
The server will start on `http://localhost:5000`.

### 2. Frontend Setup
Navigate to the client directory:
```bash
cd client
```

Install Node dependencies:
```bash
npm install
```

Start the development server:
```bash
npm run dev
```
The application will open at `http://localhost:3000` (or similar).

## Usage
1. Open the web app.
2. Paste your source code into the text area.
3. Click **Analyze Code**.
4. View the security report, including severity levels and suggested fixes.

## Project Structure
- `server/`: Flask backend and analysis logic.
  - `analyzer/`: Core analysis modules (AST, Regex, Rules).
- `client/`: React frontend.
  - `src/components/`: Reusable UI components.

## API Documentation
The backend includes built-in Swagger documentation.
Once running, visit: `http://localhost:5000/apidocs/` to explore and test the API interactively.

## Testing
To run backend tests:
```bash
pytest
```
