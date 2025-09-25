"""
Advanced NLP Feedback Generator using OpenAI GPT models
"""
import openai
import logging
from typing import Dict, List, Optional
from app.config import Config
from .prompt_templates import PromptTemplates

logger = logging.getLogger(__name__)

class FeedbackGenerator:
    """Advanced feedback generation using NLP techniques"""
    
    def __init__(self, api_key: str = None):
        """Initialize the feedback generator"""
        self.api_key = api_key or Config.OPENAI_API_KEY
        if not self.api_key:
            raise ValueError("OpenAI API key is required")
        
        openai.api_key = self.api_key
        self.prompt_templates = PromptTemplates()
    
    def generate_feedback(self, 
                         student_name: str,
                         scores: Dict[str, int],
                         feedback_type: str = "comprehensive") -> str:
        """
        Generate personalized feedback based on student scores
        
        Args:
            student_name: Name of the student
            scores: Dictionary of skill scores (1-10)
            feedback_type: Type of feedback to generate
            
        Returns:
            Generated feedback text
        """
        try:
            # Validate scores
            self._validate_scores(scores)
            
            # Analyze performance patterns
            performance_analysis = self._analyze_performance(scores)
            
            # Generate appropriate prompt
            prompt = self._create_prompt(student_name, scores, performance_analysis, feedback_type)
            
            # Generate feedback using OpenAI
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": self.prompt_templates.get_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=300,
                presence_penalty=0.1,
                frequency_penalty=0.1
            )
            
            feedback = response.choices[0].message.content.strip()
            
            # Post-process feedback
            feedback = self._post_process_feedback(feedback, student_name)
            
            logger.info(f"Generated feedback for {student_name}")
            return feedback
            
        except Exception as e:
            logger.error(f"Error generating feedback: {str(e)}")
            return self._generate_fallback_feedback(student_name, scores)
    
    def _validate_scores(self, scores: Dict[str, int]) -> None:
        """Validate input scores"""
        required_skills = ['communication', 'teamwork', 'creativity', 'critical_thinking', 'presentation']
        
        for skill in required_skills:
            if skill not in scores:
                raise ValueError(f"Missing score for {skill}")
            
            score = scores[skill]
            if not isinstance(score, int) or score < 1 or score > 10:
                raise ValueError(f"Invalid score for {skill}: {score}. Must be integer 1-10")
    
    def _analyze_performance(self, scores: Dict[str, int]) -> Dict[str, List[str]]:
        """Analyze performance patterns to categorize strengths and areas for improvement"""
        strengths = []
        good_areas = []
        improvement_areas = []
        
        for skill, score in scores.items():
            skill_display = skill.replace('_', ' ').title()
            
            if score >= 8:
                strengths.append(skill_display)
            elif score >= 6:
                good_areas.append(skill_display)
            else:
                improvement_areas.append(skill_display)
        
        return {
            'strengths': strengths,
            'good_areas': good_areas,
            'improvement_areas': improvement_areas,
            'average_score': sum(scores.values()) / len(scores)
        }
    
    def _create_prompt(self, 
                      student_name: str, 
                      scores: Dict[str, int],
                      analysis: Dict[str, List[str]],
                      feedback_type: str) -> str:
        """Create a structured prompt for feedback generation"""
        
        if feedback_type == "comprehensive":
            return self.prompt_templates.get_comprehensive_prompt(student_name, scores, analysis)
        elif feedback_type == "brief":
            return self.prompt_templates.get_brief_prompt(student_name, scores, analysis)
        else:
            return self.prompt_templates.get_comprehensive_prompt(student_name, scores, analysis)
    
    def _post_process_feedback(self, feedback: str, student_name: str) -> str:
        """Post-process the generated feedback"""
        # Ensure student name is properly used
        if student_name not in feedback:
            feedback = f"{student_name}, {feedback.lower()}"
        
        # Clean up formatting
        feedback = feedback.strip()
        if not feedback.endswith('.'):
            feedback += '.'
        
        return feedback
    
    def _generate_fallback_feedback(self, student_name: str, scores: Dict[str, int]) -> str:
        """Generate basic feedback if AI generation fails"""
        avg_score = sum(scores.values()) / len(scores)
        
        if avg_score >= 8:
            return f"{student_name} demonstrates excellent performance across all areas with an average score of {avg_score:.1f}/10. Continue maintaining this high standard of work."
        elif avg_score >= 6:
            return f"{student_name} shows good performance with an average score of {avg_score:.1f}/10. Focus on strengthening weaker areas to achieve excellence."
        else:
            return f"{student_name} has room for improvement with an average score of {avg_score:.1f}/10. Consider additional practice and support in key skill areas."
    
    def batch_generate_feedback(self, student_data: List[Dict]) -> List[Dict]:
        """Generate feedback for multiple students"""
        results = []
        
        for data in student_data:
            try:
                feedback = self.generate_feedback(
                    data['student_name'],
                    data['scores'],
                    data.get('feedback_type', 'comprehensive')
                )
                
                results.append({
                    'student_name': data['student_name'],
                    'feedback': feedback,
                    'status': 'success'
                })
                
            except Exception as e:
                results.append({
                    'student_name': data.get('student_name', 'Unknown'),
                    'feedback': None,
                    'status': 'error',
                    'error': str(e)
                })
        
        return results