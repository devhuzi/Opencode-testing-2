import streamlit as st
import re
import sys
import os

st.set_page_config(page_title="One Step Sol - Onboarding", page_icon="🎉")

st.write("DEBUG: Starting app...")

try:
    sys.path.insert(0, '/app/execution')
    from send_onboarding_email import send_email
    st.write("DEBUG: Import successful!")
except Exception as e:
    st.error(f"DEBUG - Import failed: {str(e)}")
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
        st.error("Email function not available. Check import error above.")
    else:
        try:
            st.write(f"DEBUG: Sending email to {email}...")
            send_email(name, email)
            st.success(f"Welcome email sent to {email}! 🎉")
        except Exception as e:
            st.error(f"DEBUG - Send failed: {str(e)}")
            print(f"ERROR sending email: {str(e)}", flush=True)
