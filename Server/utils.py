import random
import string
from flask_mail import Message
from Server import mail, codes_dict

PASSWORD_RESET_CODE_LEN = 6
CHARS = string.digits + string.ascii_uppercase

def generate_random_code(user):
    """
    This function will generate the random code which the client will enter in the application and will add it to the codes dict
    :param user: the user to add the code to, in the codes dict (User)
    :return: a code to be sent to the user (str)
    """
    code = ''.join(random.choice(CHARS) for i in range(PASSWORD_RESET_CODE_LEN))
    # Even if there already exists a code for the client, a new one is generated
    codes_dict[user.email] = code
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
    

