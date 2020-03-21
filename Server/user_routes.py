from Server import app, db, bcrypt, mail
from flask import request, jsonify
from Server.models import User
from flask_login import login_user, current_user, logout_user, login_required
from Server.validators import *
import Server.internet_scrappers as internet_scrappers
from Server.config import ProtocolErrors
from Server.utils import send_reset_email, verify_code, send_email_verification

@app.route('/register', methods=['POST'])
def register():
    if current_user.is_authenticated:
        return jsonify([False, ProtocolErrors.USER_ALREADY_LOGGED.value])

    username = request.form.get('username')
    password = request.form.get('password')
    email = request.form.get('email')
    if not (username and email and password):
        return jsonify([False, ProtocolErrors.INVALID_PARAMETERS.value])

    if validate_username(username) and validate_email(email) and validate_password(password):
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        send_email_verification(user)
        return jsonify([True, {}])
    # add custom error msg later
    return jsonify([False, ProtocolErrors.PARAMETERS_DO_NOT_MATCH_REQUIREMENTS.value])


@app.route('/validate_email/<token>')
def validate_email_token(token):
    email = request.form.get('email')
    if not email:
        return jsonify([False, ProtocolErrors.INVALID_PARAMETERS.value])
    
    user = User.query.filter_by(email=email)
    if not user:
        return jsonify([False, ProtocolErrors.INVALID_PARAMETERS.value]) 

    user.confirmed = True
    db.session.commit()


@app.route('/login', methods=['POST'])
def login():
    if current_user.is_authenticated:
        return jsonify([False, ProtocolErrors.USER_ALREADY_LOGGED.value])

    auth = request.form.get('auth')
    password = request.form.get('password')
    if not (auth and password):
        return jsonify([False, ProtocolErrors.INVALID_PARAMETERS.value])

    # Checking for both options (username validation or email validation)
    user = User.query.filter_by(email=auth).first()
    if not user:
        user = User.query.filter_by(username=auth).first()

    if user and bcrypt.check_password_hash(user.password, password):
        # Login user using flask-login function
        login_user(user)  # Not sure how to use the remember argument
        return jsonify([True, {}])

    return jsonify([False, ProtocolErrors.INVALID_CREDENTIALS.value])


@app.route('/logout')
@login_required
def logout():
    # A flask-login function that disconnects the user
    logout_user()
    return jsonify([True, {}])


@app.route("/get_password_reset_token", methods=['POST'])
def get_password_reset_token():
    # May need to add support for password change later
    if current_user.is_authenticated:
        return jsonify([False, ProtocolErrors.USER_ALREADY_LOGGED.value])
 
    email = request.form.get('email')
    if not email:
        return jsonify([False, ProtocolErrors.INVALID_PARAMETERS.value])
    
    user = User.query.filter_by(email=email).first()
    if user is None:
        return jsonify([False, ProtocolErrors.INVALID_PARAMETERS.value])
  
    send_reset_email(user)
    
    return jsonify([True, {}])

@app.route('/validate_code', methods=['POST'])
def validate_code():
    if current_user.is_authenticated:
        return jsonify([False, ProtocolErrors.USER_ALREADY_LOGGED.value])

    code = request.form.get('code')
    # The email might not be neccesairy in this request, need to check
    email = request.form.get('email')

    if not email or not code:
        return jsonify([False,ProtocolErrors.INVALID_PARAMETERS.value])
    # Used for creating a token
    user = User.query.filter_by(email=email).first()
    if user is None:
        return jsonify([False, ProtocolErrors.INVALID_PARAMETERS.value])
    
    if not verify_code(user,code):
        return jsonify([False, ProtocolErrors.INVALID_RESET_CODE.value])

    token = user.get_token('PASSWORD_RESET')
    return jsonify([True, {'token' : str(token)}])
    
    
@app.route('/new_password/<token>',methods=['POST'])
def new_password(token):
    # May need to add support for password change later
    if current_user.is_authenticated:
        return jsonify([False, ProtocolErrors.USER_ALREADY_LOGGED.value])

    new_password = request.form.get('password')
    if not new_password:
        return jsonify([False, ProtocolErrors.INVALID_PARAMETERS.value])

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
    

@app.route('/profile', methods=['GET'])
@login_required
def profile():
    """
    This function will return the profile details of the logged user
    :return: the details of the user (json) or None
    """
    user = current_user
    # Later, add this to support smart house devices and/or specific user settings
    return jsonify([True,{
        'username': user.username,
        'email': user.email,
        'image': user.profile_image # Need to send the actual data and not only the string
    }])    

