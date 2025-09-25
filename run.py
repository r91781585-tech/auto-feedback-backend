"""
Main application runner for Auto Feedback Generator
"""
import os
from app import create_app, db
from app.config import config

def create_tables():
    """Create database tables"""
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")

if __name__ == '__main__':
    # Get configuration from environment
    config_name = os.environ.get('FLASK_CONFIG', 'development')
    
    # Create app
    app = create_app(config[config_name])
    
    # Create tables if they don't exist
    create_tables()
    
    # Run the application
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5000)),
        debug=app.config['DEBUG']
    )