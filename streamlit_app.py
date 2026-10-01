import pandas as pd
import streamlit as st
import os

st.set_page_config(
    page_title="MERA MITWA Portal",
    page_icon="🚗",
    layout="wide"
)

st.title("🚗 MERA MITWA Portal")
st.write("Welcome to your mobile Streamlit application!")

# Simple login test
username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    if username == "admin" and password == "mitwa2026":
        st.success("Login Successful!")
    else:
        st.error("Invalid credentials. Try admin / mitwa2026")
