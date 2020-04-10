from Server.db_models import User
import string
from validate_email import validate_email 

class Validators:
    def __init__(self, max_password_len, min_password_len):
        self._max_password_len = max_password_len
        self._min_password_len = min_password_len
        
    @staticmethod
    def username(username):
        """
        The function will validate username (check if he is already taken)
        :param username: username to check (str)
        :return: is the user valid or not (bool)
        """
        if any(char in string.punctuation for char in username):
            return False

        user = User.query.filter_by(username=username).first()
        return user is None

    @staticmethod
    def email(email):
        """
        The function will validate email (check if he is already taken, and if it is in correct format)
        :param username: username to check (str)
        :return: is the user valid or not (bool)
        """
        if not validate_email(email): # For now only checks the email format (later emaill verification will be sent)
            return False
            
        email = User.query.filter_by(email=email).first()
        return email is None

    def password(self, password):
        """
        This function will validate that the password fits the standards of the app
        :param password: the password to check (str)
        :return: does the password fit the standards or not (bool)
        """
        if not (self._min_password_len < len(password) < self._max_password_len):
            return False
        lower = any(char.islower() for char in password)
        upper = any(char.isupper() for char in password)
        number = any(char.isdigit() for char in password)
        return lower and upper and number
