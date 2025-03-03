import hashlib
import smtplib
import random
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from utils.email_query import check_email_format, get_user_by_email, get_user_code
from utils.queries import (update_is_login, add_user, check_password_format,
                           add_code_query, update_user_status)
import threading


def send_email(email, subject, message):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'ilyosovdadahon62@gmail.com'

    smtp_password = 'gwql ptul znzf sfjx'
    from_email = 'ilyosovdadahon62@gmail.com'

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        msg = MIMEMultipart()

        msg['From'] = from_email
        msg['To'] = email
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))
        server.sendmail(from_email, email, msg.as_string())

        return True
    except Exception as e:
        print(f"Failed to send Password to: {email}. Error: {e}")
        return False
    finally:
        server.quit()


def generate_verify_code(email: str):
    new_code = random.randint(100000, 999999)

    user_code = get_user_code(email=email, code=new_code)
    if user_code:
        return generate_verify_code(email=email)

    return new_code


def verify_code(email: str) -> bool:
    code = int(input("Enter the verification code: "))

    user_code = get_user_code(email=email, code=code)
    if not user_code:
        print("Invalid verification code!")
        return register()
    current_datetime = datetime.now()
    diff = current_datetime - user_code[-1]
    minute = diff.total_seconds() // 60
    if minute > 4:
        print("Verification code expired!")
        return False
    update_user_status(email=email, status=1)
    print("Registration successful!")
    return True


def register():

    """Register a new user"""
    print("Register")

    full_name = input("Enter your full name: ")

    email = input("Enter email: ")

    if not check_email_format(email):
        return register()

    password = input("Enter password: ")

    if not check_password_format(password):
        return register()

    confirm_password = input("Confirm your password: ")

    if password != confirm_password:
        print("Passwords do not match!")
        return register()

    if get_user_by_email(email=email):
        print("Email already exists!")
        return False

    code = generate_verify_code(email=email)

    add_code_query(email=email, code=code)
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    add_user(full_name=full_name, email=email, password=hashed_password)
    subject = "Verification code from Contacts!"
    body = f"Your verification code {code}."
    email_thread = threading.Thread(target=send_email, args=(email, subject, body))
    email_thread.start()

    return verify_code(email)


def login():

    email = input("Enter your email address: ")
    password = input("Enter your password: ")

    user = get_user_by_email(email=email)
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    if user[3] == hashed_password and user[-1] == 1:
        update_is_login(user_id=user[0], status=1)
        return user[0]
    else:
        print("Invalid email or password!")
        return False
