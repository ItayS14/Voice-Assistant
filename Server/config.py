import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')


internet_scrappers = {
    'SENTENCES_COUNT' : 2,
    'EXCHANGE_API_URL' : r"https://api.exchangerate-api.com/v4/latest/"
}


calculator = {
    'MAX_PASSWORD_LEN': 32,
    'MIN_PASSWORD_LEN': 8
}