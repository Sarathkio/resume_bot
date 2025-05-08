import streamlit as st
from datetime import datetime
from streamlit_lottie import st_lottie
import requests
import os

# --- Initialize session state ---
if "upload_history" not in st.session_state:
    st.session_state.upload_history = []
if "profile_image" not in st.session_state:
    st.session_state.profile_image = "https://cdn-icons-png.flaticon.com/512/3135/3135715.png"
if "password" not in st.session_state:
    st.session_state.password = "admin123"
if "email" not in st.session_state:
    st.session_state.email = "user@example.com"
if "username" not in st.session_state:
    st.session_state.username = st.session_state.email.split('@')[0]
if "phone" not in st.session_state:
    st.session_state.phone = "+91XXXXXXXXXX"
if "account_type" not in st.session_state:
    st.session_state.account_type = "Standard User"
if "show_dashboard" not in st.session_state:
    st.session_state.show_dashboard = True

# ----------------------------
# CSS and Theme Integration
# ----------------------------

def inject_custom_css(theme="light"):
    if theme == "dark":
        background = "#0e1117"
        text_color = "#fafafa"
        accent_color = "#1f6feb"
    else:
        background = "#ffffff"
        text_color = "#000000"
        accent_color = "#0366d6"

    st.markdown(f"""
        <style>
            html, body, [class*="css"] {{
                background-color: {background} !important;
                color: {text_color} !important;
                transition: all 0.3s ease-in-out;
            }}
            .stButton > button {{
                background-color: {accent_color};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 16px;
                transition: 0.3s;
            }}
            .stButton > button:hover {{
                background-color: #444;
                transform: scale(1.05);
            }}
            .stTextInput > div > div > input,
            .stFileUploader > div > div {{
                background-color: transparent !important;
                color: {text_color} !important;
            }}
            .sidebar .sidebar-content {{
                background: {'#161b22' if theme == 'dark' else '#f0f2f6'};
            }}
        </style>
    """, unsafe_allow_html=True)


# ----------------------------
# Lottie Animation
# ----------------------------

def load_lottie_url(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

animation = load_lottie_url("https://assets4.lottiefiles.com/packages/lf20_cg3eqk.json")

# ----------------------------
# UI Page Functions
# ----------------------------

def show_dashboard():
    st.markdown(f"""
        <div style="text-align: center;">
            <h3>Welcome, {st.session_state.username}!</h3>
        </div>
    """, unsafe_allow_html=True)

    if animation:
        st_lottie(animation, height=300)
    st.success("Use the sidebar to explore your features!")

def show_profile():
    st.header("👤 User Profile")
    col1, col2 = st.columns([1, 4])

    with col1:
        try:
            if isinstance(st.session_state.profile_image, str):
                if st.session_state.profile_image.startswith("http"):
                    st.image(st.session_state.profile_image, width=100)
                elif os.path.exists(st.session_state.profile_image):
                    st.image(st.session_state.profile_image, width=100)
                else:
                    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100)
            else:
                st.image(st.session_state.profile_image, width=100)
        except Exception:
            st.warning("⚠️ Failed to load profile image.")
            st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100)

    with col2:
        st.markdown(f"**Username:** `{st.session_state.username}`")
        st.markdown(f"**Email:** `{st.session_state.email}`")
        st.markdown(f"**Phone:** `{st.session_state.phone}`")
        st.markdown(f"**Account Type:** `{st.session_state.account_type}`")

def show_uploads():
    st.header("🕓 Recent Upload History")
    with st.expander("📁 View Uploads"):
        if st.session_state.upload_history:
            for i, item in enumerate(reversed(st.session_state.upload_history), 1):
                st.write(f"{i}. 📄 {item['filename']} - ⏱️ {item['timestamp']}")
            if st.button("🧹 Clear History"):
                st.session_state.upload_history.clear()
                st.success("✅ Upload history cleared.")
        else:
            st.info("No uploads yet.")

def show_settings():
    st.header("⚙️ Settings")

    st.subheader("🖼️ Change Profile Image")
    uploaded_file = st.file_uploader("Upload New Profile Image", type=["png", "jpg", "jpeg"])
    if uploaded_file:
        st.session_state.profile_image = uploaded_file
        st.success("✅ Profile image updated!")

    try:
        if isinstance(st.session_state.profile_image, str):
            if st.session_state.profile_image.startswith("http"):
                st.image(st.session_state.profile_image, width=120)
            elif os.path.exists(st.session_state.profile_image):
                st.image(st.session_state.profile_image, width=120)
            else:
                st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=120)
        else:
            st.image(st.session_state.profile_image, width=120)
    except Exception:
        st.warning("⚠️ Failed to load profile image.")
        st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=120)

    st.subheader("📱 Update Phone Number")
    new_phone = st.text_input("Enter new phone number", value=st.session_state.phone)
    if st.button("Update Phone"):
        if new_phone.strip():
            st.session_state.phone = new_phone.strip()
            st.success("✅ Phone number updated!")

    st.subheader("🔐 Change Password")
    with st.form("password_form", clear_on_submit=True):
        current_password = st.text_input("Current Password", type="password")
        new_password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm New Password", type="password")
        submitted = st.form_submit_button("Apply Changes")
        if submitted:
            if current_password != st.session_state.password:
                st.error("❌ Current password is incorrect.")
            elif new_password != confirm_password:
                st.error("❌ New passwords do not match.")
            elif new_password.strip() == "":
                st.warning("⚠️ New password cannot be empty.")
            else:
                st.session_state.password = new_password
                st.success("✅ Password updated successfully.")


# ----------------------------
# Main Dashboard Function
# ----------------------------
def dashboard():
    if "show_dashboard" not in st.session_state:
        st.session_state.show_dashboard = True

    theme = "light"
    inject_custom_css(theme)

    try:
        if isinstance(st.session_state.profile_image, str):
            if st.session_state.profile_image.startswith("http"):
                st.sidebar.image(st.session_state.profile_image, width=80)
            elif os.path.exists(st.session_state.profile_image):
                with open(st.session_state.profile_image, "rb") as img_file:
                    st.sidebar.image(img_file, width=80)
            else:
                st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=80)
        else:
            st.sidebar.image(st.session_state.profile_image, width=80)
    except Exception:
        st.sidebar.warning("⚠️ Failed to load image.")
        st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=80)

    # Display user info in sidebar
    st.sidebar.markdown(f"**👤 {st.session_state.username}**")
    st.sidebar.markdown(f"📞 {st.session_state.phone}")

    menu = st.sidebar.radio("📋 Menu", ["Dashboard", "Profile", "Recent Uploads", "Settings"])

    toggle_dashboard = st.sidebar.checkbox("Show/Hide Dashboard", value=st.session_state.show_dashboard)
    st.session_state.show_dashboard = toggle_dashboard

    if st.sidebar.button("🚪 Logout"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

    if menu == "Dashboard" and st.session_state.show_dashboard:
        show_dashboard()
    elif menu == "Profile":
        show_profile()
    elif menu == "Recent Uploads":
        show_uploads()
    elif menu == "Settings":
        show_settings()


# ----------------------------
# Run App
# ----------------------------

if __name__ == "__main__":
    dashboard()
