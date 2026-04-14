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
st.button("Login")
col1,col2=st.columns([1,0.05])
with col1:
            st.write("Dont have Account?")
with col2:
            st.button("Sign in")



