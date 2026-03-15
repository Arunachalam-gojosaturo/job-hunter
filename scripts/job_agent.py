#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════╗
║   JOB HUNTER AGENT v3.2 — LIGHTWEIGHT       ║
║   AI: Groq FREE (no install needed)         ║
║   Alerts: Telegram + WhatsApp + Email + SMS ║
║   Scans Reddit + Upwork every 30 mins       ║
║   Runs 24/7 on cloud — PC can be OFF        ║
╚══════════════════════════════════════════════╝
"""

import os, json, time, hashlib, smtplib, logging, requests, feedparser, schedule
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

# ─── LOGGING ──────────────────────────────────
os.makedirs('logs', exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('logs/agent.log'),
        logging.StreamHandler()
    ]
)
log = logging.getLogger(__name__)

# ─── CONFIG ───────────────────────────────────
# AI — Groq is FREE, fast, no install needed
GROQ_KEY      = os.getenv('GROQ_API_KEY', '')
GROQ_MODEL    = os.getenv('GROQ_MODEL', 'llama3-8b-8192')

# Alerts
GMAIL_USER    = os.getenv('GMAIL_USER', '')
GMAIL_PASS    = os.getenv('GMAIL_APP_PASSWORD', '')
ALERT_EMAIL   = os.getenv('ALERT_EMAIL', '')
WA_PHONE      = os.getenv('WHATSAPP_PHONE', '')
WA_KEY        = os.getenv('CALLMEBOT_API_KEY', '')
TG_TOKEN      = os.getenv('TELEGRAM_BOT_TOKEN', '')
TG_CHAT       = os.getenv('TELEGRAM_CHAT_ID', '')
SMS_GATEWAY   = os.getenv('SMS_GATEWAY_EMAIL', '')
TB_PHONE      = os.getenv('TEXTBELT_PHONE', '')

# Your profile
YOUR_NAME     = os.getenv('YOUR_NAME', 'Developer')
YOUR_SKILLS   = os.getenv('YOUR_SKILLS', 'Full Stack, Python, Linux, Cybersecurity, n8n')
YOUR_DELIVERY = os.getenv('YOUR_DELIVERY', '24 hours')
YOUR_RATE     = os.getenv('YOUR_RATE', 'Starting at $30')

# Scanner settings
KEYWORDS  = [k.strip() for k in os.getenv('KEYWORDS',
    'python,linux,automation,cybersecurity,n8n,fullstack,web,ai,security,bash,docker,'
    'hire,hiring,help,need,looking,developer,programmer,coder,script,bot,api,'
    'server,setup,install,fix,bug,website,freelance,job,project,paid,work').split(',')]
INTERVAL  = int(os.getenv('SCAN_INTERVAL_MINUTES', '30'))

# ─── JOB SOURCES ──────────────────────────────
RSS_FEEDS = [
    # Reddit - all working
    ("r/forhire",         "https://www.reddit.com/r/forhire/new/.rss"),
    ("r/slavelabour",     "https://www.reddit.com/r/slavelabour/new/.rss"),
    ("r/webdev_jobs",     "https://www.reddit.com/r/webdev_jobs/new/.rss"),
    ("r/netsec",          "https://www.reddit.com/r/netsec/new/.rss"),
    ("r/learnpython",     "https://www.reddit.com/r/learnpython/new/.rss"),
    ("r/python",          "https://www.reddit.com/r/python/new/.rss"),
    ("r/cybersecurity",   "https://www.reddit.com/r/cybersecurity/new/.rss"),
    ("r/devops",          "https://www.reddit.com/r/devops/new/.rss"),
    ("r/sysadmin",        "https://www.reddit.com/r/sysadmin/new/.rss"),
    ("r/homelab",         "https://www.reddit.com/r/homelab/new/.rss"),
    # Freelancer RSS (working)
    ("Freelancer-Python", "https://www.freelancer.com/rss/category/3?jobs=1"),
    ("Freelancer-Web",    "https://www.freelancer.com/rss/category/2?jobs=1"),
    ("Freelancer-Linux",  "https://www.freelancer.com/rss/category/6?jobs=1"),
]

# ─── SEEN JOBS CACHE ──────────────────────────
SEEN_FILE = 'logs/seen_jobs.json'

def load_seen():
    try:
        with open(SEEN_FILE) as f: return set(json.load(f))
    except: return set()

def save_seen(seen):
    with open(SEEN_FILE, 'w') as f:
        json.dump(list(seen)[-1000:], f)

def job_id(entry):
    return hashlib.md5((entry.get('id','') + entry.get('title','')).encode()).hexdigest()

# Subreddits that are ALL job posts - accept everything from them
JOB_SUBREDDITS = ['r/forhire', 'r/slavelabour', 'r/webdev_jobs',
                  'Freelancer-Python', 'Freelancer-Web', 'Freelancer-Linux']

def is_relevant(title, body, source=''):
    # Accept ALL posts from job-specific subreddits
    if source in JOB_SUBREDDITS:
        return True
    # Filter other subreddits by keywords
    text = (title + ' ' + body).lower()
    return any(kw in text for kw in KEYWORDS)

# ─── AI REPLY (Groq FREE) ─────────────────────
def ai_reply(title, desc):
    prompt = f"""Write a short freelancer proposal (under 120 words) for this job:

