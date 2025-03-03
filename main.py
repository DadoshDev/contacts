from auth.auth import login, register
from config.menu import user_menu, auth_menu
from utils.queries import (create_tables, logout_query, get_self_info, add_contact, get_all_contacts, edit_contact,
                           edit_fullname, delete_contact, log_out)
print("\n     Contact ")


def show_auth_menu():
    print(auth_menu)
    choice = input("Select from menu: ")

    if choice == "1":
        user_id = login()
        show_user_menu(user_id)

    elif choice == "2":
        register()

    elif choice == "3":
        print("See you later.")
        quit()

    else:
        print("Invalid choice !")
    return show_auth_menu()


def show_user_menu(user_id):
    print(user_menu)
    choice = input("Select from menu: ")
    if choice == "1":
        result = get_self_info(user_id)

        if result:
            print("\nSelf information \n")
            print(f"Full name: {result[1]}\n"
                  f"email: {result[2]}.\n")
            return show_user_menu(user_id)

    elif choice == "2":
        edit_fullname()
        return show_user_menu(user_id)

    elif choice == "3":
        add_contact(user_id)
        return show_user_menu(user_id)

    elif choice == "4":
        get_all_contacts(user_id)
        return show_user_menu(user_id)

    elif choice == "5":
        delete_contact(user_id)
        return show_user_menu(user_id)

    elif choice == "6":
        edit_contact(user_id)
        return show_user_menu(user_id)

    # elif choice == "7":
    #     contact_search(user_id)
    #     return show_user_menu(user_id)

    elif choice == "7":
        print("Logging out...")
        log_out(user_id)

    else:
        print("Invalid input! Please try again.")
        return show_user_menu(id)


if __name__ == "__main__":
    create_tables()
    logout_query()
    show_auth_menu()
