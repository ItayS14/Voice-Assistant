from Server.config import Config, server_features_handler_config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from enum import Enum
from Server.server_features import ServerFeaturesHandler
import spacy


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
mail = Mail(app)
server_features_handler = ServerFeaturesHandler(**server_features_handler_config)

nlp = spacy.load('en_core_web_sm')


from Server import user_routes, features_routes