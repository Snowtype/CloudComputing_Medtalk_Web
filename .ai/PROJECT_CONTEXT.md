# 🤖 AI Context: MedTalk Assist - Whisper Transcription Service

> **이 문서는 AI가 프로젝트를 빠르게 이해하고 작업을 이어갈 수 있도록 작성된 컨텍스트 문서입니다.**

---

## 📋 프로젝트 개요

**이름**: MedTalk Assist - Whisper Transcription Microservice  
**목적**: 의료 오디오 녹음을 텍스트로 변환하는 마이크로서비스  
**역할**: 팀 프로젝트에서 음성→텍스트 변환 담당  
**상태**: ✅ 프로덕션 배포 완료 (GCP VM)

### 핵심 기능

1. **음성 파일 업로드** → OpenAI Whisper API 호출 → **텍스트 반환**
2. 지원 형식: MP3, WAV, M4A, WebM, OGG, FLAC (최대 25MB)
3. 다국어 지원 (자동 감지 또는 수동 지정)
4. RESTful API + 웹 UI 제공

---

## 🏗 시스템 아키텍처

### 구조

```
┌─────────────────────────────────────────┐
│  GCP VM (34.71.58.225)                  │
│                                         │
│  ┌──────────────────────────────────┐  │
│  │ Frontend Web UI (Port 5000)      │  │
│  │ - Vanilla HTML/CSS/JS            │  │
│  │ - /home/aidesigner/medtalk-*     │  │
│  └──────────────────────────────────┘  │
│            │                            │
│            ▼ HTTP Request               │
│  ┌──────────────────────────────────┐  │
│  │ Backend API (Port 8000)          │  │
│  │ - FastAPI + Uvicorn              │  │
│  │ - /home/mk4434/whisper-service/  │  │
│  └──────────────────────────────────┘  │
│            │                            │
│            ▼ API Call                   │
│  ┌──────────────────────────────────┐  │
│  │ OpenAI Whisper API               │  │
│  │ - External Service               │  │
│  └──────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

### 기술 스택

| 구분 | 기술 |
|------|------|
| **Backend** | Python 3.11, FastAPI 0.115.6, Uvicorn 0.34.0 |
| **AI Model** | OpenAI Whisper API (whisper-1) |
| **Frontend** | Vanilla HTML/CSS/JavaScript |
| **Deployment** | GCP Compute Engine (Debian 12, e2-micro) |
| **Version Control** | Git, GitHub (CloudComputing_Medtalk_Web) |

---

## 📁 파일 구조 및 역할

```
WEBUI/
├── .ai/                           # AI 컨텍스트 문서 (이 디렉토리)
│   ├── PROJECT_CONTEXT.md         # 프로젝트 전체 개요 (현재 파일)
│   ├── ARCHITECTURE.md            # 상세 아키텍처 설명
│   ├── DEPLOYMENT_HISTORY.md      # 배포 이력 및 변경사항
│   └── WORK_LOG.md                # 작업 일지
│
├── whisper-api-server.py          # 메인 FastAPI 백엔드 서버
│   - POST /transcribe: 음성 → 텍스트 변환
│   - POST /batch-transcribe: 여러 파일 동시 처리
│   - GET /health: 서비스 상태 확인
│   - GET /: API 정보
│
├── requirements-whisper-api.txt   # Python 패키지 의존성
│   - fastapi==0.115.6
│   - uvicorn==0.34.0
│   - openai==1.57.4
│   - python-multipart==0.0.20
│   - python-dotenv==1.0.1
│
├── deployed-version/
│   └── index.html                 # 웹 UI (프로덕션)
│       - 파일 업로드 UI
│       - 실시간 transcription 결과 표시
│       - 서비스 상태 체크
│
├── venv/                          # Python 가상환경 (로컬 개발용)
│   └── .gitignore                 # venv 제외 설정
│
├── .gitignore                     # Git 제외 파일 목록
│   - .env, *.env, api_keys.txt
│   - 민감한 정보 보호
│
└── README.md                      # 사용자용 문서
    - 지환님(팀원)을 위한 API 연동 가이드
```

---

## 🔑 핵심 엔드포인트

### **POST /transcribe**

**용도**: 음성 파일을 텍스트로 변환

**요청**:
```http
POST http://34.71.58.225:8000/transcribe
Content-Type: multipart/form-data

file: [audio_file]
language: "en" (optional)
```

**응답**:
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

### **GET /health**

**용도**: 서비스 상태 확인

**응답**:
```json
{
  "status": "healthy",
  "service": "transcription",
  "api_configured": true,
  "timestamp": "2025-11-22T10:30:00.000000"
}
```

---

## 🔐 환경 변수 및 보안

### 필수 환경 변수

```bash
OPENAI_API_KEY="sk-proj-..."  # OpenAI API 키 (read-only)
PORT=8000                      # 서버 포트 (선택사항, 기본값: 8000)
```

### 보안 정책

- ✅ API 키는 **환경 변수**로만 관리 (코드에 하드코딩 금지)
- ✅ `.gitignore`에 `.env`, `api_keys.txt` 등록
- ✅ OpenAI API 키는 **read-only 권한** 사용 (안전)
- ✅ GitHub Push Protection 통과 (민감 정보 차단)
- ⚠️ 프로덕션 API는 현재 공개 (필요시 인증 레이어 추가 고려)

---

## 🌐 프로덕션 배포 정보

### GCP VM 상세

- **인스턴스명**: whisper-ai-web
- **외부 IP**: 34.71.58.225
- **리전**: us-central1
- **머신 타입**: e2-micro (2 vCPU, 1GB RAM)
- **OS**: Debian 12 (Bookworm)
- **디스크**: 10GB SSD

### 실행 중인 프로세스

#### 1. Backend API (Port 8000)
```bash
# 위치: /home/mk4434/whisper-service/
# 실행 명령:
cd ~/whisper-service
source venv/bin/activate
export OPENAI_API_KEY="sk-proj-..."
nohup python3 whisper-api-server.py > server.log 2>&1 &

