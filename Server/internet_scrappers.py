import wikipedia
from wikipedia.exceptions import DisambiguationError
import requests
from Server.config import internet_scrappers as settings
from Server import nlp, ProtocolErrors


class NoResultsFound(Exception):
    """Raised when there are no results from keyword search in wikipedia"""
    pass


class InvalidCurrencyCode(Exception):
    """Raised when one of the parameters for coin_exchange function is an invalid code"""
    pass


def nlp_wiki(text):
    """
    The function will parse wiki question and return the parameter from the text query
    :param text: the query to parse (str - for now)
    :return: the parameter (str)
    """
    doc = nlp(text)
    for word in doc:
        if word.pos_ == 'AUX':
            return doc[word.i + 1:].text.replace('?', '')
    r = [span.text for span in doc.noun_chunks] # In case that the sentence had no auxilary verbs grouping all noun chunks except the first one
    return ' '.join(r[1:])    

def nlp_coin_exchange(text): #TODO: return currency code
    """
    The function will parse exchange query and return the parameters found
    :param text: the query to parse (str - for now)
    :return: dictionary dictionary that contains the parameters (from_coin, to_coin, _amoun) 
    """
    doc = nlp(text)
    from_c = amount = to_c = None
    for noun in doc.noun_chunks: #root of the noun chunks will be always the currency
        if noun.root.i > 0 and doc[noun.root.i - 1].pos_ == 'NUM': # if there was a number before the currency it indicates that that's the part to exchange
            from_c = noun.root
            amount = doc[noun.root.i - 1]
        else:
            to_c = noun.root
    
    if not (from_c and amount and to_c):
        return ProtocolErrors.INVALID_PARAMETERS_ERROR
    return dict(from_coin=from_c, to_coin=to_c, amount=amount)

def wiki_search(keyword):
    """
    The function will search for keyword in wikipedia
    :param keyword: keyword to search (str)
    :return: the title of the page and the summary (dictionary)
    """
    title = wikipedia.suggest(keyword) 
    if title == None:
        title = keyword
    search_results = wikipedia.search(title)

    if len(search_results) == 0:
        raise NoResultsFound

    for result in search_results: #getting the first result which is a real page 
        try:
            return {
                "title" : result,
                "summary": wikipedia.summary(result, sentences=settings['SENTENCES_COUNT'], auto_suggest=False)
            } 
        except DisambiguationError:
            continue
    
    raise NoResultsFound


def coin_exchange(from_coin, to_coin, amount=1):
    """
    The function will exchange coins with real time exchange rate
    :param from_coin: the currency code to exchange from (str)
    :param to_coin: the currency code to exchange to (str)
    :param amount: the amount to exchange (1 by defult - which returns the rate of a coin - int or float)
    :return: the amount in the requested coin (int)
    """
    response = requests.get(f'{settings["EXCHANGE_API_URL"]}/{from_coin}')
    if not response.ok: #if there was error in the resonse (if from_coin was not valid)
        raise InvalidCurrencyCode
    data = response.json()

    to_coin = to_coin.upper() 
    if "result" in data.keys() or to_coin not in data["rates"].keys(): #invalid from_coin or to_coin
        raise InvalidCurrencyCode
    
    rate = data["rates"][to_coin]
    return rate * amount
    


