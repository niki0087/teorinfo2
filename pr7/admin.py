"""_summary_

    Returns:
        _type_: _description_
"""
import sqlite3
from database import hash_password, DB_PATH

def add_user(login, password, utype_id):
    """_summary_

    Args:
        login (_type_): _description_
        password (_type_): _description_
        utype_id (_type_): _description_
    """
    hashed_password = hash_password(password)
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        cursor.execute("INSERT INTO Users (login, password, utype_id) VALUES (?,?,?);",
                       (login, hashed_password, utype_id))
        connection.commit()
        cursor.close()
        print("Пользователь добавлен в базу данных")
    except sqlite3.Error as error:
        print("Ошибка при добавлении пользователя:", error)
    finally:
        if connection:
            connection.close()

def get_all_users():
    """_summary_

    Returns:
        _type_: _description_
    """
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute("SELECT login FROM Users")
    all_user=cursor.fetchall()
    cursor.close()
    return all_user

def delete_user_by_login(login):
    """_summary_

    Args:
        login (_type_): _description_
    """
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        cursor.execute("DELETE FROM Users WHERE login=?", (login,))
        connection.commit()
        cursor.close()
        print("Пользователь удален из базы данных")
    except sqlite3.Error as error:
        print("Ошибка при удалении пользователя:", error)
    finally:
        if connection:
            connection.close()
