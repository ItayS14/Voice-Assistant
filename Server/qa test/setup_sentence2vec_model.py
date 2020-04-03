
from models import InferSent
import torch
import pandas as pd
from textblob import TextBlob

df = pd.read_csv('train.csv')

blob = TextBlob(" ".join(df['context'].drop_duplicates().reset_index(drop=True))) # Droping all dupliacte context from the dataframe
sentences = [item.raw for item in blob.sentences]

MODEL_PATH = 'encoder/infersent1.pkl'
GLOVE_PATH = 'glove.840B.300d.txt'
params_model = {'bsize': 64, 'word_emb_dim': 300, 'enc_lstm_dim': 2048,
                'pool_type': 'max', 'dpout_model': 0.0, 'version': 1}
model = InferSent(params_model)
model.load_state_dict(torch.load(MODEL_PATH))
model.set_w2v_path(GLOVE_PATH)
model.build_vocab(sentences, tokenize=True)

torch.save(model, 'saved.pt')