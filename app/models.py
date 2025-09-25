"""
Database models for the Auto Feedback Generator
"""
from datetime import datetime
from app import db

class Student(db.Model):
    """Student model"""
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship with feedback
    feedbacks = db.relationship('Feedback', backref='student', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'created_at': self.created_at.isoformat()
        }

class Rubric(db.Model):
    """Rubric model for evaluation criteria"""
    __tablename__ = 'rubrics'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    criteria = db.Column(db.JSON, nullable=False)  # Store criteria as JSON
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'criteria': self.criteria,
            'created_at': self.created_at.isoformat()
        }

class Feedback(db.Model):
    """Feedback model"""
    __tablename__ = 'feedbacks'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=True)
    student_name = db.Column(db.String(100), nullable=False)  # For cases without student record
    
    # Performance scores
    communication = db.Column(db.Integer, nullable=False)
    teamwork = db.Column(db.Integer, nullable=False)
    creativity = db.Column(db.Integer, nullable=False)
    critical_thinking = db.Column(db.Integer, nullable=False)
    presentation = db.Column(db.Integer, nullable=False)
    
    # Generated feedback
    feedback_text = db.Column(db.Text, nullable=False)
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    model_used = db.Column(db.String(50), default='gpt-3.5-turbo')
    
    def to_dict(self):
        return {
            'id': self.id,
            'student_name': self.student_name,
            'scores': {
                'communication': self.communication,
                'teamwork': self.teamwork,
                'creativity': self.creativity,
                'critical_thinking': self.critical_thinking,
                'presentation': self.presentation
            },
            'feedback_text': self.feedback_text,
            'created_at': self.created_at.isoformat(),
            'model_used': self.model_used
        }