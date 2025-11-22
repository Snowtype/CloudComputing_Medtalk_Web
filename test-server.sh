#!/bin/bash
# 테스트용 서버 시작 스크립트

cd "/Users/aidesigner/Columbia Univ Course/CloudComputing/WEBUI"

echo "🔧 Activating virtual environment..."
source venv/bin/activate

echo "🔑 Using your OpenAI API key..."
# OpenAI API 키는 터미널에서 미리 export 해주세요
# export OPENAI_API_KEY="sk-proj-..."
export PORT=8001

echo "🚀 Starting Whisper API Server on port 8001..."
echo "📝 API Docs: http://localhost:8001/docs"
echo "❤️  Health: http://localhost:8001/health"
echo ""

python whisper-api-server.py

