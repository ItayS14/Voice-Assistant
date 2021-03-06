from flask import Flask
from Server import db, login_manager, app
from flask_login import UserMixin
# May need to change the type of the serializer, but this works just fine for now
from itsdangerous import URLSafeTimedSerializer as Serializer


@login_manager.user_loader  # user loader function for flask-login extension
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(16), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    reset_code = db.Column(db.String(6), unique=True, nullable=True)
    updated_time = db.Column(db.Float, nullable=True)
    profile_image = db.Column(db.String(32), nullable=False, default='default.jpg')
    confirmed = db.Column(db.Boolean, nullable=False, default=False)

    def get_token(self, salt):
        """
        This function will get a token (for email verification/password reset), based on the user's id
        :param salt: The salt to add to the user's id, in order to create 2 different signatures (tokens) based on the 
                     user's needs - different tokens for email verification and password reset (str)
        :return: the token to use for the verification/reset (str)
        """
        # CHANGE THIS to our secret key later
        s = Serializer(app.config['SECRET_KEY'], 1800)  # Tokens last for 30 mins
        # Added salt because the tokens can be used for both password reset and email verification
        return s.dumps({'user_id': self.id}, salt=salt)

    @staticmethod
    def verify_token(token, salt):
        """
        This function will verify that a certain token is valid and refers to a specific user
        :param token: the token to check if valid (str)
        :param salt: the salt to use while serializing (str)
        :return: the user that the token refers to if it's valid (User) or None if it isn't (or the user id doesn't exist)
        """
        s = Serializer(app.config['SECRET_KEY'], salt=salt)
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)
        
    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"
