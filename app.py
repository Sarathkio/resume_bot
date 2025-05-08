# ================================
# 📄 ResumeBot - AI Interview Coach
# Main Application Script
# ================================

# ---------- Imports ----------
import streamlit as st
import os
from dotenv import load_dotenv
from pypdf import PdfReader
from langchain.chains import LLMChain
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import SecretStr
from langchain.prompts import PromptTemplate
import speech_recognition as sr
from datetime import datetime
from login import login
from dashboard import dashboard  # Sidebar and dashboard logic
from resume_score import show_resume_score

# ---------- Load API Key ----------
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY environment variable is not set")

# ---------- Initialize LLM (Gemini 2.0 Flash) ----------
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", api_key=SecretStr(api_key))

# ---------- Session Setup ----------
if "upload_history" not in st.session_state:
    st.session_state.upload_history = []

# ---------- Helper Functions ----------

# 📄 Extract resume text from PDF
def extract_text_from_pdf(pdf_file):
    pdf_reader = PdfReader(pdf_file)
    return "".join([page.extract_text() for page in pdf_reader.pages if page.extract_text()])

# 🤖 Generate interview questions using LLM
def generate_questions(resume_text):
    template = """
    Based on the following resume, generate 10 relevant interview questions:
    {resume_text}
    
    Format the questions as a numbered list.
    """
    prompt = PromptTemplate(input_variables=["resume_text"], template=template)
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain.run(resume_text=resume_text)

# ✅ Provide AI feedback for answer
def provide_feedback(question, answer):
    feedback_template = """
    Question: {question}
    Candidate's Answer: {answer}
    
    Please provide constructive feedback on this answer, considering:
    1. Relevance to the question
    2. Clarity and structure
    3. Specific improvements
    
    Keep the feedback professional and encouraging.
    """
    prompt = PromptTemplate(input_variables=["question", "answer"], template=feedback_template)
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain.run(question=question, answer=answer)

# 🎙️ Record voice input and convert to text
def record_voice():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 Listening... Speak now!")
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio)
            st.success(f"✅ You said: {text}")
            return text
        except sr.UnknownValueError:
            st.error("❌ Sorry, I could not understand the audio.")
        except sr.RequestError as e:
            st.error(f"❌ API error: {e}")
    return ""

# ---------- Main App ----------
def main():
    st.set_page_config(page_title="ResumeBot - AI Interview Coach", page_icon="🤖")

    # ---------- Session Initialization ----------
    default_session_values = {
        "logged_in": False,
        "upload_history": [],
        "questions": None,
        "voice_answer": "",
        "profile_image": "default_profile_image.png",  # Use a default image path or URL
        "username": "",
        "email": "",
        "phone": "",
        "account_type": "user"
    }

    for key, value in default_session_values.items():
        if key not in st.session_state:
            st.session_state[key] = value

    # ---------- Login Check ----------
    if not st.session_state.logged_in:
        login()
        return

    # 🎨 App Header
    st.title("🤖 ResumeBot - AI Interview Coach")
    st.write("Upload your resume and practice interview questions with voice or text!")

    # 📂 File Upload
    uploaded_file = st.file_uploader("📄 Upload your resume (PDF)", type="pdf")

    if uploaded_file:
        resume_text = extract_text_from_pdf(uploaded_file)

        # Save upload info
        st.session_state.upload_history.append({
            "filename": uploaded_file.name,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        if st.session_state.questions is None:
            st.session_state.questions = generate_questions(resume_text)

        # Display questions
        st.subheader("🎯 Interview Questions:")
        questions_list = [q for q in st.session_state.questions.split('\n') if q.strip()]
        st.write(questions_list)

        # Select question
        selected_question = st.selectbox("👉 Select a question to answer:", questions_list)

        # Text answer input
        user_answer = st.text_area("✍️ Type your Answer:")

        # Voice answer section
        st.markdown("---")
        st.markdown("### 🎙️ OR Record your Voice Answer")
        col1, col2 = st.columns([1, 5])

        with col1:
            if st.button("🎤"):
                voice_text = record_voice()
                if voice_text:
                    st.session_state.voice_answer = voice_text

        with col2:
            st.write(st.session_state.get("voice_answer", ""))

        # Final answer preference
        final_answer = st.session_state.get("voice_answer", "") or user_answer

        # Feedback generation
        st.markdown("---")
        if st.button("🚀 Get Feedback"):
            if final_answer:
                feedback = provide_feedback(selected_question, final_answer)
                st.subheader("📋 Feedback on Your Answer:")
                st.write(feedback)
            else:
                st.warning("⚠️ Please provide an answer by text or voice.")

    # 📊 Sidebar Dashboard
    dashboard()
    # 🔻 Footer
    st.markdown(r"""
       <style>
        .footer {
            position: fixed;
            left: 0;
            bottom: -60px;
            width: 100%;
            background-color: rgba(14, 17, 23, 0.95);
            text-align: center;
            font-size: 14px;
            color: #ffffff;
            border-top: 1px solid #444;
            transition: bottom 0.4s ease;
            padding: 15px 10px;
            z-index: 9999;
        }

        body:hover .footer {
            bottom: 0;
        }

        .footer a {
            margin: 0 10px;
            text-decoration: none;
            color: #ffffff;
            font-weight: bold;
            font-size: 15px;
            display: inline-flex;
            align-items: center;
        }

        .footer a img {
            margin-right: 6px;
            width: 20px;
            height: 20px;
        }

        .footer a:hover {
            color: #4da6ff;
        }

        @media screen and (max-width: 600px) {
            .footer {
                font-size: 12px;
            }

            .footer a {
                font-size: 13px;
            }

            .footer a img {
                width: 16px;
                height: 16px;
            }
        }
    </style>
    <div class='footer'>
        Developed with ❤️ by Sarathkumar R | © 2025. All Rights Reserved.
        <br>
        <a href="https://www.linkedin.com/in/sarathkumar9843/" target="_blank">
            <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" alt="LinkedIn Icon"> LinkedIn
        </a> |
        <a href="https://sarathkio.github.io/Sarath_Profile/" target="_blank">
            <img src="https://cdn-icons-png.flaticon.com/512/841/841364.png" alt="Portfolio Icon"> Portfolio
        </a>
    </div>
    """, unsafe_allow_html=True)

# Run App
if __name__ == "__main__":
    main()
