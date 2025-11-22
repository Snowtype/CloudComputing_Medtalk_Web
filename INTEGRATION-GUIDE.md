# 🔗 Whisper Transcription Service - Integration Guide

> **담당자**: 너의이름  
> **서비스**: 음성 → 텍스트 변환 (OpenAI Whisper API)  
> **포트**: 8002 (권장)

---

## 📋 서비스 개요

**기능**: 오디오 파일(mp3, wav, m4a 등)을 받아서 텍스트로 변환

**사용 기술**:

- **Backend**: FastAPI (Python 3.9+)
- **API Provider**: OpenAI Whisper API
- **Frontend**: Vanilla HTML/CSS/JavaScript (React 빌드 필요 없음)

**구조**:

```
WEBUI/
├── whisper-api-server.py       # FastAPI 백엔드
├── deployed-version/
│   ├── index.html              # 프로덕션 UI (GCP용)
│   └── index-local.html        # 로컬 테스트용
├── requirements-whisper-api.txt
└── venv/                       # Python 가상환경
```

---

## 🚀 API 엔드포인트

### **Base URL**

- **로컬**: `http://localhost:8002`
- **GCP**: `http://<VM_IP>:8002`

### **1. Health Check**

```bash
GET /health
```

**응답:**

```json
{
  "status": "healthy",
  "service": "transcription",
  "api_configured": true,
  "timestamp": "2025-11-22T..."
}
```

### **2. 음성 → 텍스트 변환 (Main API)**

```bash
POST /transcribe
Content-Type: multipart/form-data

Body:
  file: (audio file)
  language: "en" (optional)
  prompt: "medical context" (optional)
```

**응답 예시:**

```json
{
  "success": true,
  "text": "This is the transcribed text from the audio.",
  "language": "en",
  "filename": "audio.wav",
  "file_size_mb": 2.29,
  "model": "whisper-1",
  "provider": "OpenAI",
  "timestamp": "2025-11-22T12:00:00.000Z"
}
```

**에러 응답:**

```json
{
  "detail": "Error message here"
}
```

### **3. 일괄 처리 (Batch)**

```bash
POST /batch-transcribe
Content-Type: multipart/form-data

Body:
  files[]: (multiple audio files)
```

---

## 🔧 Composite Service에서 호출 방법

### **Python 예시:**

```python
import requests

def call_transcription_service(audio_file_path):
    url = "http://localhost:8002/transcribe"

    with open(audio_file_path, 'rb') as f:
        files = {'file': f}
        data = {'language': 'en'}

        response = requests.post(url, files=files, data=data)

        if response.status_code == 200:
            result = response.json()
            return result['text']
        else:
            raise Exception(f"Transcription failed: {response.text}")

# 사용 예시
text = call_transcription_service("audio.wav")
print(f"Transcribed: {text}")
```

### **JavaScript/Node.js 예시:**

```javascript
const FormData = require("form-data");
const fs = require("fs");
const axios = require("axios");

async function transcribeAudio(audioPath) {
  const form = new FormData();
  form.append("file", fs.createReadStream(audioPath));
  form.append("language", "en");

  const response = await axios.post("http://localhost:8002/transcribe", form, {
    headers: form.getHeaders(),
  });

  return response.data.text;
}
```

### **cURL 예시:**

```bash
curl -X POST http://localhost:8002/transcribe \
  -F "file=@audio.wav" \
  -F "language=en"
```

---

## ⚙️ 로컬 실행 방법

### **1. 패키지 설치**

```bash
cd WEBUI
python3 -m venv venv
source venv/bin/activate
pip install -r requirements-whisper-api.txt
```

### **2. 환경 변수 설정**

```bash
# OpenAI API 키 필수!
export OPENAI_API_KEY="sk-proj-..."
export PORT=8002
```

### **3. 서버 실행**

```bash
python whisper-api-server.py
```

**실행 확인:**

```
INFO:__main__:✅ OpenAI API key configured
INFO:__main__:🚀 Starting Whisper API Server on port 8002
INFO:     Uvicorn running on http://0.0.0.0:8002
```

---

## 🔑 OpenAI API 키 관리

**현재 상황**: 내(너의이름) API 키 사용 중

**옵션 1 - 공용 사용 (권장)**:

- 내 API 키 계속 사용
- 환경 변수로만 관리 (Git에 안 올림)
- 비용: 사용량 기준 청구 (Whisper는 저렴함)

**옵션 2 - 개별 발급**:

- https://platform.openai.com/api-keys
- 각자 발급해서 사용

**API 키 형식**:

