import pandas as pd
import torch
from textblob import TextBlob
import pickle


df = pd.read_csv('data/train.csv')
infersent = torch.load('models/infersent_trained.pt')

df['sentences'] = df['context'].apply(lambda x: [item.raw for item in TextBlob(x).sentences])
df = df[df['sentences'].map(len) <= 10]
sentences = df["sentences"].reset_index(drop= True).tolist()

s = set()
for i in sentences:
    for j in i:
        s.add(j)

dict_emb = {} 
for sent in s:
    dict_emb[sent] = infersent.encode([sent], tokenize=True)
for question in df['questions'].tolist():
    dict_emb[question] = infersent.encode([question], tokenize=True)

d1 = {key:dict_emb[key] for i, key in enumerate(dict_emb) if i % 2 == 0}
d2 = {key:dict_emb[key] for i, key in enumerate(dict_emb) if i % 2 == 1}

with open('data/dict_emb1.pickle', 'wb') as handle:
    pickle.dump(d1, handle)
with open('data/dict_emb2.pickle', 'wb') as handle:
    pickle.dump(d2, handle)

