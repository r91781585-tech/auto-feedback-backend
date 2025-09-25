"""
API routes for the Auto Feedback Generator
"""
from flask import Blueprint, request, jsonify
from app.nlp import FeedbackGenerator
from app.models import Feedback, Student, db
from app.utils.validators import validate_feedback_request
import logging

logger = logging.getLogger(__name__)

bp = Blueprint('api', __name__)

# Initialize feedback generator
feedback_generator = FeedbackGenerator()

@bp.route('/generate-feedback', methods=['POST'])
def generate_feedback():
    """Generate feedback for a student based on performance scores"""
    try:
        # Validate request data
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        # Validate required fields
        validation_result = validate_feedback_request(data)
        if not validation_result['valid']:
            return jsonify({'error': validation_result['message']}), 400
        
        # Extract data
        student_name = data['student_name']
        scores = {
            'communication': data['communication'],
            'teamwork': data['teamwork'],
            'creativity': data['creativity'],
            'critical_thinking': data['critical_thinking'],
            'presentation': data['presentation']
        }
        
        feedback_type = data.get('feedback_type', 'comprehensive')
        
        # Generate feedback
        feedback_text = feedback_generator.generate_feedback(
            student_name=student_name,
            scores=scores,
            feedback_type=feedback_type
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
        
        # Return response
        response = {
            'success': True,
            'feedback': feedback_text,
            'student_name': student_name,
            'scores': scores,
            'feedback_id': feedback_record.id
        }
        
        logger.info(f"Generated feedback for {student_name} (ID: {feedback_record.id})")
        return jsonify(response), 200
        
    except Exception as e:
        logger.error(f"Error in generate_feedback: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Internal server error occurred while generating feedback'
        }), 500

@bp.route('/batch-feedback', methods=['POST'])
def batch_generate_feedback():
    """Generate feedback for multiple students"""
    try:
        data = request.get_json()
        if not data or 'students' not in data:
            return jsonify({'error': 'No students data provided'}), 400
        
        students_data = data['students']
        if not isinstance(students_data, list):
            return jsonify({'error': 'Students data must be a list'}), 400
        
        # Process batch
        results = feedback_generator.batch_generate_feedback(students_data)
        
        # Save successful results to database
        saved_count = 0
        for result in results:
            if result['status'] == 'success':
                try:
                    student_data = next(s for s in students_data if s['student_name'] == result['student_name'])
                    scores = student_data['scores']
                    
                    feedback_record = Feedback(
                        student_name=result['student_name'],
                        communication=scores['communication'],
                        teamwork=scores['teamwork'],
                        creativity=scores['creativity'],
                        critical_thinking=scores['critical_thinking'],
                        presentation=scores['presentation'],
                        feedback_text=result['feedback']
                    )
                    
                    db.session.add(feedback_record)
                    saved_count += 1
                    
                except Exception as e:
                    logger.error(f"Error saving feedback for {result['student_name']}: {str(e)}")
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'results': results,
            'total_processed': len(results),
            'saved_to_database': saved_count
        }), 200
        
    except Exception as e:
        logger.error(f"Error in batch_generate_feedback: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Internal server error occurred during batch processing'
        }), 500

@bp.route('/feedback/<int:feedback_id>', methods=['GET'])
def get_feedback(feedback_id):
    """Retrieve a specific feedback record"""
    try:
        feedback = Feedback.query.get_or_404(feedback_id)
        return jsonify({
            'success': True,
            'feedback': feedback.to_dict()
        }), 200
        
    except Exception as e:
        logger.error(f"Error retrieving feedback {feedback_id}: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Feedback not found'
        }), 404

@bp.route('/feedback', methods=['GET'])
def list_feedback():
    """List all feedback records with pagination"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        student_name = request.args.get('student_name')
        
        query = Feedback.query
        
        if student_name:
            query = query.filter(Feedback.student_name.ilike(f'%{student_name}%'))
        
        feedbacks = query.order_by(Feedback.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'success': True,
            'feedbacks': [f.to_dict() for f in feedbacks.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': feedbacks.total,
                'pages': feedbacks.pages,
                'has_next': feedbacks.has_next,
                'has_prev': feedbacks.has_prev
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error listing feedback: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error retrieving feedback list'
        }), 500

@bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Auto Feedback Generator API',
        'version': '1.0.0'
    }), 200