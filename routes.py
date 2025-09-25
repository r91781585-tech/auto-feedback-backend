from flask import Blueprint, render_template, request, jsonify
from ..ai import generate_feedback
from app.models import Feedback
from app import afg_db

bp = Blueprint('main', __name__)

@bp.route('/', methods=['GET', 'POST'])
def index():
    feedback = None
    if request.method == 'POST':
        rubric = request.form['rubric']
        performance = request.form['performance']
        feedback_text = generate_feedback(rubric, performance)

        # Save feedback to the database
        new_feedback = Feedback(
            rubric_text=rubric,
            performance_text=performance,
            generated_feedback=feedback_text
        )
        afg_db.session.add(new_feedback)
        afg_db.session.commit()

        feedback = feedback_text

    return render_template('index.html', feedback=feedback)
