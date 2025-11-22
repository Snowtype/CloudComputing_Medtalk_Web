#!/bin/bash
# Whisper API 서버 시작 스크립트

echo "🚀 Starting Whisper API Server..."

# 가상환경 활성화
source venv/bin/activate

# OpenAI API 키 확인
if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  Warning: OPENAI_API_KEY not set!"
    echo "Set it with: export OPENAI_API_KEY='sk-your-key'"
    echo ""
fi

# 서버 실행
python whisper-api-server.py

