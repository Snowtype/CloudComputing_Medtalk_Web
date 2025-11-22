# 🎤 MedTalk Assist - Whisper 음성인식 서비스

**OpenAI Whisper API를 사용한 음성→텍스트 변환 마이크로서비스**

---

## ✅ 배포 완료!

### 🌐 **현재 운영 중인 서비스**

- **프로덕션 API**: `http://34.71.58.225:8000`
- **웹 인터페이스**: `http://34.71.58.225:5000`
- **API 문서**: `http://34.71.58.225:8000/docs`
- **상태 확인**: `http://34.71.58.225:8000/health`

### 📊 **서버 정보**

- **GCP VM**: whisper-ai-web (34.71.58.225)
- **리전**: us-central1
- **OS**: Debian 12
- **포트**: 8000 (API), 5000 (Web UI)

---

## 🎯 지환님 - Composite Service 연동 가이드

### 1️⃣ **API 테스트**

브라우저나 터미널에서:

```bash
# 상태 확인
curl http://34.71.58.225:8000/health

# 응답 예시:
# {"status":"healthy","service":"transcription","api_configured":true,"timestamp":"..."}
```

### 2️⃣ **음성 파일 전송**

```bash
curl -X POST http://34.71.58.225:8000/transcribe \
  -F "file=@음성파일.wav" \
  -F "language=en"
```

**응답 (JSON):**

```json
{
  "success": true,
  "text": "음성에서 변환된 텍스트 내용입니다.",
  "language": "en",
  "filename": "음성파일.wav",
  "file_size_mb": 2.5,
  "model": "whisper-1",
  "provider": "OpenAI",
  "timestamp": "2025-11-22T10:30:00.000000Z"
}
```

### 3️⃣ **Python 연동 예제**

```python
import requests

def transcribe_audio(audio_file_path):
    """음성 파일을 텍스트로 변환"""
    url = "http://34.71.58.225:8000/transcribe"

    with open(audio_file_path, 'rb') as f:
        files = {'file': f}
        data = {'language': 'en'}  # 선택사항 (자동 감지 가능)

        response = requests.post(url, files=files, data=data)

    if response.status_code == 200:
        result = response.json()
        return result['text']  # 변환된 텍스트 반환
    else:
        raise Exception(f"변환 실패: {response.text}")

# 사용 예시
transcribed_text = transcribe_audio("환자대화.wav")
print(transcribed_text)
```

### 4️⃣ **JavaScript/Node.js 연동 예제**

```javascript
const FormData = require("form-data");
const fs = require("fs");
const axios = require("axios");

async function transcribeAudio(audioFilePath) {
  const form = new FormData();
  form.append("file", fs.createReadStream(audioFilePath));
  form.append("language", "en");

  const response = await axios.post(
    "http://34.71.58.225:8000/transcribe",
    form,
    {
      headers: form.getHeaders(),
    }
  );

  return response.data.text;
}

// 사용 예시
transcribeAudio("환자대화.wav")
  .then((text) => console.log(text))
  .catch((error) => console.error(error));
```

---

## 📋 API 명세

### **POST /transcribe**

음성 파일을 텍스트로 변환합니다.

**요청 파라미터:**

- `file` (필수): 음성 파일 (multipart/form-data)
  - 지원 형식: MP3, WAV, M4A, MPEG, MPGA, WebM, OGG, FLAC
  - 최대 크기: 25MB
- `language` (선택): 언어 코드 (예: `en`, `ko`, `es`, `fr`)
  - 미지정 시 자동 감지
- `prompt` (선택): 컨텍스트 힌트 (정확도 향상용)

**응답 (성공 - HTTP 200):**

```json
{
  "success": true,
  "text": "변환된 텍스트",
  "language": "en",
  "filename": "audio.wav",
  "file_size_mb": 2.5,
  "model": "whisper-1",
  "provider": "OpenAI",
  "timestamp": "2025-11-22T10:30:00.000000Z"
}
```

**응답 (에러 - HTTP 4xx/5xx):**

```json
{
  "detail": "에러 메시지 설명"
}
```

### **GET /health**

서비스 상태를 확인합니다.

**응답:**

```json
{
  "status": "healthy",
  "service": "transcription",
  "api_configured": true,
  "timestamp": "2025-11-22T10:30:00.000000"
}
```

### **POST /batch-transcribe**

여러 음성 파일을 한 번에 변환합니다.

**요청 파라미터:**

- `files` (필수): 여러 개의 음성 파일

**응답:**

```json
{
  "batch_results": [
    { "filename": "file1.wav", "success": true, "result": {...} },
    { "filename": "file2.wav", "success": true, "result": {...} }
  ],
  "total_files": 2,
  "successful": 2,
  "failed": 0,
  "timestamp": "2025-11-22T10:30:00.000000Z"
}
```

---

## 📂 프로젝트 구조

```
WEBUI/
├── whisper-api-server.py          # FastAPI 백엔드 서버
├── requirements-whisper-api.txt   # Python 패키지 목록
├── deployed-version/
│   └── index.html                 # 웹 UI (프로덕션)
├── venv/                          # Python 가상환경 (로컬 개발용)
└── README.md                      # 이 파일
```

---

## 🛠 기술 스택

- **백엔드**: FastAPI 0.115.6
- **서버**: Uvicorn 0.34.0
- **AI 모델**: OpenAI Whisper API (whisper-1)
- **언어**: Python 3.11
- **배포**: GCP Compute Engine (Debian 12)
- **프론트엔드**: Vanilla HTML/CSS/JavaScript

---

## 💻 로컬 개발 환경 설정

### 사전 준비

- Python 3.11+
- OpenAI API 키 (read-only 권한이면 충분)

