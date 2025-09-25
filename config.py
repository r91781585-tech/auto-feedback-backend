#Store configuration variables (API keys, debug mode):
import os

# Load the API key from environment variables for security
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev')
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY') or 'a-very-secret-key'
