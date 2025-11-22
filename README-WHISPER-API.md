# 🎤 Whisper API Transcription Service

너의 담당 백엔드: OpenAI Whisper API를 사용한 음성 인식 서비스

## 🚀 빠른 시작

### 1. 의존성 설치

```bash
cd WEBUI
pip install -r requirements-whisper-api.txt
```

### 2. 환경 변수 설정

```bash
# .env 파일 생성
cp env.whisper.example .env

# OpenAI API 키 입력 (편집기로 열어서)
nano .env
```

`.env` 파일:

```env
OPENAI_API_KEY=sk-proj-your-actual-api-key-here
PORT=8000
```

### 3. 서버 실행

```bash
# 개발 모드
python whisper-api-server.py

# 또는 환경변수와 함께
OPENAI_API_KEY=sk-your-key PORT=8000 python whisper-api-server.py
```

서버 시작되면:

- API 문서: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

## 📡 API 엔드포인트

### 1. Health Check

```bash
GET /health
```

**응답:**

```json
{
  "status": "healthy",
  "service": "transcription",
  "api_configured": true,
  "timestamp": "2025-11-22T12:00:00.000Z"
}
```

### 2. 음성 → 텍스트 변환

```bash
POST /transcribe
Content-Type: multipart/form-data

file: (audio file)
language: "en" (optional)
prompt: "medical context" (optional)
```

**응답:**

```json
{
  "success": true,
  "text": "This is the transcribed text from the audio file.",
  "language": "en",
  "filename": "audio.wav",
  "file_size_mb": 2.29,
  "model": "whisper-1",
  "provider": "OpenAI",
  "timestamp": "2025-11-22T12:00:00.000Z"
}
```

### 3. 일괄 처리

```bash
POST /batch-transcribe
Content-Type: multipart/form-data

files[]: (multiple audio files)
```

## 🧪 테스트

### cURL로 테스트

```bash
# Health Check
curl http://localhost:8000/health

# 파일 업로드 테스트
curl -X POST http://localhost:8000/transcribe \
  -F "file=@test_audio.wav" \
  -F "language=en"
```

### Python으로 테스트

```python
import requests

# 파일 업로드
with open("test_audio.wav", "rb") as f:
    response = requests.post(
        "http://localhost:8000/transcribe",
        files={"file": f},
        data={"language": "en"}
    )

print(response.json())
```

## 🔗 프론트엔드 연결

`deployed-version/index.html`의 `transcribeAudio()` 함수 수정:

```javascript
async function transcribeAudio() {
  if (!selectedFile) {
    updateStatus("Please select an audio file first.", "error");
    return;
  }

  const engine = document.getElementById("engineSelect").value;
  const transcribeBtn = document.getElementById("transcribeBtn");

  transcribeBtn.disabled = true;
  transcribeBtn.innerHTML = "<span>⏳</span> Processing...";

  try {
    // FormData 생성
    const formData = new FormData();
    formData.append("file", selectedFile);
    formData.append("language", "en"); // 또는 사용자 선택

    // 실제 API 호출!
    const response = await fetch("http://localhost:8000/transcribe", {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const result = await response.json();

    // 성공 메시지 표시
    updateStatus(
      `✅ Transcription completed!<br>` +
        `<strong>Text:</strong> ${result.text}<br>` +
        `<small>Language: ${result.language} | Duration: ${result.file_size_mb}MB</small>`,
      "success"
    );
  } catch (error) {
    updateStatus(`❌ Transcription failed: ${error.message}`, "error");
  } finally {
    transcribeBtn.disabled = false;
    transcribeBtn.innerHTML = "<span>🚀</span> Start Transcription";
  }
}
```

## 🚢 GCP VM 배포

### 1. 서버에 파일 업로드

```bash
scp whisper-api-server.py mk4434@34.71.58.225:~/
scp requirements-whisper-api.txt mk4434@34.71.58.225:~/
```

### 2. VM에서 설정

```bash
ssh mk4434@34.71.58.225

# 의존성 설치
pip3 install -r requirements-whisper-api.txt

# 환경 변수 설정
export OPENAI_API_KEY="sk-your-actual-key"

# 백그라운드 실행
nohup python3 whisper-api-server.py > whisper-api.log 2>&1 &

# 또는 systemd 서비스로 등록 (권장)
```

### 3. 방화벽 설정

```bash
sudo ufw allow 8000
```

### 4. 테스트

```bash
curl http://34.71.58.225:8000/health
```

## 💡 다음 단계

1. ✅ **로컬 테스트**: `python whisper-api-server.py`
2. ✅ **프론트엔드 연결**: `index.html` 수정
3. ✅ **GCP 배포**: VM에 업로드 및 실행
4. 🔜 **지환님 Composite와 연결**: API 엔드포인트 공유

## 📝 참고사항

- OpenAI API 키 필수!
- 파일 크기 제한: 25MB
- 지원 포맷: mp3, wav, m4a, webm, ogg, flac
- CORS 활성화됨 (모든 origin 허용 - 프로덕션에서는 제한 필요)

## 🐛 문제 해결

**API 키 에러:**

```bash
export OPENAI_API_KEY="sk-your-key"
python whisper-api-server.py
```

**포트 이미 사용 중:**

```bash
PORT=8001 python whisper-api-server.py
```

**CORS 에러:**

- 백엔드가 실행 중인지 확인
- 프론트엔드 URL이 CORS allowed origins에 포함되어 있는지 확인
