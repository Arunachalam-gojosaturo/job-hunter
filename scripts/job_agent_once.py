#!/usr/bin/env python3
"""
Single-run version for GitHub Actions
Scans once, sends alerts, exits
"""
import os, json, time, hashlib, smtplib, logging, requests, feedparser
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
log = logging.getLogger(__name__)

GROQ_KEY      = os.getenv('GROQ_API_KEY', '')
GROQ_MODEL    = os.getenv('GROQ_MODEL', 'llama-3.1-8b-instant')
GMAIL_USER    = os.getenv('GMAIL_USER', '')
GMAIL_PASS    = os.getenv('GMAIL_APP_PASSWORD', '')
ALERT_EMAIL   = os.getenv('ALERT_EMAIL', '')
TG_TOKEN      = os.getenv('TELEGRAM_BOT_TOKEN', '')
TG_CHAT       = os.getenv('TELEGRAM_CHAT_ID', '')
SMS_GATEWAY   = os.getenv('SMS_GATEWAY_EMAIL', '')
YOUR_NAME     = os.getenv('YOUR_NAME', 'Arunachalam')
YOUR_SKILLS   = os.getenv('YOUR_SKILLS', 'Full Stack, Python, Linux, Cybersecurity, n8n')
YOUR_DELIVERY = os.getenv('YOUR_DELIVERY', '24 hours')
YOUR_RATE     = os.getenv('YOUR_RATE', '30 USD')
KEYWORDS      = [k.strip() for k in os.getenv('KEYWORDS','hire,hiring,paid,freelance,developer').split(',')]

RSS_FEEDS = [
    ("r/forhire",      "https://www.reddit.com/r/forhire/new/.rss"),
    ("r/slavelabour",  "https://www.reddit.com/r/slavelabour/new/.rss"),
    ("r/webdev_jobs",  "https://www.reddit.com/r/webdev_jobs/new/.rss"),
    ("r/netsec",       "https://www.reddit.com/r/netsec/new/.rss"),
    ("r/devops",       "https://www.reddit.com/r/devops/new/.rss"),
]

JOB_FEEDS = ['r/forhire', 'r/slavelabour', 'r/webdev_jobs']
SEEN_FILE = '/tmp/seen_jobs.json'

def load_seen():
    try:
        with open(SEEN_FILE) as f: return set(json.load(f))
    except: return set()

def save_seen(seen):
    with open(SEEN_FILE, 'w') as f: json.dump(list(seen)[-500:], f)

def job_id(entry):
    return hashlib.md5((entry.get('id','') + entry.get('title','')).encode()).hexdigest()

def is_relevant(title, body, source=''):
    if source in JOB_FEEDS: return True
    text = (title + ' ' + body).lower()
    return any(kw in text for kw in KEYWORDS)

def ai_reply(title, desc):
    if not GROQ_KEY:
        return f"Hi! I'm {YOUR_NAME}, expert in {YOUR_SKILLS}. I deliver in {YOUR_DELIVERY}. {YOUR_RATE}. DM me now!"
    try:
        r = requests.post("https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"},
            json={"model": GROQ_MODEL, "max_tokens": 150, "temperature": 0.7,
                  "messages": [{"role": "user", "content": f"Write 80 word freelancer proposal for: {title}. Developer: {YOUR_NAME}, skills: {YOUR_SKILLS}, delivers in {YOUR_DELIVERY}. Confident tone, end with call to action."}]},
            timeout=15)
        return r.json()['choices'][0]['message']['content'].strip()
    except Exception as e:
        log.error(f"Groq error: {e}")
        return f"Hi! I'm {YOUR_NAME}, expert in {YOUR_SKILLS}. I deliver complete solutions in {YOUR_DELIVERY}. DM me now!"

