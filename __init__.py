from app import afg_db
from werkzeug.security import generate_password_hash, check_password_hash

class User(afg_db.Model):
    __tablename__ = 'users'

    id = afg_db.Column(afg_db.Integer, primary_key=True)
    name = afg_db.Column(afg_db.String(255))
    email = afg_db.Column(afg_db.String(255), unique=True, nullable=False)
    password = afg_db.Column(afg_db.String(255), nullable=False)
    user_type = afg_db.Column(afg_db.String(50), nullable=False)
    created_at = afg_db.Column(afg_db.DateTime)

    def set_password(self, raw_password):
        self.password = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        return check_password_hash(self.password, raw_password)

    def __repr__(self):
        return f"<User {self.email}>"


class Rubric(afg_db.Model):
    __tablename__ = 'rubrics'

    id = afg_db.Column(afg_db.Integer, primary_key=True)
    title = afg_db.Column(afg_db.String(255), nullable=False)
    description = afg_db.Column(afg_db.Text)
    created_by = afg_db.Column(afg_db.Integer, afg_db.ForeignKey('users.id', ondelete='SET NULL'))
    created_at = afg_db.Column(afg_db.DateTime)


class Criterion(afg_db.Model):
    __tablename__ = 'criteria'

    id = afg_db.Column(afg_db.Integer, primary_key=True)
    rubric_id = afg_db.Column(afg_db.Integer, afg_db.ForeignKey('rubrics.id', ondelete='CASCADE'))
    name = afg_db.Column(afg_db.String(255), nullable=False)
    description = afg_db.Column(afg_db.Text)
    max_score = afg_db.Column(afg_db.Integer)


class MentorInput(afg_db.Model):
    __tablename__ = 'mentor_inputs'

    id = afg_db.Column(afg_db.Integer, primary_key=True)
    student_id = afg_db.Column(afg_db.Integer, afg_db.ForeignKey('users.id', ondelete='CASCADE'))
    rubric_id = afg_db.Column(afg_db.Integer, afg_db.ForeignKey('rubrics.id', ondelete='CASCADE'))
    evaluator_id = afg_db.Column(afg_db.Integer, afg_db.ForeignKey('users.id', ondelete='SET NULL'))
    submitted_at = afg_db.Column(afg_db.DateTime)


class PerformanceData(afg_db.Model):
    __tablename__ = 'performance_data'

    id = afg_db.Column(afg_db.Integer, primary_key=True)
    mentor_input_id = afg_db.Column(afg_db.Integer, afg_db.ForeignKey('mentor_inputs.id', ondelete='CASCADE'))
    criterion_id = afg_db.Column(afg_db.Integer, afg_db.ForeignKey('criteria.id', ondelete='CASCADE'))
    score = afg_db.Column(afg_db.Integer)
    remarks = afg_db.Column(afg_db.Text)


class Feedback(afg_db.Model):
    __tablename__ = 'feedbacks'

    id = afg_db.Column(afg_db.Integer, primary_key=True)
    mentor_input_id = afg_db.Column(afg_db.Integer, afg_db.ForeignKey('mentor_inputs.id', ondelete='CASCADE'))
    feedback_text = afg_db.Column(afg_db.Text)
    generated_at = afg_db.Column(afg_db.DateTime)
