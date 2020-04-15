import pandas as pd

train = pd.read_json("data/train-v2.0.json")

contexts = []
answers_text = []
questions = []
answers_start = []
for index in train.index:
    topic = train.iloc[index]['data']
    for para in topic['paragraphs']:
        for q_a in para['qas']:
            if q_a['answers']:
                contexts.append(para['context'])
                answers_text.append(q_a['answers'][0]['text'])
                questions.append(q_a['question'])
                answers_start.append(q_a['answers'][0]['answer_start'])

df = pd.DataFrame({"context":contexts, "question": questions, "answer_start": answers_start, "text": answers_text})

df.to_csv("data/train.csv", index = None)
