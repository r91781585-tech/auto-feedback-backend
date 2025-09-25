#Encapsulates  AI logic (OpenAI API interaction, NLP processing)
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_feedback(rubric, performance):
    prompt = f"Generate feedback based on this rubric: {rubric} and student performance: {performance}"
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=150,
        temperature=0.7
    )
    return response.choices[0].text.strip()
