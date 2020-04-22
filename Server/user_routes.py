from Server import app, db, bcrypt, mail, validators_handler, utils
from flask import request, jsonify, url_for
from Server.db_models import User
from flask_login import login_user, current_user, logout_user, login_required
from Server.config import ProtocolErrors
from Server.utils import validate_params, activated_required
import base64
import binascii

@app.route('/register', methods=['POST'])
@validate_params('username', 'email', 'password', get=False)
def register(username, email, password):
    if current_user.is_authenticated:
        return jsonify([False, ProtocolErrors.USER_ALREADY_LOGGED.value])

    if not validators_handler.username(username):
        return jsonify([False, ProtocolErrors.INVALID_USERNAME.value]) 
    if not validators_handler.email(email):
        return jsonify([False, ProtocolErrors.INVALID_EMAIL.value])
    if not validators_handler.password(password):
        return jsonify([False, ProtocolErrors.INVALID_PASSWORD.value]) 

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user = User(username=username, email=email, password=hashed_password)
    db.session.add(user)
    db.session.commit()
    utils.send_email_verification(user)
    return jsonify([True, {}])


@app.route('/validate_email/<token>')
def validate_email(token):
    user = User.verify_token(token, 'EMAIL_VALIDATION')
    if not user:
        return jsonify([False, ProtocolErrors.INVALID_EMAIL.value]) 
    user.confirmed = True
    db.session.commit()
    return "Email is now validated!"

@app.route('/login', methods=['POST'])
@validate_params('auth', 'password', get=False)
def login(auth, password):
    if current_user.is_authenticated:
        return jsonify([False, ProtocolErrors.USER_ALREADY_LOGGED.value])
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
@validate_params('email', get=False)
def get_password_reset_token(email):
    # May need to add support for password change later
    if current_user.is_authenticated:
        return jsonify([False, ProtocolErrors.USER_ALREADY_LOGGED.value])
    
    user = User.query.filter_by(email=email).first()
    if user is None:
        return jsonify([False, ProtocolErrors.INVALID_PARAMETERS.value])
  
    utils.send_reset_email(user)
    
    return jsonify([True, {}])

@app.route('/validate_code', methods=['POST'])
@validate_params('code', 'email', get=False)
def validate_code(code, email):
    if current_user.is_authenticated:
        return jsonify([False, ProtocolErrors.USER_ALREADY_LOGGED.value])

    # Used for creating a token
    user = User.query.filter_by(email=email).first()
    if user is None:
        return jsonify([False, ProtocolErrors.INVALID_PARAMETERS.value])
    
    if not utils.verify_code(user,code):
        return jsonify([False, ProtocolErrors.INVALID_RESET_CODE.value])

    token = user.get_token('PASSWORD_RESET')
    return jsonify([True, {'token' : str(token)}])
    
    
@app.route('/new_password/<token>',methods=['POST'])
@validate_params('password', get=False)
def new_password(new_password, token):
    # May need to add support for password change later
    if current_user.is_authenticated:
        return jsonify([False, ProtocolErrors.USER_ALREADY_LOGGED.value])

    user = User.verify_token(token, 'PASSWORD_RESET')
    if user is None:
        return jsonify([False, ProtocolErrors.INVALID_TOKEN.value])

    # Make sure that password is strong enough and create new hash
    if validators_handler.password(new_password):
        hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        return jsonify([True, {}])
        
    return jsonify([False, ProtocolErrors.INVALID_PASSWORD.value])
    

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
        'image': url_for('static', filename=f'profile_pics/{user.profile_image}', _external=True) 
    }])    
    

@app.route('/update_img', methods=['POST'])
@activated_required
@validate_params('file_name','img', get=False)
def update_img(file_name, img):
    #TODO: validate types of inputs - Security issue
    try:
        raw_data = base64.b64decode(img)
    except binascii.Error: 
        return jsonify[False, ProtocolErrors.INVALID_BASE64_STRING.value]
    else:
        file_name = utils.save_picture(file_name, raw_data)
        current_user.profile_image = file_name
        db.session.commit()
    return jsonify([True, {}])


