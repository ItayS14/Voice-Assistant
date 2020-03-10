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

PASSWORD_RESET_CODE_LEN = 6

ProtocolErrors = Enum('ProtocolErrors', [
    'INVALID_PARAMETERS',
    'USER_ALREADY_LOGGED',
    'INVALID_CREDENTIALS',
    'USER_NOT_LOGGED',
    'PARAMETERS_DO_NOT_MATCH_REQUIREMENTS',
    'INVALID_TOKEN',
    'INVALID_CURRENCY_CODE',
    'NO_RESULTS_FOUND',
    'UNSUPPORTED_COMMAND',
    'INVALID_RESET_CODE'])

class ProtocolException(Exception):
    def __init__(self, error):
        self._error = error

ServerMethods = Enum('ServerMethods', [
    'TRANSLATE',
    'EXCHANGE',
    'WIKI_SEARCH',
    'CALCULATE'
    ], start=100)

ClientMethods = Enum('ClientMethods',[], start=200)


class InternetScrappersSettings():
    SENTENCES_COUNT = 2
    EXCHANGE_API_URL = r"https://api.exchangerate-api.com/v4/latest/"


class ValidatorsSettings():
    MAX_PASSWORD_LEN = 32
    MIN_PASSWORD_LEN = 8


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
    CALCULATE_PATTERN = [{'POS': {'IN': ['SYM','PUNCT']}}]
