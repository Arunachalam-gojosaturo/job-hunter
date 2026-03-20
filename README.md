<div align="center">

<img src="https://capsule-render.vercel.app/api?type=cylinder&color=0:0d0a00,50:2d1f00,100:0d0a00&height=200&section=header&text=JOB%20HUNTER%20AGENT&fontSize=58&fontColor=f59e0b&fontAlignY=50&animation=fadeIn&desc=v3.0%20%7C%20Scan%20%E2%80%A2%20Filter%20%E2%80%A2%20Reply%20%E2%80%A2%20Alert%20%E2%80%A2%20Repeat%20%E2%80%A2%2024%2F7&descSize=15&descAlignY=72&descColor=78716c"/>

</div>

<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=JetBrains+Mono&weight=600&size=14&pause=900&color=F59E0B&center=true&vCenter=true&width=800&lines=INITIALIZING+JOB+HUNTER+AGENT+v3...;Connecting+to+Reddit+API...+%E2%9C%93;Connecting+to+Upwork+Scraper...+%E2%9C%93;Groq+%2F+OpenAI+%2F+Ollama+AI+Engine...+%E2%9C%93;Telegram+%7C+WhatsApp+%7C+Email+%7C+SMS...+%E2%9C%93;n8n+Workflow+Engine...+%E2%9C%93;%5B+ALL+SYSTEMS+ONLINE+%5D+Hunting+jobs+every+30+minutes." alt="Typing SVG"/>

</div>

