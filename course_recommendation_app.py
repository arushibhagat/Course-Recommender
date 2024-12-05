import streamlit as st
import json
import spacy
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

# Load Spacy model for NLP (resume processing)
nlp = spacy.load("en_core_web_sm")

# Load your courses metadata
with open('courses_metadata.json', 'r') as file:
    courses = json.load(file)

# Convert the courses list to a pandas DataFrame for easy manipulation
courses_df = pd.DataFrame(courses)

# Function to extract skills from resume text
def extract_skills_from_text(text):
    doc = nlp(text)
    skills = []
    for token in doc:
        if token.pos_ in ["NOUN", "PROPN"]:  # Extract nouns as potential skills (could be customized)
            skills.append(token.text)
    return set(skills)

# Function to recommend courses based on student skills and career goals
def recommend_courses(student_skills, student_industry_interest):
    recommendations = []

    for index, course in courses_df.iterrows():
        course_skills = set(course['metadata']['skills'])
        course_industry = set(course['metadata']['industry_relevance'])

        # Match skills
        skill_overlap = student_skills & course_skills
        industry_overlap = student_industry_interest & course_industry

        # If there is skill or industry match, recommend the course
        if skill_overlap or industry_overlap:
            recommendations.append(course['course_name'])
    
    return recommendations

# Streamlit UI setup
st.title('Automated Course Recommendation System')

# Step 1: Student Input
st.header("Step 1: Enter Your Information")
student_name = st.text_input("Your Name:")
career_goals = st.text_area("Enter Your Career Goals (e.g., Software Development, Data Science):")
resume_text = st.text_area("Paste your resume or relevant career text here:")

# Step 2: Parse Career Goals and Resume
if st.button('Submit'):
    # Extract skills from the resume using NLP
    student_skills = extract_skills_from_text(resume_text)
    
    # Extract industry interests from the career goals
    student_industry_interest = set(career_goals.split(','))

    # Recommend courses
    recommended_courses = recommend_courses(student_skills, student_industry_interest)

    if recommended_courses:
        st.write(f"Recommended Courses for {student_name}:")
        for course in recommended_courses:
            st.write(f"- {course}")
    else:
        st.write("No matching courses found. Try providing more details in your career goals or resume.")
