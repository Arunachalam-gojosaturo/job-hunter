#!/bin/bash
G='\033[0;32m'; C='\033[0;36m'; Y='\033[1;33m'; N='\033[0m'

echo -e "${C}Starting Job Hunter Agent v3...${N}"
mkdir -p logs

# Load env
set -a; [ -f .env ] && source .env; set +a

# Start n8n
echo -e "${Y}Starting n8n...${N}"
nohup n8n start > logs/n8n.log 2>&1 &
echo $! > logs/n8n.pid

sleep 4

# Start Python agent
echo -e "${Y}Starting Python scanner...${N}"
nohup python3 scripts/job_agent.py > logs/agent.log 2>&1 &
echo $! > logs/agent.pid

echo -e "${G}"
echo "╔══════════════════════════════════════════╗"
echo "║        ALL AGENTS RUNNING 🚀             ║"
echo "╠══════════════════════════════════════════╣"
echo "║  n8n:    http://localhost:5678           ║"
echo "║  Logs:   tail -f logs/agent.log          ║"
echo "║  Stop:   ./stop.sh                       ║"
echo "╚══════════════════════════════════════════╝"
echo -e "${N}"
