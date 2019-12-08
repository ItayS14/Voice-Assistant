from Server.config import Config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from enum import Enum

class ProtocolErrors(Enum):
    INVALID_PARAMETERS_ERROR, USER_ALREADY_LOGGED_ERROR, INVALID_CREDENTIALS_ERROR, USER_NOT_LOGGED_ERROR, PARAMETERS_DO_NOT_MATCH_REQUIREMENTS, INVALID_TOKEN, INVALID_CURRENCY_CODE, NO_RESULTS_FOUND = range(8)

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
mail = Mail(app)

from Server import routes