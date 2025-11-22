#!/bin/bash

# GCP VM에 Whisper API 서비스 배포

set -e

# 설정 (여기 수정하세요!)

VM_NAME="whisper-ai-web" # VM 이름
ZONE="us-central1-a" # Zone
VM_USER="mk4434" # SSH 사용자명
SERVICE_PORT=8002 # 서비스 포트

echo "🚀 Deploying Whisper API Service to GCP VM..."
echo "VM: $VM_NAME ($ZONE)"
echo "Port: $SERVICE_PORT"
echo ""

# 1. VM 외부 IP 가져오기

VM_IP=$(gcloud compute instances describe $VM_NAME --zone=$ZONE \
 --format='get(networkInterfaces[0].accessConfigs[0].natIP)')

echo "📍 VM IP: $VM_IP"
echo ""

# 2. 파일 업로드

echo "📤 Uploading files..."
scp whisper-api-server.py ${VM_USER}@${VM_IP}:~/
scp requirements-whisper-api.txt ${VM_USER}@${VM_IP}:~/

# 3. VM에서 설정 실행

echo "⚙️ Setting up on VM..."
gcloud compute ssh ${VM_NAME} --zone=${ZONE} --command="
echo '🔧 Installing dependencies...'
sudo apt update -qq
sudo apt install -y python3 python3-pip python3-venv

    echo '📁 Creating project directory...'
    mkdir -p ~/whisper-service
    mv ~/whisper-api-server.py ~/whisper-service/
    mv ~/requirements-whisper-api.txt ~/whisper-service/
    cd ~/whisper-service

    echo '🐍 Setting up Python virtual environment...'
    python3 -m venv venv
    source venv/bin/activate
    pip install -q --upgrade pip
    pip install -q -r requirements-whisper-api.txt

    echo '✅ Setup complete!'

"

# 4. 방화벽 규칙 확인/추가

echo "🔥 Checking firewall rules..."
if ! gcloud compute firewall-rules describe allow-whisper-api-${SERVICE_PORT} &>/dev/null; then
    echo "Creating firewall rule..."
    gcloud compute firewall-rules create allow-whisper-api-${SERVICE_PORT} \
 --allow tcp:${SERVICE_PORT} \
 --source-ranges 0.0.0.0/0 \
 --description "Allow Whisper API on port ${SERVICE_PORT}"
else
echo "Firewall rule already exists ✅"
fi

echo ""
echo "✅ Deployment complete!"
echo ""
echo "📝 Next steps:"
echo "1. SSH into VM: gcloud compute ssh $VM_NAME --zone=$ZONE"
echo "2. Set API key: export OPENAI_API_KEY='sk-proj-...'"
echo "3. Run server: cd ~/whisper-service && source venv/bin/activate && PORT=$SERVICE_PORT python whisper-api-server.py"
echo ""
echo "🌐 Service will be available at: http://${VM_IP}:${SERVICE_PORT}"
echo "📚 API docs: http://${VM_IP}:${SERVICE_PORT}/docs"
