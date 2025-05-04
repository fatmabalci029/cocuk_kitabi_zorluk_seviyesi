import os
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer, PorterStemmer
import pandas as pd

nltk.download("punkt")
nltk.download("stopwords")
nltk.download("wordnet")

raw_path = "data/raw"
processed_path = "data/processed"
lemmatizer = WordNetLemmatizer()
stemmer = PorterStemmer()
stop_words = set(stopwords.words("english"))

def clean_text(text):
    tokens = word_tokenize(text)
    tokens = [word.lower() for word in tokens if word.isalpha()]
    tokens = [word for word in tokens if word not in stop_words]
    return tokens

lemmatized_docs, stemmed_docs = [], []

for filename in os.listdir(raw_path):
    with open(os.path.join(raw_path, filename), "r", encoding="utf-8") as file:
        text = file.read()
        tokens = clean_text(text)
        lemmatized = [lemmatizer.lemmatize(word) for word in tokens]
        stemmed = [stemmer.stem(word) for word in tokens]
        lemmatized_docs.append(" ".join(lemmatized))
        stemmed_docs.append(" ".join(stemmed))

pd.DataFrame({"text": lemmatized_docs}).to_csv(f"{processed_path}/lemmatized.csv", index=False)
pd.DataFrame({"text": stemmed_docs}).to_csv(f"{processed_path}/stemmed.csv", index=False)
print("✅ Temizlenmiş veriler kaydedildi.")