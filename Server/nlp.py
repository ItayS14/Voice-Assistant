from Server import ProtocolErrors, nlp
from Server.config import NLPSettings as Settings

class NotSupportedCommand(Exception):
    pass


def parse(text):
    """
    The function is the main nlp parsing, it will return the proper nlp function for that text and nlp doc
    :param text: the text to parse (str)
    :return: tupple - (doc, function)
    """
    doc = nlp(text) # Maybe disable some pipes later
    first_token = doc[0].lower_
    if doc[-1].text == '?' or first_token in wh_dict.keys():
        return (globals()[Settings.wh_dict[first_token]], doc)
    if first_token == 'how':
        return (globals()[Settings.how_dict[doc[1].text]], doc)
    # Checking if the first word is a VERB might not work
    if first_token not in command_dict.keys():
        raise NotSupportedCommand
    return (globals()[Settings.command_dict[first_token]], doc)


def nlp_wiki(doc):
    """
    The function will parse wiki question and return the parameter from the text query
    :param doc: the query to parse (as Spacy doc)
    :return: the parameter (str)
    """
    for word in doc:
        if word.pos_ == 'AUX':
            return doc[word.i + 1:].text.replace('?', '')
    r = [span.text for span in doc.noun_chunks] # In case that the sentence had no auxilary verbs grouping all noun chunks except the first one
    return ' '.join(r[1:])    


def nlp_coin_exchange(doc): #TODO: return currency code
    """
    The function will parse exchange query and return the parameters found
    :param doc: the query to parse (as Spacy doc)
    :return: dictionary dictionary that contains the parameters (from_coin, to_coin, _amoun) 
    """
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


def nlp_translate(doc):
	"""
	This function will get the relevant parameters for the translate function 
	:param doc: the command the user gave (as Spacy doc)
	:return: the relevant parameters to the translate function (dict of param_name:param)
	"""
	matcher = Matcher(nlp.vocab)
	matcher.add("LANGUAGE_PATTERN",[Settings.LANGUAGE_PATTERN])
	matches = matcher(doc)
	# Couldn't find language to translate to, or 'in/to <LANGUAGE>' appears more than once
	if not matches or len(matches) > 1: 
		return jsonify([False, ProtocolErrors.PARAMETERS_DO_NOT_MATCH_REQUIREMENTS.value])
	
	match = matcher(doc)[0] 
	start, end = match[1], match[2]

	# doc[start:end] creates a span - of which we take the second word ('in Hebrew', 'to English' etc)
	lang = doc[start:end][1]

	first_verb = None
	for token in doc:
		if token.pos_ == 'VERB':
			first_verb = token.i
			break
	if first_verb is None:
		return jsonify([False, ProtocolErrors.PARAMETERS_DO_NOT_MATCH_REQUIREMENTS.value])
	# The text is everything between the first verb (tranlate, say etc) and the language to translate to, and everything after the language name - one of them will be an empty string
	translate_text =  doc[first_verb+1:start].text + doc[end:].text 
	params = {'lang': lang.text, 'text': translate_text}
	return params

