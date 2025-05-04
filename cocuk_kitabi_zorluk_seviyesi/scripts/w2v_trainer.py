import pandas as pd
from gensim.models import Word2Vec

params = [
    {"sg": 0, "window": 2, "vector_size": 100},
    {"sg": 1, "window": 2, "vector_size": 100},
    {"sg": 0, "window": 4, "vector_size": 100},
    {"sg": 1, "window": 4, "vector_size": 100},
    {"sg": 0, "window": 2, "vector_size": 300},
    {"sg": 1, "window": 2, "vector_size": 300},
    {"sg": 0, "window": 4, "vector_size": 300},
    {"sg": 1, "window": 4, "vector_size": 300}
]

for mode in ["lemmatized", "stemmed"]:
    df = pd.read_csv(f"data/processed/{mode}.csv")
    tokenized = [text.split() for text in df["text"]]
    for p in params:
        model = Word2Vec(sentences=tokenized, sg=p["sg"], window=p["window"], vector_size=p["vector_size"])
        fname = f"models/{mode}/word2vec_{mode}_{'cbow' if p['sg']==0 else 'skipgram'}_win{p['window']}_dim{p['vector_size']}.model"
        model.save(fname)
        print(f"✅ Model kaydedildi: {fname}")