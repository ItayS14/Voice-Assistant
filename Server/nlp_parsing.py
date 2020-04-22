from Server import nlp
from Server.config import NLPSettings as Settings, ProtocolErrors, ClientMethods, ProtocolException
from spacy.matcher import Matcher
from flask import url_for


def parse(text):
	"""
	The function is the main nlp parsing, it will return the proper nlp function for that text and nlp doc
	:param text: the text to parse (str)
	:return: tuple - (doc, function)
	"""
	doc = nlp(text) # Maybe disable some pipes later
	first_token = doc[0].lower_
	print(first_token)
	if doc[-1].text == '?' or first_token in Settings.wh_dict.keys():
		return (globals()[Settings.wh_dict[first_token]], doc)
	if first_token == 'how':
		return (globals()[Settings.how_dict[doc[1].text]], doc)
	# Checking if the first word is a VERB might not work
	if first_token not in Settings.command_dict.keys():
		raise ProtocolException(ProtocolErrors.UNSUPPORTED_COMMAND)
	return (globals()[Settings.command_dict[first_token]], doc)


def nlp_search(doc):
	"""
	The function will parse wiki question and return the parameter from the text query
	:param doc: the query to parse (as Spacy doc)
	:return: the parameter (str)
	"""
	text = None
	for word in doc:
		if word.pos_ == 'AUX':
			text = doc[word.i + 1:].text.replace('?', '')
	if not text:
		r = [span.text for span in doc.noun_chunks] # In case that the sentence had no auxilary verbs grouping all noun chunks except the first one
		text = ' '.join(r[1:])
	params = {'keywords': text,'question': str(doc)}
	return {'route': url_for('search'), 'params': params}


def nlp_coin_exchange(doc): 
	"""
	The function will parse exchange query and return the parameters found
	:param doc: the query to parse (as Spacy doc)
	:return: dictionary dictionary that contains the parameters (from_coin, to_coin, amount) 
	"""
	from_c = amount = to_c = None
	for noun in doc.noun_chunks: #root of the noun chunks will be always the currency
		if noun.root.i > 0 and doc[noun.root.i - 1].pos_ == 'NUM': # if there was a number before the currency it indicates that that's the part to exchange
			from_c = noun.root.text
			amount = doc[noun.root.i - 1].text
		else:
			to_c = noun.root.text
	
	if not (from_c and amount and to_c):
		raise ProtocolException(ProtocolErrors.INVALID_PARAMETERS)

	params = dict(from_coin=from_c, to_coin=to_c, amount=amount) #ERROR: Somtimes from and to coin are not in the correct order
	return {'route': url_for('exchange'), 'params' : params}


def nlp_translate(doc):
	"""
	This function will get the relevant parameters for the translate function 
	:param doc: the command the user gave (as Spacy doc)
	:return: the relevant parameters to the translate function (dictionary)
	"""
	matcher = Matcher(nlp.vocab)
	matcher.add("LANGUAGE_PATTERN",[Settings.LANGUAGE_PATTERN])
	matches = matcher(doc)
	# Couldn't find language to translate to, or 'in/to <LANGUAGE>' appears more than once
	if not matches or len(matches) > 1: 
		raise ProtocolException(ProtocolErrors.PARAMETERS_DO_NOT_MATCH_REQUIREMENTS)
	
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
		raise ProtocolException(ProtocolErrors.PARAMETERS_DO_NOT_MATCH_REQUIREMENTS)
	# The text is everything between the first verb (tranlate, say etc) and the language to translate to, and everything after the language name - one of them will be an empty string
	translate_text =  doc[first_verb+1:start].text + doc[end:].text 
	params = {'lang': lang.text, 'text': translate_text}
	return {'route': url_for('translate'),'params' : params }

def nlp_calculate(doc):
	"""
	This function will get the relevant parameters for the calculation function
	:param doc: the command the user gave (Spacy Doc)
	:return: the math calculation to be performed (dictionary)
	"""
	matcher = Matcher(nlp.vocab)
	matcher.add("CALCULATE_PATTERN",[Settings.CALCULATE_PATTERN])
	matches = matcher(doc)
	if not matches:
		raise ProtocolException(ProtocolErrors.PARAMETERS_DO_NOT_MATCH_REQUIREMENTS)
	
	# Start from the first number and end in the last number of the last match 
	# For example, it will work on 'calculate 5 + 5 + 5'
	start, end = matcher(doc)[0][1], matcher(doc)[-1][2]
	expression = str(doc[start:end])
	return {'route': url_for('calculate'), 'params': {'expression': expression}}
	

def determine_how_func(doc):
	"""
	This function will determine which function should be used when the keywords 'how much' are used
	:param doc: the command the user gave (Spacy Doc)
	:return: the result of the one of the functions this function has called (dictionary)
	"""
	first, second = None, None
	matcher = Matcher(nlp.vocab)
	matcher.add("CALCULATE_PATTERN",[Settings.CALCULATE_PATTERN])
	matches = matcher(doc)
	
	# First, check if you can find a math calculation in the sentence
	# May be more efficient way to check instead of matching twice
	if matches:
		first, second = nlp_calculate, nlp_coin_exchange
	else:
		first, second = nlp_coin_exchange, nlp_calculate
	
	try:
		return first(doc)
	except:
		return second(doc)

