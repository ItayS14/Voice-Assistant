from Server.config import Config, server_features_handler_config, validators_config, utils_config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from enum import Enum
import spacy

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
mail = Mail(app)
nlp = spacy.load('en_core_web_sm')

from Server.validators import Validators
from Server.utils import Utils
from Server.server_features import ServerFeaturesHandler

server_features_handler = ServerFeaturesHandler(**server_features_handler_config)
utils = Utils(**utils_config)
validators_handler = Validators(**validators_config)

from Server import user_routes, features_routes