import os
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from app.models import Rubric
from app import afg_db

file_bp = Blueprint('file_bp', __name__)

RUBRIC_FOLDER = os.path.join(os.getcwd(), 'uploads', 'rubric_files')
os.makedirs(RUBRIC_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {'csv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@file_bp.route('/upload-rubric', methods=['POST'])
def upload_rubric():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No file selected'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(RUBRIC_FOLDER, filename)
        file.save(filepath)

        # Save file info to database
        new_rubric = Rubric(
            title=filename,
            description='Uploaded rubric file'
        )
        afg_db.session.add(new_rubric)
        afg_db.session.commit()

        return jsonify({
            'message': 'Rubric file uploaded and saved to DB',
            'rubric_id': new_rubric.id,
            'filename': filename
        }), 200
    else:
        return jsonify({'message': 'File type not allowed'}), 400

@file_bp.route('/rubric-files', methods=['GET'])
def list_rubric_files():
    rubrics = Rubric.query.all()
    return jsonify({
        'rubrics': [
            {
                'id': rubric.id,
                'title': rubric.title,
                'description': rubric.description
            }
            for rubric in rubrics
        ]
    })