### 설치 및 실행

```bash
# 저장소 클론
git clone https://github.com/Snowtype/CloudComputing_Medtalk_Web.git
cd CloudComputing_Medtalk_Web

# 가상환경 생성
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 패키지 설치
pip install -r requirements-whisper-api.txt

# API 키 설정 (본인의 OpenAI API 키로 교체)
export OPENAI_API_KEY="sk-proj-your-api-key-here"

# 서버 실행
python3 whisper-api-server.py
```

서버가 시작되면:

- **API**: `http://localhost:8000`
- **문서**: `http://localhost:8000/docs`
- **상태**: `http://localhost:8000/health`

### 웹 UI 로컬 실행

```bash
# deployed-version 디렉토리에서
cd deployed-version
python3 -m http.server 8080

# 브라우저에서 http://localhost:8080 접속
```

**주의**: 로컬 테스트 시 `index.html`의 API URL을 `http://localhost:8000`으로 수정 필요

---

## 🌐 GCP 프로덕션 배포 정보

### 현재 배포 상태

- **VM 인스턴스**: `whisper-ai-web`
- **외부 IP**: `34.71.58.225`
- **리전**: us-central1
- **머신 타입**: e2-micro
- **OS**: Debian 12

### 실행 중인 서비스

**1. 백엔드 API (포트 8000)**

- 경로: `/home/mk4434/whisper-service/`
- 실행 방법: `nohup python3 whisper-api-server.py &`
- 로그: `~/whisper-service/server.log`

**2. 프론트엔드 Web UI (포트 5000)**

- 경로: `/home/aidesigner/medtalk-project/`
- 실행 방법: `npx serve -s . -p 5000`
- 로그: `~/medtalk-project/server.log`

### 방화벽 설정

- **포트 8000**: Whisper API (외부 접근 가능)
- **포트 5000**: Web UI (외부 접근 가능)
- **포트 22**: SSH (관리용)

---

## 🔐 보안

- ✅ OpenAI API 키는 **읽기 전용** (안전)
- ✅ API 키는 **환경 변수**로 관리 (코드에 없음)
- ✅ API 키는 **Git에 커밋 안 됨** (`.gitignore` 보호)
- ✅ CORS 활성화 (크로스 도메인 요청 지원)
- ⚠️ 프로덕션 API는 **공개 접근** (민감한 데이터는 인증 추가 권장)

---

## 📊 모니터링 & 로그

### 백엔드 상태 확인

```bash
# VM SSH 접속
gcloud compute ssh whisper-ai-web --zone=us-central1-a

# 서버 실행 확인
ps aux | grep whisper-api-server

# 로그 확인
tail -f ~/whisper-service/server.log

# 헬스 체크
curl http://localhost:8000/health
```

### 프론트엔드 상태 확인

```bash
# 서버 실행 확인
ps aux | grep "npx serve"

# 로그 확인
tail -f ~/medtalk-project/server.log
```

---

## 🐛 문제 해결

### API가 응답하지 않을 때

```bash
# 백엔드 재시작
cd ~/whisper-service
source venv/bin/activate
export OPENAI_API_KEY="your-key-here"
nohup python3 whisper-api-server.py > server.log 2>&1 &
```

### Web UI가 로딩되지 않을 때

```bash
# 프론트엔드 재시작
cd ~/medtalk-project
pkill -f "npx serve"
nohup npx serve -s . -p 5000 > server.log 2>&1 &
```

### 방화벽 문제

```bash
# 방화벽 규칙 확인
gcloud compute firewall-rules list | grep whisper

# 방화벽 규칙 추가 (필요시)
gcloud compute firewall-rules create allow-whisper-8000 \
    --allow tcp:8000 \
    --source-ranges 0.0.0.0/0
```

---

## 🤝 팀 연동 가이드 (지환님용)

### Composite Service에서 필요한 것

1. **Endpoint URL**
   ```
   http://34.71.58.225:8000/transcribe
   ```

2. **음성 파일**
   - 사용자/시스템에서 받은 오디오 파일

3. **HTTP 클라이언트**
   - Python: `requests`
   - Node.js: `axios`, `node-fetch`
   - Java: `HttpClient`, `OkHttp`

### 받을 수 있는 것

- ✅ 변환된 텍스트 (`result['text']`)
- ✅ 감지된 언어 (`result['language']`)
- ✅ 파일 메타데이터 (크기, 이름)
- ✅ 타임스탬프

### 에러 처리

| HTTP 코드 | 의미 | 대응 방법 |
|-----------|------|-----------|
| 200 | 성공 | `response.json()['text']` 사용 |
| 400 | 잘못된 요청 | 파일 형식/크기 확인 |
| 413 | 파일 너무 큼 | 25MB 이하로 제한 |
| 500 | 서버 에러 | 로그 확인 필요 |
| 502 | OpenAI API 에러 | Rate limit, API 장애 등 |

---

## 📞 연락처

- **GitHub**: [CloudComputing_Medtalk_Web](https://github.com/Snowtype/CloudComputing_Medtalk_Web)
- **Issues**: GitHub Issue 또는 팀 채팅으로 문의

---

## 📝 완료된 작업

- ✅ OpenAI Whisper API 연동
- ✅ FastAPI 백엔드 구현
- ✅ Web UI 프론트엔드 구현
- ✅ GCP VM 배포 완료
- ✅ 방화벽 설정 완료
- ✅ 실제 음성 파일 테스트 완료
- ✅ Composite Service 연동 준비 완료

---

**최종 업데이트**: 2025년 11월 22일  
**상태**: ✅ 프로덕션 운영 중  
**버전**: 1.0.0
