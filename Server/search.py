from textblob import TextBlob
import xgboost as xgb
from Server import nlp
from scipy import spatial
import torch
import googlesearch
import wikipedia
import numpy as np
from functools import wraps
from urllib.parse import unquote

# Decorator function that pad the result list to size of new_len
def pad_result(new_len, num):
	def _pad_result(fnc):
		@wraps(fnc)
		def inner(*args, **kwargs):
			li = fnc(*args, **kwargs)
			return li + [num] * (new_len - len(li))
		return inner
	return _pad_result

# The class handles all the QA 
class QA:
	def __init__(self, path_to_infersent, path_to_xgboost):
		self._infersent = torch.load(path_to_infersent) # Loading the infersent encoder model
		self._infersent.eval()
		self._xgb = xgb.XGBClassifier() # Loading the XGBoost model
		self._xgb.load_model(path_to_xgboost)


	def predict(self, question, keywords):
		"""
		This function will predict the answer to a given question
		:param question: The question asked by the user (str)
		:param keywords: The key words to search on google to find context for the answer (str)
		:return: A sentence containing the answer to the question (str)
		"""
		context = QA._get_context(keywords) 
		roots = self._match_roots(question, context)
		dists = self._find_cosine_sim(question, context)
		print(len(roots),len(dists))
		index = self._xgb.predict(np.array([roots + dists]).reshape((1,-1)))[0]
		assert index < len(context), "Invalid index for answer {index} len of content {len(conte"
		return context[index] 

	@staticmethod
	@pad_result(10, 0)
	def _match_roots(question, context):
		"""
		The function will check if the root of the question is one of the roots of the sentence
		:param question: the question to check (str)
		:param context: the context to check (list of str) - each list item is a sentence
		:return: in which sentence the roots match with the question root (binary list)
		"""
		question_root = [sent.root.lemma_ for sent in nlp(question).sents][0]
		# Create roots for all the sentences in the context
		sents_roots = []
		for sent in context:
			sent_nlp = nlp(sent)
			roots = [chunk.root.head.lemma_ for chunk in sent_nlp.noun_chunks]
			sents_roots.append(roots)
		# Check if the root of the question is also one of the roots of the sentence
		return [int(question_root in sent_roots) for sent_roots in sents_roots] # int on True or False - to get 1 and 0 


	@pad_result(10, 1)
	def _find_cosine_sim(self, question, context):
		"""
		The function will get the sentence the most simillar to the question
		:param question: the question to check (str)
		:param context: list of sentences to check (list of str)
		:return: the distances (list of floats)
		"""
		quest_vec = self._infersent.encode([question], tokenize=True)[0]
		context_vec = self._infersent.encode(context, tokenize=True)
		return [spatial.distance.cosine(sentence, quest_vec) for sentence in context_vec] # Getting the distances
		 
	@staticmethod
	def _get_context(keywords):
		"""
		This function will get the context for the question to answer
		:param keywords: the question that has been asked by the user - only the keywords part (str)
		:return: the information related to the question that has been asked (str)
		"""
		res  = next(googlesearch.search('site:en.wikipedia.org ' + keywords, 'com', 'en'))
		#unicodedata.normalize('NFD', '').encode('ascii', 'ignore').decode()
	
		page = unquote(res[res.rfind('/') + 1:])
		blob = TextBlob(wikipedia.summary(page, auto_suggest=False))
		return [item.raw for item in blob.sentences] [:10:1]


