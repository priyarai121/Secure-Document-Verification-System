import os
import hashlib
from flask import Flask, render_template, redirect, url_for, flash, request, jsonify, send_from_directory
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from models import db
from models.user import User
from models.document import Document
from utils.encryption import encrypt_hash
from utils.encoding import encode_base64
from utils.verification import verify_document_hash
from datetime import datetime

app = Flask(__name__)
# Secret key for session management (in a real app, load this from .env)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default-dev-secret-key-123')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # 16MB
ALLOWED_EXTENSIONS = {'pdf', 'txt', 'docx', 'png', 'jpg', 'jpeg'}

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Initialize DB
db.init_app(app)

# Setup Login Manager
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create database tables before first request
with app.app_context():
    db.create_all()

# --- ROUTES ---

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validation
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return redirect(url_for('register'))
            
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already registered.', 'error')
            return redirect(url_for('register'))
            
        user_name = User.query.filter_by(username=username).first()
        if user_name:
            flash('Username already exists.', 'error')
            return redirect(url_for('register'))
            
        # Create new user
        new_user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password, method='pbkdf2:sha256')
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
        
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash('Logged in successfully.', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password.', 'error')
            
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    documents = Document.query.filter_by(user_id=current_user.id).order_by(Document.upload_date.desc()).all()
    total_docs = len(documents)
    verified_docs = sum(1 for d in documents if d.verification_status == 'Verified')
    tampered_docs = sum(1 for d in documents if d.verification_status == 'Tampered')
    
    # Calculate upload trends (last 7 days)
    trends = {}
    for doc in documents:
        date_str = doc.upload_date.strftime('%Y-%m-%d')
        trends[date_str] = trends.get(date_str, 0) + 1
        
    # Sort trends by date
    sorted_trends = dict(sorted(trends.items())[-7:]) # Get up to 7 most recent days
    trend_labels = list(sorted_trends.keys())
    trend_data = list(sorted_trends.values())
    
    return render_template('dashboard.html', 
                           documents=documents, 
                           total_docs=total_docs,
                           verified_docs=verified_docs,
                           tampered_docs=tampered_docs,
                           trend_labels=trend_labels,
                           trend_data=trend_data)

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
            
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            
            # Calculate SHA-256 hash
            sha256_hash = hashlib.sha256()
            # Read in chunks to avoid memory issues with large files
            for chunk in iter(lambda: file.read(4096), b""):
                sha256_hash.update(chunk)
            
            file_hash = sha256_hash.hexdigest()
            file.seek(0) # Reset file pointer to beginning after reading for hash
            
            # Encrypt the hash and encode to base64
            encrypted_bytes = encrypt_hash(file_hash)
            base64_encoded_data = encode_base64(encrypted_bytes)
            
            # Check for duplicates for this user
            existing_doc = Document.query.filter_by(user_id=current_user.id, file_hash=file_hash).first()
            if existing_doc:
                return jsonify({'error': 'File already uploaded.'}), 400
            
            # Save file
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            # Handle naming collision if a different file has the same name
            base, ext = os.path.splitext(filename)
            counter = 1
            while os.path.exists(file_path):
                filename = f"{base}_{counter}{ext}"
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                counter += 1
                
            file.save(file_path)
            
            # Create DB record
            new_doc = Document(
                user_id=current_user.id,
                filename=filename,
                file_hash=file_hash,
                encrypted_hash=encrypted_bytes.hex(),
                base64_data=base64_encoded_data,
                verification_status='Pending'
            )
            db.session.add(new_doc)
            db.session.commit()
            
            return jsonify({'success': 'File uploaded successfully', 'redirect': url_for('dashboard')}), 200
            
        return jsonify({'error': 'File type not allowed'}), 400
        
    return render_template('upload.html')

@app.route('/download/<int:doc_id>')
@login_required
def download_file(doc_id):
    doc = Document.query.get_or_404(doc_id)
    if doc.user_id != current_user.id:
        flash('Unauthorized access', 'error')
        return redirect(url_for('dashboard'))
    return send_from_directory(app.config['UPLOAD_FOLDER'], doc.filename)

@app.route('/document/<int:doc_id>')
@login_required
def document_detail(doc_id):
    doc = Document.query.get_or_404(doc_id)
    if doc.user_id != current_user.id:
        flash('Unauthorized access', 'error')
        return redirect(url_for('dashboard'))
    return render_template('document_detail.html', doc=doc)

@app.route('/verify', methods=['GET', 'POST'])
@login_required
def verify():
    # Get all documents uploaded by the user to populate the dropdown
    user_documents = Document.query.filter_by(user_id=current_user.id).order_by(Document.upload_date.desc()).all()
    
    if request.method == 'POST':
        doc_id = request.form.get('document_id')
        if not doc_id:
            return jsonify({'error': 'Please select a document.'}), 400
            
        doc = Document.query.get(doc_id)
        if not doc or doc.user_id != current_user.id:
            return jsonify({'error': 'Invalid document selected.'}), 400
            
        if 'file' not in request.files:
            return jsonify({'error': 'No file part.'}), 400
            
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file.'}), 400
            
        if file:
            is_verified = verify_document_hash(file, doc.file_hash)
            doc.verification_status = 'Verified' if is_verified else 'Tampered'
            doc.verification_date = datetime.utcnow()
            db.session.commit()
            
            return jsonify({
                'success': True,
                'status': doc.verification_status,
                'message': 'Document Verified Successfully' if is_verified else 'Document Tampered / Modified'
            }), 200
            
    return render_template('verify.html', documents=user_documents)

@app.route('/history')
@login_required
def history():
    status_filter = request.args.get('status')
    search_query = request.args.get('search')
    
    query = Document.query.filter(
        Document.user_id == current_user.id,
        Document.verification_status.in_(['Verified', 'Tampered'])
    )
    
    if status_filter and status_filter in ['Verified', 'Tampered']:
        query = query.filter(Document.verification_status == status_filter)
        
    if search_query:
        query = query.filter(Document.filename.ilike(f'%{search_query}%'))
        
    verified_docs = query.order_by(Document.verification_date.desc()).all()
    
    return render_template('history.html', documents=verified_docs)

if __name__ == '__main__':
    app.run(debug=True)
