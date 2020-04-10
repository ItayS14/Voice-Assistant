import random
import string
from flask_mail import Message
from Server import mail, db
from Server.db_models import User
import datetime
import sqlalchemy as sqla
import Server.config



class Utils:
    chars_for_code = string.digits + string.ascii_uppercase
    
    def __init__(self, code_len, max_seconds):
        self._code_len = code_len
        self._max_seconds = max_seconds

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
        url = f'http://localhost:5000/validate_email/{token}'
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


