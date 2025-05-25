# Install core Streamlit package for building the app
pip install streamlit

# Install python-dotenv to manage environment variables (.env files)
pip install python-dotenv

# Install PyPDF to parse PDFs
pip install pypdf

# Install LangChain and Google Gemini API support
pip install langchain langchain-google-genai

# Install Pydantic for data validation and secure secrets management
pip install pydantic

# Install SpeechRecognition for voice command support
pip install SpeechRecognition

# Install PyAudio for capturing microphone input (skip on Windows)
pip install pyaudio  # If on Windows, install via precompiled binaries or skip

# Install Pillow for image processing (profile images etc.)
pip install pillow

# Install requests for HTTP operations (if needed)
pip install requests

# Optional: Install Streamlit Lottie for animations
pip install streamlit-lottie

# Optional: Install Streamlit Option Menu for sidebar navigation UI
pip install streamlit-option-menu

# Program Run 
python -m streamlit run main.py