# Secure Document Verification System

A secure web application for document verification built using Flask. This system provides foundational architecture including user authentication (registration/login), password hashing, and a responsive frontend, serving as a base for future cryptographic and document verification features.

## Features

- **User Authentication**: Secure registration and login functionalities.
- **Password Hashing**: Utilizes Werkzeug's `pbkdf2:sha256` for secure password storage.
- **Database Integration**: Uses SQLAlchemy with an SQLite database.
- **Responsive UI**: A modern, responsive frontend using HTML, CSS, and JavaScript.

## Technology Stack

- **Backend**: Python, Flask
- **Database**: SQLite, Flask-SQLAlchemy
- **Authentication**: Flask-Login, Werkzeug
- **Cryptography**: `cryptography`, `pycryptodome`

## Installation

1. **Clone the repository or download the source code.**

2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   python app.py
   ```

5. **Access the application:**
   Open your web browser and navigate to `http://127.0.0.1:5000/`.

## Project Structure

- `app.py`: Main Flask application file containing routes and configuration.
- `models/`: Contains database models (e.g., `user.py`).
- `templates/`: HTML templates for the frontend.
- `static/`: Static assets (CSS, JavaScript, images).
- `requirements.txt`: List of Python dependencies.
- `instance/`: Directory containing the SQLite database file (`database.db`).

## Future Enhancements

- Cryptographic document signing and verification.
- Document upload and secure storage.
- Admin dashboard for managing verification requests.
