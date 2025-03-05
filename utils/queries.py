import hashlib

from auth.auth import send_email
from config.db_settings import execute_query
from utils.email_query import get_user_by_email


def create_tables() -> None:
    users = """CREATE TABLE IF NOT EXISTS users(
                id SERIAL PRIMARY KEY,
                full_name VARCHAR(32),
                email VARCHAR(32) UNIQUE NOT NULL,
                password VARCHAR(256),
                is_login SMALLINT NOT NULL DEFAULT 0,
                status SMALLINT NOT NULL DEFAULT 0
                )"""

    contacts = """ CREATE TABLE IF  NOT EXISTS contacts(
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id),
                fUll_name varchar(32) NOT NULL,
                email VARCHAR(32) UNIQUE NOT NULL,
                phone_number VARCHAR(15),
                status BOOLEAN, 
                created_at TIMESTAMP DEFAULT current_timestamp)"""

    verification_codes = """ 
                CREATE TABLE IF NOT EXISTS verification_codes(
                id SERIAL PRIMARY KEY,
                email VARCHAR(32) NOT NULL,
                code INT NOT NULL,
                created_at TIMESTAMP DEFAULT current_timestamp)
                 """

    try:
        execute_query(query=users)
        execute_query(query=contacts)
        execute_query(query=verification_codes)
        print("All tables created successfully.")

    except Exception as e:
        print(f"Failed to create tables. Error: {e}")


def check_password_format(password):
    """Check password"""

    if (8 <= len(password) <= 20 and any(char.isdigit() for char in password)
            and any(char.isalpha() for char in password) and any(char.islower() for char in password)
            and any(char.isupper() for char in password)):

        return True
    else:
        print("Password must be between 8 and 20 characters long.\n"
              "Contains at least one uppercase letter, one lowercase letter,\n"
              "one digit, and one special character.")
        return False


def add_code_query(email, code):
    try:
        query = """
        INSERT INTO verification_codes (email, code) VALUES (%s, %s);
        """
        params = (email, code)
        execute_query(query=query, params=params)
        print("Verification code sent successfully!")
        return True
    except Exception as e:
        print(f"Failed to add verification code. Error: {e}")
        return False


def update_is_login(status: int, user_id: int):
    try:
        query = """
        UPDATE users SET is_login = %s WHERE id = %s"""
        execute_query(query=query, params=(status, user_id,))
        return True
    except Exception as e:
        print(e)
        return False


def logout_query():
    try:
        query = """
        UPDATE users SET is_login = %s WHERE is_login = %s
        """
        execute_query(query=query, params=(0, 1,))
        return True
    except Exception as e:
        print(e)
        return False


def add_user(full_name: str, email: str, password: str):
    """Add a new user to the database."""
    try:
        query = """
        INSERT INTO users (full_name, email, password) VALUES (%s, %s, %s)
        """
        params = (full_name, email, password)
        execute_query(query=query, params=params)
        return True
    except Exception as e:
        print(f"Failed to add user. Error: {e}")


def update_user_status(email: str, status: int):
    try:
        query = """
        UPDATE users SET status = %s WHERE email = %s"""
        execute_query(query=query, params=(status, email,))
        return True
    except Exception as e:
        print(e)
        return False


def get_self_info(user_id):
    """View user's own information.""""'"

    query = "SELECT * FROM users WHERE id = %s "
    params = (user_id,)
    user_info = execute_query(query, params, "one")

    return user_info


def edit_fullname():
    """Update user's own information."""
    try:

        full_name = input("Enter new full name (leave blank to keep the same): ")
        f_n = True  # full name is true for do update
        if full_name == "":
            f_n = False  # full name is false for do not update

        if f_n:
            email = input("Enter your email address: ")
            password = input("Enter your current password: ")
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            user = get_user_by_email(email=email)

            if user[3] == hashed_password and user[-1] == 1:
                print("Password is correct.")
                update_query = """UPDATE Users SET full_name = %s WHERE id = %s """
                params = (full_name, user[0])
                execute_query(query=update_query, params=params,)
                print("Your information updated successfully.")
                return True

            else:
                print("Password is incorrect or user is not active.")
                return False

        else:
            print("Your information not updated.")
            return False

    except Exception as e:
        print(e)
        return False


