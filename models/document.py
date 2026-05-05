from . import db
from datetime import datetime

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    file_hash = db.Column(db.String(64), nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    verification_status = db.Column(db.String(50), default='Pending')

    def __repr__(self):
        return f'<Document {self.filename}>'
