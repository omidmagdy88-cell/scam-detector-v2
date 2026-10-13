import json
import pandas as pd

print("Loading urls.json (this may take a few minutes)...")

with open('urls.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Total records: {len(data)}")

urls = [item['text'] for item in data if 'text' in item and 'label' in item]
labels = [item['label'] for item in data if 'text' in item and 'label' in item]

print(f"Safe: {labels.count(0)}")
print(f"Phishing: {labels.count(1)}")

df = pd.DataFrame({'url': urls, 'verdict': labels})
df = df.sample(frac=1, random_state=42).reset_index(drop=True)
df.to_csv('phishing_dataset_huge.csv', index=False)
print("Saved: phishing_dataset_huge.csv")