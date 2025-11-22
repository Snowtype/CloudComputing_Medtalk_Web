#!/bin/bash
# Whisper API 테스트 스크립트

# API 키는 환경 변수에서 가져오기
# export OPENAI_API_KEY="your-api-key-here"
PORT=8002

echo "🧪 Testing Whisper API Transcription Service"
echo "=============================================="
echo ""

# 1. Health Check
echo "1️⃣ Health Check..."
curl -s http://localhost:$PORT/health | jq '.'
echo ""

# 2. Root endpoint
echo "2️⃣ Service Info..."
curl -s http://localhost:$PORT/ | jq '.'
echo ""

echo "3️⃣ Ready to test transcription!"
echo ""
echo "📝 You can test with a real audio file using:"
echo "   curl -X POST http://localhost:$PORT/transcribe \\"
echo "     -F \"file=@your_audio.wav\" \\"
echo "     -F \"language=en\""
echo ""
echo "Or use the browser UI at: http://localhost:8080/index-local.html"

