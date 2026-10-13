from flask import Flask, request, render_template
import joblib
import re
import whois
from datetime import datetime
from urllib.parse import urlparse

app = Flask(__name__)
model = joblib.load('phishing_model.pkl')

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

def get_domain_age(url):
    try:
        domain = urlparse(url).netloc
        w = whois.whois(domain)
        if w.creation_date:
            created = w.creation_date
            if isinstance(created, list):
                created = created[0]
            if created.tzinfo is not None:
                created = created.replace(tzinfo=None)
            return (datetime.now() - created).days
    except:
        pass
    return None

@app.route("/", methods=["GET", "POST"])
def home():
    result = ""
    if request.method == "POST":
        url = request.form["url"]
        features = extract_features(url)
        pred = model.predict([features])[0]
        probs = model.predict_proba([features])[0]
        score = probs[1] * 100
        age = get_domain_age(url)
        reasons = []
        
        if age is not None:
            if age < 180:
                reasons.append('<li class="warn">⚠️ دامنه فقط ' + str(age) + ' روز پیش ثبت شده است</li>')
            elif age < 365:
                reasons.append('<li class="warn">⚠️ دامنه ' + str(age) + ' روز سابقه دارد (کم‌سابقه)</li>')
            else:
                reasons.append('<li class="ok">✅ دامنه ' + str(age // 365) + ' سال سابقه دارد</li>')
        else:
            reasons.append('<li class="warn">⚠️ اطلاعات دامنه در دسترس نیست</li>')
        
        if url.startswith('https'):
            reasons.append('<li class="ok">✅ پروتکل HTTPS فعال است</li>')
        else:
            reasons.append('<li class="warn">⚠️ پروتکل HTTPS ندارد</li>')
        
        if pred == 1:
            final = '<div class="result danger">❌ این سایت احتمالاً کلاهبرداری است</div>'
        else:
            final = '<div class="result safe">✅ این سایت سالم به نظر می‌رسد</div>'
        
        details = '<div class="details"><div class="score-box"><span class="score-label">امتیاز ریسک:</span><span class="score-value">' + str(round(score, 1)) + '%</span></div><h3>📋 دلایل تحلیل:</h3><ul>' + ''.join(reasons) + '</ul></div>'
        result = final + details
    
    return render_template('index.html', result=result)

if __name__ == "__main__":
    app.run(debug=True)
    