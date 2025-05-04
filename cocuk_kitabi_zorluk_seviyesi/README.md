# 📚 Çocuk Kitabı Zorluk Seviyesi Belirleme Projesi

Bu proje, çocuk kitaplarının metin içeriklerine göre zorluk seviyelerini analiz etmeyi amaçlamaktadır. Kullanılan yöntemler sayesinde kitapların yaş grubuna uygunluğu değerlendirilebilir hale getirilmiştir.

---

## 🔧 Kullanılan Yöntemler ve Akış

### 1. Veri Toplama (Project Gutenberg)
Python `requests` kütüphanesi ile 70 çocuk kitabı **Project Gutenberg** üzerinden otomatik olarak indirilir. Her kitap `.txt` formatındadır.

### 2. Ön İşleme Adımları
- Küçük harfe çevirme
- Noktalama temizliği
- Stopword (gereksiz kelime) çıkarımı
- Tokenization (kelime parçalama)
- Lemmatization (`WordNetLemmatizer`)
- Stemming (`PorterStemmer`)

> ✔️ Çıktılar: `data/processed/lemmatized.csv`, `data/processed/stemmed.csv`

### 3. Zipf Yasası Analizi
Lemmatize ve stemlenmiş veriler üzerinde **log-log** ölçekli Zipf grafikleri çizilir.

> 📊 Çıktılar: `outputs/zipf_lemmatized.png`, `outputs/zipf_stemmed.png`

### 4. TF-IDF Vektörleştirme
İki ayrı veri seti için `TfidfVectorizer` uygulanarak belge-kelime matrisleri oluşturulur.

> 📁 Çıktılar: `data/processed/tfidf_lemmatized.csv`, `tfidf_stemmed.csv`

### 5. Word2Vec Model Eğitimi
Her veri seti için 8 farklı parametre kombinasyonuyla **16 Word2Vec modeli** eğitilir.

| Parametre        | Değerler             |
|------------------|----------------------|
| model_type       | CBOW / SkipGram      |
| window           | 2, 4                 |
| vector_size      | 100, 300             |

> 💾 Modeller: `models/lemmatized/` ve `models/stemmed/` klasörlerine kaydedilir.

---

## ⚙️ Kurulum

```bash
pip install -r requirements.txt
```

## 🚀 Çalıştırmak için

```bash
python main.py
```

---

## 📂 Klasör Yapısı

```
cocuk_kitabi_zorluk_seviyesi/
│
├── data/
│   ├── raw/                # Ham metinler
│   └── processed/          # Temizlenmiş CSV ve TF-IDF çıktıları
│
├── models/                 # Word2Vec çıktıları
│   ├── lemmatized/
│   └── stemmed/
│
├── outputs/                # Zipf grafikleri
├── scripts/                # Tüm işlem adımları
├── islem_baslatma/         # Ana çalıştırma dosyası (main.py)
├── README.md
└── requirements.txt
```

---

## 📌 Notlar

- Projede kullanılan tüm kitaplar kamuya açık ve yasal olarak erişilebilen içeriklerdir.
- Bu yapı, yaş grubu tahminleme gibi ileri analizlere temel oluşturabilir.