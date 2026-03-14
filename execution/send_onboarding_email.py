import os
import sys
import smtplib
import ssl
import re
import socket
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

socket.setdefaulttimeout(30)

load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", 465))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
SMTP_FROM = os.getenv("SMTP_FROM", SMTP_USER)

EMAIL_SUBJECT = "Welcome to One Step Sol – Let's Get Started!"

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def test_smtp_connection():
    if not SMTP_HOST:
        return "SMTP_HOST not configured"
    try:
        sock = socket.create_connection((SMTP_HOST, SMTP_PORT), timeout=10)
        sock.close()
        return None
    except Exception as e:
        return str(e)

def get_email_body(name):
    greeting = name if name.strip() else "Friend"
    
    html_body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
            <h1 style="color: #2c3e50;">Welcome to One Step Sol! 🎉</h1>
            
            <p>Hi {greeting},</p>
            
            <p>We're thrilled to have you on board. Our mission is to provide you with seamless solutions that make your life easier.</p>
            
            <h3 style="color: #2c3e50;">Here's what to expect from us:</h3>
            <ul>
                <li>Personalized support tailored to your needs</li>
                <li>Quick responses to your questions</li>
                <li>Regular updates on new features and improvements</li>
            </ul>
            
            <p>If you have any questions, just reply to this email – we're here to help!</p>
            
            <hr style="border: none; border-top: 1px solid #eee; margin: 20px 0;">
            
            <p style="color: #7f8c8d; font-size: 14px;">
                Best regards,<br>
                <strong>The One Step Sol Team</strong><br>
                <a href="mailto:admin@onestepsol.com" style="color: #3498db;">admin@onestepsol.com</a>
            </p>
        </div>
    </body>
    </html>
    """
    
    plain_body = f"""
Hi {greeting},

Welcome to One Step Sol! 🎉

We're thrilled to have you on board. Our mission is to provide you with seamless solutions that make your life easier.

Here's what to expect from us:
- Personalized support tailored to your needs
- Quick responses to your questions
- Regular updates on new features and improvements

If you have any questions, just reply to this email – we're here to help!

Best regards,
The One Step Sol Team
admin@onestepsol.com
"""
    return plain_body, html_body

def send_email(name, email, max_retries=3):
    if not validate_email(email):
        raise ValueError("Invalid email format")
    
    if not all([SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS]):
        raise ValueError("SMTP credentials not configured in .env")
    
    plain_body, html_body = get_email_body(name)
    
    msg = MIMEMultipart('alternative')
    msg['From'] = str(SMTP_FROM)
    msg['To'] = email
    msg['Subject'] = EMAIL_SUBJECT
    
    msg.attach(MIMEText(plain_body, 'plain'))
    msg.attach(MIMEText(html_body, 'html'))
    
    context = ssl.create_default_context()
    
    for attempt in range(1, max_retries + 1):
        try:
            with smtplib.SMTP_SSL(str(SMTP_HOST), SMTP_PORT, context=context) as server:
                server.login(str(SMTP_USER), str(SMTP_PASS))
                server.sendmail(str(SMTP_FROM), email, msg.as_string())
            return True
        except smtplib.SMTPAuthenticationError:
            raise Exception("SMTP authentication failed")
        except Exception as e:
            if attempt == max_retries:
                raise Exception(f"SMTP connection failed after {max_retries} attempts: {str(e)}")
            import time
            time.sleep(2)
    
    return False

def main():
    if len(sys.argv) != 3:
        print("Usage: python send_onboarding_email.py \"Name\" email@example.com")
        sys.exit(1)
    
    name = sys.argv[1]
    email = sys.argv[2]
    
    try:
        send_email(name, email)
        print(f"[X] Welcome email sent successfully to {email} ({name})")
    except ValueError as e:
        print(f"[X] Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"[X] Failed to send email: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