<br/>

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-f59e0b?style=flat-square&logo=python&logoColor=black&labelColor=0d0a00)
![n8n](https://img.shields.io/badge/Workflow-n8n-f59e0b?style=flat-square&labelColor=0d0a00)
![AI](https://img.shields.io/badge/AI-Groq%20%7C%20OpenAI%20%7C%20Ollama-f59e0b?style=flat-square&labelColor=0d0a00)
![Cloud](https://img.shields.io/badge/Cloud-Oracle%20Always--Free-f59e0b?style=flat-square&labelColor=0d0a00)
![License](https://img.shields.io/badge/Cost-100%25%20FREE-22c55e?style=flat-square&labelColor=0d0a00)
![Status](https://img.shields.io/badge/Status-24%2F7%20ACTIVE-f59e0b?style=flat-square&labelColor=0d0a00)

</div>

---

## `>> WHAT DOES IT DO?`

```
Scans Reddit + Upwork every 30 minutes for jobs matching your skills.
AI reads each listing, decides if it's a match, writes a professional reply.
Fires alerts to ALL your devices simultaneously — even while your PC is OFF.
Zero cost. Zero babysitting. Just money in.
```

---

## `>> ALERT CHANNELS`

<div align="center">

| `CHANNEL` | `COST` | `SPEED` | `SETUP TIME` |
|---|:---:|:---:|:---:|
| 📲 Telegram Bot | `FREE forever` | Instant | 2 mins |
| 📱 WhatsApp (Callmebot) | `FREE` | ~30 sec | 3 mins |
| 📧 Gmail | `FREE` | ~1 min | 2 mins |
| 💬 SMS via Carrier Gateway | `FREE forever` | ~1 min | 1 min |
| 📟 Textbelt SMS | `FREE (1/day)` | Instant | 0 mins |

</div>

---

## `>> AGENT LOOP`

```
  ┌─────────────────────────────────────────────────────────────────────┐
  │                    AGENT WAKES EVERY 30 MINS                        │
  │                                                                      │
  │   [Reddit API]  ──┐                                                  │
  │   [Upwork]      ──┴──► [Job Aggregator] ──► [AI Filter + Scorer]   │
  │                                                    │                 │
  │                                             Skill match? YES        │
  │                                                    │                 │
  │                                          [AI Reply Generator]       │
  │                                                    │                 │
  │                         ┌─────────────────────────┤                 │
  │                         ▼         ▼         ▼     ▼                 │
  │                    Telegram   WhatsApp   Email   SMS                 │
  │                         │                                            │
  │                    logs/jobs_found.log ← archived                   │
  │                         │                                            │
  │                   sleeps 30 mins → repeats forever                  │
  └─────────────────────────────────────────────────────────────────────┘
```

---

## `>> SETUP — 10 STEPS TO GO LIVE`

### `STEP 1` — Clone & Prepare

```bash
git clone https://github.com/Arunachalam-gojosaturo/job-hunter-agent-v3
cd job-hunter-agent-v3
chmod +x setup.sh start.sh stop.sh start_cloud.sh
./setup.sh
```

---

### `STEP 2` — Telegram Bot `[FREE · 2 mins]`

```
1. Open Telegram → search @BotFather
2. Send: /newbot
3. Name it: JobHunterBot
4. Username: myjobhunter_bot
5. Copy the TOKEN

6. Get your Chat ID:
   - Send "hi" to your bot
   - Open: https://api.telegram.org/bot<TOKEN>/getUpdates
   - Find "chat":{"id": 123456789} — that's your CHAT_ID

7. Add to .env:
   TELEGRAM_BOT_TOKEN = your_token
   TELEGRAM_CHAT_ID   = your_chat_id
```

---

### `STEP 3` — WhatsApp via Callmebot `[FREE · 3 mins]`

```
1. Save +34 644 59 21 48 as "Callmebot" in contacts
2. WhatsApp them: "I allow callmebot to send me messages"
3. They'll reply with your API key

4. Add to .env:
   WHATSAPP_PHONE      = +91XXXXXXXXXX
   CALLMEBOT_API_KEY   = the_key_received
```

---

### `STEP 4` — Gmail Alerts `[FREE · 2 mins]`

```
1. Go to: https://myaccount.google.com/apppasswords
2. Select: Mail + Windows Computer → Generate
3. Copy the 16-char password (remove spaces)

4. Add to .env:
   GMAIL_USER          = your@gmail.com
   GMAIL_APP_PASSWORD  = abcdefghijklmnop
   ALERT_EMAIL         = your@gmail.com
```

---

### `STEP 5` — Free SMS via Carrier Gateway `[1 min]`

```bash
# Indian carriers — replace 9999999999 with your number:
Airtel  →  9999999999@airtelmail.in
Jio     →  9999999999@jio.com
Vi/Voda →  9999999999@vitext.com
BSNL    →  9999999999@bsnlmobile.in

# Add to .env:
SMS_GATEWAY_EMAIL  = 9999999999@jio.com
TEXTBELT_PHONE     = +919999999999
```

---

### `STEP 6` — AI Engine `[Pick One]`

```bash
# ── OPTION A: OpenAI (free credits for new accounts) ──────────────
# Go to: https://platform.openai.com → API Keys → Create key
# .env:
OPENAI_API_KEY = sk-...

# ── OPTION B: Ollama LOCAL (100% free forever, no internet) ───────
curl https://ollama.ai/install.sh | sh
ollama pull mistral

# .env:
USE_OLLAMA   = true
OLLAMA_MODEL = mistral

# ── OPTION C: Groq (free tier, ultra-fast) ────────────────────────
# Go to: https://console.groq.com → API Keys
# .env:
GROQ_API_KEY = gsk_...
```

---

### `STEP 7` — Fill Your Profile

```ini
YOUR_NAME      = Arunachalam
YOUR_SKILLS    = Full Stack Dev, Python, Linux, Cybersecurity, React, TypeScript
YOUR_DELIVERY  = 24 hours
YOUR_RATE      = Starting at $30
```

---

### `STEP 8` — Launch

```bash
./start.sh

# Monitor live:
tail -f logs/agent.log
cat  logs/jobs_found.log
```

---

### `STEP 9` — n8n Workflow

```
1. Open: http://localhost:5678
2. New account (first time only)
3. New Workflow → ⋮ → Import from File
4. Select: workflows/job_hunter_v3.json
5. Click "📧 Email Alert" node → add Gmail credential
6. Toggle RED → GREEN (top right)
7. Workflow is LIVE ✓
```

---

### `STEP 10` — Deploy 24/7 `[PC OFF]`

<div align="center">
<table>
<tr>
<td width="60%" valign="top">

#### ☁️ Oracle Cloud Always-Free VPS *(Recommended)*

```bash
# 1. Sign up: https://oracle.com/cloud/free
#    (free debit card verification only)
# 2. Create Instance:
#    Image : Ubuntu 22.04
#    Shape : VM.Standard.A1.Flex  ← FREE FOREVER
#    RAM   : 24 GB
#    CPU   : 4 cores

# 3. Upload + Deploy:
scp -i key.pem -r ./ ubuntu@VPS_IP:~/job-hunter-v3/
ssh -i key.pem ubuntu@VPS_IP
cd job-hunter-v3 && ./setup.sh
nano .env       # fill your keys
./start.sh      # agent is now live 24/7

# 4. Access n8n from anywhere:
#    http://YOUR_VPS_IP:5678
```

</td>
<td width="40%" valign="top">

#### 🐳 Docker *(Easiest)*

```bash
# Fill .env first, then:
docker-compose up -d

# Logs:
docker-compose logs -f

# Auto-restarts on crash ✓
# Survives reboots ✓
# Zero manual babysitting ✓
```

</td>
</tr>
</table>
</div>

---

## `>> COMMANDS`

```bash
./start.sh                    # Start all services
./stop.sh                     # Stop all services
./setup.sh                    # Re-run initial setup

tail -f logs/agent.log        # Watch live agent output
cat  logs/jobs_found.log      # All jobs found so far
tail -f logs/n8n.log          # n8n workflow engine logs
```

---

## `>> PROJECTED EARNINGS`

<div align="center">

| `TIMELINE` | `ALERTS` | `OUTCOME` | `EARNING` |
|:---:|:---:|---|:---:|
| Day 1 | 5–20 | Reply to best matches | `$0 – $50` |
| Day 2 | 5–20 | 1–2 clients respond | `$30 – $100` |
| Day 3 | 5–20 | First payment arrives | `$50 – $200` |
| Week 1 | 50–100+ | Multiple active clients | `$100 – $500` |

</div>

> ⚡ *Zero upfront cost. Runs while you sleep. Pays while you rice your desktop.*

---

## `>> TECH STACK`

<div align="center">

| `MODULE` | `TECH` | `PURPOSE` |
|---|---|---|
| 🔍 Job Scraping | `Reddit API + Upwork` | Source raw job listings |
| 🧠 AI Engine | `Groq / OpenAI / Ollama` | Filter + write replies |
| 🔁 Workflow | `n8n` | Orchestrate automation |
| 📲 Telegram | `Telegram Bot API` | Instant alerts with AI reply |
| 📱 WhatsApp | `Callmebot API` | Quick mobile alerts |
| 📧 Email | `Gmail SMTP` | Detailed formatted alerts |
| 💬 SMS | `Carrier Gateway + Textbelt` | No-app fallback alerts |
| ☁️ Hosting | `Oracle Cloud Free / Docker` | 24/7 with PC off |
| 🐍 Runtime | `Python 3.10+` | Agent core |

</div>

---

## `>> CREATOR`

<div align="center">

```
  BUILT BY   : ARUNACHALAM
  ALIAS      : gojosaturo
  BASE       : Vellore, Tamil Nadu 🇮🇳
  OS         : Arch Linux + Hyprland
  STACK      : Python · Node.js · Linux · AI · Cybersecurity
  MOTIVE     : Zero-investment freelancing on full autopilot.
```

[![GitHub](https://img.shields.io/badge/GITHUB-Arunachalam--gojosaturo-f59e0b?style=for-the-badge&logo=github&logoColor=black&labelColor=0d0a00)](https://github.com/Arunachalam-gojosaturo)
[![Instagram](https://img.shields.io/badge/INSTAGRAM-@saturogojo__ac-f59e0b?style=for-the-badge&logo=instagram&logoColor=black&labelColor=0d0a00)](https://instagram.com/saturogojo_ac)

</div>

---

<div align="center">

*Built for zero-investment freelancing. Fork it. Run it. Get paid.*

<img src="https://capsule-render.vercel.app/api?type=cylinder&color=0:0d0a00,50:2d1f00,100:0d0a00&height=90&section=footer&text=JOB+HUNTER+AGENT+v3+%7C+BUILT+BY+ARUNACHALAM&fontSize=14&fontColor=f59e0b&animation=fadeIn"/>

</div>
