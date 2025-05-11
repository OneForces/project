from datetime import datetime
from core import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    position = db.Column(db.String(100), nullable=False)

    sent_assignments = db.relationship('Assignment', foreign_keys='Assignment.sender_id', backref='sender', lazy=True)
    received_assignments = db.relationship('Assignment', foreign_keys='Assignment.receiver_id', backref='receiver', lazy=True)
    documents = db.relationship('Document', backref='uploader', foreign_keys='Document.uploaded_by', lazy=True)
    actions = db.relationship('ActionLog', backref='user', lazy=True)

    @classmethod
    def get_by_role(cls, role):
        return cls.query.filter_by(role=role).all()

    def __repr__(self):
        return f"<User {self.full_name} ({self.role})>"

class Stage(db.Model):
    __tablename__ = 'stages'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    deadline = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='Не начат')

    assignments = db.relationship('Assignment', backref='stage', lazy=True)
    documents = db.relationship('Document', backref='stage', lazy=True)

    def __repr__(self):
        return f"<Stage {self.name} - {self.status}>"

class Assignment(db.Model):
    __tablename__ = 'assignments'

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    stage_id = db.Column(db.Integer, db.ForeignKey('stages.id'), nullable=False)
    file_path = db.Column(db.String(255))
    response_file = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default='отправлено')

    def __repr__(self):
        return f"<Assignment to {self.receiver_id} file={self.file_path}>"

class ActionLog(db.Model):
    __tablename__ = 'action_logs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    action_type = db.Column(db.String(50))
    description = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<ActionLog {self.user_id}: {self.action_type}>"

class Document(db.Model):
    __tablename__ = 'documents'

    id = db.Column(db.Integer, primary_key=True)
    stage_id = db.Column(db.Integer, db.ForeignKey('stages.id'), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    uploaded_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Document {self.file_path}>"

class RegistrationCode(db.Model):
    __tablename__ = 'registration_codes'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f"<RegistrationCode {self.code}>"
