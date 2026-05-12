# Secure Document Verification System

## Project Overview
The Secure Document Verification System is a robust web application built with Flask that allows users to upload, securely store, and verify the integrity of their sensitive documents. Using advanced cryptographic techniques, the system ensures that any unauthorized modification or tampering of a document is immediately detected.

## Features
- **User Authentication:** Secure registration and login system with hashed passwords.
- **Document Uploads:** Upload documents securely with Base64 encoding.
- **Tamper Detection:** Verification engine that checks uploaded files against their original SHA-256 hash.
- **Cryptographic Security:** Documents are protected using RSA encryption (PKCS1_OAEP) and SHA-256 hashing.
- **Dashboard & Analytics:** A modern, glassmorphic dashboard displaying document statistics and upload trends.
- **History Tracking:** Comprehensive history of verified and tampered documents.
- **Responsive UI/UX:** A modern cybersecurity-themed interface with smooth animations and intuitive navigation.

## Installation Steps
1. **Clone the repository:**
   ```bash
   git clone <repository_url>
   cd "Secure Document Verification System"
   ```
2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the application:**
   ```bash
   python app.py
   ```
5. **Access the application:** Open your browser and navigate to `http://127.0.0.1:5000/`

## Folder Structure
```text
Secure Document Verification System/
│
├── app.py                 # Main Flask application
├── requirements.txt       # Project dependencies
├── README.md              # Project documentation
│
├── blockchain/            # Future blockchain integration placeholder
│   ├── blockchain.py
│   ├── smart_contracts/
│   └── ledger/
│
├── models/                # Database models
│   ├── __init__.py
│   ├── document.py
│   └── user.py
│
├── utils/                 # Cryptographic utilities
│   ├── encoding.py
│   ├── encryption.py
│   └── verification.py
│
├── static/                # Static assets (CSS, JS, Uploads)
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── main.js
│   └── uploads/
│
└── templates/             # HTML templates (Jinja2)
    ├── base.html
    ├── index.html
    ├── dashboard.html
    ├── upload.html
    ├── verify.html
    ├── history.html
    ├── login.html
    ├── register.html
    ├── 404.html
    └── 500.html
```



## Security Concepts Used
- **SHA-256 Hashing:** Used to create a unique digital fingerprint of each document.
- **RSA Encryption (PKCS1_OAEP):** Used to securely encrypt the document hashes before storing them in the database.
- **Base64 Encoding:** Ensures safe transport and storage of binary encrypted data.
- **Password Hashing (PBKDF2):** Secures user credentials.
- **Secure File Handling:** Werkzeug's `secure_filename` is used to prevent directory traversal attacks during uploads.

## Future Blockchain Integration Plan
In the next phase of development, the verification system will be decentralized using blockchain technology.
- **Smart Contracts:** Will be used to automatically verify document hashes without relying on a central database.
- **Ledger:** An immutable ledger will store the history of document verifications, providing mathematical proof of existence and integrity.
- **Structure:** The `blockchain/` directory has been set up as a placeholder for these future modules.
