from flask import Flask
from Server import db, login_manager
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
    house_id = db.Column(db.Integer, db.ForeignKey('house.id'))
    profile_image = db.Column(
        db.String(32), nullable=False, default='default.jpg')

    def get_token(self, salt):
        """
        This function will get a token (for email verification/password reset), based on the user's id
        :param salt: The salt to add to the user's id, in order to create 2 different signatures (tokens) based on the 
                     user's needs - different tokens for email verification and password reset (str)
        :return: the token to use for the verification/reset (str)
        """
        # CHANGE THIS to our secret key later
        s = Serializer('SECRETKEY', 1800)  # Tokens last for 30 mins
        # Added salt because the tokens can be used for both password reset and email verification
        return s.dumps({'user_id': self.id}, salt=salt).decode('utf-8')

    @staticmethod
    def verify_token(token, salt):
        s = Serializer('SECRETKEY', salt=salt)
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    # Maybe need to convert this to db.ForeignKey
    device_type_id = db.Column(db.Integer)
    options = db.Column(db.String(100))
    house_id = db.Column(db.Integer, db.ForeignKey('house.id'), nullable=False)

    def __repr__(self):
        return f"Device('{self.device_name}', Type: {self.device_type_id})"

# Need to think how to connect an house to the server


class House(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    devices = db.relationship('Device', backref='house', lazy=True)
    users = db.relationship('User', backref='house', lazy=True)

    def __repr__(self):
        return f"House('{self.name}', Devices: {self.devices}, Users: {self.users})"


class DeviceType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"DeviceType({self.device_type_id})"

# Implementation of this model might vastly change


class Command(db.Model):
    index = db.Column(db.Integer, primary_key=True)
    # All the words that can describe the command, as a list
    command_words = db.Column(db.String(5000))

    def __repr__(self):
        return f"Command('{self.index}': {self.command_words})"
