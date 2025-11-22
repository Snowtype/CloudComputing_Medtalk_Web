# 🎤 MedTalk Assist - Whisper 음성인식 서비스

**OpenAI Whisper API를 사용한 음성→텍스트 변환 마이크로서비스**

---

## 🎯 **형님, 여기만 보시면 됩니다!**

### ✅ **서비스 준비 완료**

프로덕션 환경에서 이미 동작 중입니다!

- **API Endpoint**: `http://34.71.58.225:8000/transcribe`
- **상태 확인**: `http://34.71.58.225:8000/health`
- **API 문서**: `http://34.71.58.225:8000/docs` (브라우저에서 직접 테스트 가능)

---

### 📋 **사용 방법**

#### **1. 빠른 테스트**

```bash
# 상태 확인
curl http://34.71.58.225:8000/health

# 음성 파일 변환
curl -X POST http://34.71.58.225:8000/transcribe \
  -F "file=@your_audio.wav" \
  -F "language=en"
```

#### **2. Python 코드 예제**

```python
import requests

def transcribe_audio(audio_file_path):
    url = "http://34.71.58.225:8000/transcribe"

    with open(audio_file_path, 'rb') as f:
        files = {'file': f}
        data = {'language': 'en'}  # 선택사항
        response = requests.post(url, files=files, data=data)

    if response.status_code == 200:
        result = response.json()
        return result['text']  # 변환된 텍스트
    else:
        raise Exception(f"변환 실패: {response.text}")

# 사용
text = transcribe_audio("patient_audio.wav")
print(text)
```

#### **3. JavaScript/Node.js 코드 예제**

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
    { headers: form.getHeaders() }
  );

  return response.data.text;
}

// 사용
transcribeAudio("patient_audio.wav")
  .then((text) => console.log(text))
  .catch((error) => console.error(error));
```

---

### 📤 **요청 형식**

```
POST http://34.71.58.225:8000/transcribe
Content-Type: multipart/form-data

Parameters:
- file: 음성 파일 (필수)
  • 지원 형식: MP3, WAV, M4A, WebM, OGG, FLAC 등
  • 최대 크기: 25MB
- language: 언어 코드 (선택) - 예: "en", "ko", "es"
  • 미지정 시 자동 감지
```

### 📥 **응답 형식**

```json
{
  "success": true,
  "text": "변환된 텍스트 내용",
  "language": "en",
  "filename": "audio.wav",
  "file_size_mb": 2.5,
  "model": "whisper-1",
  "provider": "OpenAI",
  "timestamp": "2025-11-22T10:30:00.000000Z"
}
```

**필요한 부분**: `result['text']` ← 여기에 변환된 텍스트가 있습니다

---

### ⚠️ **에러 처리**

| HTTP 코드 | 의미            | 대응 방법                      |
| --------- | --------------- | ------------------------------ |
| 200       | 성공            | `response.json()['text']` 사용 |
| 400       | 잘못된 요청     | 파일 형식/크기 확인            |
| 413       | 파일 너무 큼    | 25MB 이하로 제한               |
| 500       | 서버 에러       | 저한테 연락 주세요             |
| 502       | OpenAI API 에러 | Rate limit/API 장애 (일시적)   |

---

### 🔗 **추가 엔드포인트**

#### **GET /health** - 서비스 상태 확인

```json
{
  "status": "healthy",
  "service": "transcription",
  "api_configured": true,
  "timestamp": "2025-11-22T10:30:00.000000"
}
```

#### **POST /batch-transcribe** - 여러 파일 한번에 변환

```python
# 여러 파일 동시 처리
files = [
    ('files', open('audio1.wav', 'rb')),
    ('files', open('audio2.wav', 'rb'))
]
response = requests.post('http://34.71.58.225:8000/batch-transcribe', files=files)
```

---

## 🎉 **이상입니다!**

위 내용만 참고하시면 Composite Service에서 바로 사용하실 수 있습니다.

궁금하신 점이나 문제 있으시면 언제든지 말씀해주세요! 🚀

---

---

---

# 📚 부가 정보 (개발/배포 참고용)

<details>
<summary><b>📂 프로젝트 구조</b></summary>

```
WEBUI/
├── whisper-api-server.py          # FastAPI 백엔드 서버
├── requirements-whisper-api.txt   # Python 패키지 목록
├── deployed-version/
│   └── index.html                 # 웹 UI (프로덕션)
├── venv/                          # Python 가상환경 (로컬 개발용)
└── README.md                      # 이 파일
```

</details>

<details>
<summary><b>🛠 기술 스택</b></summary>

- **백엔드**: FastAPI 0.115.6
- **서버**: Uvicorn 0.34.0
- **AI 모델**: OpenAI Whisper API (whisper-1)
- **언어**: Python 3.11
- **배포**: GCP Compute Engine (Debian 12)
- **프론트엔드**: Vanilla HTML/CSS/JavaScript

</details>

<details>
<summary><b>💻 로컬 개발 환경 설정</b></summary>

### 사전 준비

- Python 3.11+
- OpenAI API 키

### 설치 및 실행

```bash
# 저장소 클론
git clone https://github.com/Snowtype/CloudComputing_Medtalk_Web.git
cd CloudComputing_Medtalk_Web

