import os
import joblib
import gensim
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def load_csv(version):
    return pd.read_csv(f"data/{version}.csv")

def train_tfidf(version):
    df = load_csv(version)
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(df["text"])
    joblib.dump((vectorizer, tfidf_matrix), f"models/tfidf_{version}.pkl")

def tfidf_similarity(input_text, version):
    vectorizer, tfidf_matrix = joblib.load(f"models/tfidf_{version}.pkl")
    df = load_csv(version)
    input_vec = vectorizer.transform([input_text])
    scores = cosine_similarity(input_vec, tfidf_matrix)[0]
    top5_idx = np.argsort(scores)[-5:][::-1]
    return df.iloc[top5_idx]["text"].tolist(), scores[top5_idx].tolist()

def avg_vector(model, text):
    words = text.split()
    vectors = [model.wv[w] for w in words if w in model.wv]
    return np.mean(vectors, axis=0) if vectors else None

def word2vec_similarity(input_text, model_path, csv_path):
    model = gensim.models.Word2Vec.load(model_path)
    df = pd.read_csv(csv_path)
    input_vec = avg_vector(model, input_text)
    if input_vec is None:
        return [], []
    df["vec"] = df["text"].apply(lambda x: avg_vector(model, x))
    df = df[df["vec"].notnull()]
    mat = np.vstack(df["vec"].values)
    scores = cosine_similarity([input_vec], mat)[0]
    top5_idx = np.argsort(scores)[-5:][::-1]
    return df.iloc[top5_idx]["text"].tolist(), scores[top5_idx].tolist()

def jaccard_score(set1, set2):
    return len(set1 & set2) / len(set1 | set2)

def generate_excel_report(results, jaccard_matrix):
    os.makedirs("outputs", exist_ok=True)
    with pd.ExcelWriter("outputs/benzerlik_raporu.xlsx") as writer:
        # Her modelin sonucu ayrı sayfa olarak ekle
        for model, data in results.items():
            df = pd.DataFrame({
                "Benzer Metin": data["texts"],
                "Benzerlik Skoru": data["scores"],
                "Anlamsal Puan (1-5)": [""] * len(data["texts"])
            })
            df.to_excel(writer, sheet_name=model[:31], index=False)

        # Jaccard matrisi ayrı sayfa olarak yaz
        jaccard_matrix.to_excel(writer, sheet_name="Jaccard_Matrisi")

def main():
    os.makedirs("outputs", exist_ok=True)
    for version in ["lemmatized", "stemmed"]:
        train_tfidf(version)

    df = load_csv("lemmatized")
    input_text = df["text"].iloc[0]

    results = {}

    # TF-IDF sonuçları
    for version in ["lemmatized", "stemmed"]:
        texts, scores = tfidf_similarity(input_text, version)
        results[f"tfidf_{version}"] = {"texts": texts, "scores": scores}

    # Word2Vec sonuçları
    for m in os.listdir("models"):
        if m.endswith(".model"):
            path = os.path.join("models", m)
            vtype = "lemmatized" if "lemmatized" in m else "stemmed"
            texts, scores = word2vec_similarity(input_text, path, f"data/{vtype}.csv")
            results[m] = {"texts": texts, "scores": scores}

    # Jaccard matrisi
    model_names = list(results.keys())
    sets = {m: set(results[m]["texts"]) for m in model_names}
    mat = pd.DataFrame(index=model_names, columns=model_names, dtype=float)

    for m1 in model_names:
        for m2 in model_names:
            mat.loc[m1, m2] = jaccard_score(sets[m1], sets[m2]) if m1 != m2 else 1.0

    generate_excel_report(results, mat)
    print("✅ Excel dosyası başarıyla oluşturuldu: outputs/benzerlik_raporu.xlsx")

if __name__ == "__main__":
    main()
