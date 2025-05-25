# Import core libraries
import streamlit as st                                     # Web framework for UI
from datetime import datetime                              # To timestamp uploads
import os                                                  # For environment variables
from dotenv import load_dotenv                             # Load .env file
from pypdf import PdfReader                                # PDF parsing library
from langchain.chains import LLMChain                      # LangChain chain handler for LLM workflows
from langchain_google_genai import ChatGoogleGenerativeAI  # Google Gemini LLM wrapper
from pydantic import SecretStr                             # Secure string wrapper for sensitive info
from langchain.prompts import PromptTemplate               # Template prompt for LLM inputs
import speech_recognition as sr                            # Speech-to-text for voice input

# Import custom app pages (modules) from 'app' folder
# main.py
from app.login import login
from app.profile import profile
from app.uploads import uploads
from app.settings import settings


# Set the Streamlit app page configuration with a title and favicon
st.set_page_config(page_title="ResumeBot - AI Interview Coach", page_icon="🤖")

# Load environment variables from a .env file
load_dotenv()
# Get the API key from environment variables

# Read API key from Streamlit secrets

# Step 1: Load your Google API key securely
def get_google_api_key():
    try:
        return st.secrets["GOOGLE_API_KEY"]
    except KeyError:
        api_key = os.getenv("GOOGLE_API_KEY")
        if api_key:
            return api_key
        else:
            raise ValueError("❌ GOOGLE_API_KEY not found in secrets or environment variables.")

api_key = get_google_api_key()

# Step 2: Initialize the Google Gemini AI model with the API key
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", api_key=api_key)


# Define default session state values to persist across user sessions
default_session = {
    "logged_in": False,
    "username": "",
    "email": "",
    "phone": "",
    "account_type": "User",
    "password": "",
    "profile_image": "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
    "upload_history": [],   # Stores metadata of uploaded resumes
    "questions": None,      # Generated interview questions storage
    "voice_answer": ""      # Voice input text
}

# Initialize session state keys if not already set (avoid overwriting existing data)
for k, v in default_session.items():
    st.session_state.setdefault(k, v)

# If user is not logged in, show login page and halt further execution
if not st.session_state.logged_in:
    login()
    st.stop()

# Sidebar UI with enhanced styles
with st.sidebar:
    st.markdown("""
    <div style="text-align: center;">
        <img src="{}" width="100">
        <h4 style="margin-top: 10px; text-decoration: underline;">{}</h4>
    </div>
    """.format(st.session_state.profile_image, st.session_state.username), unsafe_allow_html=True)

    page = st.radio("🌐 Navigation", ["🏠 Dashboard", "🧑‍💼 Profile", "📁 Recent Uploads", "⚙️ Settings"])

    st.markdown("<hr>", unsafe_allow_html=True)

    if st.button("🚪 Logout"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# Dashboard function: handles uploading resume, generating questions,
# answering questions by text or voice, and getting AI feedback
def show_interview_dashboard():
    st.title("🤖 ResumeBot - AI Interview Coach")
    st.write("Upload your resume and practice answering interview questions with text or voice!")

    # File uploader widget for PDF resumes
    uploaded_file = st.file_uploader("📄 Upload your resume (PDF)", type="pdf")
    if uploaded_file:
        # Parse uploaded PDF and extract text from all pages
        pdf_reader = PdfReader(uploaded_file)
        resume_text = "".join([page.extract_text() for page in pdf_reader.pages if page.extract_text()])

        # Append file metadata to upload history in session state
        st.session_state.upload_history.append({
            "filename": uploaded_file.name,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        # Generate interview questions once per resume upload
        if st.session_state.questions is None:
            prompt = PromptTemplate(
                input_variables=["resume_text"],
                template="Based on the following resume, generate 10 relevant interview questions:\n{resume_text}"
            )
            chain = LLMChain(llm=llm, prompt=prompt)
            st.session_state.questions = chain.run(resume_text=resume_text)

        st.subheader("🎯 Interview Questions:")
        # Split questions by newlines and filter out empty lines
        questions = [q for q in st.session_state.questions.split("\n") if q.strip()]
        st.write(questions)

        # Allow user to select question and answer via text area
        selected_question = st.selectbox("👉 Select a question to answer:", questions)
        user_answer = st.text_area("✍️ Type your Answer:")

        # Voice answer section: record and convert speech to text
        st.markdown("### 🎙️ OR Record your Voice Answer")
        col1, col2 = st.columns([1, 5])

        with col1:
            if st.button("🎤 Record"):
                recognizer = sr.Recognizer()
                with sr.Microphone() as source:
                    st.info("Listening...")
                    try:
                        audio = recognizer.listen(source, timeout=5)
                        text = recognizer.recognize_google(audio)
                        st.success(f"You said: {text}")
                        st.session_state.voice_answer = text
                    except:
                        st.error("Voice not recognized.")

        with col2:
            st.write(st.session_state.get("voice_answer", ""))

        # Use voice answer if provided, else fallback to typed answer
        final_answer = st.session_state.get("voice_answer") or user_answer

        # Button to generate AI feedback on user's answer
        if st.button("🚀 Get Feedback"):
            if final_answer:
                feedback_prompt = PromptTemplate(
                    input_variables=["question", "answer"],
                    template="""
                    Question: {question}
                    Candidate's Answer: {answer}
                    Please provide professional feedback on relevance, clarity, and improvement.
                    """
                )
                feedback_chain = LLMChain(llm=llm, prompt=feedback_prompt)
                feedback = feedback_chain.run(question=selected_question, answer=final_answer)
                st.subheader("📋 Feedback:")
                st.write(feedback)
            else:
                st.warning("Provide an answer by text or voice.")

# Route to selected page based on sidebar navigation
if page == "🏠 Dashboard":
    show_interview_dashboard()
elif page == "🧑‍💼 Profile":
    profile()
elif page == "📁 Recent Uploads":
    uploads()
elif page == "⚙️ Settings":
    settings()

# Sticky footer at the bottom of the app page
st.markdown("""
<style>
.footer {
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    text-align: center;
    color: #888;
    font-size: 0.9em;
    padding: 8px;
    background-color: #f9f9f9;
    border-top: 1px solid #ddd;
}
</style>
<div class='footer'>Developed with ❤️ by Sarathkumar R | © 2025</div>
""", unsafe_allow_html=True)
