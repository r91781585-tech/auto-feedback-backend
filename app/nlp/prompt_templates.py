"""
Prompt templates for feedback generation
"""
from typing import Dict, List

class PromptTemplates:
    """Collection of prompt templates for different feedback types"""
    
    def get_system_prompt(self) -> str:
        """System prompt to set the AI's role and behavior"""
        return """You are an experienced educational assessor and mentor who provides constructive, 
        personalized feedback to students. Your feedback should be:
        
        1. Encouraging and positive in tone
        2. Specific and actionable
        3. Balanced (highlighting both strengths and areas for improvement)
        4. Professional yet warm
        5. Focused on growth and development
        
        Always structure feedback to:
        - Start with positive recognition of strengths
        - Acknowledge areas that are developing well
        - Provide specific, actionable suggestions for improvement
        - End with encouragement and forward-looking statements
        
        Keep feedback concise but meaningful, typically 2-3 sentences."""
    
    def get_comprehensive_prompt(self, 
                               student_name: str, 
                               scores: Dict[str, int],
                               analysis: Dict[str, List[str]]) -> str:
        """Generate comprehensive feedback prompt"""
        
        strengths_text = self._format_skills_list(analysis['strengths'], "strong")
        good_areas_text = self._format_skills_list(analysis['good_areas'], "good")
        improvement_text = self._format_skills_list(analysis['improvement_areas'], "needs improvement")
        
        prompt = f"""Generate personalized feedback for {student_name} based on these performance scores:

Performance Scores (1-10 scale):
- Communication: {scores['communication']}/10
- Teamwork: {scores['teamwork']}/10  
- Creativity: {scores['creativity']}/10
- Critical Thinking: {scores['critical_thinking']}/10
- Presentation: {scores['presentation']}/10

Performance Analysis:
{strengths_text}
{good_areas_text}
{improvement_text}

Average Score: {analysis['average_score']:.1f}/10

Write constructive, encouraging feedback that:
1. Acknowledges {student_name}'s strongest areas
2. Recognizes areas showing good progress
3. Provides specific, actionable suggestions for improvement
4. Maintains an encouraging, growth-focused tone

Focus on practical next steps and maintain a balance between recognition and development opportunities."""
        
        return prompt
    
    def get_brief_prompt(self, 
                        student_name: str, 
                        scores: Dict[str, int],
                        analysis: Dict[str, List[str]]) -> str:
        """Generate brief feedback prompt"""
        
        top_strength = analysis['strengths'][0] if analysis['strengths'] else "overall performance"
        main_improvement = analysis['improvement_areas'][0] if analysis['improvement_areas'] else "consistency"
        
        prompt = f"""Write brief, encouraging feedback for {student_name}:

Scores: Communication {scores['communication']}, Teamwork {scores['teamwork']}, 
Creativity {scores['creativity']}, Critical Thinking {scores['critical_thinking']}, 
Presentation {scores['presentation']} (all out of 10)

Highlight: {top_strength} as strength, suggest improvement in {main_improvement}.
Keep it concise, positive, and actionable (2-3 sentences maximum)."""
        
        return prompt
    
    def get_rubric_based_prompt(self, 
                              student_name: str,
                              rubric_criteria: Dict[str, str],
                              scores: Dict[str, int]) -> str:
        """Generate feedback based on specific rubric criteria"""
        
        criteria_text = "\n".join([
            f"- {criterion}: {description} (Score: {scores.get(criterion.lower().replace(' ', '_'), 'N/A')}/10)"
            for criterion, description in rubric_criteria.items()
        ])
        
        prompt = f"""Generate feedback for {student_name} based on this rubric:

{criteria_text}

Provide specific feedback that:
1. References the rubric criteria directly
2. Explains how the scores reflect performance against each criterion
3. Offers targeted improvement strategies
4. Maintains an encouraging tone

Structure the feedback to address each criterion meaningfully while keeping it cohesive."""
        
        return prompt
    
    def _format_skills_list(self, skills: List[str], performance_level: str) -> str:
        """Format skills list for prompt inclusion"""
        if not skills:
            return f"No areas identified as {performance_level}."
        
        if len(skills) == 1:
            return f"{skills[0]} shows {performance_level} performance."
        elif len(skills) == 2:
            return f"{skills[0]} and {skills[1]} show {performance_level} performance."
        else:
            return f"{', '.join(skills[:-1])}, and {skills[-1]} show {performance_level} performance."
    
    def get_improvement_suggestions(self, skill: str, score: int) -> str:
        """Get specific improvement suggestions for each skill"""
        
        suggestions = {
            'communication': {
                'low': "Practice active listening, ask clarifying questions, and work on expressing ideas clearly and concisely.",
                'medium': "Focus on adapting communication style to different audiences and improving non-verbal communication.",
                'high': "Develop advanced presentation skills and mentor others in effective communication techniques."
            },
            'teamwork': {
                'low': "Practice collaborative problem-solving, learn to compromise, and actively contribute to group discussions.",
                'medium': "Take on different team roles, improve conflict resolution skills, and support team members more actively.",
                'high': "Lead team initiatives, facilitate group discussions, and help develop other team members' collaborative skills."
            },
            'creativity': {
                'low': "Explore different brainstorming techniques, challenge assumptions, and seek inspiration from diverse sources.",
                'medium': "Experiment with combining ideas from different fields and practice thinking outside conventional frameworks.",
                'high': "Lead creative initiatives, mentor others in innovative thinking, and develop original methodologies."
            },
            'critical_thinking': {
                'low': "Practice analyzing information systematically, question assumptions, and evaluate evidence objectively.",
                'medium': "Develop skills in logical reasoning, learn to identify biases, and practice structured problem-solving.",
                'high': "Apply critical thinking to complex scenarios, teach analytical skills to others, and develop evaluation frameworks."
            },
            'presentation': {
                'low': "Practice organizing content clearly, work on public speaking confidence, and use visual aids effectively.",
                'medium': "Develop storytelling skills, improve audience engagement techniques, and refine delivery style.",
                'high': "Master advanced presentation techniques, adapt to diverse audiences, and mentor others in presentation skills."
            }
        }
        
        if score <= 5:
            level = 'low'
        elif score <= 7:
            level = 'medium'
        else:
            level = 'high'
        
        return suggestions.get(skill, {}).get(level, "Continue developing this skill through practice and feedback.")