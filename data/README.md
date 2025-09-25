# Data Directory

This directory contains data files used by the Auto Feedback Generator:

## Files

- `rubrics.csv`: Evaluation rubrics and criteria definitions
- `student_performance_list.csv`: Sample student performance data
- `prompt_templates/`: Directory containing prompt template files

## Usage

These files are used for:
- Training and testing the feedback generation system
- Providing sample data for development
- Defining evaluation criteria and rubrics

## Format

### rubrics.csv
Contains rubric definitions with columns:
- Rubric ID
- Criterion
- Description  
- Score Range

### student_performance_list.csv
Contains sample student data with performance scores across different criteria.

## Adding New Data

When adding new data files:
1. Follow the existing CSV format
2. Include appropriate headers
3. Validate data integrity
4. Update this README if needed