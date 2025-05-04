import subprocess

print("🔹 1. Veri indiriliyor...")
subprocess.run(["python", "scripts/source.py"])

print("🔹 2. Ön işleme başlatılıyor...")
subprocess.run(["python", "scripts/preprocessing.py"])

print("🔹 3. TF-IDF işlemi başlatılıyor...")
subprocess.run(["python", "scripts/vectorizer.py"])

print("🔹 4. Word2Vec modelleri eğitiliyor...")
subprocess.run(["python", "scripts/w2v_trainer.py"])

print("🔹 5. Zipf grafikleri oluşturuluyor...")
subprocess.run(["python", "scripts/zipf_plotter.py"])

print("✅ Tüm işlemler başarıyla tamamlandı.")