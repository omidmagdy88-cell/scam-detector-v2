import whois
import requests
from datetime import datetime
from urllib.parse import urlparse

def check_whois(url):
    try:
        domain = urlparse(url).netloc
        w = whois.whois(domain)
        if w.creation_date:
            created = w.creation_date
            if isinstance(created, list):
                created = created[0]
            if created.tzinfo is not None:
                created = created.replace(tzinfo=None)
                age = (datetime.now() - created).days
            return {'age': age, 'error': None}
        else:
            return {'age': None, 'error': 'unknown'}
    except Exception as e:
        return {'age': None, 'error': str(e)}

def check_ssl(url):
    if url.startswith('https://'):
        return True
    return False

def check_content(url):
    try:
        r = requests.get(url, timeout=5, headers={'User-Agent': 'Mozilla/5.0'})
        text = r.text.lower()
        suspicious = ['login', 'verify', 'urgent', 'prize', 'winner', 'free', 'click here', 'confirm password']
        found = [w for w in suspicious if w in text]
        has_form = '<form' in text
        has_password = 'type="password"' in text
        return {'words': found[:5], 'has_form': has_form, 'has_password': has_password, 'error': None}
    except Exception as e:
        return {'words': [], 'has_form': False, 'has_password': False, 'error': str(e)}

def analyze(url):
    print("="*50)
    print("Analyzing: " + url)
    print("="*50)
    
    w = check_whois(url)
    if w['age'] is not None:
        if w['age'] < 180:
            print("WARNING: Domain registered only " + str(w['age']) + " days ago")
        elif w['age'] < 365:
            print("WARNING: Domain is " + str(w['age']) + " days old")
        else:
            print("OK: Domain is " + str(w['age']) + " days old")
    else:
        print("WHOIS error: " + str(w['error']))
    
    if check_ssl(url):
        print("OK: HTTPS enabled")
    else:
        print("WARNING: No HTTPS")
    
    c = check_content(url)
    if c['error']:
        print("Content error: " + str(c['error']))
    else:
        if c['words']:
            print("WARNING: Suspicious words: " + ", ".join(c['words']))
        else:
            print("OK: No suspicious words")
        if c['has_form']:
            print("WARNING: Has login form")
        if c['has_password']:
            print("WARNING: Has password field")

if __name__ == "__main__":
    analyze("https://amazon.com")
    analyze("https://google.com")
    analyze("http://free-prize-now.xyz")