from Server import app, db, bcrypt, ProtocolErrors, mail
from flask import request, jsonify, url_for
from Server.models import User
from flask_login import login_user, current_user, logout_user, login_required
from Server.validators import *
from flask_mail import Message
import Server.internet_scrappers as internet_scrappers
from Server.calculator import calculate


@app.route('/register', methods=['POST'])
def register():
    if current_user.is_authenticated:
        return jsonify([False, ProtocolErrors.USER_ALREADY_LOGGED_ERROR.value])

    username = request.form.get('username')
    password = request.form.get('password')
    email = request.form.get('email')
    if not (username and email and password):
        return jsonify([False, ProtocolErrors.INVALID_PARAMETERS_ERROR.value])

    if validate_username(username) and validate_email(email) and validate_password(password):
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return jsonify([True, {}])

    # add custom error msg later
    return jsonify([False, ProtocolErrors.PARAMETERS_DO_NOT_MATCH_REQUIREMENTS.value])


@app.route('/login', methods=['POST'])
def login():
    if current_user.is_authenticated:
        return jsonify([False, ProtocolErrors.USER_ALREADY_LOGGED_ERROR.value])

    auth = request.form.get('auth')
    password = request.form.get('password')
    if not (auth and password):
        return jsonify([False, ProtocolErrors.INVALID_PARAMETERS_ERROR.value])

    # Checking for both options (username validation or email validation)
    user = User.query.filter_by(email=auth).first()
    if not user:
        user = User.query.filter_by(username=auth).first()

    if user and bcrypt.check_password_hash(user.password, password):
        # Login user using flask-login function
        login_user(user)  # Not sure how to use the remember argument
        return jsonify([True, {}])

    return jsonify([False, ProtocolErrors.INVALID_CREDENTIALS_ERROR.value])


@app.route('/logout')
@login_required
def logout():
    # A flask-login function that disconnects the user
    logout_user()
    return jsonify([True, {}])


def send_reset_email(user):
    """
    The function will send reset email to user
    :param user: The user to send the maill to (User class)
    """
    token = user.get_token('PASSWORD_RESET')
    msg = Message('Password Reset Request',
                  sender='noreply@carmelvoiceassistant.com',
                  recipients=[user.email])
    # Direct the user to the password reset route (may need to change this to open the flutter app later)
    msg.body = f'''To reset your password, visit the following link:
{url_for('password_reset', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)


@app.route("/get_password_reset_token", methods=['POST'])
def get_password_reset_token():
    # May need to add support for password change later
    if current_user.is_authenticated:
        return jsonify([False, ProtocolErrors.USER_ALREADY_LOGGED_ERROR.value])
   
    email = request.form.get('email')
    if not email:
        return jsonify([False, ProtocolErrors.INVALID_PARAMETERS_ERROR.value])

    user = User.query.filter_by(email=email).first()
    if user is None:
        return jsonify([False, ProtocolErrors.INVALID_PARAMETERS_ERROR.value])

    send_reset_email(user)
    return jsonify([True, {}])


@app.route('/password_reset/<token>', methods=['POST'])
def password_reset(token):
    # May need to add support for password change later
    if current_user.is_authenticated:
        return jsonify([False, ProtocolErrors.USER_ALREADY_LOGGED_ERROR.value])

    new_password = request.form.get('password')
    if not new_password:
        return jsonify([False, ProtocolErrors.INVALID_PARAMETERS_ERROR.value])

    user = User.verify_token(token, 'PASSWORD_RESET')
    if user is None:
        return jsonify([False, ProtocolErrors.INVALID_TOKEN.value])

    # Make sure that password is strong enough and create new hash
    if validate_password(new_password):
        hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        return jsonify([True, {}])
        
    return jsonify([False, ProtocolErrors.PARAMETERS_DO_NOT_MATCH_REQUIREMENTS.value])


@app.route('/exchange', methods=['GET'])
@login_required
def exchange():
    amount = request.args.get('amount')
    to_coin = request.args.get('to_coin')
    from_coin = request.args.get('from_coin')

    if not (amount and to_coin and from_coin):
        return jsonify([False, ProtocolErrors.INVALID_PARAMETERS_ERROR.value])
    
    try:
        result = internet_scrappers.coin_exchange(from_coin, to_coin, float(amount))
        return jsonify([True, result]) # For example: [True, 3]
    except internet_scrappers.InvalidCurrencyCode: 
        return jsonify([False, ProtocolErrors.INVALID_CURRENCY_CODE.value])
    except ValueError: # If amount was not float value 
        return jsonify([False, ProtocolErrors.INVALID_PARAMETERS_ERROR.value])  


@app.route('/search/<key>', methods=['GET'])
@login_required
def search(key):
    try:
        res = internet_scrappers.wiki_search(key)
        return jsonify([True, res])
    except internet_scrappers.NoResultsFound: # There are no results for that key
        return jsonify([False, ProtocolErrors.NO_RESULTS_FOUND.value])

@app.route('/translate', methods=['GET'])
@login_required
def translate():
    data = request.args.get('data')
    dest_lang = request.args.get('dest_lang')
    # Can't think of a specific exception case currently, might need to add later
    res = internet_scrappers.translate(data,dest_lang)
    return jsonify([True, res])
    

    


# NOTE: how should we use the is_active method for current_user?
# NOTE: the login process should be diffrent for API?
