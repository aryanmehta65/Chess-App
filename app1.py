import streamlit as st
st.markdown("<h1 style ='color:green; text-align:center;'>CHESS</h1>",
            unsafe_allow_html=True)
st.write("Login")
st.text_input("Username")
st.text_input("Password",type="password")
st.button("Login")
st.write("Dont have Account?")
st.button("Sign in")


