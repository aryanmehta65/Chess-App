import streamlit as st
st.markdown("<h1 style ='color:lime; text-align:center;'>Checkmate-Chess</h1>",
            unsafe_allow_html=True)
st.markdown("<h1 style ='color:yellow; text-align:center;'>Welcome!!</h1>",
            unsafe_allow_html=True)
st.write("Login")
st.text_input("Username")
st.text_input("Password",type="password")
st.button("Login")
st.write("Dont have Account?")
st.button("Sign in")


