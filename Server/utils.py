import random
import string
from flask_mail import Message
from Server import mail, db
from Server.models import User
import datetime

PASSWORD_RESET_CODE_LEN = 6
TIMESTAMP_TO_INT = 1000000
# 60 seconds in every minute of the 30 minutes
MAX_SECONDS = 60 * 30
CHARS = string.digits + string.ascii_uppercase

def generate_random_code(user):
    """
    This function will generate the random code which the client will enter in the application and will add it to the codes dict
    :param user: the user to add the code to, in the codes dict (User)
    :return: a code to be sent to the user (str)
    """
    code = ''.join(random.choice(CHARS) for i in range(PASSWORD_RESET_CODE_LEN))
    # Even if there already exists a code for the client, a new one is generated
    user.reset_code = code
    time = int(datetime.datetime.now().timestamp() * TIMESTAMP_TO_INT)
    user.updated_time = time
    db.session.commit()
    return code

def send_reset_email(user):
    """
    The function will send reset email to user
    :param user: The user to send the maill to (User class)
    """
    code = generate_random_code(user)
    msg = Message(f'Your Password Reset Code is - {code}',
                  sender='noreply@carmelvoiceassistant.com',
                  recipients=[user.email])
    # Direct the user to the password reset route (may need to change this to open the flutter app later)
    msg.body = f'''To reset your password, please enter the following code: {code}, in the application screen in front of you.
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)

def send_email_verification(user):
    """
    The function will send email validation toeen to usre
    :param user: The user to send the mail to (User)
    """
    token = user.get_token('EMAIL_VALIDATION')
    url = f'http://localhost:5000/validate_email/{token}'
    msg = Message(f'Hey {user.username}, thanks for signing up to our application',
                    sender='noreply@carmelvoiceassistant.com',
                    recipients=[user.email])
    msg.body = f'''In order to start using our application you must click on the link below in order to activate your account:
    {url}
    '''
    mail.send(msg)
    
def verify_code(user,code):
    """
    This function will verify that a code is valid and in the correct time
    :param user: the user to check the code for (User)
    :param code: the given code from the app (int)
    :return: valid code or not (bool)
    """
    db_code = user.reset_code
    now = datetime.datetime.now()
    updated_time = datetime.datetime.fromtimestamp(user.updated_time / TIMESTAMP_TO_INT)
    delta_time = now - updated_time
    # If the code wasn't used within half an hour, remove it from the db
    if delta_time.days > 0 or delta_time.seconds > MAX_SECONDS:
        user.reset_code = None
        db.session.commit()
        return False
    # Check if the code is valid code
    return True if db_code and db_code == code else False

    
    

