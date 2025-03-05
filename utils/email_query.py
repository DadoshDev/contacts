import smtplib
import os
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config.db_settings import execute_query


load_dotenv()

SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
FROM_EMAIL = os.getenv("FROM_EMAIL")


def send_email(email, subject, message):
    """Send email."""
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        msg = MIMEMultipart()

        msg['From'] = FROM_EMAIL
        msg['To'] = email
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))
        server.sendmail(FROM_EMAIL, email, msg.as_string())

        return True
    except Exception as e:
        print(f"Failed to send Password to: {email}. Error: {e}")
        return False
    finally:
        server.quit()


def get_user_by_email(email: str):
    try:
        query = """
            SELECT * FROM users WHERE email=%s"""
        return execute_query(query=query, params=(email,), fetch="one")
    except Exception as e:
        print(e)
        return False


def get_user_code(email: str, code: int):
    try:
        query = """
        SELECT * FROM verification_codes WHERE email=%s AND code=%s ORDER BY ID DESC"""
        return execute_query(query=query, params=(email, code,), fetch="one")
    except Exception as e:
        print(e)
        return False


def check_email_format(email):
    """Check email"""

    if "@" in email and "." in email:

        if email.count("@") == 1 and email.count(".") == 1:

            if len(email.split("@")[0]) <= 64 and len(email.split("@")[1]) <= 255:

                return True

            else:

                print("Email domain name must be between 1 and 64 characters long.")
                return False

    else:

        print("Invalid email format.")
        return False
