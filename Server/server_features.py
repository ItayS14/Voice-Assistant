import wikipedia
from wikipedia.exceptions import DisambiguationError
import requests
from googletrans import Translator
from py_expression_eval import Parser
import pycountry
from fuzzywuzzy import process
import torch
from scipy import spatial
import googlesearch
from textblob import TextBlob

class ServerFeaturesHandler:
	exchange_api_url = r"https://api.exchangerate-api.com/v4/latest/"
	languages = [country.name for country in pycountry.languages]
	currencies = dict({currency.name:currency.alpha_3.upper() for currency in pycountry.currencies}, **{'Dollar': 'USD', 'Shekel': 'ILS'})

	def __init__(self, sentence_count, path_to_model):
		self._sentence_count = sentence_count
		self._model = torch.load(path_to_model)
		self._model.eval()
		
	def find_min_cosine_sim(self, question, context):
		"""
		The function will get the sentence the most simillar to the question
		:param question: the question to check (str)
		:param context: list of sentences to check (list of str)
		:return: the closest sentence sentence - str
		"""
		quest_vec = self._model.encode([question], tokenize=True)[0]
		context_vec = self._model.encode(context, tokenize=True)
		distances = (spatial.distance.cosine(sentence, quest_vec) for sentence in context_vec) # Getting the distances
		return min(zip(context, distances), key= lambda x : x[1])[0]

	@staticmethod
	def get_context(keywords):
		"""
		This function will get the context for the question to answer
		:param keywords: the question that has been asked by the user - only the keywords part (str)
		:return: the information related to the question that has been asked (str)
		"""

		res  = next(googlesearch.search('site:en.wikipedia.org ' + keywords, 'com', 'en'))
		blob = TextBlob(wikipedia.summary(res[res.rfind('/') + 1:], auto_suggest=False))
		return [item.raw for item in blob.sentences]
	

	def search(self, question, keywords):
		"""
		The function will search for keyword in wikipedia
		:param keyword: keyword to search (str)
		:return: the title of the page and the summary (dictionary)
		"""
		context = ServerFeaturesHandler.get_context(keywords)
		return self.find_min_cosine_sim(question,context)
		

	@classmethod
	def coin_exchange(cls,from_coin, to_coin, amount=1):
		"""
		The function will exchange coins with real time exchange rate
		:param from_coin: the currency code to exchange from (str)
		:param to_coin: the currency code to exchange to (str)
		:param amount: the amount to exchange (1 by defult - which returns the rate of a coin - int or float)
		:return: the amount in the requested coin (int)
		:raise: InvalidCurrencyCode if to_coin or from_coin was invalid
		"""
		from_coin = cls._currency_converter(from_coin)
		to_coin = cls._currency_converter(to_coin)

		response = requests.get(f'{cls.exchange_api_url}/{from_coin}')
		if not response.ok: #if there was error in the resonse (if from_coin was not valid)
			raise ValueError('Invalid currency code')
		data = response.json()

		to_coin = to_coin.upper() 
		if "result" in data.keys() or to_coin not in data["rates"].keys(): #invalid from_coin or to_coin
			raise ValueError('Invalid currency code')
		
		rate = data["rates"][to_coin]
		return rate * amount

	@classmethod
	def translate(cls, text, dest_lang):
		"""
		This function will translate the given text from one language to another
		:param text: The text to translate in the source language (str)
		:param dest_lang: The destination language to translate to (str)
		:return: The text in the translated language (str)
		:raise: InvalidLanguageName if the name of the language isn't detected in the list of names
		NOTE: Currently the assistant only supports translating from English to other languages,
			as supporting other languages would complicate the code massively.
			
		"""
		dest_lang = cls._get_language(dest_lang)
		translator = Translator()
		return translator.translate(text,dest=dest_lang).text

	@staticmethod
	def calculate(expression):
		"""
		This function will calculate the result of the mathematical expression
		:param expression: the expression to be calculated/evaluated (str)
		:return: the result of the calculation (float or int)
		"""
		parser = Parser() 
		return parser.parse(expression).evaluate({})

	@classmethod
	def _currency_converter(cls, currency): # Special case that need to be checked: gettings USD
		"""
		The function will get the currency code for a currency name (closest as possible)
		:param currency: the currency to change
		:return: The 3 letters currency code
		:raise: KeyError if no likely match found
		"""
		currency, ratio = process.extractOne(currency, cls.currencies.keys())
		if ratio < 70: # Unlikely to get a good match
			raise ValueError('Invalid currency code')
		return cls.currencies[currency]
	
	@classmethod
	def _get_language(cls, language):
		"""
		This function will convert a name of a given language to one of the languages in the list 
		:param language: the name of the language to find and convert (str)
		:return: the name of the language after the conversion (str)
		:raise: IndexError if no likely match was found
		"""
		lang, ratio = process.extractOne(language, cls.languages)
		if ratio < 70: # Unlikely to get a good match
			raise ValueError('Invalid language name')
		if lang == 'Chinese': # Special case
			lang = 'zh-CN'
		return lang

		
