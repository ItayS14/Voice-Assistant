import random
import string
from flask_mail import Message
from Server import mail, db, app
from Server.db_models import User
import datetime
from Server.config import ProtocolErrors
from flask import request, jsonify, url_for
from functools import wraps
from flask_login import login_required, current_user
import os


def validate_params(*params, get):
    """
    Decorator that validate flask params
    :param *params: every param to validate (list)
    :param get: is it get or post request (bool)
    """
    def _validate_params(fnc):
        @wraps(fnc)
        def wrapper(*args, **kwargs):
            params_to_fnc = [request.args.get(param) if get else request.form.get(param) for param in params]
            if None in params_to_fnc:
                return jsonify([False, ProtocolErrors.INVALID_PARAMETERS.value])
            return fnc(*args, *params_to_fnc, **kwargs)
        return wrapper
    return _validate_params


def activated_required(fnc):
    """
    Decorator that require the user to be login and activated
    """
    @login_required
    @wraps(fnc)
    def wrapper(*args, **kwargs):
        if not current_user.confirmed:
            return jsonify([False, ProtocolErrors.USER_IS_NOT_ACTIVE.value])
        return fnc(*args, **kwargs)
    return wrapper


class Utils:
    chars_for_code = string.digits + string.ascii_uppercase
    
    def __init__(self, code_len, max_seconds, pic_url):
        self._code_len = code_len
        self._max_seconds = max_seconds
        self._pic_url = pic_url

    def send_reset_email(self, user):
        """
        The function will send reset email to user
        :param user: The user to send the maill to (User class)
        """
        code = self._generate_random_code(user)
        title = f'Your Password Reset Code is - {code}'
        body = f'''To reset your password, please enter the following code: {code}, in the application screen in front of you.
    If you did not make this request then simply ignore this email and no changes will be made.
    '''
        Utils._send_mail(title, body, user)

    @staticmethod
    def send_email_verification(user):
        """
        The function will send email validation toeen to usre
        :param user: The user to send the mail to (User)
        """
        token = user.get_token('EMAIL_VALIDATION')
        url =  url_for('validate_email', token=token, _external=True) 
        title = f'Hey {user.username}, thanks for signing up to our application'
        body = f'''In order to start using our application you must click on the link below in order to activate your account:
        {url}
        '''
        Utils._send_mail(title, body, user)

    def verify_code(self, user, code):
        """
        This function will verify that a code is valid and in the correct time
        :param user: the user to check the code for (User)
        :param code: the given code from the app (int)
        :return: valid code or not (bool)
        """
        db_code = user.reset_code
        now = datetime.datetime.now()
        updated_time = datetime.datetime.fromtimestamp(user.updated_time)
        delta_time = now - updated_time
        # If the code wasn't used within half an hour, remove it from the db
        if delta_time.days > 0 or delta_time.seconds > self._max_seconds:
            user.reset_code = None
            db.session.commit()
            return False
        # Check if the code is valid code
        return True if db_code and db_code == code else False

    def _generate_random_code(self, user):
        """
        This function will generate the random code which the client will enter in the application and will add it to the codes dict
        :param user: the user to add the code to, in the codes dict (User)
        :return: a code to be sent to the user (str)
        """
        code = ''.join(random.sample(Utils.chars_for_code, self._code_len))
        # Even if there already exists a code for the client, a new one is generated
        user.reset_code = code
        time = datetime.datetime.now().timestamp()
        user.updated_time = time
        db.session.commit()
        return code

    @staticmethod
    def _send_mail(subject, body, user):
        """
        This function will send a mail to a user with a specified body and title
        :param subject: the title of the mail to be sent (str)
        :param body: the body/message of the mail to be sent (str)
        :param user: the user to send the mail to (User)
        :return: None
        """
        msg = Message(
            subject,
            sender = 'noreply@carmelvoiceassistant.com',
            recipients=[user.email],
            body=body)
        mail.send(msg)

    def save_picture(self, file_name, content):
        """
        The function will save image to the server (image name would be the current_user username)
        :param file_name: the file name on the client (need it for the extenstion) - str
        :param content: the content to save - bytes
        :return: file name of the saved picture
        """
        _, ext = os.path.splitext(file_name)
        file_name = current_user.username + ext
        path = os.path.join(app.root_path, self._pic_url, file_name)
        with open(path, 'wb') as f:
            f.write(content)
        return file_name