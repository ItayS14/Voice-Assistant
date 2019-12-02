from Server import app, db, bcrypt
from flask import request
from Server.models import User
from flask_login import login_user
from validators import validate_username, validate_email

@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    email = request.form.get('email')

    if username and email and password and validate_username(username) and validate_email(): #Add validators
        user = User(username=username, email=email, password=bcrypt.generate_password_hash(password).decode('utf-8'))
        db.session.add(user)
        db.session.commit()

        return [
            True,
            {}
        ]

    return [
        False,
        {} # add custom error msg later
    ]


@app.route('/login', methods=['POST'])
def login():
    auth =  request.form.get('auth')
    password = request.form.get('password')
    
    user = User.query.filter_by(email=auth).first() # Checking for both options (username validation or email validation)
    if not user:
        user = User.query.filter_by(username=auth).first()
    if user and bcrypt.check_password_hash(user.password, password):
        login_user(user)

    return [
        True,
        {}
    ]