# 가상환경 생성
python3 -m venv venv
source venv/bin/activate

# 패키지 설치
pip install -r requirements-whisper-api.txt

# API 키 설정
export OPENAI_API_KEY="sk-proj-your-api-key-here"

# 서버 실행
python3 whisper-api-server.py
```

서버: `http://localhost:8000`

### 웹 UI 로컬 실행

```bash
cd deployed-version
python3 -m http.server 8080
# 브라우저: http://localhost:8080
```

</details>

<details>
<summary><b>🌐 GCP 프로덕션 배포 정보</b></summary>

### 현재 배포 상태

- **VM 인스턴스**: `whisper-ai-web`
- **외부 IP**: `34.71.58.225`
- **리전**: us-central1
- **머신 타입**: e2-micro
- **OS**: Debian 12

### 실행 중인 서비스

**1. 백엔드 API (포트 8000)**

- 경로: `/home/mk4434/whisper-service/`
- 실행: `nohup python3 whisper-api-server.py &`
- 로그: `~/whisper-service/server.log`

**2. 프론트엔드 Web UI (포트 5000)**

- 경로: `/home/aidesigner/medtalk-project/`
- 실행: `npx serve -s . -p 5000`
- 로그: `~/medtalk-project/server.log`

### 방화벽 설정

- 포트 8000: Whisper API
- 포트 5000: Web UI
- 포트 22: SSH

</details>

<details>
<summary><b>🔐 보안 정보</b></summary>

- ✅ OpenAI API 키는 **읽기 전용**
- ✅ API 키는 **환경 변수**로 관리
- ✅ API 키는 **Git에 커밋 안 됨** (`.gitignore`)
- ✅ CORS 활성화
- ⚠️ 프로덕션 API는 공개 접근 (필요시 인증 추가 가능)

</details>

<details>
<summary><b>📊 모니터링 & 로그</b></summary>

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
ps aux | grep "npx serve"
tail -f ~/medtalk-project/server.log
```

</details>

<details>
<summary><b>🐛 문제 해결</b></summary>

### API가 응답하지 않을 때

```bash
cd ~/whisper-service
source venv/bin/activate
export OPENAI_API_KEY="your-key-here"
nohup python3 whisper-api-server.py > server.log 2>&1 &
```

### Web UI가 로딩되지 않을 때

```bash
cd ~/medtalk-project
pkill -f "npx serve"
nohup npx serve -s . -p 5000 > server.log 2>&1 &
```

### 방화벽 문제

```bash
gcloud compute firewall-rules list | grep whisper

# 방화벽 규칙 추가
gcloud compute firewall-rules create allow-whisper-8000 \
    --allow tcp:8000 \
    --source-ranges 0.0.0.0/0
```

</details>

<details>
<summary><b>📝 완료된 작업</b></summary>

- ✅ OpenAI Whisper API 연동
- ✅ FastAPI 백엔드 구현
- ✅ Web UI 프론트엔드 구현
- ✅ GCP VM 배포 완료
- ✅ 방화벽 설정 완료
- ✅ 실제 음성 파일 테스트 완료
- ✅ Composite Service 연동 준비 완료

</details>

---

**최종 업데이트**: 2025년 11월 22일  
**상태**: ✅ 프로덕션 운영 중  
**버전**: 1.0.0

---

## 📞 연락처

- **GitHub**: [CloudComputing_Medtalk_Web](https://github.com/Snowtype/CloudComputing_Medtalk_Web)
- 문제 발생 시 팀 채팅으로 문의
