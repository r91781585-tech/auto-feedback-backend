"""
Web interface routes for the Auto Feedback Generator
"""
from flask import Blueprint, render_template, request, flash, redirect, url_for
from app.nlp import FeedbackGenerator
from app.models import Feedback, db
import logging

logger = logging.getLogger(__name__)

bp = Blueprint('main', __name__)

# Initialize feedback generator
feedback_generator = FeedbackGenerator()

@bp.route('/')
def index():
    """Main page with feedback form"""
    return render_template('index.html')

@bp.route('/generate', methods=['POST'])
def generate_feedback_web():
    """Generate feedback via web form"""
    try:
        # Get form data
        student_name = request.form.get('student_name', '').strip()
        
        # Get scores
        scores = {}
        score_fields = ['communication', 'teamwork', 'creativity', 'critical_thinking', 'presentation']
        
        for field in score_fields:
            try:
                scores[field] = int(request.form.get(field, 0))
            except (ValueError, TypeError):
                flash(f'Invalid score for {field.replace("_", " ").title()}', 'error')
                return redirect(url_for('main.index'))
        
        # Validate
        if not student_name:
            flash('Student name is required', 'error')
            return redirect(url_for('main.index'))
        
        for field, score in scores.items():
            if score < 1 or score > 10:
                flash(f'{field.replace("_", " ").title()} score must be between 1 and 10', 'error')
                return redirect(url_for('main.index'))
        
        # Generate feedback
        feedback_text = feedback_generator.generate_feedback(
            student_name=student_name,
            scores=scores,
            feedback_type='comprehensive'
        )
        
        # Save to database
        feedback_record = Feedback(
            student_name=student_name,
            communication=scores['communication'],
            teamwork=scores['teamwork'],
            creativity=scores['creativity'],
            critical_thinking=scores['critical_thinking'],
            presentation=scores['presentation'],
            feedback_text=feedback_text
        )
        
        db.session.add(feedback_record)
        db.session.commit()
        
        flash('Feedback generated successfully!', 'success')
        return render_template('result.html', 
                             feedback=feedback_text, 
                             student_name=student_name,
                             scores=scores)
        
    except Exception as e:
        logger.error(f"Error generating feedback via web: {str(e)}")
        flash('An error occurred while generating feedback. Please try again.', 'error')
        return redirect(url_for('main.index'))

@bp.route('/history')
def feedback_history():
    """View feedback history"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = 10
        
        feedbacks = Feedback.query.order_by(Feedback.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return render_template('history.html', feedbacks=feedbacks)
        
    except Exception as e:
        logger.error(f"Error loading feedback history: {str(e)}")
        flash('Error loading feedback history', 'error')
        return redirect(url_for('main.index'))

@bp.route('/feedback/<int:feedback_id>')
def view_feedback(feedback_id):
    """View individual feedback"""
    try:
        feedback = Feedback.query.get_or_404(feedback_id)
        return render_template('feedback_detail.html', feedback=feedback)
        
    except Exception as e:
        logger.error(f"Error loading feedback {feedback_id}: {str(e)}")
        flash('Feedback not found', 'error')
        return redirect(url_for('main.feedback_history'))