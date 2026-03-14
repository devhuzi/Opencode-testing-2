import streamlit as st
import subprocess
import re
import os

st.set_page_config(page_title="One Step Sol - Onboarding", page_icon="🎉")

st.title("Welcome to One Step Sol!")
st.write("Please fill in your details to get started.")

with st.form("onboarding_form"):
    name = st.text_input("Full Name", placeholder="John Doe")
    email = st.text_input("Email Address", placeholder="john@example.com")
    submitted = st.form_submit_button("Get Started")

if submitted:
    if not name.strip():
        st.error("Please enter your name.")
    elif not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
        st.error("Please enter a valid email address.")
    else:
        try:
            result = subprocess.run(
                ["python", "execution/send_onboarding_email.py", name, email],
                capture_output=True,
                text=True,
                cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            )
            if result.returncode == 0:
                st.success(f"Welcome email sent to {email}! 🎉")
            else:
                st.error(f"Failed to send email: {result.stderr}")
        except Exception as e:
            st.error(f"Error: {e}")
