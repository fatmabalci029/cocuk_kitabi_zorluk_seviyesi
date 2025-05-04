import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

data_path = "data/processed"

for mode in ["lemmatized", "stemmed"]:
    df = pd.read_csv(f"{data_path}/{mode}.csv")
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(df["text"])
    tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=vectorizer.get_feature_names_out())
    tfidf_df.to_csv(f"{data_path}/tfidf_{mode}.csv", index=False)
    print(f"✅ TF-IDF vektörü oluşturuldu: tfidf_{mode}.csv")