import requests
import pandas as pd
import io

print("Downloading dataset...")

# لینک دانلود مستقیم
url = "https://huggingface.co/datasets/ealvaradob/phishing-dataset/resolve/main/processed/phishing_dataset.csv"

try:
    response = requests.get(url, timeout=60)
    response.raise_for_status()
    
    df = pd.read_csv(io.StringIO(response.text))
    print("Columns:", df.columns.tolist())
    print("Rows:", len(df))
    print(df.head())
    
    df.to_csv('phishing_dataset_new.csv', index=False)
    print("Saved: phishing_dataset_new.csv")
    
except Exception as e:
    print("Error:", e)
    print("Trying alternative URL...")
    
    url2 = "https://huggingface.co/datasets/ealvaradob/phishing-dataset/resolve/main/processed/urls.csv"
    try:
        response = requests.get(url2, timeout=60)
        response.raise_for_status()
        df = pd.read_csv(io.StringIO(response.text))
        print("Columns:", df.columns.tolist())
        print("Rows:", len(df))
        df.to_csv('phishing_dataset_new.csv', index=False)
        print("Saved: phishing_dataset_new.csv")
    except Exception as e2:
        print("Error 2:", e2)