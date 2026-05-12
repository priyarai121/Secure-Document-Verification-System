# Project Report: Secure Document Verification System

## 1. Abstract
The **Secure Document Verification System** is a robust, web-based application designed to ensure the integrity, authenticity, and secure storage of sensitive digital documents. By leveraging advanced cryptographic techniques—such as SHA-256 hashing, RSA encryption, and Base64 encoding—the system provides a tamper-evident environment where users can confidently upload and verify their files.

---

## 2. Problem Statement
In the digital age, documents such as academic transcripts, legal contracts, and financial records are frequently shared online. However, digital files are highly susceptible to unauthorized modifications, forgery, and tampering. Traditional centralized databases often lack the necessary cryptographic layers to prove that a document has remained absolutely unaltered since its creation or upload. There is a critical need for a system that can mathematically guarantee a document's integrity and immediately detect any tampering attempts.

---

## 3. Proposed Solution
The Secure Document Verification System solves this problem by generating a unique digital fingerprint (SHA-256 hash) for every uploaded document. Instead of storing the hash in plain text, the system encrypts the hash using RSA encryption (PKCS1_OAEP) and encodes it in Base64 for secure database storage. When a user wishes to verify a document, they re-upload the file. The system calculates the new hash and compares it against the securely stored original hash. Any mismatch immediately flags the document as **Tampered**, ensuring 100% data integrity.

---

## 4. Technology Stack Used
- **Backend Framework:** Python (Flask)
- **Database:** SQLite with Flask-SQLAlchemy (ORM)
- **Frontend Technologies:** HTML5, CSS3 (Custom Glassmorphism & Cybersecurity Theme), Vanilla JavaScript
- **Cryptographic Libraries:** `hashlib` (SHA-256), `cryptography` / `pycryptodome` (RSA Encryption), `base64`
- **Authentication:** Flask-Login, Werkzeug Security (PBKDF2 Password Hashing)
- **Data Visualization:** Chart.js (for Dashboard Analytics)

---

## 5. Key Features of the Project
1. **Secure User Authentication:** Encrypted password storage using `pbkdf2:sha256` ensures user credentials cannot be compromised. Role-based session management using Flask-Login.
2. **Cryptographic Uploads:** Uploaded documents are never just saved; they are hashed, and the hash is securely encrypted via RSA public keys before being stored in the database.
3. **Tamper Detection Engine:** A dedicated verification module that recalculates the hash of a tested file and compares it to the original encrypted hash, accurately detecting even a single byte of modification.
4. **Modern Dashboard Analytics:** A visually appealing dashboard that visualizes document upload trends and verification statistics using Chart.js.
5. **Comprehensive History Tracking:** A detailed audit trail of all uploaded documents, their upload dates, and their current verification status (Verified, Tampered, or Pending).
6. **Cybersecurity-Themed UI/UX:** A responsive, "glassmorphic" user interface featuring a dark mode color palette (black, dark blue, neon green), smooth animations, and interactive elements.
7. **Robust Error Handling:** Custom 404 (Not Found) and 500 (Server Error) pages, alongside intelligent file-upload validation.

---

## 6. Project Development Stages
The project was developed methodically through the following stages:

### **Stage 1: Foundational Architecture**
- Setup of the Flask environment and SQLite database.
- Implementation of the User and Document models using SQLAlchemy.
- Creation of the user registration, login, and session management system.
- Development of the base HTML templates and routing.

### **Stage 2: Cryptographic Implementation**
- Integration of `hashlib` to calculate the SHA-256 hash of documents in chunks to handle large files efficiently.
- Implementation of RSA key generation, encryption of the hash using PKCS1_OAEP, and Base64 encoding to store binary encrypted data safely in the database.

### **Stage 3: Verification & Dashboard**
- Development of the verification algorithm to decrypt, decode, and compare document hashes.
- Creation of the Dashboard to display document statistics, upload trends, and recent activity.
- Implementation of the History page to filter and search through past document verifications.

### **Final Stage: Polish, UI/UX, and Future-Proofing**
- Comprehensive CSS overhaul to introduce the modern cybersecurity theme, loading animations, and active page highlighting.
- Addition of flash message alerts with SVG icons.
- Implementation of global error handling (404 and 500 pages).
- Setup of the `blockchain/` folder structure to prepare for decentralized smart contract integration.
- Final code cleanup, commenting, and documentation generation (`README.md`, `requirements.txt`).

---

## 7. Advantages of the System
- **Immutable Proof:** Provides mathematical certainty regarding document integrity.
- **Privacy Preserving:** The system only needs to compare hashes; it does not need to read the contents of the document during verification.
- **High Security:** By combining SHA-256 hashing with RSA encryption, the system protects against both tampering and database breaches.
- **User-Friendly:** Abstract complex cryptography behind a clean, intuitive, and modern user interface.
- **Scalable Foundation:** Built on a modular architecture that easily allows for future technological upgrades.

---

## 8. Future Scope (Blockchain Integration)
While the current system relies on a centralized SQLite database to store the encrypted hashes, the next evolution of this project involves decentralization.
- **Smart Contracts:** The system will interact with Ethereum-based smart contracts to anchor document hashes directly onto the blockchain.
- **Decentralized Ledger:** By storing the hash on an immutable public ledger, the system will completely remove the single point of failure associated with centralized databases. Even if the application server is compromised, the mathematical proof of the document will remain intact on the blockchain.

---

## 9. Conclusion
The Secure Document Verification System successfully bridges the gap between advanced cryptographic security and user-friendly web design. By implementing robust hashing, encryption, and an intuitive UI, the project effectively solves the problem of digital document forgery. It stands as a secure, reliable, and scalable platform that is fully prepared for its next phase of blockchain-based decentralization.

---

## 10. References
1. **Flask Documentation:** https://flask.palletsprojects.com/
2. **Python Cryptography Authority:** https://cryptography.io/
3. **SHA-2 Secure Hash Algorithms:** NIST FIPS 180-4
4. **SQLAlchemy ORM Documentation:** https://www.sqlalchemy.org/
5. **Chart.js Documentation:** https://www.chartjs.org/
6. **MDN Web Docs (Base64 & Web APIs):** https://developer.mozilla.org/
