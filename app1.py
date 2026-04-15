import streamlit as st
import json
import os
st.markdown("<h1 style='text-align=center;color=lime;'>Checkmate-Chess</h1>",
            unsafe_allow_html=True)
st.markdown("<h1 style='text-align=center;color=yellow;'>Welcome!!</h1>",
            unsafe_allow_html=True)
# ------------------ FILE SETUP ------------------
USER_FILE = "users.json"

if not os.path.exists(USER_FILE):
    with open(USER_FILE, "w") as f:
        json.dump({}, f)


# ------------------ FUNCTIONS ------------------
def load_users():
    with open(USER_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f)


def signup(username, password):
    users = load_users()
    
    if username in users:
        return False  # username already exists
    
    users[username] = password
    save_users(users)
    return True


def login(username, password):
    users = load_users()
    
    if username in users and users[username] == password:
        return True
    
    return False


# ------------------ SESSION ------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "page" not in st.session_state:
    st.session_state.page = "login"


# ------------------ UI ------------------

# HOME SCREEN
def home():
    st.title("🏠 Home Screen")
    st.success(f"Welcome {st.session_state.username} 🎉")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.page = "login"


# LOGIN PAGE
def login_page():
    st.title("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if login(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.page = "home"
            st.rerun()
        else:
            st.error("Invalid username or password")

    if st.button("Go to Signup"):
        st.session_state.page = "signup"
        st.rerun()


# SIGNUP PAGE
def signup_page():
    st.title("📝 Signup")

    username = st.text_input("Create Username")
    password = st.text_input("Create Password", type="password")

    if st.button("Signup"):
        if signup(username, password):
            st.success("Account created! Please login.")
        else:
            st.error("Username already exists ❌")

    if st.button("Back to Login"):
        st.session_state.page = "login"
        st.rerun()


# ------------------ PAGE CONTROL ------------------

if st.session_state.logged_in:
    home()
else:
    if st.session_state.page == "login":
        login_page()
    elif st.session_state.page == "signup":
        signup_page()
            
