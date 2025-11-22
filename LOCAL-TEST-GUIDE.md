# 🧪 로컬 테스트 가이드

## 🚀 빠른 시작

### 1. 백엔드 서버 실행

터미널 1에서:

```bash
cd "/Users/aidesigner/Columbia Univ Course/CloudComputing/WEBUI"
./test-server.sh
```

서버가 시작되면:

- 🌐 http://localhost:8001
- 📚 http://localhost:8001/docs (Swagger UI)
- ❤️ http://localhost:8001/health

### 2. 프론트엔드 실행

터미널 2에서:

```bash
cd "/Users/aidesigner/Columbia Univ Course/CloudComputing/WEBUI/deployed-version"

# 포트 8080에서 실행 (8000은 Docker가 사용중)
python3 -m http.server 8080
```

브라우저에서 열기:

- 🌐 http://localhost:8080

### 3. API URL 수정 (중요!)

`deployed-version/index.html` 파일을 열어서 API URL을 수정해야 해:

**찾기:**

```javascript
const response = await fetch('http://localhost:8000/transcribe', {
```

**바꾸기:**

```javascript
const response = await fetch('http://localhost:8001/transcribe', {
```

## 🧪 테스트 방법

### Method 1: 브라우저 UI 테스트

1. http://localhost:8080 접속
2. 오디오 파일 선택 (wav, mp3 등)
3. "Start Transcription" 버튼 클릭
4. 결과 확인

**주의:** OpenAI API 키가 설정되어 있어야 실제로 작동해. 현재는 테스트 키로 실행 중이라 에러가 날 거야.

### Method 2: cURL 테스트

```bash
# Health Check
curl http://localhost:8001/health

# Root 엔드포인트
curl http://localhost:8001/

# 파일 업로드 테스트 (실제 오디오 파일 필요)
curl -X POST http://localhost:8001/transcribe \
  -F "file=@test_audio.wav" \
  -F "language=en"
```

### Method 3: Swagger UI 테스트

1. http://localhost:8001/docs 접속
2. "POST /transcribe" 펼치기
3. "Try it out" 클릭
4. 파일 업로드하고 "Execute"

## 🔑 실제 API 키로 테스트

실제로 음성 인식을 테스트하려면:

```bash
# OpenAI API 키 설정
export OPENAI_API_KEY="sk-proj-실제-키-입력"

# 서버 재시작
cd "/Users/aidesigner/Columbia Univ Course/CloudComputing/WEBUI"
source venv/bin/activate
PORT=8001 python whisper-api-server.py
```

## 📝 테스트 체크리스트

- [ ] 백엔드 서버 시작됨 (port 8001)
- [ ] Health endpoint 응답함
- [ ] Swagger UI 접속됨
- [ ] 프론트엔드 UI 로드됨 (port 8080)
- [ ] 파일 업로드 UI 작동
- [ ] API 호출 연결 (CORS 에러 없음)
- [ ] 실제 transcription 작동 (API 키 필요)

## 🐛 문제 해결

### 포트 충돌

```bash
# 8001 포트 사용 중인 프로세스 찾기
lsof -i :8001

# 프로세스 종료
kill -9 <PID>
```

### CORS 에러

백엔드에서 CORS가 활성화되어 있어야 해:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 개발용
    ...
)
```

### API 키 에러

```
"OpenAI API key not configured"
```

→ 환경 변수 설정 필요:

```bash
export OPENAI_API_KEY="sk-proj-..."
```

## 🎯 다음 단계

1. ✅ 로컬 테스트 완료
2. 🔜 프론트엔드 API URL 수정 (8001로)
3. 🔜 실제 OpenAI API 키로 테스트
4. 🔜 GCP VM에 배포
5. 🔜 지환님 Composite 서비스와 연결

## 💡 유용한 명령어

```bash
# 실행 중인 Python 프로세스 보기
ps aux | grep python

# 백엔드 로그 보기 (백그라운드 실행 시)
tail -f nohup.out

# 포트 사용 확인
lsof -i :8001
lsof -i :8080
```
