import streamlit as st
from supabase import create_client, Client
import hashlib
import chess
import chess.engine
import os
import urllib.request
import zipfile
from streamlit_chess import st_chess

# ---------------- HASH ----------------
def hash_pass(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ---------------- SUPABASE ----------------
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

# ---------------- SESSION ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "page" not in st.session_state:
    st.session_state.page = "login"

if "board" not in st.session_state:
    st.session_state.board = chess.Board()

# ---------------- ENGINE DOWNLOAD ----------------
def download_stockfish():
    if not os.path.exists("stockfish"):
        url = "https://stockfishchess.org/files/stockfish_15_linux_x64_avx2.zip"
        urllib.request.urlretrieve(url, "stockfish.zip")

        with zipfile.ZipFile("stockfish.zip", 'r') as zip_ref:
            zip_ref.extractall()

        for file in os.listdir():
            if "stockfish" in file and not file.endswith(".zip"):
                os.rename(file, "stockfish")

        os.chmod("stockfish", 0o755)

# ---------------- AUTH ----------------
def signup(username, password):
    username = username.strip()
    password = hash_pass(password)

    existing = supabase.table("users").select("*").eq("username", username).execute()
    if existing.data:
        return "exists"

    supabase.table("users").insert({
        "username": username,
        "password": password
    }).execute()

    return "success"


def login(username, password):
    username = username.strip()
    password = hash_pass(password)

    data = supabase.table("users").select("*").eq("username", username).execute()

    if data.data:
        if data.data[0]["password"] == password:
            return True
        else:
            return "wrong_password"

    return "no_user"

# ---------------- HOME ----------------
def home():
    col1, col2, col3 = st.columns([1,3,1])

    with col1:
        if st.button("👤"):
            st.info(f"User: {st.session_state.username}")

    with col2:
        st.markdown("<h3 style='text-align:center;'>♟️ Checkmate-Chess</h3>", unsafe_allow_html=True)

    with col3:
        if st.button("🔔"):
            show_notifications()

    st.divider()

    if st.button("🤖 Play with Bot"):
        st.session_state.page = "bot"
        st.rerun()

    if st.button("👥 Add Friend"):
        st.session_state.page = "friends"
        st.rerun()

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.page = "login"
        st.rerun()

# ---------------- BOT ----------------
def bot_page():
    st.title("♟️ Play with Bot")

    rating = st.slider("Engine Rating", 400, 2000, 800, step=100)

    board = st.session_state.board

    # REAL CHESS BOARD
    move = st_chess(board)

    if move:
        try:
            board.push_uci(move)

            download_stockfish()
            engine = chess.engine.SimpleEngine.popen_uci("./stockfish")

            skill = int((rating - 400) / 80)
            skill = max(0, min(skill, 20))

            engine.configure({"Skill Level": skill})

            result = engine.play(board, chess.engine.Limit(time=0.2))
            board.push(result.move)

            engine.quit()

            st.session_state.board = board

        except:
            st.error("Invalid move ❌")

    if st.button("Reset Game"):
        st.session_state.board = chess.Board()

    if st.button("Back"):
        st.session_state.page = "home"
        st.rerun()

# ---------------- FRIENDS ----------------
def friend_page():
    st.title("👥 Add Friend")

    friend = st.text_input("Enter Username")

    if st.button("Send Request"):
        supabase.table("friends").insert({
            "sender": st.session_state.username,
            "receiver": friend,
            "status": "pending"
        }).execute()

        supabase.table("notifications").insert({
            "username": friend,
            "message": f"{st.session_state.username} sent request"
        }).execute()

        st.success("Request sent ✅")

    st.subheader("Incoming Requests")

    data = supabase.table("friends") \
        .select("*") \
        .eq("receiver", st.session_state.username) \
        .eq("status", "pending").execute()

    for req in data.data:
        st.write(req["sender"])

        if st.button(f"Accept {req['sender']}", key=req["id"]):
            supabase.table("friends") \
                .update({"status": "accepted"}) \
                .eq("id", req["id"]).execute()

    if st.button("Back"):
        st.session_state.page = "home"
        st.rerun()

# ---------------- NOTIFICATIONS ----------------
def show_notifications():
    st.subheader("🔔 Notifications")

    data = supabase.table("notifications") \
        .select("*") \
        .eq("username", st.session_state.username).execute()

    if data.data:
        for note in data.data:
            st.write(note["message"])
    else:
        st.write("No notifications")

# ---------------- LOGIN ----------------
def login_page():
    st.markdown("<h1 style='text-align:center;color:lime;'>Checkmate-Chess</h1>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align:center;color:yellow;'>Welcome!!</h1>", unsafe_allow_html=True)
    st.title("🔐 Login")

    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login"):
        result = login(username, password)

        if result == True:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.page = "home"
            st.rerun()

        elif result == "wrong_password":
            st.error("Wrong password ❌")

        else:
            st.error("Username not found ❌")

    st.write("Don't have an account?")
    if st.button("Sign up"):
        st.session_state.page = "signup"
        st.rerun()

# ---------------- SIGNUP ----------------
def signup_page():
    st.markdown("<h1 style='text-align:center;color:lime;'>Checkmate-Chess</h1>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align:center;color:yellow;'>Welcome!!</h1>", unsafe_allow_html=True)
    st.title("📝 Signup")

    username = st.text_input("Create Username", key="signup_username")
    password = st.text_input("Create Password", type="password", key="signup_password")

    if st.button("Signup"):
        result = signup(username, password)

        if result == "success":
            st.success("Account created! Please login.")

        elif result == "exists":
            st.error("Username already exists ❌")

        else:
            st.error("Something went wrong ⚠️")

    if st.button("Back to Login"):
        st.session_state.page = "login"
        st.rerun()

# ---------------- MAIN ----------------
if st.session_state.logged_in:
    if st.session_state.page == "home":
        home()
    elif st.session_state.page == "bot":
        bot_page()
    elif st.session_state.page == "friends":
        friend_page()
    else:
        home()
else:
    if st.session_state.page == "login":
        login_page()
    else:
        signup_page()
