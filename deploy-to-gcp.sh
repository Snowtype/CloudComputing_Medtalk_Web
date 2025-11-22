#!/bin/bash
# GCP VM에 Whisper API 서비스 배포 스크립트

set -e

VM_IP="34.71.58.225"
VM_USER="mk4434"
# API_KEY는 VM에서 직접 환경 변수로 설정!

echo "🚀 Deploying Whisper API to GCP VM"
echo "VM: ${VM_IP}"
echo ""

# 1. 파일 업로드
echo "📤 Uploading files..."
scp whisper-api-server.py ${VM_USER}@${VM_IP}:~/
scp requirements-whisper-api.txt ${VM_USER}@${VM_IP}:~/

# 2. VM에서 설정 및 실행
echo "⚙️  Setting up on VM..."
ssh ${VM_USER}@${VM_IP} << 'ENDSSH'
    echo "🔧 Installing dependencies..."
    sudo apt update -qq
    sudo apt install -y python3 python3-pip python3-venv

    echo "📁 Setting up project..."
    mkdir -p ~/whisper-service
    cd ~/whisper-service
    
    # 파일 이동
    mv ~/whisper-api-server.py ./ 2>/dev/null || true
    mv ~/requirements-whisper-api.txt ./ 2>/dev/null || true

    echo "🐍 Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    
    echo "📦 Installing Python packages..."
    pip install -q --upgrade pip
    pip install -q -r requirements-whisper-api.txt

    echo "✅ Setup complete!"
ENDSSH

echo ""
echo "✅ Files uploaded and environment set up!"
echo ""
echo "📝 Next steps:"
echo "1. SSH into VM:"
echo "   ssh ${VM_USER}@${VM_IP}"
echo ""
echo "2. Set API key and run:"
echo "   cd ~/whisper-service"
echo "   source venv/bin/activate"
echo "   export OPENAI_API_KEY=\"sk-proj-YOUR-API-KEY-HERE\""
echo "   PORT=8002 python whisper-api-server.py"
echo ""
echo "🌐 Service will be at: http://${VM_IP}:8002"

