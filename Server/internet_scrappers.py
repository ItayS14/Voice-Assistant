import wikipedia
from wikipedia.exceptions import DisambiguationError
import requests
from googletrans import Translator
from Server.config import internet_scrappers as settings

class NoResultsFound(Exception):
    """Raised when there is no results from keyowrd search in wikipedia"""
    pass

class InvalidCurrencyCode(Exception):
    """Raised when one of the parameters for coin_exchange function is an invalid code"""
    pass

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
        raise NoReusltsFound

    for result in search_results: #getting the first result which is a real page 
        try:
            return {
                "title" : result,
                "summary": wikipedia.summary(result, sentences=settings['SENTENCES_COUNT'], auto_suggest=False)
            } 
        except DisambiguationError:
            continue
    
    raise NoReusltsFound


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
    return rate*amount
    
def translate(text, dest_lang):
    """
    This function will translate the given text from one language to another
    :param text: The text to translate in the source language (str)
    :param dest_lang: (OPTIONAL) The destination language to translate to (str)
    :return: The text in the translated language (str)
    NOTE: Currently the assistant only supports translating from English to other languages,
          as supporting other languages would complicate the code massively.
    """
    translator = Translator()
    return translator.translate(text,dest=dest_lang)
