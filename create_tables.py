from app import create_app, afg_db
from app.models import User, Rubric, Criterion, MentorInput, PerformanceData, Feedback

app = create_app()

with app.app_context():
    afg_db.create_all()
    print("Tables created successfully!")








