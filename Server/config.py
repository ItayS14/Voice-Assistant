import os
from enum import Enum, auto


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')

ProtocolErrors = Enum('ProtocolErrors', [
    'INVALID_PARAMETERS',
    'USER_ALREADY_LOGGED',
    'INVALID_CREDENTIALS',
    'USER_NOT_LOGGED',
    'INVALID_PASSWORD',
    'INVALID_EMAIL',
    'INVALID_USERNAME',
    'PARAMETERS_DO_NOT_MATCH_REQUIREMENTS',
    'INVALID_TOKEN',
    'INVALID_CURRENCY_CODE',
    'NO_RESULTS_FOUND',
    'UNSUPPORTED_COMMAND',
    'INVALID_RESET_CODE',
    'USER_IS_NOT_ACTIVE'])

class ProtocolException(Exception):
    def __init__(self, error):
        self._error = error

ServerMethods = Enum('ServerMethods', [
    'TRANSLATE',
    'EXCHANGE',
    'WIKI_SEARCH',
    'CALCULATE'
    ], start=100)

ClientMethods = 1


server_features_handler_config = {'sentence_count': 2}


validators_config = {
    'max_password_len': 32,
    'min_password_len': 8
}

utils_config = {
    'code_len': 6,
    'max_seconds': 60 * 30 # 30 Minutes with 60 seconds
}


class NLPSettings(): # Settings for the nlp module
    command_dict = {
    'exchange': 'nlp_coin_exchange',
    'translate': 'nlp_translate',
    'say': 'nlp_translate',
    'tell': 'nlp_wiki',
    'calculate': 'nlp_calculate'    
    }
    wh_dict = {
        'what': 'nlp_wiki',
        'who': 'nlp_wiki',
        'where': 'nlp_wiki',
        'which': 'nlp_wiki',
    }
    how_dict = {
        'much': 'determine_how_func',
        'many': 'nlp_coin_exchange', # might change
        'does': 'nlp_wiki',
        'do': 'nlp_translate' 
    }
    LANGUAGE_PATTERN = [{'LOWER': {'IN': ['to','in']}}, {'ENT_TYPE': {'IN': ['GPE','NORP','LANGUAGE']}}]
    CALCULATE_PATTERN = [{'POS': 'NUM'}, {'LOWER': {'IN': ['+', '-', '*', '/', '^', '%']}}, {'POS': 'NUM'}]
