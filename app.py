import streamlit as st
from pypdf import PdfReader
import google.generativeai as genai
from dotenv import load_dotenv
import os
import random
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.5-flash")

def home_page():
    st.title("🎓Placement Companion AI")

    st.caption("Your AI Partner for Placement Success")

    name=st.text_input("Enter your name:")

    if st.button("Submit"):
        st.subheader(f"Good Evening,{name}!🫡")

        if "resume_text" in st.session_state:
            st.write("📄 Resume Status")
            st.write("Uploaded✅")
        else:
            st.write("📄 Resume Status")
            st.write("Upload your resume to unlock my full potential!")
            
        with st.container(border=True):
            companion_messages = [
            "I'm ready to help you achieve your placement goals. 🚀",
            "Every great software engineer started where you are today.",
            "One small step today is better than no step at all.",
            "Let's make today's effort count!",
            "Your next offer letter starts with today's work.",
            "Progress isn't always visible—but it's always happening.",
            "Keep showing up. Consistency wins placements.",
            "Let's build something you'll be proud to show in interviews.",
            "Today's effort is tomorrow's confidence.",
            "I'm here to guide you through your placement journey. 💙"
            ]
            st.subheader("💙 Message for YOU ")    
            st.write(random.choice(companion_messages))
        with st.container(border=True): 
            missions=[
            "Solve 2 LeetCode problems.",
            "Revise one DSA topic for 30 minutes.",
            "Push today's code to GitHub.",
            "Improve one section of your resume.",
            "Practice 10 aptitude questions.",
            "Learn one new SQL query.",
            "Read about one interview question.",
            "Spend 30 minutes on your project.",
            "Review Python functions and OOP.",
            "Practice one coding problem without hints.",
            "Watch one placement interview experience.",
            "Revise Git commands and workflows.",
            "Improve one project description.",
            "Learn one new Python library.",
            "Read one article about system design.",
            "Practice one HR interview question.",
            "Refactor a piece of your code.",
            "Write clean comments for your project.",
            "Learn one new concept instead of memorizing code.",
            "Stay consistent today—small progress counts."
            ]
            st.subheader("🎯 Today's Mission")  
            st.write(random.choice(missions))
        with st.container(border=True):
            tips = [
            "Keep your resume to one page whenever possible.",
            "Use action verbs like Built, Developed, Designed, and Optimized.",
            "Quantify achievements whenever you can.",
            "Projects with GitHub links stand out more.",
            "Consistency beats intensity during placement season.",
            "Practice explaining your projects out loud.",
            "Recruiters value problem-solving more than memorization.",
            "Learn concepts, not just syntax.",
            "Commit your code regularly to GitHub.",
            "Customize your resume for each job description.",
            "Strong fundamentals beat knowing many frameworks.",
            "Focus on one project and make it excellent.",
            "Debugging is one of the fastest ways to improve.",
            "Write readable code—your interviewer will appreciate it.",
            "Interviewers often ask why you made design choices.",
            "Practice coding without looking at solutions first.",
            "Every rejected interview is valuable feedback.",
            "Keep learning, even on days you don't feel motivated.",
            "Small improvements every day lead to big results.",
            "Confidence comes from preparation, not luck."
            ]
            st.subheader("💡 AI Tips")
            st.write(random.choice(tips))

        st.header("🔍 Quick Actions")
        st.write("📄 Resume Analyzer")
        st.write("🎤 Interview Preparation")
        st.write("🗺️ Learning Roadmap")

def main():
    st.set_page_config(
    page_title="Placement Companion AI",
    page_icon="🎓",
    layout="wide"
    )
    st.sidebar.title("Navigation")

    page=st.sidebar.radio(
        "Choose a page",
        [
            "🏡Home",
            "📄Resume Analyzer",
            "⌛ Interview Preparation"
        ]
    )
    if page=="🏡Home":
        home_page()
    elif page=="📄Resume Analyzer":
        resume_page()
    elif page=="⌛ Interview Preparation":
        interview_page()

def extract_file(uploaded_file):
    reader=PdfReader(uploaded_file)
    text=""
    for page in reader.pages:
        text+=page.extract_text()
    return text

def analyze_resume(resume_text,jd_text):
    prompt = create_prompt(resume_text,jd_text)
    response = model.generate_content(prompt)
    return response.text

