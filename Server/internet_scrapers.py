import wikipedia
from wikipedia.exceptions import DisambiguationError

class NoReusltsFound(Exception):
    """Raised when there is no results from keyowrd search in wikipedia"""
    pass

def wiki_search(keyword):
    """
    The function will search for keyword in wikipedia
    :param keyword: keyword to search (str)
    :return: dictionary 
    """

    SENTENCES_COUNT = 2

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
                "summary": wikipedia.summary(result, sentences=SENTENCES_COUNT, auto_suggest=False)
            } 
        except DisambiguationError:
            continue
    
    raise NoReusltsFound