def alert_telegram(title, link, reply):
    if not TG_TOKEN or not TG_CHAT: return
    try:
        msg = f"🔥 *NEW JOB!*\n\n📋 *{title[:80]}*\n\n✅ *Reply:*\n```\n{reply[:250]}\n```\n\n🔗 {link}"
        requests.post(f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage",
            json={"chat_id": TG_CHAT, "text": msg, "parse_mode": "Markdown"}, timeout=10)
        log.info("  ✓ Telegram sent")
    except Exception as e: log.error(f"Telegram error: {e}")

def alert_email(title, desc, link, reply, source):
    if not GMAIL_USER or not GMAIL_PASS or not ALERT_EMAIL: return
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"🔥 Job: {title[:60]}"
        msg['From'] = GMAIL_USER
        msg['To'] = ALERT_EMAIL
        html = f"""<html><body style='font-family:Arial;max-width:660px;margin:auto;padding:20px'>
<div style='background:linear-gradient(135deg,#0f0f1a,#1a1a2e);padding:25px;border-radius:12px;margin-bottom:15px'>
  <h2 style='color:#00ff88;margin:0'>🔥 New Job!</h2>
  <p style='color:#888;margin:5px 0 0'>{source}</p>
</div>
<div style='background:white;border-radius:10px;padding:20px;margin-bottom:15px;border:1px solid #eee'>
  <h3>{title}</h3>
  <p style='color:#555'>{desc[:300]}</p>
  <a href='{link}' style='background:#007bff;color:white;padding:10px 20px;border-radius:6px;text-decoration:none'>View Job →</a>
</div>
<div style='background:#f0fff4;border:2px solid #00cc66;border-radius:10px;padding:20px'>
  <h3 style='color:#006622'>✅ AI Reply — Copy and Send</h3>
  <div style='background:white;border:1px solid #ccc;border-radius:6px;padding:15px;white-space:pre-wrap'>{reply}</div>
</div>
</body></html>"""
        msg.attach(MIMEText(html, 'html'))
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as s:
            s.login(GMAIL_USER, GMAIL_PASS)
            s.sendmail(GMAIL_USER, ALERT_EMAIL, msg.as_string())
        log.info("  ✓ Email sent")
    except Exception as e: log.error(f"Email error: {e}")

def alert_sms(title):
    if not SMS_GATEWAY or not GMAIL_USER or not GMAIL_PASS: return
    try:
        msg = MIMEText(f"JOB: {title[:80]} - Check email!")
        msg['Subject'] = "Job Alert"
        msg['From'] = GMAIL_USER
        msg['To'] = SMS_GATEWAY
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as s:
            s.login(GMAIL_USER, GMAIL_PASS)
            s.sendmail(GMAIL_USER, SMS_GATEWAY, msg.as_string())
        log.info("  ✓ SMS sent")
    except Exception as e: log.error(f"SMS error: {e}")

def main():
    log.info("🔍 GitHub Actions Job Scan Started")
    seen = load_seen()
    found = 0

    for source_name, feed_url in RSS_FEEDS:
        try:
            feed = feedparser.parse(feed_url, request_headers={
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
                'Accept': 'application/rss+xml, */*'
            })
            log.info(f"  [{source_name}] {len(feed.entries)} posts")

            for entry in feed.entries[:15]:
                jid   = job_id(entry)
                title = entry.get('title', '').strip()
                desc  = entry.get('summary', '').replace('<p>','').replace('</p>',' ')[:400]
                link  = entry.get('link', '')

                if jid in seen or not is_relevant(title, desc, source_name):
                    continue

                seen.add(jid)
                found += 1
                log.info(f"  ✅ MATCH #{found}: {title[:60]}")

                reply = ai_reply(title, desc)
                alert_telegram(title, link, reply)
                alert_email(title, desc, link, reply, source_name)
                alert_sms(title)
                time.sleep(2)

        except Exception as e:
            log.error(f"Error [{source_name}]: {e}")

    save_seen(seen)
    log.info(f"✅ Done — {found} new jobs found")

if __name__ == '__main__':
    main()
