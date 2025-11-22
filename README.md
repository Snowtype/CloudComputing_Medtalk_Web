# 🎤 Whisper Transcription Service

너의 담당: OpenAI Whisper API를 사용한 음성 인식 백엔드

## 📁 파일 구조

```
WEBUI/
├── whisper-api-server.py       # 메인 백엔드 서버
├── requirements-whisper-api.txt # Python 패키지
├── env.whisper.example          # 환경 변수 템플릿
├── start-server.sh              # 서버 시작 스크립트
├── venv/                        # Python 가상환경
├── deployed-version/            # 배포된 프론트엔드
│   └── index.html              # 웹 UI
└── README.md                    # 이 파일!
```

## 🚀 빠른 시작

### 1. 패키지 설치

```bash
# 가상환경 활성화
source venv/bin/activate

# 패키지 설치 (SSL 에러 해결)
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements-whisper-api.txt
```

### 2. OpenAI API 키 설정

```bash
export OPENAI_API_KEY="sk-proj-your-actual-key-here"
```

### 3. 서버 실행

```bash
# 방법 1: 스크립트 사용
./start-server.sh

# 방법 2: 직접 실행
source venv/bin/activate
python whisper-api-server.py
```

서버 시작하면:

- 🌐 http://localhost:8000
- 📚 http://localhost:8000/docs (API 문서)
- ❤️ http://localhost:8000/health (헬스 체크)

## 🧪 테스트

```bash
# Health check
curl http://localhost:8000/health

# 파일 업로드 테스트
curl -X POST http://localhost:8000/transcribe \
  -F "file=@test.wav" \
  -F "language=en"
```

## 🌐 프론트엔드 실행

```bash
# deployed-version 디렉토리에서
cd deployed-version
python3 -m http.server 8080

# 접속: http://localhost:8080
```

**주의:** 프론트엔드의 `index.html`에서 API URL을 `http://localhost:8000`으로 수정 필요!

## 📦 GCP VM 배포

상세한 배포 가이드는 `README-WHISPER-API.md` 참고

## 💡 다음 단계

1. ✅ 로컬에서 테스트
2. 🔜 프론트엔드와 연결
3. 🔜 GCP VM에 배포
4. 🔜 지환님 Composite 서비스와 통합

## 🐛 문제 해결

**SSL 에러:**

```bash
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org fastapi uvicorn openai python-multipart
```

**포트 충돌:**

```bash
PORT=8001 python whisper-api-server.py
```

**API 키 에러:**
OpenAI API 키가 설정되지 않았거나 잘못됨

```bash
export OPENAI_API_KEY="sk-proj-..."
```