Title: {title}
Description: {desc[:400]}

Developer:
- Name: {YOUR_NAME}
- Skills: {YOUR_SKILLS}
- Delivers in: {YOUR_DELIVERY}
- Rate: {YOUR_RATE}

Rules:
- Confident, human tone
- Mention 1-2 skills matching the job
- End with clear call to action
- Do NOT start with "I am perfect"
- Under 120 words"""

    if GROQ_KEY:
        try:
            r = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {GROQ_KEY}",
                         "Content-Type": "application/json"},
                json={"model": GROQ_MODEL,
                      "messages": [{"role": "user", "content": prompt}],
                      "max_tokens": 200, "temperature": 0.7},
                timeout=15
            )
            data = r.json()
            if 'choices' in data:
                log.info("  AI: Groq ✓")
                return data['choices'][0]['message']['content'].strip()
            else:
                log.warning(f"  Groq response issue: {data.get('error', {}).get('message', 'unknown')}")
        except Exception as e:
            log.warning(f"  Groq error: {e}")

    # Fallback — always works, no internet needed
    log.info("  AI: Using template reply")
    return f"""Hi! I can help with this project.

I'm {YOUR_NAME} — expert in {YOUR_SKILLS}. I deliver complete, tested, and deployed solutions within {YOUR_DELIVERY}.

{YOUR_RATE}. I can start immediately and guarantee quality work.

DM me — let's get started!"""

# ─── ALERT 1: TELEGRAM ────────────────────────
def alert_telegram(title, link, reply):
    if not TG_TOKEN or not TG_CHAT: return
    try:
        msg = (f"🔥 *NEW JOB!*\n\n📋 *{title[:80]}*\n\n"
               f"💬 *Reply ready:*\n```\n{reply[:300]}\n```\n\n🔗 [View Job]({link})")
        requests.post(f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage",
            json={"chat_id": TG_CHAT, "text": msg, "parse_mode": "Markdown"},
            timeout=10)
        log.info("  ✓ Telegram sent")
    except Exception as e:
        log.error(f"  Telegram error: {e}")

# ─── ALERT 2: WHATSAPP ────────────────────────
def alert_whatsapp(title, link):
    if not WA_PHONE or not WA_KEY: return
    try:
        msg = f"🔥 NEW JOB!\n{title[:60]}\nAI reply in email!\n{link}"
        requests.get("https://api.callmebot.com/whatsapp.php",
            params={"phone": WA_PHONE, "text": msg, "apikey": WA_KEY},
            timeout=10)
        log.info("  ✓ WhatsApp sent")
    except Exception as e:
        log.error(f"  WhatsApp error: {e}")

# ─── ALERT 3: EMAIL ───────────────────────────
def alert_email(title, desc, link, reply, source):
    if not GMAIL_USER or not GMAIL_PASS or not ALERT_EMAIL: return
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"🔥 Job: {title[:60]}"
        msg['From']    = GMAIL_USER
        msg['To']      = ALERT_EMAIL
        html = f"""<!DOCTYPE html><html><body style="font-family:Arial;max-width:660px;margin:auto;padding:20px;background:#f4f4f4">
<div style="background:linear-gradient(135deg,#0f0f1a,#1a1a2e);padding:28px;border-radius:12px;margin-bottom:16px">
  <h2 style="color:#00ff88;margin:0">🔥 New Job Match!</h2>
  <p style="color:#888;margin:6px 0 0;font-size:13px">Source: {source} • {datetime.now().strftime('%d %b %Y, %I:%M %p')}</p>
</div>
<div style="background:white;border-radius:10px;padding:22px;margin-bottom:16px">
  <h3 style="margin:0 0 12px">{title}</h3>
  <p style="color:#555;background:#f9f9f9;padding:14px;border-radius:8px;border-left:4px solid #007bff">{desc[:400]}...</p>
  <a href="{link}" style="display:inline-block;margin-top:14px;background:#007bff;color:white;padding:12px 28px;border-radius:8px;text-decoration:none;font-weight:bold">View Job →</a>
</div>
<div style="background:#f0fff4;border:2px solid #00cc66;border-radius:10px;padding:22px">
  <h3 style="margin:0 0 6px;color:#006622">✅ AI Reply — Copy & Send</h3>
  <div style="background:white;border:1px solid #ccc;border-radius:8px;padding:16px;font-size:14px;line-height:1.7;white-space:pre-wrap">{reply}</div>
</div>
<p style="text-align:center;color:#aaa;font-size:11px;margin-top:20px">Job Hunter Agent v3.2 — Running 24/7</p>
</body></html>"""
        msg.attach(MIMEText(html, 'html'))
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as s:
            s.login(GMAIL_USER, GMAIL_PASS)
            s.sendmail(GMAIL_USER, ALERT_EMAIL, msg.as_string())
        log.info("  ✓ Email sent")
    except Exception as e:
        log.error(f"  Email error: {e}")

