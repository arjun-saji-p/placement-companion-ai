import streamlit as st
from pypdf import PdfReader
def home_page():
    st.title("🎓Placement Companion AI")

    st.write("Welcome to your personal placement preparation assistant!")

    name=st.text_input("Enter your name:")

    if st.button("Submit"):
        st.write(f"Welcome,{name}!🎉")

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
            "📄Resume Analyzer"
        ]
    )
    if page=="🏡Home":
        home_page()
    elif page=="📄Resume Analyzer":
        resume_page()

def resume_page():
    st.title("📄Resume Analyzer")
    
    uploaded_file= st.file_uploader(
        "Upload your resume",
        type=["pdf"]
    )
    if uploaded_file is not None:
        reader=PdfReader(uploaded_file)
        text=""

        for page in reader.pages:
            text+=page.extract_text()

        st.success("Resume uploaded successfully!🎉")
        st.text_area(
            "Resume Content",
            text,
            height=300
        )
        required_skills=[
            "Python",
            "Java",
            "SQL",
            "Git",
            "Machine Learning",
            "HTML",
            "CSS",
            "JavaScript"
        ]
        st.subheader("Skill Analysis")
        text=text.lower()
        matched_skills=0
        for skill in required_skills:
            matched_skills+=1
            if skill.lower() in text:
                st.success(f"✅ {skill}")
            else:
                st.error(f"❌ {skill}")
        score=(matched_skills/len(required_skills))*100
        st.subheader("Resume Score")
        st.progress(score/100)
        st.write(f"Score: {score:.0f}%")


main()
    
