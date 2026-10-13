import pandas as pd
import random

# ۱. خواندن دیتاست قدیمی
df_old = pd.read_csv('phishing_dataset.csv')
old_phishing = df_old[df_old['verdict'] == 1]['url'].tolist()
old_safe = df_old[df_old['verdict'] == 0]['url'].tolist()
print(f"سالم قدیمی: {len(old_safe)}")
print(f"کلاهبردار قدیمی: {len(old_phishing)}")

# ۲. خواندن لینک‌های کلاهبردار جدید
new_phishing = []
with open('phishing_only.txt', 'r', encoding='utf-8', errors='ignore') as f:
    for line in f:
        url = line.strip()
        if url and url.startswith('http'):
            new_phishing.append(url)

# یکتا کردن کلاهبردارها
all_phishing = list(set(old_phishing + new_phishing))
print(f"کلاهبردار یکتا: {len(all_phishing)}")

# ۳. لیست لینک‌های سالم متنوع و معروف (برای تقویت دیتاست سالم)
safe_websites = [
    # سایت‌های جهانی
    "https://google.com", "https://www.google.com", "https://mail.google.com",
    "https://youtube.com", "https://www.youtube.com", "https://facebook.com",
    "https://www.facebook.com", "https://twitter.com", "https://www.twitter.com",
    "https://instagram.com", "https://www.instagram.com", "https://linkedin.com",
    "https://www.linkedin.com", "https://reddit.com", "https://www.reddit.com",
    "https://wikipedia.org", "https://www.wikipedia.org", "https://en.wikipedia.org",
    "https://amazon.com", "https://www.amazon.com", "https://aws.amazon.com",
    "https://apple.com", "https://www.apple.com", "https://support.apple.com",
    "https://microsoft.com", "https://www.microsoft.com", "https://office.microsoft.com",
    "https://github.com", "https://www.github.com", "https://gist.github.com",
    "https://stackoverflow.com", "https://www.stackoverflow.com",
    "https://netflix.com", "https://www.netflix.com", "https://spotify.com",
    "https://www.spotify.com", "https://dropbox.com", "https://www.dropbox.com",
    "https://yahoo.com", "https://www.yahoo.com", "https://bing.com",
    "https://www.bing.com", "https://cloudflare.com", "https://www.cloudflare.com",
    "https://mozilla.org", "https://www.mozilla.org", "https://python.org",
    "https://www.python.org", "https://pypi.org", "https://npmjs.com",
    "https://www.npmjs.com", "https://wordpress.com", "https://www.wordpress.com",
    "https://medium.com", "https://www.medium.com", "https://quora.com",
    "https://www.quora.com", "https://pinterest.com", "https://www.pinterest.com",
    "https://tumblr.com", "https://www.tumblr.com", "https://flickr.com",
    "https://www.flickr.com", "https://vimeo.com", "https://www.vimeo.com",
    "https://twitch.tv", "https://www.twitch.tv", "https://discord.com",
    "https://www.discord.com", "https://zoom.us", "https://www.zoom.us",
    "https://slack.com", "https://www.slack.com", "https://notion.so",
    "https://www.notion.so", "https://trello.com", "https://www.trello.com",
    "https://bbc.com", "https://www.bbc.com", "https://cnn.com",
    "https://www.cnn.com", "https://nytimes.com", "https://www.nytimes.com",
    "https://theguardian.com", "https://www.theguardian.com",
    "https://forbes.com", "https://www.forbes.com", "https://bloomberg.com",
    "https://www.bloomberg.com", "https://reuters.com", "https://www.reuters.com",
    # سایت‌های ایرانی
    "https://digikala.com", "https://www.digikala.com", "https://aparat.com",
    "https://www.aparat.com", "https://beytoote.com", "https://www.beytoote.com",
    "https://varzesh3.com", "https://www.varzesh3.com", "https://irna.ir",
    "https://www.irna.ir", "https://mehrnews.com", "https://www.mehrnews.com",
    "https://tasnimnews.com", "https://www.tasnimnews.com", "https://farsnews.ir",
    "https://www.farsnews.ir", "https://khabaronline.ir", "https://www.khabaronline.ir",
    "https://shaparak.ir", "https://www.shaparak.ir", "https://bmi.ir",
    "https://www.bmi.ir", "https://mci.ir", "https://www.mci.ir","https://irancell.ir", "https://www.irancell.ir", "https://rightel.ir",
    "https://www.rightel.ir", "https://shatel.ir", "https://www.shatel.ir",
    "https://asiatech.ir", "https://www.asiatech.ir", "https://parsonline.com",
    "https://www.parsonline.com", "https://bazar.ir", "https://www.bazar.ir",
    "https://divar.ir", "https://www.divar.ir", "https://sheypoor.com",
    "https://www.sheypoor.com", "https://torob.com", "https://www.torob.com",
    "https://basalam.com", "https://www.basalam.com", "https://modiseh.com",
    "https://www.modiseh.com", "https://snapp.ir", "https://www.snapp.ir",
    "https://tapsi.ir", "https://www.tapsi.ir", "https://alibaba.ir",
    "https://www.alibaba.ir", "https://flytoday.ir", "https://www.flytoday.ir",
    "https://cafebazaar.ir", "https://www.cafebazaar.ir", "https://myket.ir",
    "https://www.myket.ir", "https://sibapp.com", "https://www.sibapp.com",
    "https://zoomit.ir", "https://www.zoomit.ir", "https://digiato.com",
    "https://www.digiato.com", "https://hamshahrionline.ir", "https://www.hamshahrionline.ir",
]

print(f"سالم جدید: {len(safe_websites)}")

# ترکیب لینک‌های سالم قدیمی + جدید
all_safe = list(set(old_safe + safe_websites))
print(f"سالم یکتا: {len(all_safe)}")

# ۴. تعداد نهایی: ۱۵,۰۰۰ از هرکدوم
NUM = 4000
phishing_final = random.sample(all_phishing, min(NUM, len(all_phishing)))
safe_final = random.sample(all_safe, min(NUM, len(all_safe)))

print(f"\nتعداد کلاهبردار نهایی: {len(phishing_final)}")
print(f"تعداد سالم نهایی: {len(safe_final)}")

# ۵. ساخت دیتاست نهایی
new_df = pd.DataFrame({
    'url': phishing_final + safe_final,
    'verdict': [1] * len(phishing_final) + [0] * len(safe_final)
})

# ۶. شافل کردن
new_df = new_df.sample(frac=1, random_state=42).reset_index(drop=True)

# ۷. ذخیره
new_df.to_csv('phishing_dataset_balanced.csv', index=False)
print(f"\n✅ دیتاست جدید ساخته شد: phishing_dataset_balanced.csv")
print(f"   کل رکوردها: {len(new_df)}")
print(f"   سالم: {(new_df['verdict'] == 0).sum()}")
print(f"   کلاهبردار: {(new_df['verdict'] == 1).sum()}")