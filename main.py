from auth.auth import login, register
from config.menu import user_menu, auth_menu, admin_menu
from utils.queries import (create_tables, logout_query, get_self_info, add_contact, get_all_contacts, edit_contact,
                           edit_fullname, delete_contact, log_out, view_all_users, view_all_contacts, get_active_users,
                           send_massage_admin)
print("\n     Contact ")


def show_auth_menu():
    print(auth_menu)
    choice = input("Select from menu: ")

    if choice == "1":
        email = input("Enter your email address: ")
        password = input("Enter your password: ")

        if email == 'admin' and password == 'admin':
            return show_admin_menu()

        user_id = login(email, password)
        if user_id:
            return show_user_menu(user_id)

    elif choice == "2":
        register()

    elif choice == "3":
        print("See you later.")
        quit()

    else:
        print("Invalid choice !")
    return show_auth_menu()


def show_user_menu(user_id):
    while True:
        print(user_menu)
        choice = input("Select from menu: ")
        if choice == "1":
            result = get_self_info(user_id)

            if result:
                print("\nSelf information \n")
                print(f"Full name: {result[1]}\n"
                      f"email: {result[2]}.\n")

        elif choice == "2":
            edit_fullname()

        elif choice == "3":
            add_contact(user_id)

        elif choice == "4":
            get_all_contacts(user_id)

        elif choice == "5":
            delete_contact(user_id)

        elif choice == "6":
            edit_contact(user_id)

        elif choice == "7":
            print("Logging out...")
            log_out(user_id)
            break

        else:
            print("Invalid input! Please try again.")


def show_admin_menu():
    while True:
        print(admin_menu)
        choice = input("Select from menu: ")

        if choice == "1":
            view_all_users()
        elif choice == "2":
            view_all_contacts()
        elif choice == "3":
            get_active_users()
        elif choice == "4":
            send_massage_admin()
        elif choice == "5":
            print("Logging out...")
            break  # Tsikldan chiqish
        else:
            print("Invalid input! Please try again.")


if __name__ == "__main__":
    create_tables()
    logout_query()
    show_auth_menu()
