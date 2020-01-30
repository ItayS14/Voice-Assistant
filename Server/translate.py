from spacy.matcher import Matcher
from Server import nlp, ProtocolErrors
from flask import jsonify
from googletrans import Translator

LANGUAGE_PATTERN = [{'LOWER': {'IN': ['to','in']}}, {'ENT_TYPE': {'IN': ['NORP','LANGUAGE']}}]

def get_parameters(text):
	"""
	This function will get the relevant parameters for the translate function 
	:param text: the command the user gave (str)
	:return: the relevant parameters to the translate function (dict of param_name:param)
	"""
	doc = nlp(text)
	matcher = Matcher(nlp.vocab)
	matcher.add("LANGUAGE_PATTERN",[LANGUAGE_PATTERN])
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
	return translator.translate(text,dest=dest_lang).text


