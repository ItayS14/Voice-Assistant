import os
from enum import Enum, auto


server_features_handler_config = {
    'sentence_count': 2, 
    'path_to_infersent': 'Server/QA_Test/models/infersent_trained.pt',
    'path_to_xgboost': 'Server/QA_test/models/xgb.model'
}

validators_config = {
    'max_password_len': 32,
    'min_password_len': 8
}

utils_config = {
    'code_len': 6,
    'pic_url': 'static/profile_pics',
    'max_seconds': 60 * 30 # 30 Minutes with 60 seconds
}

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')

class ProtocolErrors:
    INVALID_PARAMETERS = 'Invalid parameters for that function!'
    USER_ALREADY_LOGGED = 'You are already logged into the system!'
    INVALID_CREDENTIALS = 'You entered invalid credentials!'
    INVALID_PASSWORD = f'Passoword must be at least {validators_config["min_password_len"]} characters long and has to contain a capital letter, a small letter and a digit.'
    INVALID_EMAIL = 'Email is not in a valid format or is already used by another user!'
    INVALID_USERNAME = 'Username already taken!' 
    PARAMETERS_DO_NOT_MATCH_REQUIREMENTS = 'Parameters are in an invalid form!'
    INVALID_TOKEN = 'The token is invalid!'
    INVALID_CURRENCY_CODE = 'Invalid currency to extract!'
    NO_RESULTS_FOUND = "Sorry, couldn't find an answer."
    UNSUPPORTED_COMMAND = "Sorry, we don't support that command yet."
    INVALID_RESET_CODE = 'Wrong password reset code!\nPlease try again.'
    USER_IS_NOT_ACTIVE = 'Email is not validated yet!'
    INVALID_BASE64_STRING = 'Image is not encoded in base64 form!\nPlease upload a different image and try again.'
    NOT_EXISTING_EMAIL = "The email you entered doesn't exist!"

class ProtocolException(Exception):
    def __init__(self, error):
        self._error = error

class NLPSettings: # Settings for the nlp module
    command_dict = {
    'exchange': 'nlp_coin_exchange',
    'translate': 'nlp_translate',
    'say': 'nlp_translate',
    'tell': 'nlp_search',
    'calculate': 'nlp_calculate'    
    }
    wh_dict = {
        'what': 'nlp_search',
        'who': 'nlp_search',
        'where': 'nlp_search',
        'which': 'nlp_search',
    }
    how_dict = {
        'much': 'determine_how_func',
        'many': 'nlp_coin_exchange', # might change
        'does': 'nlp_wiki',
        'do': 'nlp_translate' 
    }
    LANGUAGE_PATTERN = [{'LOWER': {'IN': ['to','in']}}, {'ENT_TYPE': {'IN': ['GPE','NORP','LANGUAGE']}}]
    CALCULATE_PATTERN = [{'POS': 'NUM'}, {'LOWER': {'IN': ['+', '-', '*', '/', '^', '%']}}, {'POS': 'NUM'}]
