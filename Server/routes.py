from Server import app, db, bcrypt
from flask import request
from Server.models import User

@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    email = request.form.get('email')

    if username and email and password: #Add query to check unique username and email, add validators
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

