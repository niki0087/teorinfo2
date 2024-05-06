"""_summary_

    Returns:
        _type_: _description_
"""
from database import get_user_by_login, hash_password

def authenticate_user(login, password):
    """_summary_

    Args:
        login (_type_): _description_
        password (_type_): _description_

    Returns:
        _type_: _description_
    """
    user = get_user_by_login(login)
    if user:
        hashed_password = hash_password(password)
        if user[2] == hashed_password:
            return True, user[3]
    return False, None

def authorize_user(user_type):
    """_summary_

    Args:
        user_type (_type_): _description_

    Returns:
        _type_: _description_
    """
    if user_type == 1:
        return "Авторизация с правами администратора."
    elif user_type == 2:
        return "Авторизация с правами пользователя."
    else:
        return "Некорректный тип пользователя."
    