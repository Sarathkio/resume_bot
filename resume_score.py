import streamlit as st
import fitz  # PyMuPDF
from datetime import datetime

# --- Keyword sections used for scoring ---
REQUIRED_SECTIONS = {
    "contact": ["email", "phone", "linkedin", "github"],
    "education": ["bachelor", "master", "degree", "university", "college"],
    "experience": ["intern", "experience", "project", "developer", "engineer"],
    "skills": ["python", "java", "sql", "html", "css", "javascript"],
    "achievements": ["award", "certification", "hackathon", "scholarship"]
}

POWER_WORDS = ["lead", "developed", "implemented", "designed", "analyzed"]

# --- Function to extract raw text from uploaded PDF ---
def extract_text_from_pdf(file):
    text = ""
    doc = fitz.open(stream=file.read(), filetype="pdf")
    for page in doc:
        text += page.get_text()
    return text.lower()

# --- Resume score logic ---
def calculate_resume_score(text):
    score = 0
    feedback = []
    section_score = 100 // len(REQUIRED_SECTIONS)

    for section, keywords in REQUIRED_SECTIONS.items():
        if any(k in text for k in keywords):
            score += section_score
        else:
            feedback.append(f"❌ *{section.capitalize()}* section or related keywords not found.")

    # Add bonus points for power/action words
    if any(word in text for word in POWER_WORDS):
        score += 5
        feedback.append("✅ Good use of action/power words detected.")

    return min(score, 100), feedback

# --- Main UI function for Resume Score page ---
def show_resume_score():
    st.header("📄 Resume Score Checker")
    st.markdown("Upload your resume PDF to get a quality score out of 100 with improvement suggestions.")

    uploaded_resume = st.file_uploader("Upload Resume (PDF)", type=["pdf"], key="unique_resume_uploader")

    if uploaded_resume:
        with st.spinner("Analyzing your resume..."):
            extracted_text = extract_text_from_pdf(uploaded_resume)
            score, suggestions = calculate_resume_score(extracted_text)

        # --- Display Circular Score Indicator ---
        if score >= 80:
            color = "green"
        elif score >= 50:
            color = "orange"
        else:
            color = "red"

        st.markdown(
            f"""
            <div style='text-align:center;'>
                <div style='
                    width: 180px;
                    height: 180px;
                    border-radius: 50%;
                    background: conic-gradient({color} {score}%, #eee {score}%);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    margin: auto;
                    font-size: 32px;
                    font-weight: bold;
                    color: #333;
                '>
                    {score}%
                </div>
                <p style='font-size: 18px; margin-top: 10px;'>Resume Score</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        # --- Feedback Section ---
        st.subheader("✅ Good Sections")
        found_sections = []
        for section, keywords in REQUIRED_SECTIONS.items():
            if any(k in extracted_text for k in keywords):
                st.markdown(f"<span style='color:green;'>✔ {section.capitalize()}</span>", unsafe_allow_html=True)
                found_sections.append(section)

        st.subheader("❌ Missing / Needs Improvement")
        for section in REQUIRED_SECTIONS:
            if section not in found_sections:
                st.markdown(f"<span style='color:red;'>✖ {section.capitalize()}</span>", unsafe_allow_html=True)

        # --- Suggestions ---
        st.subheader("💡 Suggestions")
        if suggestions:
            for s in suggestions:
                st.markdown(f"- {s}")
        else:
            st.success("Your resume is well-structured and includes all important sections!")

        # Save upload history
        if "upload_history" not in st.session_state:
            st.session_state.upload_history = []

        st.session_state.upload_history.append({
            "filename": uploaded_resume.name,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "score": score
        })