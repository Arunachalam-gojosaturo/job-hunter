#!/bin/bash
echo "Stopping Job Hunter Agent..."
[ -f logs/n8n.pid   ] && kill $(cat logs/n8n.pid)   2>/dev/null && rm logs/n8n.pid   && echo "✓ n8n stopped"
[ -f logs/agent.pid ] && kill $(cat logs/agent.pid) 2>/dev/null && rm logs/agent.pid && echo "✓ Agent stopped"
echo "All stopped."
