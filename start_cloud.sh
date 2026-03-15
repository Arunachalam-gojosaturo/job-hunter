#!/bin/bash
mkdir -p logs
echo "Starting Python agent..."
python3 scripts/job_agent.py > logs/agent.log 2>&1 &
echo "Starting n8n..."
exec n8n start
