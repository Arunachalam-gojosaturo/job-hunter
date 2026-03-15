# 🔥 Job Hunter Agent v3
### Scans Reddit + Upwork → AI writes reply → Alerts on Telegram + WhatsApp + Email + SMS
### Runs 24/7 on cloud — PC can be completely OFF

---

## 📱 Alert Channels

| Channel | Cost | Speed | Setup |
|---------|------|-------|-------|
| Telegram Bot | FREE forever | Instant | 2 mins |
| WhatsApp (Callmebot) | FREE | ~30 sec | 3 mins |
| Email (Gmail) | FREE | ~1 min | 2 mins |
| SMS via Email Gateway | FREE forever | ~1 min | 1 min |
| Textbelt SMS | FREE (1/day) | Instant | 0 mins |

---

## ⚡ STEP-BY-STEP SETUP

---

### STEP 1 — Run Setup Script
```bash
chmod +x setup.sh start.sh stop.sh start_cloud.sh
./setup.sh
```

---

### STEP 2 — Setup Telegram Bot (FREE, 2 mins)
```
1. Open Telegram app
2. Search for: @BotFather
3. Send: /newbot
4. Enter a name: JobHunterBot
5. Enter username: myjobhunter_bot
6. Copy the TOKEN it gives you

7. Now get your Chat ID:
   - Message your new bot once (send "hi")
   - Open this URL in browser:
     https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates
   - Find "chat":{"id": 123456789}
   - That number is your CHAT_ID

8. Add to .env:
   TELEGRAM_BOT_TOKEN=your_token
   TELEGRAM_CHAT_ID=your_chat_id
```

---

### STEP 3 — Setup WhatsApp (FREE, 3 mins)
```
1. Save this number in your phone contacts:
   +34 644 59 21 48
   (name it: Callmebot)

2. Send this WhatsApp message to that number:
   I allow callmebot to send me messages

3. You will receive an API key via WhatsApp

4. Add to .env:
   WHATSAPP_PHONE=+91XXXXXXXXXX
   CALLMEBOT_API_KEY=the_key_you_received
```

---

### STEP 4 — Setup Gmail Alerts (FREE, 2 mins)
```
1. Go to: https://myaccount.google.com/apppasswords
2. Select: Mail + Windows Computer
3. Click Generate
4. Copy the 16-character password (like: abcd efgh ijkl mnop)
5. Remove spaces when pasting

6. Add to .env:
   GMAIL_USER=your@gmail.com
   GMAIL_APP_PASSWORD=abcdefghijklmnop
   ALERT_EMAIL=your@gmail.com
```

---

### STEP 5 — Setup FREE SMS (1 min)
```
Find your carrier gateway email:

Airtel : 9999999999@airtelmail.in
Jio    : 9999999999@jio.com
Vi/Voda: 9999999999@vitext.com
BSNL   : 9999999999@bsnlmobile.in

Replace 9999999999 with your actual phone number.

Add to .env:
SMS_GATEWAY_EMAIL=9999999999@jio.com
TEXTBELT_PHONE=+919999999999
```

---

### STEP 6 — Setup AI (Pick One)

#### Option A: OpenAI (free credits for new accounts)
```
1. Go to: https://platform.openai.com
2. Sign up → you get free credits
3. Go to API Keys → Create new key
4. Add to .env:
   OPENAI_API_KEY=sk-...
```

#### Option B: Ollama LOCAL (100% free forever, no internet needed)
```bash
# Install Ollama
curl https://ollama.ai/install.sh | sh

# Download AI model (one time)
ollama pull mistral

# In .env set:
USE_OLLAMA=true
OLLAMA_MODEL=mistral
```

---

### STEP 7 — Fill Your Profile in .env
```
YOUR_NAME=YourName
YOUR_SKILLS=Full Stack Developer, Cybersecurity, Python, n8n, Linux
YOUR_DELIVERY=24 hours
YOUR_RATE=Starting at $30
```

---

### STEP 8 — Start the Agent
```bash
./start.sh
```

---

### STEP 9 — Setup n8n Workflow
```
1. Open browser: http://localhost:5678
2. Create account (first time only)
3. Click "+" → New Workflow
4. Click ⋮ menu → Import from File
5. Select: workflows/job_hunter_v3.json
6. Click on "📧 Email Alert" node → add Gmail credential
7. Click the RED toggle at top → turns GREEN
8. Agent is now ACTIVE!
```

---

### STEP 10 — Deploy to Cloud (24/7, PC OFF)

#### Easiest: Oracle Cloud Always-Free VPS
```
1. Go to: https://oracle.com/cloud/free
2. Sign up (free, needs debit card for verification only)
3. Create Instance:
   - Image: Ubuntu 22.04
   - Shape: VM.Standard.A1.Flex (ALWAYS FREE)
   - RAM: 24GB, CPU: 4 — completely free forever
4. Download SSH key
5. Get your VPS Public IP

6. Upload and deploy:
   scp -i your_key.pem -r ./ ubuntu@YOUR_IP:~/job-hunter-v3/
   ssh -i your_key.pem ubuntu@YOUR_IP
   cd job-hunter-v3
   ./setup.sh
   nano .env   ← fill keys
   ./start.sh

7. Access n8n from anywhere:
   http://YOUR_VPS_IP:5678
```

#### Easiest Alternative: Docker
```bash
# Make sure .env is filled first
docker-compose up -d

# View logs
docker-compose logs -f

# Agent restarts automatically if it crashes
# Survives reboots automatically
```

---

## 📊 What Happens Every 30 Minutes

```
Agent wakes up
  ↓
Scans 8 job sources (Reddit + Upwork)
  ↓
AI filters jobs matching your skills
  ↓
AI writes professional reply for each job
  ↓
Sends to ALL channels simultaneously:
  ├── 📲 Telegram  (instant, with reply)
  ├── 📱 WhatsApp  (quick alert)
  ├── 📧 Email     (full details + formatted reply)
  ├── 💬 SMS       (via carrier gateway, free)
  └── 📟 Textbelt  (SMS, 1 free per day)
  ↓
Logs job to logs/jobs_found.log
  ↓
Sleeps 30 mins → repeats forever
```

---

## 🛠 Commands

```bash
./start.sh          # Start everything
./stop.sh           # Stop everything
./setup.sh          # Re-run setup

tail -f logs/agent.log        # Watch live
cat  logs/jobs_found.log      # See all jobs found
tail -f logs/n8n.log          # n8n logs
```

---

## 💰 Expected Results

| Day | Jobs Found | Action | Earning |
|-----|-----------|--------|---------|
| 1 | 5–20 alerts | Reply to best ones | $0–$50 |
| 2 | 5–20 alerts | 1–2 clients reply | $30–$100 |
| 3 | 5–20 alerts | First payment | $50–$200 |
| Week 1 | 50–100+ | Multiple clients | $100–$500 |

---

Built with ❤️ for zero-investment freelancing
Stack: Python 3.10+ • n8n • Oracle Cloud Free • Telegram API • Callmebot
