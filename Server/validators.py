from Server.models import User
import string
from validate_email import validate_email as email_validation
from Server.config import calculator as settings

def validate_username(username):
    """
    The function will validate username (check if he is already taken)
    :param username: username to check (str)
    :return: is the user valid or not (bool)
    """
    if any(char in string.punctuation for char in username):
        return False

    user = User.query.filter_by(username=username).first()
    return user is None


def validate_email(email):
    """
    The function will validate email (check if he is already taken, and if it is in correct format)
    :param username: username to check (str)
    :return: is the user valid or not (bool)
    """
    if not email_validation(email): # For now only checks the email format (later emaill verification will be sent)
        return False

    email = User.query.filter_by(email=email).first()
    return email is None


def validate_password(password):
    """
    This function will validate that the password fits the standards of the app
    :param password: the password to check (str)
    :return: does the password fit the standards or not (bool)
    """
    if not (settings['MIN_PASSWORD_LEN'] < len(password) < settings['MAX_PASSWORD_LEN']):
        return False
    lower = any(char.islower() for char in password)
    upper = any(char.isupper() for char in password)
    number = any(char.isdigit() for char in password)
    return lower and upper and number