def name_validate(name):
    """Check name"""
    if name.isalpha() and not name.isnumeric():
        return True
    else:
        print("Invalid name format. Name should only contain letters.")
        return False


def check_email_format(email):
    """Check email"""
    if "@" in email and "." in email:

        if email.count("@") == 1 and email.count(".") == 1:

            return True

        else:

            print("Invalid email format. Email should contain exactly one '@' symbol and one '.' symbol.")
            return False

    else:

        print("Invalid email format. Email should contain at least one '@' symbol and one '.' symbol.")
        return False


def check_phone_number(phone_number):
    """Check phone number"""
    if len(phone_number) == 13 and phone_number[0] == "+":
        return True
    else:
        print("Invalid phone number format. Phone number should start with '+' and have 12 digits.")
        return False


def add_contact(user_id) -> bool:
    """Add a new contact to the database."""
    try:
        name = input("Enter contact's name: ")
        name_validate(name)
        email = input("Enter contact's email: ")
        check_email_format(email)
        phone = input("Enter contact's phone: ")
        check_phone_number(phone)
        status = True
        add_contact_query = """INSERT INTO contacts (user_id, full_name, email, phone_number, status) VALUES 
        (%s, %s, %s, %s, %s)"""
        params = (user_id, name, email, phone, status)
        execute_query(query=add_contact_query, params=params)
        print("Contact added successfully!")
        return True

    except Exception as e:
        print(f"Failed to add contact. Error: {e}")
        return False


def get_contact(user_id: int, contact_id: int) -> bool:
    """Get a single contact from the database."""
    try:
        query = "SELECT * FROM contacts WHERE id = %s AND user_id = %s AND status = %s"
        status = True
        params = (contact_id, user_id, status)
        contact = execute_query(query=query, params=params, fetch="one")
        if contact:
            print(f"\nId: {contact[0]},\n"
                  f"Name: {contact[2]},\n"
                  f"Email: {contact[3]},\n"
                  f"Phone: {contact[4]}.\n")
            return True
        else:
            print("Contact not found.")
            return False

    except Exception as e:
        print(f"Failed to get contact. Error: {e}")
        return False


def get_all_contacts(user_id) -> bool:
    """ Get user's contacts from database."""
    try:
        query = "SELECT * FROM contacts WHERE user_id = %s AND status = %s"
        status = True
        params = (user_id, status)
        contacts = execute_query(query=query, params=params, fetch="all")
        if contacts:
            print("\nContacts:\n")
            for contact in contacts:
                print(f"\nId: {contact[0]},\n"
                      f"Name: {contact[2]},\n"
                      f"Email: {contact[3]},\n"
                      f"Phone: {contact[4]}.\n")
            return True
        else:
            print("No contacts found.")
            return False

    except Exception as e:
        print(f"Failed to get all contacts. Error: {e}")
        return False


def delete_contact(user_id) -> bool:
    """Delete a contact ."""
    try:
        contact_id = int(input("Enter contact's ID: "))
        if get_contact(user_id, contact_id=contact_id):
            status = False  # 0 - deleted, 1 - active
            query = "UPDATE contacts SET status = %s WHERE id = %s AND user_id = %s"
            params = (status, contact_id, user_id)
            execute_query(query=query, params=params)
            print("Contact deleted successfully!")
            return True
        else:
            return False

    except Exception as e:
        print(f"Failed to delete contact. Error: {e}")
        return False


def edit_name(user_id, contact_id):
    """Edit contact's name."""
    new_name = input("Enter new name: ")
    name_validate(new_name)
    query = "UPDATE contacts SET full_name = %s WHERE id = %s AND user_id = %s"
    params = (new_name, contact_id, user_id)
    execute_query(query=query, params=params)
    print("Name updated successfully!")


def edit_email(user_id, contact_id):
    """Edit contact's email."""
    new_email = input("Enter new email: ")
    check_email_format(new_email)
    query = "UPDATE contacts SET email = %s WHERE id = %s AND user_id = %s"
    params = (new_email, contact_id, user_id)
    execute_query(query=query, params=params)
    print("Email updated successfully!")


def edit_phone(user_id, contact_id):
    """Edit contact's phone number."""
    new_phone = input("Enter new phone: ")
    check_phone_number(new_phone)
    query = "UPDATE contacts SET phone_number = %s WHERE id = %s AND user_id = %s"
    params = (new_phone, contact_id, user_id)
    execute_query(query=query, params=params)
    print("Phone updated successfully!")


