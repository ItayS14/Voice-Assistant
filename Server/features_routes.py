from Server import app
from flask import request, jsonify, url_for
from Server.models import User
from flask_login import login_user, current_user, logout_user, login_required
import Server.internet_scrappers as internet_scrappers
import Server.translate, Server.calculator
from Server.config import ProtocolErrors, ProtocolException
import Server.nlp

@app.route('/exchange', methods=['GET'])
@login_required
def exchange():
    if not current_user.is_active:
        return jsonify([False, ProtocolErrors.USER_IS_NOT_ACTIVE.value])

    amount = request.args.get('amount')
    to_coin = request.args.get('to_coin')
    from_coin = request.args.get('from_coin')

    if not (amount and to_coin and from_coin):
        return jsonify([False, ProtocolErrors.INVALID_PARAMETERS.value])
    
    try:
        result = internet_scrappers.coin_exchange(from_coin, to_coin, float(amount))
        return jsonify([True, result]) # For example: [True, 3]
    except internet_scrappers.InvalidCurrencyCode: 
        return jsonify([False, ProtocolErrors.INVALID_CURRENCY_CODE.value])
    except ValueError: # If amount was not float value 
        return jsonify([False, ProtocolErrors.INVALID_PARAMETERS.value])  


@app.route('/search', methods=['GET'])
@login_required
def search():
    if not current_user.is_active:
        return jsonify([False, ProtocolErrors.USER_IS_NOT_ACTIVE.value])

    text = request.args.get('text')
    if not text:
        return jsonify([False, ProtocolErrors.INVALID_PARAMETERS.value])

    try:
        res = internet_scrappers.wiki_search(text)
        return jsonify([True, res])
    except internet_scrappers.NoResultsFound: # There are no results for that key
        return jsonify([False, ProtocolErrors.NO_RESULTS_FOUND.value])


@app.route('/translate', methods=['GET'])
@login_required
def translate():
    if not current_user.is_active:
        return jsonify([False, ProtocolErrors.USER_IS_NOT_ACTIVE.value])

    text = request.args.get('text')
    dest_lang = request.args.get('lang')
    if not (text and dest_lang):
        return jsonify([False, ProtocolErrors.INVALID_PARAMETERS.value])
    # Can't think of a specific exception case currently, might need to add later
    res = Server.translate.translate(text,dest_lang)
    return jsonify([True, res])


@app.route('/calculate',methods=['GET'])
@login_required
def calculate():
    if not current_user.is_active:
        return jsonify([False, ProtocolErrors.USER_IS_NOT_ACTIVE.value])

    expression = request.args.get('expression')
    if not expression:
        return jsonify([False, ProtocolErrors.INVALID_PARAMETERS.value])
    res = None
    try:
        res = Server.calculator.calculate(expression)
    except Exception:
        return jsonify([False,ProtocolErrors.INVALID_PARAMETERS.value])
    return jsonify([True, res])

@app.route('/parse/<text>', methods=['GET'])
@login_required
def parse(text):
    if not current_user.is_active:
        return jsonify([False, ProtocolErrors.USER_IS_NOT_ACTIVE.value])

    try:
        res = Server.nlp.parse(text)
        print(res)
        data = res[0](res[1])
        return jsonify([True,data])
    except ProtocolException as e:
        return jsonify([False, e._error.value])

# NOTE: how should we use the is_active method for current_user?
# NOTE: the login process should be diffrent for API?
