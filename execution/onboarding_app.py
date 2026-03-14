import streamlit as st
import re
import sys
import os
import socket

st.set_page_config(page_title="One Step Sol - Onboarding", page_icon="🎉")

st.write("DEBUG: Starting network diagnostics...")

def diagnose_network():
    results = []
    
    results.append(f"Hostname: {socket.gethostname()}")
    results.append(f"Current working dir: {os.getcwd()}")
    
    try:
        ip = socket.gethostbyname("smtp.purelymail.com")
        results.append(f"DNS lookup smtp.purelymail.com: {ip}")
    except Exception as e:
        results.append(f"DNS lookup FAILED: {e}")
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        sock.connect(("smtp.purelymail.com", 465))
        sock.close()
        results.append("Port 465 connection: SUCCESS")
    except Exception as e:
        results.append(f"Port 465 connection: FAILED - {e}")
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        sock.connect(("smtp.purelymail.com", 587))
        sock.close()
        results.append("Port 587 connection: SUCCESS")
    except Exception as e:
        results.append(f"Port 587 connection: FAILED - {e}")
    
    return results

try:
    sys.path.insert(0, '/app/execution')
    from send_onboarding_email import send_email, test_smtp_connection
    st.write("DEBUG: Import successful!")
    
    st.write("DEBUG: Running network diagnostics...")
    diagnostics = diagnose_network()
    for d in diagnostics:
        if "FAILED" in d:
            st.error(f"DEBUG: {d}")
        else:
            st.write(f"DEBUG: {d}")
            
    st.write("DEBUG: Testing SMTP connection...")
    smtp_error = test_smtp_connection()
    if smtp_error:
        st.error(f"DEBUG - SMTP unreachable: {smtp_error}")
    else:
        st.write("DEBUG: SMTP connection OK!")
except Exception as e:
    st.error(f"DEBUG - Import failed: {str(e)}")
    send_email = None
    test_smtp_connection = None

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