def edit_contact(user_id):
    """Edit a contact from the database."""
    try:
        contact_id = int(input("Enter contact's ID: "))
        if get_contact(user_id, contact_id=contact_id):
            edit_option = input("Choose an option:\n1. Name\n2. Email\n3. Phone\n")
            if edit_option == "1":
                edit_name(user_id, contact_id)
                return True  # Exit the function if name editing is done
            elif edit_option == "2":
                edit_email(user_id, contact_id)
                return True  # Exit the function if email editing is done
            elif edit_option == "3":
                edit_phone(user_id, contact_id)
                return True
            else:
                print("Invalid option.")
        else:
            return False

    except Exception as e:
        print(f"Failed to edit contact. Error: {e}")
        return False


def log_out(user_id):
    try:
        query = """
        UPDATE users SET is_login = %s WHERE user_id = %s
        """
        execute_query(query=query, params=(0, user_id,))
        return True
    except Exception as e:
        print(e)
        return False


def view_all_users():
    """View all users."""
    try:
        query = "SELECT * FROM users"
        users = execute_query(query=query, fetch="all")
        if users:
            print("\nUsers:\n")
            for user in users:
                print(f"\nUser ID: {user[0]},\n"
                      f"Username: {user[1]},\n"
                      f"Password: {user[3]},\n"
                      f"Email: {user[2]},\n"
                      f"Status: {user[5]}\n")
            return True
        else:
            print("No users found.")
            return False

    except Exception as e:
        print(f"Failed to get all users. Error: {e}")
        return False


def view_all_contacts() -> bool:
    """ Get user's contacts from database."""
    try:
        query = "SELECT * FROM contacts"
        status = True
        params = (status,)
        contacts = execute_query(query=query, params=params, fetch="all")
        if contacts:
            print("\nContacts:\n")
            for contact in contacts:
                print(f"\nId: {contact[0]},\n"
                      f"Name: {contact[2]},\n"
                      f"Email: {contact[3]},\n"
                      f"Phone: {contact[4]}.\n"
                      f"Status: {contact[5]}\n")
            return True
        else:
            print("No contacts found.")
            return False

    except Exception as e:
        print(f"Failed to get all contacts. Error: {e}")
        return False


def get_active_users():
    """ Get active users."""
    try:
        query = """
            SELECT * FROM users Where is_login = %s"""
        users = execute_query(query=query, params=(1,), fetch="all")
        if users:
            print("\nUsers:\n")
            for user in users:
                print(f"\nUser ID: {user[0]},\n"
                      f"Username: {user[1]},\n"
                      f"Password: {user[3]},\n"
                      f"Email: {user[2]},\n"
                      f"Status: {user[5]}\n")
            return True
        else:
            print("No users found.")
            return False
    except Exception as e:
        print(e)
        return False


def send_massage_admin():
    """ """
    choice = input("Do you want to send the message to everyone (y/n)? ")
    if choice.lower() == 'y':
        subject = input("Enter subject: ")
        massage = input("Enter massage: ")
        return send_massage_all(subject, massage)
    elif choice.lower() == 'n':
        email = input("Enter user's email: ")
        subject = input("Enter subject: ")
        massage = input("Enter massage: ")
        return send_massage_one(email, subject, massage)
    else:
        print("Invalid option. Please try again.")
        return False


def send_massage_all(subject: str, massage: str) -> bool:
    try:
        query = """ SELECT email FROM users"""
        emails = execute_query(query=query, fetch="all")
        if emails:
            for user in emails:
                send_email(user[0], subject, massage)
            print("Massage sent successfully to all users!")
            return True
        else:
            print("No users found.")
            return False

    except Exception as e:
        print(f"Failed to send massage to all users. Error: {e}")
        return False


def send_massage_one(email, subject, massage):
    try:
        query = """SELECT EXISTS(SELECT 1 FROM users WHERE email = %s)"""
        res = execute_query(query=query, params=(email,), fetch="one")
        if res:
            send_email(email, subject, massage)
            print(f"Massage sent successfully to {email}!")
            return True
        else:
            print("User not found.")
            return False

    except Exception as e:
        print(f"Failed to send massage to user. Error: {e}")
        return False
