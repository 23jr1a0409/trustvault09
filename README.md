# TrustVault - Secure Document Sharing Platform

## Live Application
https://trustvault09.onrender.com

## Demo Video
https://www.loom.com/share/037da7beeb9f4d5e882a192095d2459b

## GitHub Repository
https://github.com/23jr1a0409/trustvault09

## 1. Project Description

TrustVault is a secure document-sharing web application built using Python and Flask. It allows users to register, log in, upload and download documents, share files with registered users, and manage document access permissions.

The application includes role-based access control, audit logging, login rate limiting, and SHA-256 hashing to support document security and integrity verification.

## 2. Features

- User registration and login
- Secure document upload and download
- Document sharing with registered users
- Read and edit permission options
- Grant and revoke document access
- Role-based access control
- Audit logging for document activities
- Login rate limiting to help prevent brute-force attempts
- SHA-256 document integrity hashing
- File type validation and 5 MB upload limit

## 3. Technologies Used

- Python
- Flask
- Flask-SQLAlchemy
- Flask-Login
- Flask-Limiter
- SQLite
- HTML
- Git and GitHub
- Render

## 4. Project Structure

```text
trustvault09/
├── templates/
├── .gitignore
├── PROMPTS.md
├── Procfile
├── THREATS.md
├── app.py
├── requirements.txt
└── README.md
```

## 5. How to Run Locally

### Prerequisites
- Python installed
- Git installed

### Step 1: Clone the Repository

```bash
git clone https://github.com/23jr1a0409/trustvault09.git
```

### Step 2: Open the Project Folder

```bash
cd trustvault09
```

### Step 3: Create a Virtual Environment

```bash
python -m venv venv
```

### Step 4: Activate the Virtual Environment on Windows

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate the environment again.

### Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 6: Configure the Secret Key

Run this command in PowerShell:

```powershell
$env:SECRET_KEY = python -c "import secrets; print(secrets.token_hex(32))"
```

### Step 7: Start the Application

```bash
python app.py
```

### Step 8: Open the Application

Open this URL in your browser:

http://127.0.0.1:5000

Register an account or log in to use the application.

## 6. Security Measures

- Passwords are stored using password hashing.
- Login attempts are rate-limited.
- Document access is checked on the server.
- Only document owners can grant or revoke sharing permissions.
- Audit logs are restricted to administrator accounts.
- Uploaded filenames are sanitized, and unique stored filenames are generated.
- File extensions and upload size are validated.
- SHA-256 hashing is included for document integrity verification.

## 7. AI Tools Used

ChatGPT was used for implementation guidance, understanding security concepts, debugging suggestions, and improving the application. I implemented, tested, and deployed the project myself with the help of these suggestions.

## 8. Project Documentation

- `PROMPTS.md` — Records AI prompts, response summaries, implementation details, and lessons learned.
- `THREATS.md` — Documents potential security threats and mitigation strategies.

## 9. Current Limitations

- The View Audit Logs link is not currently visible on the live website, although it works locally.
- Production database persistence and data migration need further improvement.
- Additional security testing and user-interface improvements are needed.
- The Edit permission does not currently provide full document-editing functionality.

## 10. Links

- **Live Application:** https://trustvault09.onrender.com
- **Demo Video:** https://www.loom.com/share/037da7beeb9f4d5e882a192095d2459b
- **GitHub Repository:** https://github.com/23jr1a0409/trustvault09
