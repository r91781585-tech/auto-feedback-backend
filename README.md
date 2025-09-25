# Auto Feedback Backend

## How to run
1. Install dependencies: `pip install -r requirements.txt`
2. Create `.env` with your OpenAI API key.
3. Run: `python app.py`

## Test it
Use curl:
curl -X POST http://127.0.0.1:5000/generate-feedback \     -H "Content-Type: application/json" \     -d '{"student_name": "Priya Sharma", "communication": 8, "teamwork": 7, "creativity": 9, "critical_thinking": 6, "presentation": 8}'
