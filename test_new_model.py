import joblib
import re

model = joblib.load('phishing_model.pkl')

def extract_features(url):
    words = ['login', 'verify', 'secure', 'account', 'update', 'bank',
             'signin', 'confirm', 'password', 'credential', 'wallet',
             'paypal', 'amazon', 'apple', 'microsoft', 'google', 'facebook']
    url_lower = url.lower()
    special_chars = sum(1 for c in url if c in '-_=%@?&')
    domain_part = url.replace('https://', '').replace('http://', '').split('/')[0]
    return [
        len(url), url.count('.'), url.count('-'), url.count('/'),
        url.count('@'), url.count('?'), url.count('='), url.count('&'),
        sum(c.isdigit() for c in url), special_chars, len(domain_part),
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

tests = [
    "https://google.com",
    "https://amazon.com",
    "https://github.com",
    "https://www.digikala.com",
    "http://free-prize-now.xyz",
]

for url in tests:
    features = extract_features(url)
    pred = model.predict([features])[0]
    probs = model.predict_proba([features])[0]
    print(f"{url}")
    print(f"  Result: {'DANGER' if pred == 1 else 'SAFE'}")
    print(f"  Prob Safe: {probs[0]*100:.1f}% | Prob Danger: {probs[1]*100:.1f}%")
    print()