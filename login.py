import streamlit as st
import sqlite3
import hashlib

# --- Database Setup ---
def create_users_table():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    username TEXT, 
                    email TEXT PRIMARY KEY,  -- Enforce unique email
                    phone TEXT, 
                    password TEXT)''')
    conn.commit()
    conn.close()

def add_user(username, password, email, phone):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    c.execute("INSERT INTO users (username, password, email, phone) VALUES (?, ?, ?, ?)", 
              (username, hashed_password, email, phone))
    conn.commit()
    conn.close()

def validate_user(email, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    c.execute("SELECT username, email, phone FROM users WHERE email=? AND password=?", (email, hashed_password))
    result = c.fetchone()
    conn.close()
    return result  # (username, email, phone)


def email_exists(email):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT email FROM users WHERE email=?", (email,))
    result = c.fetchone()
    conn.close()
    return result is not None

# --- Streamlit UI ---
def login():
    create_users_table()


    # --- Custom Styling (Bootstrap-inspired) ---
    st.markdown("""
        <style>
            .login-title {
                font-size: 30px;
                text-align: center;
                color: #2d3436;
                font-weight: bold;
                margin-top: 20px;
                margin-bottom: 30px;
            }
            .stTabs [role="tablist"] {
                justify-content: center;
            }
            .stApp {
                background-color: #f0f2f6;
            }
            .block-container {
                max-width: 500px;
                margin: auto;
                background-color: white;
                padding: 2rem;
                border-radius: 10px;
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
            }
            input {
                border-radius: 5px !important;
            }
            button[kind="secondary"] {
                background-color: #3498db !important;
                color: white !important;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='login-title'>🔐 ResumeBot Login & Registration</div>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["🔑 Login", "📝 Register"])

    # --- Login Tab ---
    with tab1:
        with st.form("login_form"):
            email = st.text_input("📧 Email")
            password = st.text_input("🔑 Password", type="password")
            submitted = st.form_submit_button("Login", use_container_width=True)

            if submitted:
                if validate_user(email, password):
                    st.session_state.logged_in = True
                    st.session_state.email = email
                    st.success("✅ Login successful!")
                    st.rerun()
                else:
                    st.error("❌ Invalid email or password.")

    # --- Register Tab ---
    with tab2:
        with st.form("register_form"):
            username = st.text_input("👤 Username")
            email = st.text_input("📧 Email")
            phone = st.text_input("📱 Phone Number (e.g., +91XXXXXXXXXX)")
            password1 = st.text_input("🔒 New Password", type="password")
            password2 = st.text_input("✅ Confirm Password", type="password")
            registered = st.form_submit_button("Create Account", use_container_width=True)

            if registered:
                if password1 != password2:
                    st.warning("⚠️ Passwords do not match.")
                elif not all([username.strip(), password1.strip(), email.strip(), phone.strip()]):
                    st.warning("⚠️ All fields are required.")
                elif email_exists(email):
                    st.error("❌ Email already registered.")
                else:
                    add_user(username, password1, email, phone)
                    st.success("✅ Account created! You can now login.")

# --- Run the app ---
if __name__ == "__main__":
    login()
