import pandas as pd
import re
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib

# ۱. بارگذاری دیتاست نهایی
df = pd.read_csv('phishing_dataset_balanced.csv')
print("Total records:", len(df))

# ۲. تابع استخراج ویژگی (همون تابع بهبود یافته)
def extract_features(url):
    words = ['login', 'verify', 'secure', 'account', 'update', 'bank',
             'signin', 'confirm', 'password', 'credential', 'wallet',
             'paypal', 'amazon', 'apple', 'microsoft', 'google', 'facebook']
    
    url_lower = url.lower()
    special_chars = sum(1 for c in url if c in '-_=%@?&')
    domain_part = url.replace('https://', '').replace('http://', '').split('/')[0]
    
    return [
        len(url),
        url.count('.'),
        url.count('-'),
        url.count('/'),
        url.count('@'),
        url.count('?'),
        url.count('='),
        url.count('&'),
        sum(c.isdigit() for c in url),
        special_chars,
        len(domain_part),
        domain_part.count('.'),
        1 if re.search(r'\d+\.\d+\.\d+\.\d+', url) else 0,
        1 if url.startswith('https') else 0,
        1 if any(w in url_lower for w in words) else 0,
        1 if len(url) > 75 else 0,
        1 if 'www.' in url_lower else 0,
        1 if url_lower.count('http') > 1 else 0,
        1 if '//' in url[8:] else 0,
        1 if len(domain_part.split('.')) > 3 else 0,
    ]

# ۳. استخراج ویژگی‌ها
print("Extracting features (may take a few minutes)...")
X = df['url'].apply(lambda u: pd.Series(extract_features(u)))
y = df['verdict']

# ۴. تقسیم داده‌ها
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ۵. آموزش مدل XGBoost
print("Training XGBoost model...")
model = XGBClassifier(
    n_estimators=300,
    max_depth=10,
    learning_rate=0.1,
    random_state=42,
    n_jobs=-1,
    use_label_encoder=False,
    eval_metric='logloss'
)
model.fit(X_train, y_train)

# ۶. ارزیابی
preds = model.predict(X_test)
acc = accuracy_score(y_test, preds)
print(f"\nXGBoost Accuracy: {acc * 100:.2f}%")
print("\nFull Report:")
print(classification_report(y_test, preds))

# ۷. ذخیره مدل
joblib.dump(model, 'phishing_model.pkl')
print("Model saved: phishing_model.pkl")