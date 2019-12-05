from Server import app, db, bcrypt, ProtocolErrors
from flask import request, jsonify
from Server.models import User
from flask_login import login_user, current_user, logout_user, login_required
from Server.validators import validate_username, validate_email, validate_password


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
    return jsonify([False, ProtocolErrors.PARAMETERS_DOES_NOT_MATCH_REQUIREMENTS.value])


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


# NOTE: how should we use the is_active method for current_user?
# NOTE: the login process should be diffrent for API?
