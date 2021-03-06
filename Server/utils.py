import random
import string
from flask_mail import Message
from Server import mail, db, app
from Server.db_models import User
import datetime
from Server.config import ProtocolErrors
from flask import request, jsonify, url_for, render_template
from functools import wraps
from flask_login import login_required, current_user
import os
import uuid


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
                return jsonify([False, ProtocolErrors.INVALID_PARAMETERS])
            return fnc(*params_to_fnc, **kwargs)
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
            return jsonify([False, ProtocolErrors.USER_IS_NOT_ACTIVE])
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
        self._generate_random_code(user)
        Utils._send_mail(
            'Here is your reset password code', 
            'otp_template.html',
            user.email, 
            user=user
        )

    @staticmethod
    def send_email_verification(user):
        """
        The function will send email validation toeen to usre
        :param user: The user to send the mail to (User)
        """
        Utils._send_mail(
            'Thanks for signing up to our Voice Asistant app',
            'email_validation.html',
            user.email,
            token= user.get_token('EMAIL_VALIDATION'),
            user= user
        )

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
        """
        code = ''.join(random.sample(Utils.chars_for_code, self._code_len))
        # Even if there already exists a code for the client, a new one is generated
        user.reset_code = code
        time = datetime.datetime.now().timestamp()
        user.updated_time = time
        db.session.commit()

    @staticmethod
    def _send_mail(subject, html, to, **kwargs):
        """
        This function will send a mail to a user with a specified body and title
        :param subject: the title of the mail to be sent (str)
        :param html: the path to the html file to render (str)
        :param to: the recipient (str)
        :param **kwargs: any keyword argument
        """
        print(kwargs['user'])
        msg = Message(
            subject,
            sender = 'noreply@carmelvoiceassistant.com',
            recipients=[to],
            html = render_template(html, **kwargs)
        )
        mail.send(msg)

    def save_picture(self, file_name, content):
        """
        The function will save image to the server (image name would be the current_user username)
        :param file_name: the file name on the client (need it for the extenstion) - str
        :param content: the content to save - bytes
        :return: file name of the saved picture
        """
        _, ext = os.path.splitext(file_name)
        new_file_name = str(uuid.uuid1()) + ext

        # Removing old picture from the server to save space
        if current_user.profile_image != 'default.jpg': 
            os.remove(os.path.join(app.root_path, self._pic_url, current_user.profile_image))

        print('Saving', new_file_name)
        path = os.path.join(app.root_path, self._pic_url, new_file_name)
        with open(path, 'wb') as f:
            f.write(content)
        return new_file_name