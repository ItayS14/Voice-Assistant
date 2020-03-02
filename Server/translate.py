from flask import jsonify
from googletrans import Translator


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


