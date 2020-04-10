import pandas as pd
from textblob import TextBlob
from models import InferSent
import torch
import googlesearch
import wikipedia
from scipy import spatial
import numpy as np


def get_context(keywords):
    """
    This function will get the context for the question to answer
    :param keywords: the question that has been asked by the user - only the keywords part (str)
    :return: the information related to the question that has been asked (str)
    """

    res  = next(googlesearch.search('site:en.wikipedia.org ' + keywords, 'com', 'en'))
    blob = TextBlob(wikipedia.summary(res[res.rfind('/') + 1:], auto_suggest=False))
    return [item.raw for item in blob.sentences]


def find_min_cosine_sim(question, context):
    """
    The function will get the sentence the most simillar to the question
    :param question: the question to check (str)
    :param context: list of sentences to check (list of str)
    :return: 
    """
    quest_vec = model.encode([question], tokenize=True)[0]
    context_vec = model.encode(context, tokenize=True)
    distances = (spatial.distance.cosine(sentence, quest_vec) for sentence in context_vec) # Getting the distances
    return min(zip(context, distances), key= lambda x : x[1])


model = torch.load('saved.pt')
model.eval()

tests  = [
    # ('Who is the president of the USA', 'president of the USA'),
    # ('Who wrote Game of Thrones', 'Game of Thrones'),
    # ('Who are the beatles', 'The Beatles'), 
    # ('Who are the nba champions', 'nba champions'),
    # ('When does water boil', 'water boil'),
    ('Who is the president of israel', 'president of israel')
]

for test in tests:
    print('Testing:', test[0], 'Res:', find_min_cosine_sim(test[0], get_context(test[1])))


