from Server import app, db, bcrypt
from flask import request, jsonify
from Server.models import User
from flask_login import login_user, current_user, logout_user
from Server.validators import validate_username, validate_email

INVALID_PARAMETERS_ERROR = "Invalid parameters were given"
USER_ALREADY_LOGGED_ERROR = "User is already logged in"
INVALID_CREDENTIALS_ERROR = "Email, Username, or Password is invalid"
USER_NOT_LOGGED_ERROR = "User is not logged in"

@app.route('/register', methods=['POST'])
def register():
    if current_user.is_authenticated:
        return jsonify([
            False,
            USER_ALREADY_LOGGED_ERROR
        ])

    username = request.form.get('username')
    password = request.form.get('password')
    email = request.form.get('email')

    if username and email and password and validate_username(username) and validate_email(email): #Add validators
        user = User(username=username, email=email, password=bcrypt.generate_password_hash(password).decode('utf-8'))
        db.session.add(user)
        db.session.commit()

        return jsonify([
            True,
            {}
        ])

    return jsonify([
        False,
        {} # add custom error msg later
    ])


@app.route('/login', methods=['POST'])
def login():
    if current_user.is_authenticated:
        return jsonify([
            False,
            USER_ALREADY_LOGGED_ERROR
        ])
    
    auth =  request.form.get('auth')
    password = request.form.get('password')
    
    if not (auth and password):
        return jsonify([
            False,
            INVALID_PARAMETERS_ERROR
        ])
    
    user = User.query.filter_by(email=auth).first() # Checking for both options (username validation or email validation)
    if not user:
        user = User.query.filter_by(username=auth).first()
    if user and bcrypt.check_password_hash(user.password, password):
        login_user(user) # Not sure how to use the remember argument
    else:
        return jsonify([
            False,
            INVALID_CREDENTIALS_ERROR
        ])

    return jsonify([
        True,
        {}
    ])