# ─── ALERT 4: SMS GATEWAY ─────────────────────
def alert_sms_gateway(title):
    if not SMS_GATEWAY or not GMAIL_USER or not GMAIL_PASS: return
    try:
        msg = MIMEText(f"JOB: {title[:100]} - Check email!")
        msg['Subject'] = "Job Alert"
        msg['From']    = GMAIL_USER
        msg['To']      = SMS_GATEWAY
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as s:
            s.login(GMAIL_USER, GMAIL_PASS)
            s.sendmail(GMAIL_USER, SMS_GATEWAY, msg.as_string())
        log.info("  ✓ SMS gateway sent")
    except Exception as e:
        log.error(f"  SMS gateway error: {e}")

# ─── ALERT 5: TEXTBELT ────────────────────────
_tb_used = {"date": None}

def alert_textbelt(title):
    if not TB_PHONE: return
    today = datetime.now().date().isoformat()
    if _tb_used["date"] == today:
        log.info("  Textbelt: quota used today")
        return
    try:
        r = requests.post("https://textbelt.com/text", data={
            "phone": TB_PHONE,
            "message": f"🔥 Job: {title[:70]} - Check Telegram!",
            "key": "textbelt"
        }, timeout=10)
        if r.json().get('success'):
            _tb_used["date"] = today
            log.info("  ✓ Textbelt SMS sent")
        else:
            log.info(f"  Textbelt: {r.json().get('error','quota used')}")
    except Exception as e:
        log.error(f"  Textbelt error: {e}")

# ─── SEND ALL ALERTS ──────────────────────────
def send_all_alerts(title, desc, link, reply, source):
    log.info(f"  📢 Sending all alerts...")
    alert_telegram(title, link, reply)
    alert_whatsapp(title, link)
    alert_email(title, desc, link, reply, source)
    alert_sms_gateway(title)
    alert_textbelt(title)

# ─── LOG JOB ──────────────────────────────────
def log_job(title, link, source, reply):
    with open('logs/jobs_found.log', 'a') as f:
        f.write(json.dumps({
            "time": datetime.now().isoformat(),
            "title": title, "source": source,
            "link": link, "reply": reply[:150]
        }) + '\n')

# ─── MAIN SCAN ────────────────────────────────
def scan_jobs():
    log.info("═" * 50)
    log.info(f"🔍 SCAN — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    log.info("═" * 50)
    seen  = load_seen()
    found = 0

    for source_name, feed_url in RSS_FEEDS:
        try:
            feed = feedparser.parse(feed_url, request_headers={
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'application/rss+xml, application/xml, text/xml, */*',
                'Accept-Language': 'en-US,en;q=0.9',
            })
            log.info(f"  [{source_name}] {len(feed.entries)} posts")

            for entry in feed.entries[:20]:
                jid     = job_id(entry)
                title   = entry.get('title', '').strip()
                summary = entry.get('summary', '').strip()
                link    = entry.get('link', '')

                if jid in seen or not is_relevant(title, summary, source_name):
                    continue

                seen.add(jid)
                found += 1
                log.info(f"  ✅ MATCH #{found}: {title[:65]}")

                clean = summary.replace('<p>','').replace('</p>',' ')\
                               .replace('<br>',' ').replace('&amp;','&')\
                               .replace('&lt;','<').replace('&gt;','>')

                reply = ai_reply(title, clean)
                send_all_alerts(title, clean, link, reply, source_name)
                log_job(title, link, source_name, reply)
                time.sleep(2)

        except Exception as e:
            log.error(f"  Error [{source_name}]: {e}")

    save_seen(seen)
    log.info(f"═ DONE — {found} new jobs {'🔥' * min(found,5)}\n")

# ─── START ────────────────────────────────────
if __name__ == '__main__':
    ai_name = f"Groq ({GROQ_MODEL})" if GROQ_KEY else "Template (add GROQ_API_KEY for AI)"
    log.info("╔══════════════════════════════════════════╗")
    log.info("║   JOB HUNTER AGENT v3.2 STARTED 🚀       ║")
    log.info(f"║   Scanning every {INTERVAL} mins, 24/7         ║")
    log.info("╚══════════════════════════════════════════╝")
    log.info(f"  AI Engine : {ai_name}")
    log.info(f"  Name      : {YOUR_NAME}")
    log.info(f"  Skills    : {YOUR_SKILLS[:55]}")
    log.info(f"  Keywords  : {len(KEYWORDS)} loaded")
    log.info(f"  Sources   : {len(RSS_FEEDS)} feeds")
    log.info(f"  Alerts    : Telegram={bool(TG_TOKEN)} WA={bool(WA_KEY)} Email={bool(GMAIL_USER)} SMS={bool(SMS_GATEWAY)}")
    log.info("")

    scan_jobs()
    schedule.every(INTERVAL).minutes.do(scan_jobs)
    while True:
        schedule.run_pending()
        time.sleep(60)
