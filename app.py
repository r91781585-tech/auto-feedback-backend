import os
import openai
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
openai.api_key = "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"

app = Flask(__name__)

@app.route('/generate-feedback', methods=['POST'])
def generate_feedback():
    data = request.json

    student_name = data.get("student_name")
    communication = data.get("communication")
    teamwork = data.get("teamwork")
    creativity = data.get("creativity")
    critical_thinking = data.get("critical_thinking")
    presentation = data.get("presentation")

    prompt = f"""
    Write constructive, personalized performance feedback for a student named {student_name}, based on these scores:
    - Communication: {communication}/10
    - Teamwork: {teamwork}/10
    - Creativity: {creativity}/10
    - Critical Thinking: {critical_thinking}/10
    - Presentation: {presentation}/10
    Focus on strengths, one area of improvement, and how the student can improve further.
    """

    try:
        response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ],
    temperature=0.7,
    max_tokens=250
        )
        feedback = response['choices'][0]['message']['content'].strip()
        return jsonify({"feedback": feedback})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
