import streamlit as st
st.set_page_config(
            page_title="Checkmate-Chess",
            page_icon="logo.jpeg")
st.markdown("<h1 style ='color:lime; text-align:center;'>Checkmate-Chess</h1>",
            unsafe_allow_html=True)
st.markdown("<h1 style ='color:yellow; text-align:center;'>Welcome!!</h1>",
            unsafe_allow_html=True)
st.header("Login")
st.text_input("Username")
st.text_input("Password",type="password")
if st.button("Login"):
            st.write("logged in successfully!")
st.write("Dont have Account?")
if st.button("Sign in"):
            with st.form("login_form"):
            email=st.text_input("Email")
            username=st.text_input("Create Username")
            pasword=st.text_input("Create Password",type="password")
            submit=st.form_submit_buttot("Sign in")
            if submit:
                        st.success(f"Welcome{username}")


