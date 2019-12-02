from Server.models import User

def validate_username(username):
    """
    The function will validate username (check if he is already taken)
    :param username: username to check (str)
    :return: is the user valid or not (bool)
    """
    user = User.query.filter_by(username=username).first()
    return user != None

def validate_email(email)
    """
    The function will validate email (check if he is already taken, and if it is in correct format)
    :param username: username to check (str)
    :return: is the user valid or not (bool)
    """
    email = User.query.filter_by(email=email).first()
    return email != None

    