import streamlit as st
from streamlit_lottie import st_lottie
import requests

# Function to load a Lottie animation from a given URL
def load_lottie_url(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None  # Return None if the request fails
    return r.json()  # Return the JSON animation if successful

# Function to render the dashboard page
def dashboard():
    # Display a personalized welcome message using the session state's username
    st.markdown(
        f"<h2 style='text-align: center; color: #1a73e8;'>Welcome, {st.session_state.username}!</h2>",
        unsafe_allow_html=True
    )
    
    # Load and display a Lottie animation on the dashboard
    animation = load_lottie_url("https://assets4.lottiefiles.com/packages/lf20_cg3eqk.json")
    if animation:
        st_lottie(animation, height=300, key="dashboard_animation")
    
    # Provide a prompt below the animation to guide user navigation
    st.markdown(
        "<div style='text-align: center;'>Explore your features using the sidebar!</div>",
        unsafe_allow_html=True
    )
