#!/bin/bash
# ═══════════════════════════════════════════
#   JOB HUNTER AGENT v3 — ONE CLICK SETUP
# ═══════════════════════════════════════════

G='\033[0;32m'; C='\033[0;36m'; Y='\033[1;33m'; R='\033[0;31m'; N='\033[0m'

echo -e "${C}"
echo "╔══════════════════════════════════════════╗"
echo "║   JOB HUNTER AGENT v3 — SETUP 🚀         ║"
echo "║   Telegram + WhatsApp + Email + SMS      ║"
echo "╚══════════════════════════════════════════╝"
echo -e "${N}"

# ── Detect OS ───────────────────────────────
if   [ -f /etc/arch-release ];    then OS="arch"
elif [ -f /etc/debian_version ];  then OS="debian"
elif [ -f /etc/redhat-release ];  then OS="redhat"
else OS="unknown"; fi

echo -e "${Y}Detected OS: $OS${N}"

# ── Install Node + Python ────────────────────
echo -e "${Y}[1/5] Installing system packages...${N}"
if [ "$OS" = "arch" ]; then
    sudo pacman -Sy --noconfirm nodejs npm python python-pip docker docker-compose 2>/dev/null
elif [ "$OS" = "debian" ]; then
    sudo apt-get update -q
    sudo apt-get install -y nodejs npm python3 python3-pip docker.io docker-compose curl 2>/dev/null
fi
echo -e "${G}✓ System packages ready${N}"

# ── Install n8n ──────────────────────────────
echo -e "${Y}[2/5] Installing n8n...${N}"
sudo npm install -g n8n 2>/dev/null
echo -e "${G}✓ n8n installed${N}"

# ── Python deps ──────────────────────────────
echo -e "${Y}[3/5] Installing Python packages...${N}"
pip install requests python-dotenv schedule feedparser --break-system-packages 2>/dev/null || \
pip3 install requests python-dotenv schedule feedparser 2>/dev/null
echo -e "${G}✓ Python packages ready${N}"

# ── Config ───────────────────────────────────
echo -e "${Y}[4/5] Creating config...${N}"
if [ ! -f .env ]; then
    cp config/.env.template .env
    echo -e "${Y}⚠  .env created — fill your keys before starting!${N}"
else
    echo -e "${G}✓ .env already exists${N}"
fi

# ── Systemd services ─────────────────────────
echo -e "${Y}[5/5] Setting up auto-start services...${N}"

sudo tee /etc/systemd/system/job-hunter-n8n.service > /dev/null << EOF
[Unit]
Description=Job Hunter n8n
After=network.target
[Service]
Type=simple
User=$USER
WorkingDirectory=$(pwd)
ExecStart=$(which n8n) start
Restart=always
RestartSec=10
Environment=N8N_PORT=5678
[Install]
WantedBy=multi-user.target
EOF

sudo tee /etc/systemd/system/job-hunter-agent.service > /dev/null << EOF
[Unit]
Description=Job Hunter Python Agent
After=network.target
[Service]
Type=simple
User=$USER
WorkingDirectory=$(pwd)
ExecStart=$(which python3) scripts/job_agent.py
Restart=always
RestartSec=15
[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable job-hunter-n8n job-hunter-agent
echo -e "${G}✓ Auto-start on boot enabled${N}"

mkdir -p logs
echo -e "${G}"
echo "╔══════════════════════════════════════════╗"
echo "║          SETUP COMPLETE ✅               ║"
echo "╠══════════════════════════════════════════╣"
echo "║  NEXT:                                   ║"
echo "║  1. nano .env  ← fill your API keys      ║"
echo "║  2. ./start.sh ← start everything        ║"
echo "║  3. localhost:5678 ← open n8n            ║"
echo "║  4. Import workflows/job_hunter_v3.json  ║"
echo "║  5. Click ACTIVATE toggle in n8n         ║"
echo "╚══════════════════════════════════════════╝"
echo -e "${N}"
