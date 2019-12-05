from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from enum import Enum

class ProtocolErrors(Enum):
    INVALID_PARAMETERS_ERROR, USER_ALREADY_LOGGED_ERROR, INVALID_CREDENTIALS_ERROR, USER_NOT_LOGGED_ERROR, PARAMETERS_DOES_NOT_MATCH_REQUIREMENTS = range(5)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = 'temp secret key for testing'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from Server import routes