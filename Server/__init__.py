from Server.config import Config, internet_features_handler_config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from enum import Enum
from Server.internet_features import InternetFeaturesHandler
import spacy


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
mail = Mail(app)
internet_handler = InternetFeaturesHandler(**internet_features_handler_config)

nlp = spacy.load('en_core_web_sm')


from Server import user_routes, features_routes