import pandas as pd

print("Loading huge dataset...")
df = pd.read_csv('phishing_dataset_huge.csv')
print(f"Total: {len(df)}")

# نمونه‌گیری متعادل: 50,000 از هر کلاس
safe = df[df['verdict'] == 0].sample(n=50000, random_state=42)
phishing = df[df['verdict'] == 1].sample(n=50000, random_state=42)

balanced = pd.concat([safe, phishing]).sample(frac=1, random_state=42).reset_index(drop=True)
balanced.to_csv('phishing_dataset_final.csv', index=False)
print(f"Balanced dataset saved: {len(balanced)} records")
print(f"Safe: {(balanced['verdict']==0).sum()}")
print(f"Phishing: {(balanced['verdict']==1).sum()}")