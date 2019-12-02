from Server.models import User
import re

MAX_LEN = 32
MIN_LEN = 8


def validate_username(username):
    """
    The function will validate username (check if he is already taken)
    :param username: username to check (str)
    :return: is the user valid or not (bool)
    """
    # TODO: check that the username does not contain any symbols
    user = User.query.filter_by(username=username).first()
    return user != None


def validate_email(email):
    """
    The function will validate email (check if he is already taken, and if it is in correct format)
    :param username: username to check (str)
    :return: is the user valid or not (bool)
    """
    # TODO: check that the email is a vaild email address
    email = User.query.filter_by(email=email).first()
    return email != None


def validate_password(password):
    """
    This function will validate that the password fits the standards of the app
    :param password: the password to check (str)
    :return: does the password fit the standards or not (bool)
    """
    if len(password) > MAX_LEN or len(password) < MIN_LEN:
        return False
    lower = any(char.islower() for char in password)
    upper = any(char.isupper() for char in password)
    number = any(char.isdigit() for char in password)
    return lower and upper and number
