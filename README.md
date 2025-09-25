# 🎓 Auto Feedback Generator - NLP Backend

An advanced NLP-powered system for generating personalized student feedback based on performance scores across multiple criteria.

## 🚀 Features

- **Advanced NLP Processing**: Sophisticated prompt engineering and feedback generation
- **RESTful API**: Complete API endpoints for integration
- **Web Interface**: User-friendly web interface for manual feedback generation
- **Database Integration**: SQLAlchemy with PostgreSQL/SQLite support
- **Batch Processing**: Generate feedback for multiple students simultaneously
- **Structured Architecture**: Clean, modular codebase following best practices
- **Comprehensive Validation**: Input validation and error handling
- **Performance Analytics**: Track and analyze feedback patterns

## 📁 Project Structure

```
auto-feedback-backend/
├── app/
│   ├── __init__.py              # Application factory
│   ├── config.py                # Configuration management
│   ├── models.py                # Database models
│   ├── api.py                   # API routes
│   ├── routes.py                # Web interface routes
│   ├── nlp/                     # NLP processing module
│   │   ├── __init__.py
│   │   ├── feedback_generator.py # Core NLP logic
│   │   └── prompt_templates.py   # Structured prompts
│   ├── utils/                   # Utility functions
│   │   ├── __init__.py
│   │   └── validators.py        # Input validation
│   └── templates/               # HTML templates
│       ├── base.html
│       ├── index.html
│       └── result.html
├── data/                        # Data files
│   ├── rubrics.csv
│   └── student_performance_list.csv
├── run.py                       # Application runner
├── requirements.txt             # Dependencies
├── .env.example                 # Environment variables template
└── README.md                    # This file
```

## 🛠️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/r91781585-tech/auto-feedback-backend.git
cd auto-feedback-backend
git checkout restructure-nlp-backend
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Create a `.env` file in the root directory:
```env
# Required
OPENAI_API_KEY=your_openai_api_key_here

# Optional
FLASK_CONFIG=development
SECRET_KEY=your_secret_key_here
DATABASE_URL=sqlite:///feedback.db
FLASK_DEBUG=true
```

### 5. Initialize Database
```bash
python run.py
```

## 🔧 Usage

### Web Interface
1. Start the application: `python run.py`
2. Open browser to `http://localhost:5000`
3. Fill in student details and scores
4. Generate personalized feedback

### API Endpoints

#### Generate Single Feedback
```bash
POST /api/generate-feedback
Content-Type: application/json

{
  "student_name": "John Doe",
  "communication": 8,
  "teamwork": 7,
  "creativity": 9,
  "critical_thinking": 6,
  "presentation": 8,
  "feedback_type": "comprehensive"  // optional: "comprehensive" or "brief"
}
```

#### Batch Generate Feedback
```bash
POST /api/batch-feedback
Content-Type: application/json

{
  "students": [
    {
      "student_name": "Alice Smith",
      "scores": {
        "communication": 9,
        "teamwork": 8,
        "creativity": 7,
        "critical_thinking": 8,
        "presentation": 9
      }
    },
    {
      "student_name": "Bob Johnson",
      "scores": {
        "communication": 6,
        "teamwork": 7,
        "creativity": 8,
        "critical_thinking": 6,
        "presentation": 7
      }
    }
  ]
}
```

#### Get Feedback History
```bash
GET /api/feedback?page=1&per_page=10&student_name=John
```

#### Health Check
```bash
GET /api/health
```

## 🧠 NLP Features

### Advanced Prompt Engineering
- **Structured Templates**: Multiple prompt templates for different feedback types
- **Performance Analysis**: Automatic categorization of strengths and improvement areas
- **Contextual Generation**: Personalized feedback based on score patterns
- **Fallback Mechanisms**: Graceful handling of API failures

### Feedback Types
- **Comprehensive**: Detailed analysis with specific recommendations
- **Brief**: Concise feedback highlighting key points
- **Rubric-based**: Feedback aligned with specific evaluation criteria

### Quality Assurance
- **Input Validation**: Comprehensive validation of all inputs
- **Error Handling**: Robust error handling with meaningful messages
- **Post-processing**: Automatic formatting and quality checks
- **Logging**: Detailed logging for monitoring and debugging

## 📊 Database Schema

### Students Table
- `id`: Primary key
- `name`: Student name
- `email`: Student email (optional)
- `created_at`: Timestamp

### Feedback Table
- `id`: Primary key
- `student_name`: Student name
- `communication`: Score (1-10)
- `teamwork`: Score (1-10)
- `creativity`: Score (1-10)
- `critical_thinking`: Score (1-10)
- `presentation`: Score (1-10)
- `feedback_text`: Generated feedback
- `created_at`: Timestamp
- `model_used`: AI model used

## 🔒 Security Features

- **Environment Variables**: Secure API key management
- **Input Sanitization**: Protection against malicious inputs
- **Rate Limiting**: Built-in protection against abuse
- **Error Masking**: Secure error messages in production

## 🚀 Deployment

### Local Development
```bash
export FLASK_CONFIG=development
python run.py
```

### Production
```bash
export FLASK_CONFIG=production
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

### Docker (Optional)
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "run:app"]
```

## 🧪 Testing

### Manual Testing
Use the provided curl examples or the web interface to test functionality.

### API Testing
```bash
# Test health endpoint
curl http://localhost:5000/api/health

# Test feedback generation
curl -X POST http://localhost:5000/api/generate-feedback \
  -H "Content-Type: application/json" \
  -d '{
    "student_name": "Test Student",
    "communication": 8,
    "teamwork": 7,
    "creativity": 9,
    "critical_thinking": 6,
    "presentation": 8
  }'
```

## 📈 Performance Optimization

- **Batch Processing**: Efficient handling of multiple requests
- **Database Indexing**: Optimized database queries
- **Caching**: Response caching for improved performance
- **Connection Pooling**: Efficient database connections

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 🆘 Support

For issues and questions:
1. Check the documentation
2. Review existing issues
3. Create a new issue with detailed information

## 🔄 Migration from Old Structure

The new structure provides:
- ✅ Secure API key management
- ✅ Modular architecture
- ✅ Advanced NLP processing
- ✅ Comprehensive error handling
- ✅ Database integration
- ✅ Web interface
- ✅ API documentation
- ✅ Production-ready configuration