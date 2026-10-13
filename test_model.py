import joblib
import re

model = joblib.load('phishing_model.pkl')

def extract_features(url):
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
        1 if re.search(r'\d+\.\d+\.\d+\.\d+', url) else 0,
        1 if url.startswith('https') else 0,
        1 if any(w in url.lower() for w in ['login', 'verify', 'secure', 'account', 'update', 'bank', 'paypal', 'signin']) else 0,
        1 if len(url) > 75 else 0,
        1 if 'www.' in url.lower() else 0,
    ]

def test(url):
    features = extract_features(url)
    pred = model.predict([features])[0]
    probs = model.predict_proba([features])[0]
    print(f"\nURL: {url}")
    print(f"ویژگی‌ها: {features}")
    print(f"نتیجه: {'❌ کلاهبردار' if pred == 1 else '✅ سالم'}")
    print(f"احتمال کلاهبردار: {probs[1]*100:.1f}%")
    print(f"احتمال سالم: {probs[0]*100:.1f}%")

# تست سایت‌های مختلف
test("https://amazon.com")
test("http://amazon.com")
test("https://google.com")
test("https://www.digikala.com")