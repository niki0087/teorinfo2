"""_summary_
"""
from authentication import authenticate_user, authorize_user
from database import create_database, change_password
from admin import get_all_users, delete_user_by_login, add_user

def admin_menu():
    """_summary_
    """
    while True:
        print("\nМеню администратора:")
        print("1. Вывести список пользователей")
        print("2. Удалить пользователя")
        print("3. Добавить нового пользователя")
        print("4. Сменить свой пароль")
        print("5. Выйти из учетной записи")

        choice = input("Введите номер действия: ")

        if choice == "1":
            print(get_all_users())
        elif choice == "2":
            login = input("Введите логин пользователя для удаления: ")
            delete_user_by_login(login)
        elif choice == "3":
            login = input("Введите логин нового пользователя: ")
            password = input("Введите пароль нового пользователя: ")
            user_type = input("Введите тип пользователя (1 - администратор, 2 - пользователь): ")
            add_user(login, password, user_type)
        elif choice == "4":
            login=input("Введите свой логин: ")
            new_password = input("Введите новый пароль: ")
            change_password(login, new_password)
        elif choice == "5":
            print("Выход из учетной записи.")
            break
        else:
            print("Некорректный ввод. Попробуйте снова.")
def user_menu():
    """_summary_
    """
    while True:
        print("\nМеню пользователя:")
        print("1. Сменить свой пароль")
        print("2. Выйти из программы")
        choice = input("Введите номер действия: ")
        if choice =="1":
            login=input("Введите свой логин: ")
            new_password = input("Введите новый пароль: ")
            change_password(login,new_password)
        elif choice =="2":
            break
        else:
            print("Неккоректный ввод, попробуйте снова.")


def main():
    """_summary_
    """
    create_database()
    add_user("admin", "0000", 1)

    while True:
        print("\nВыберите действие:")
        print("1. Войти")
        print("2. Зарегистрироваться")
        print("3. Выйти из программы")

        choice = input("Выберите действие: ")

        if choice == "1":
            login = input("Введите логин: ")
            password = input("Введите пароль: ")
            authenticated, user_type = authenticate_user(login, password)
            if authenticated:
                authorize_user(user_type)
                if user_type == 1:
                    admin_menu()
                elif user_type == 2:
                    user_menu()
                else:
                    print("Некорректный тип пользователя.")
            else:
                print("Ошибка аутентификации. Попробуйте снова.")
        elif choice == "2":
            login=input("Введите логин: ")
            password=input("Введите пароль: ")
            add_user(login,password,2)

        elif choice == "3":
            print("Программа завершена")
            break
        else:
            print("Некорректный ввод. Попробуйте снова.")

if __name__ == "__main__":
    main()
