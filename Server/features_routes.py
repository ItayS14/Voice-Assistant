from Server import app, server_features_handler
from flask import request, jsonify, url_for
from Server.db_models import User
from flask_login import login_user, current_user, logout_user, login_required
from Server.config import ProtocolErrors, ProtocolException
import Server.nlp


@app.route('/exchange', methods=['GET'])
@login_required
def exchange():
    if not current_user.confirmed:
        return jsonify([False, ProtocolErrors.USER_IS_NOT_ACTIVE.value])

    amount = request.args.get('amount')
    to_coin = request.args.get('to_coin')
    from_coin = request.args.get('from_coin')

    if not (amount and to_coin and from_coin):
        return jsonify([False, ProtocolErrors.INVALID_PARAMETERS.value])
    
    try:
        result = server_features_handler.coin_exchange(from_coin, to_coin, float(amount))
        return jsonify([True, result]) 
    except ValueError: # If amount was not float value or invalid currency code
        return jsonify([False, ProtocolErrors.INVALID_CURRENCY_CODE.value])  


@app.route('/search', methods=['GET'])
@login_required
def search():
    if not current_user.confirmed:
        return jsonify([False, ProtocolErrors.USER_IS_NOT_ACTIVE.value])

    question = request.args.get('question')
    keywords = request.args.get('keywords')
    if not question and keywords:
        return jsonify([False, ProtocolErrors.INVALID_PARAMETERS.value])

    return jsonify([True, server_features_handler.search(question, keywords)])

@app.route('/translate', methods=['GET'])
@login_required
def translate():
    if not current_user.confirmed:
        return jsonify([False, ProtocolErrors.USER_IS_NOT_ACTIVE.value])

    text = request.args.get('text')
    dest_lang = request.args.get('lang')
    if not (text and dest_lang):
        return jsonify([False, ProtocolErrors.INVALID_PARAMETERS.value])
    # Can't think of a specific exception case currently, might need to add later
    try:
        res = server_features_handler.translate(text,dest_lang)
    except ValueError:
        return jsonify([False, ProtocolErrors.PARAMETERS_DO_NOT_MATCH_REQUIREMENTS.value])
    return jsonify([True, res])


@app.route('/calculate',methods=['GET'])
@login_required
def calculate():
    if not current_user.confirmed:
        return jsonify([False, ProtocolErrors.USER_IS_NOT_ACTIVE.value])

    expression = request.args.get('expression')
    if not expression:
        return jsonify([False, ProtocolErrors.INVALID_PARAMETERS.value])
    res = None
    try:
        res = server_features_handler.calculate(expression)
    except Exception:
        return jsonify([False,ProtocolErrors.INVALID_PARAMETERS.value])
    return jsonify([True, res])


@app.route('/parse/<text>', methods=['GET'])
@login_required
def parse(text):
    if not current_user.confirmed:
        return jsonify([False, ProtocolErrors.USER_IS_NOT_ACTIVE.value])

    try:
        res = Server.nlp.parse(text)
        print(res)
        data = res[0](res[1])
        return jsonify([True,data])
    except ProtocolException as e:
        return jsonify([False, e._error.value])
