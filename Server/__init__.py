from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from enum import Enum


class ProtocolErrors(Enum):
    INVALID_PARAMETERS_ERROR, USER_ALREADY_LOGGED_ERROR, INVALID_CREDENTIALS_ERROR, USER_NOT_LOGGED_ERROR, PARAMETERS_DO_NOT_MATCH_REQUIREMENTS, INVALID_TOKEN, INVALID_CURRENCY_CODE, NO_RESULTS_FOUND = range(8)


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = 'temp secret key for testing'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
# ADD CONFIG FILE LATER
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'carmelvoiceassistant@gmail.com'
app.config['MAIL_PASSWORD'] = 'a1db2ec3f'
mail = Mail(app)

from Server import routes