from Server.config import Config
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

from Server import routes