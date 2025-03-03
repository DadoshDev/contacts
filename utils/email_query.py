from config.db_settings import execute_query


def get_user_by_email(email: str):
    try:
        query = """
            SELECT * FROM users WHERE email=%s"""
        return execute_query(query=query, params=(email,),fetch="one")
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



    
