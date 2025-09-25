"""
Validation utilities for the Auto Feedback Generator
"""
from typing import Dict, Any

def validate_feedback_request(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate feedback generation request data
    
    Args:
        data: Request data dictionary
        
    Returns:
        Dictionary with 'valid' boolean and 'message' string
    """
    required_fields = ['student_name', 'communication', 'teamwork', 'creativity', 'critical_thinking', 'presentation']
    
    # Check for required fields
    for field in required_fields:
        if field not in data:
            return {
                'valid': False,
                'message': f'Missing required field: {field}'
            }
    
    # Validate student name
    if not isinstance(data['student_name'], str) or not data['student_name'].strip():
        return {
            'valid': False,
            'message': 'Student name must be a non-empty string'
        }
    
    # Validate scores
    score_fields = ['communication', 'teamwork', 'creativity', 'critical_thinking', 'presentation']
    for field in score_fields:
        score = data[field]
        
        if not isinstance(score, int):
            return {
                'valid': False,
                'message': f'{field} score must be an integer'
            }
        
        if score < 1 or score > 10:
            return {
                'valid': False,
                'message': f'{field} score must be between 1 and 10'
            }
    
    # Validate optional feedback_type
    if 'feedback_type' in data:
        valid_types = ['comprehensive', 'brief']
        if data['feedback_type'] not in valid_types:
            return {
                'valid': False,
                'message': f'feedback_type must be one of: {", ".join(valid_types)}'
            }
    
    return {
        'valid': True,
        'message': 'Valid request'
    }

def validate_batch_request(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate batch feedback generation request
    
    Args:
        data: Request data dictionary
        
    Returns:
        Dictionary with 'valid' boolean and 'message' string
    """
    if 'students' not in data:
        return {
            'valid': False,
            'message': 'Missing required field: students'
        }
    
    students = data['students']
    if not isinstance(students, list):
        return {
            'valid': False,
            'message': 'students field must be a list'
        }
    
    if len(students) == 0:
        return {
            'valid': False,
            'message': 'students list cannot be empty'
        }
    
    if len(students) > 50:  # Reasonable batch limit
        return {
            'valid': False,
            'message': 'Maximum 50 students allowed per batch request'
        }
    
    # Validate each student entry
    for i, student in enumerate(students):
        if not isinstance(student, dict):
            return {
                'valid': False,
                'message': f'Student entry {i+1} must be a dictionary'
            }
        
        # Check required structure
        if 'student_name' not in student or 'scores' not in student:
            return {
                'valid': False,
                'message': f'Student entry {i+1} missing required fields: student_name, scores'
            }
        
        # Validate individual student data
        student_data = {
            'student_name': student['student_name'],
            **student['scores']
        }
        
        validation = validate_feedback_request(student_data)
        if not validation['valid']:
            return {
                'valid': False,
                'message': f'Student entry {i+1}: {validation["message"]}'
            }
    
    return {
        'valid': True,
        'message': 'Valid batch request'
    }

def sanitize_student_name(name: str) -> str:
    """
    Sanitize student name for safe processing
    
    Args:
        name: Raw student name
        
    Returns:
        Sanitized student name
    """
    if not isinstance(name, str):
        return "Unknown Student"
    
    # Remove extra whitespace and limit length
    sanitized = name.strip()[:100]
    
    # Ensure it's not empty after sanitization
    if not sanitized:
        return "Unknown Student"
    
    return sanitized