def create_prompt(resume_text,jd_text):
    if jd_text:
        prompt = f""" 
    You are an expert ATS Resume Reviewer.
    Compare the resume with the given Job Description.
    Return the response in Markdown format.
    Use ONLY these given below.
    
    # 📊 Match Score

    # ✅ Matching Skills

    # ❌ Missing Skills

    # 💪 Resume Strengths

    # ⚠️ Resume Weaknesses

    # 📄 ATS Suggestions

    # 🎯 Interview Topics

    Use short bullet points.
    Do not write long paragraphs.

    Resume:
    {resume_text}
    Job Description:
    {jd_text}
    """
    else:
        prompt=f"""
    You are an ATS Resume Reviewer and Placement Mentor.
    Analyze the following resume.
    
    IMPORTANT:
    - Return the response in Markdown format.
    - Use ONLY the headings given below.
    - Use short bullet points.
    - Keep every bullet to one point.
    - Do not write long paragraphs.

    Your response must follow this format exactly:
    
    # 📊 Resume Score
    Give a score out of 100.
    Also explain the score in 2-3 bullet points.

    # 💪 Strengths

    # ⚠️ Areas to Improve

    # 📄 ATS Suggestions

    # 📚 Skills to Learn

    # 🎯 Interview Topics

    Resume:
    {resume_text}
    """
    return prompt 
def resume_page():
    st.title("📄Resume Analyzer")
    
    uploaded_file= st.file_uploader(
        "Upload your resume (PDF)",
        type=["pdf"]
    )
    if uploaded_file:
        if uploaded_file is not None:
            text=extract_file(uploaded_file)
            st.session_state["resume_text"]=text
            st.session_state["resume_name"]=uploaded_file.name
            st.success("Resume uploaded successfully!🎉")
            st.text_area(
                "Resume Content",
                text,
                height=300
            )
            jd_text=st.text_area(
            "📋 Paste Job Description(Optional)",
            height=200,
            placeholder="Paste the job description here..."
            )
            if jd_text:
                st.subheader("📋 Job Description")
                st.write(jd_text)
        
            if st.button("Analyze Resume🪄"):
                with st.spinner("🤖 Analyzing your resume..."):
                    analysis = analyze_resume(text,jd_text)
                    st.success("✅ Analysis Complete!")
                    st.subheader("🤖 Resume Analysis")
                    st.markdown(analysis)
    else:
        st.warning("⚠️ Please upload your resume first.")

def interview_page():
    st.header("🎤 AI Interview Preparation")
    st.subheader("Practice personalized interview questions generated from your resume.")
    if "resume_text" in st.session_state:
        st.subheader("🎯 Select Difficulty")
        difficulty=st.radio(
            "Difficulty",
            ["Easy","Medium","Hard"]
        )
        st.subheader("🎤 Interview Questions")
        interview_type=st.radio(
            "Interview Type",
            ["Techncal","HR","Mixed"]
        )
        st.subheader("📝 Number of Questions")
        num_questions=st.radio(
            "Select Number of Questions",
            [5,10,15]
        )
        if st.button("🎤 Generate Interview Questions"):
            with st.spinner("🤖 Generating Questions..."):
                if "resume_text" not in st.session_state:
                    st.warning("⚠️ Please upload your resume first.")
                else:
                    resume_text=st.session_state["resume_text"]
                    prompt= create_interview_prompt(
                        resume_text,
                        difficulty,
                        interview_type,
                        num_questions
                    )
                    response= model.generate_content(prompt)
                    st.markdown(response.text) 
    else:
        st.write("⚠️ No Resume Found ")
        st.write("Upload your resume first.")
        st.write("Go to Resume Analyzer")

def create_interview_prompt(resume_text,difficulty,interview_type,num_questions):
    prompt= f"""
    You are an experienced software engineer interviewer.
    The candidate's resume is given below.
    Resume:
    {resume_text}
    Difficulty: {difficulty}
    Interview Type: {interview_type}
    Number of Questions: {num_questions}

    Generate {num_questions} interview questions.
    Rules:
    -Base the questions on the resume.
    -If Interview Type is Technical,ask only technical questions.
    -If Interview Type is HR,ask only HR/personality questions.
    -If Interview Type is Mixed,include both technical and HR questions.
    -Match the selected difficulty level.
    -Do not provide answers.
    -Number the questions clearly.
    """
    return prompt

main()
      