import os
from Server.nlp import nlp_wiki, nlp_coin_exchange, nlp_translate

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')


class InternetScrappersSettings():
    SENTENCES_COUNT = 2
    EXCHANGE_API_URL = r"https://api.exchangerate-api.com/v4/latest/"


class ValidatorsSettings():
    MAX_PASSWORD_LEN = 32
    MIN_PASSWORD_LEN = 8


class NLPSettings(): # Settings for the nlp module
    command_dict = {
    'exchange': nlp_coin_exchange,
    'translate': nlp_translate,
    'say': nlp_translate,
    'tell': nlp_wiki    
    }
    wh_dict = {
        'what': nlp_wiki,
        'who': nlp_wiki,
        'where': nlp_wiki,
        'which': nlp_wiki,
    }
    how_dict = {
        'much': nlp_coin_exchange,
        'many': nlp_coin_exchange, # might change
        'does': nlp_wiki,
        'do': nlp_translate 
    }
    LANGUAGE_PATTERN = [{'LOWER': {'IN': ['to','in']}}, {'ENT_TYPE': {'IN': ['NORP','LANGUAGE']}}]
