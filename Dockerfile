FROM node:20-slim
RUN apt-get update && apt-get install -y python3 python3-pip curl && rm -rf /var/lib/apt/lists/*
RUN npm install -g n8n
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --break-system-packages -r requirements.txt || pip3 install -r requirements.txt
COPY . .
RUN mkdir -p logs && chmod +x start_cloud.sh
EXPOSE 5678
HEALTHCHECK --interval=30s --timeout=10s CMD curl -f http://localhost:5678/healthz || exit 1
CMD ["./start_cloud.sh"]
