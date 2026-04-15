import streamlit as st
from supabase import create_client, Client
import hashlib

# ---------------- HASH FUNCTION ----------------
def hash_pass(password):
    return hashlib.sha256(password.encode()).hexdigest()


# ---------------- SUPABASE SETUP ----------------
url = "https://acspvvfxhputejndpluk.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFjc3B2dmZ4aHB1dGVqbmRwbHVrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzYyNTk5MjksImV4cCI6MjA5MTgzNTkyOX0.u6QA3HI2ZsAVR4cbpUuKZAULkBH96VMrkRPU5FWN3As"

supabase: Client = create_client(url, key)


# ---------------- SESSION ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "page" not in st.session_state:
    st.session_state.page = "login"


# ---------------- FUNCTIONS ----------------
def signup(username, password):
    password = hash_pass(password)  # 🔐 hash password

    try:
        supabase.table("users").insert({
            "username": username,
            "password": password
        }).execute()
        return True
    except:
        return False  # username already exists


def login(username, password):
    password = hash_pass(password)  # 🔐 hash input

    data = supabase.table("users").select("*").eq("username", username).execute()

    if data.data:
        if data.data[0]["password"] == password:
            return True
    return False


# ---------------- PAGES ----------------
def home():
    st.title("🏠 Home Screen")
    st.success(f"Welcome {st.session_state.username} 🎉")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.page = "login"
        st.rerun()


def login_page():
    st.title("🔐 Login")

    username = st.text_input("Username",
                            key="login_username")
    password = st.text_input("Password", type="password",
                            key="login_password")

    if st.button("Login",key="login_btn"):
        if login(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.page = "home"
            st.rerun()
        else:
            st.error("Invalid username or password")

    if st.button("Go to Signup",key="goto_signup"):
        st.session_state.page = "signup"
        st.rerun()


def signup_page():
    st.title("📝 Signup")

    username = st.text_input("Create Username",key="signup_username")
    password = st.text_input("Create Password", type="password",key="signup_password")

    if st.button("Signup",key="signup_btn"):
        if signup(username, password):
            st.success("Account created! Please login.")
        else:
            st.error("Username already exists ❌")

    if st.button("Back to Login",key="back_login"):
        st.session_state.page = "login"
        st.rerun()


# ---------------- MAIN ----------------
if st.session_state.logged_in:
    home()
else:
    if st.session_state.page == "login":
        login_page()
    elif st.session_state.page == "signup":
        signup_page()

# ---------------- MAIN ----------------
if st.session_state.logged_in:
    home()
else:
    if st.session_state.page == "login":
        login_page()
    elif st.session_state.page == "signup":
        signup_page()
