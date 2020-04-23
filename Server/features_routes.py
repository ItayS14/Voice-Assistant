from Server import app, server_features_handler
from flask import request, jsonify, url_for
from Server.db_models import User
from flask_login import login_user, current_user, logout_user, login_required
from Server.config import ProtocolErrors, ProtocolException
from Server.utils import validate_params, activated_required
import Server.nlp_parsing

@app.route('/exchange', methods=['GET'])
@activated_required
@validate_params('amount', 'from_coin', 'to_coin', get=True)
def exchange(amount, from_coin, to_coin):
    try:
        result = server_features_handler.coin_exchange(from_coin, to_coin, float(amount))
        return jsonify([True, result]) 
    except ValueError: # If amount was not float value or invalid currency code
        return jsonify([False, ProtocolErrors.INVALID_CURRENCY_CODE])  


@app.route('/search', methods=['GET'])
@activated_required
@validate_params('question', 'keywords', get=True)
def search(question, keywords):
    try:
        return jsonify([True, server_features_handler.search(question, keywords)])
    except StopIteration: # When there are no results from the google search
        return jsonify([False, ProtocolErrors.NO_RESULTS_FOUND])


@app.route('/translate', methods=['GET'])
@activated_required
@validate_params('text', 'lang', get=True)
def translate(text, dest_lang):
    # Can't think of a specific exception case currently, might need to add later
    try:
        res = server_features_handler.translate(text,dest_lang)
    except ValueError:
        return jsonify([False, ProtocolErrors.PARAMETERS_DO_NOT_MATCH_REQUIREMENTS])
    return jsonify([True, res])


@app.route('/calculate',methods=['GET'])
@activated_required
@validate_params('expression', get=True)
def calculate(expression):
    try:
        res = server_features_handler.calculate(expression)
    except Exception:
        return jsonify([False,ProtocolErrors.INVALID_PARAMETERS])
    else:
        return jsonify([True, res])


@app.route('/parse', methods=['GET'])
@activated_required
@validate_params('text', get=True)
def parse(text):
    try:
        res = Server.nlp_parsing.parse(text)
        data = res[0](res[1])
        return jsonify([True,data])
    except ProtocolException as e:
        return jsonify([False, e._error])
