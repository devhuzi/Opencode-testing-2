import streamlit as st
import re
import sys
import os

st.set_page_config(page_title="One Step Sol - Onboarding", page_icon="🎉")

try:
    sys.path.insert(0, '/app/execution')
    from send_onboarding_email import send_email, test_smtp_connection
except Exception as e:
    st.error(f"Import failed: {str(e)}")
    send_email = None

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
    elif send_email is None:
        st.error("Email function not available.")
    else:
        try:
            send_email(name, email)
            st.success(f"Welcome email sent to {email}! 🎉")
        except Exception as e:
            st.error(f"Failed to send email: {str(e)}")
