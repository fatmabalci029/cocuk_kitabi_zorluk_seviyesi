import os
import requests

RAW_DATA_DIR = "data/raw"
os.makedirs(RAW_DATA_DIR, exist_ok=True)

book_ids = [11, 16, 55, 21, 236, 19942, 19551, 203, 514, 58, 74, 14916, 1837, 17208, 20916, 23026, 2435, 45, 103, 1400, 157, 164, 174, 185, 219, 254, 278, 315, 329, 371, 408, 450, 486, 567, 678, 709, 777, 890, 907, 943, 1080, 1123, 1228, 1342, 1412, 1514, 1587, 1661, 1765, 1883, 2004, 2123, 2212, 2390, 2542, 2784, 3057, 3207, 3300, 3457, 3676, 3908, 4001, 4212, 4358, 4586, 4701, 4981, 5098, 5237]

def download_book(book_id):
    url = f"https://www.gutenberg.org/files/{book_id}/{book_id}-0.txt"
    response = requests.get(url)
    if response.status_code == 200:
        with open(os.path.join(RAW_DATA_DIR, f"book_{book_id}.txt"), "w", encoding="utf-8") as f:
            f.write(response.text)
        print(f"Book {book_id} indirildi.")
    else:
        print(f"Book {book_id} indirilemedi. Hata kodu: {response.status_code}")

if __name__ == "__main__":
    for book_id in book_ids:
        download_book(book_id)