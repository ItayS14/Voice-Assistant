from Server import app, db, bcrypt, ProtocolErrors, mail
from flask import request, jsonify, url_for
from Server.models import User
from flask_login import login_user, current_user, logout_user, login_required
from Server.validators import validate_username, validate_email, validate_password
from flask_mail import Message


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
        hashed_password = bcrypt.generate_password_hash(
            password).decode('utf-8')
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


@app.route("/password_reset", methods=[ 'POST'])
def password_reset_request():
    # May need to add support for password change later
    if current_user.is_authenticated:
        return jsonify([False, ProtocolErrors.USER_ALREADY_LOGGED_ERROR.value])
    email = request.form.get('email')
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

    user = User.verify_token(token, 'PASSWORD_RESET')
    if user is None:
        return jsonify([False, ProtocolErrors.INVALID_TOKEN.value])

    
    new_password = request.form.get('password')
    # Make sure that password is strong enough and create new hash
    if validate_password(new_password):
        hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        user2 = User.query.filter_by(password=hashed_password)
        return jsonify([True, {}])
        
    return jsonify([False, ProtocolErrors.PARAMETERS_DO_NOT_MATCH_REQUIREMENTS.value])


# NOTE: how should we use the is_active method for current_user?
# NOTE: the login process should be diffrent for API?