# 로그: ~/whisper-service/server.log
# 프로세스 확인: ps aux | grep whisper-api-server
```

#### 2. Frontend Web UI (Port 5000)
```bash
# 위치: /home/aidesigner/medtalk-project/
# 실행 명령:
cd ~/medtalk-project
nohup npx serve -s . -p 5000 > server.log 2>&1 &

# 로그: ~/medtalk-project/server.log
# 프로세스 확인: ps aux | grep "npx serve"
```

### 방화벽 규칙

```bash
# Port 8000: Whisper API
gcloud compute firewall-rules create allow-whisper-8000 \
    --allow tcp:8000 \
    --source-ranges 0.0.0.0/0

# Port 5000: Web UI (이미 열려있음)
# Port 22: SSH (기본)
```

---

## 👥 팀 구조 및 연동

### 역할 분담

- **나 (현재 개발자)**: Whisper 음성인식 마이크로서비스
- **지환님**: Composite Service (모든 마이크로서비스 통합)
- **다른 팀원들**: Summarization, Patient Records 등 다른 마이크로서비스

### 연동 방식

지환님의 Composite Service에서:
```python
import requests

# 우리 서비스 호출
response = requests.post(
    'http://34.71.58.225:8000/transcribe',
    files={'file': audio_file},
    data={'language': 'en'}
)
transcribed_text = response.json()['text']
```

---

## 🛠 로컬 개발 가이드

### 초기 설정

```bash
# 1. Clone
git clone https://github.com/Snowtype/CloudComputing_Medtalk_Web.git
cd CloudComputing_Medtalk_Web

# 2. 가상환경 생성
python3 -m venv venv
source venv/bin/activate

# 3. 패키지 설치
pip install -r requirements-whisper-api.txt

# 4. 환경 변수 설정
export OPENAI_API_KEY="sk-proj-your-key-here"

# 5. 서버 실행
python3 whisper-api-server.py
```

### 테스트

```bash
# Health check
curl http://localhost:8000/health

# Transcription test
curl -X POST http://localhost:8000/transcribe \
  -F "file=@test_audio.wav" \
  -F "language=en"
```

### 웹 UI 로컬 실행

```bash
cd deployed-version
python3 -m http.server 8080
# 브라우저: http://localhost:8080
```

---

## 🐛 자주 발생하는 문제 및 해결

### 1. OpenAI API 버전 호환성 문제

**증상**: `ImportError: cannot import name 'OpenAI'`

**원인**: `openai` 패키지 버전 불일치

**해결**:
```bash
pip install --upgrade openai==1.57.4
```

### 2. httpx 프록시 에러

**증상**: `TypeError: Client.__init__() got an unexpected keyword argument 'proxies'`

**원인**: `openai` 1.35.1 이하 버전과 최신 `httpx` 충돌

**해결**: requirements-whisper-api.txt에서 `openai>=1.57.4` 사용

### 3. 포트 충돌

**증상**: `[Errno 48] Address already in use`

**해결**:
```bash
# 기존 프로세스 종료
pkill -f whisper-api-server

# 다른 포트 사용
PORT=8001 python3 whisper-api-server.py
```

### 4. SSL Certificate 에러 (pip install)

**증상**: `SSL: CERTIFICATE_VERIFY_FAILED`

**해결**:
```bash
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements-whisper-api.txt
```

### 5. Debian venv 에러

**증상**: `ensurepip is not available`

**해결**:
```bash
sudo apt update
sudo apt install -y python3.11-venv
python3 -m venv venv
```

---

## 📊 성능 및 제약사항

### OpenAI Whisper API 제약

- 파일 크기: 최대 25MB
- 지원 형식: MP3, MP4, MPEG, MPGA, M4A, WAV, WebM, OGG, FLAC
- Rate Limit: API 키 플랜에 따라 다름
- 비용: 분당 $0.006 (2025년 기준)

### GCP VM 제약

- e2-micro (1GB RAM): 무료 티어
- 동시 처리: 메모리 부족 주의
- 네트워크: 기본 1Gbps

---

## 🚀 향후 개선 사항

### 우선순위 높음

- [ ] API 인증/인가 추가 (JWT 또는 API Key)
- [ ] Rate Limiting (악용 방지)
- [ ] 로깅 시스템 개선 (ELK Stack 또는 GCP Logging)

### 우선순위 중간

- [ ] Batch 처리 성능 최적화
- [ ] Redis 캐싱 (동일 파일 중복 처리 방지)
- [ ] 에러 리포팅 (Sentry 연동)

### 우선순위 낮음

- [ ] Docker 컨테이너화
- [ ] CI/CD 파이프라인 (GitHub Actions)
- [ ] 다국어 UI 지원

---

## 📚 참고 문서

- [OpenAI Whisper API 공식 문서](https://platform.openai.com/docs/guides/speech-to-text)
- [FastAPI 공식 문서](https://fastapi.tiangolo.com/)
- [GCP Compute Engine 문서](https://cloud.google.com/compute/docs)

---

**작성일**: 2025-11-22  
**작성자**: AI Developer  
**최종 업데이트**: 2025-11-22