```bash
export OPENAI_API_KEY="sk-proj-GtuD..."  # 실제 키
```

**보안 주의사항**:

- ✅ 환경 변수로만 관리
- ✅ `.gitignore`에 `.env` 추가됨
- ❌ 코드에 하드코딩 금지
- ❌ Git에 커밋 금지

---

## 🌐 GCP VM 배포

### **1. VM 준비**

```bash
# GCP VM SSH 접속
gcloud compute ssh <vm-name> --zone=us-central1-a

# 또는 브라우저 SSH 사용
```

### **2. 서버 설정**

```bash
# 시스템 업데이트
sudo apt update && sudo apt upgrade -y

# Python 설치
sudo apt install -y python3 python3-pip python3-venv

# 프로젝트 디렉토리
mkdir -p ~/whisper-service
cd ~/whisper-service
```

### **3. 파일 업로드**

```bash
# 로컬에서 실행
scp whisper-api-server.py <user>@<VM_IP>:~/whisper-service/
scp requirements-whisper-api.txt <user>@<VM_IP>:~/whisper-service/
```

### **4. VM에서 실행**

```bash
cd ~/whisper-service

# 가상환경 생성
python3 -m venv venv
source venv/bin/activate

# 패키지 설치
pip install -r requirements-whisper-api.txt

# 환경 변수 설정
export OPENAI_API_KEY="sk-proj-..."
export PORT=8002

# 백그라운드 실행
nohup python whisper-api-server.py > server.log 2>&1 &

# 로그 확인
tail -f server.log
```

### **5. 방화벽 설정**

```bash
# GCP 방화벽 규칙 추가
gcloud compute firewall-rules create allow-whisper-api \
    --allow tcp:8002 \
    --source-ranges 0.0.0.0/0 \
    --description "Allow Whisper API access"
```

---

## 🧪 테스트 방법

### **1. Health Check**

```bash
curl http://<VM_IP>:8002/health
```

### **2. Transcription Test**

```bash
# 테스트 오디오 파일로
curl -X POST http://<VM_IP>:8002/transcribe \
  -F "file=@test.wav" \
  -F "language=en"
```

### **3. Swagger UI**

브라우저에서:

```
http://<VM_IP>:8002/docs
```

---

## 📊 Composite Service 통합 시 고려사항

### **1. 에러 처리**

```python
try:
    response = requests.post(url, files=files, timeout=60)
    response.raise_for_status()
    result = response.json()
except requests.exceptions.Timeout:
    # 타임아웃 처리 (큰 파일은 시간 오래 걸림)
    pass
except requests.exceptions.HTTPError as e:
    # HTTP 에러 처리
    error_detail = e.response.json().get('detail')
    pass
```

### **2. 파일 크기 제한**

- **최대**: 25MB
- 초과 시 `413 Payload Too Large` 에러

### **3. 지원 포맷**

- mp3, mp4, mpeg, mpga, m4a, wav, webm, ogg, flac

### **4. 응답 시간**

- 짧은 오디오 (< 1분): 2-5초
- 긴 오디오 (5분+): 10-30초
- **타임아웃 설정**: 최소 60초 권장

### **5. CORS**

- 이미 모든 origin 허용됨 (`allow_origins=["*"]`)
- 프로덕션에서는 특정 도메인만 허용 권장

### **6. 비용**

- Whisper API: $0.006 / 분
- 예: 1시간 오디오 = $0.36

---

## 🐛 문제 해결

### **"Connection refused"**

→ 서버 실행 중인지 확인: `ps aux | grep whisper-api-server`

### **"OpenAI API key not configured"**

→ 환경 변수 설정: `export OPENAI_API_KEY="sk-proj-..."`

### **"Unsupported file format"**

→ 지원 포맷 확인: mp3, wav, m4a, webm, ogg, flac

### **500 Internal Server Error**

→ 서버 로그 확인: `tail -f server.log` 또는 `tail -f nohup.out`

---

## 📞 연락처

**담당자**: 너의이름  
**Email**: your.email@columbia.edu  
**Slack/WhatsApp**: @yourhandle

**이슈 발생 시**:

1. 로그 파일 확인 (`server.log`)
2. 위 "문제 해결" 섹션 참고
3. 안되면 연락 주세요!

---

## 📚 참고 자료

- **OpenAI Whisper API 문서**: https://platform.openai.com/docs/guides/speech-to-text
- **FastAPI 문서**: https://fastapi.tiangolo.com/
- **Swagger UI**: `http://localhost:8002/docs` (서버 실행 후)
