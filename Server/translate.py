from spacy.matcher import Matcher
from Server import nlp

LANGUAGE_PATTERN = [{'LOWER': {'IN': ['to','in']}}, {'ENT_TYPE': {'IN': ['NORP','LANGUAGE']}}]

def get_parameters(text):
    """
    REMEMBER TO COMMENT
    """
    doc = nlp(text)
    matcher = Matcher(nlp.vocab)
    matcher.add("LANGUAGE_PATTERN",[LANGUAGE_PATTERN])
    # This line might create some special cases - on certain sentences
    match = matcher(doc)[0] 
    start, end = match[1], match[2]

    # doc[start:end] creates a span - of which we take the second word ('in Hebrew', 'to English' etc)
    lang = doc[start:end][1]

    params = {'lang': lang}
    return params


