# 🚀 GCP VM 수동 배포 가이드

## Step 1: 파일 준비

로컬에서 파일 복사:

```bash
cd "/Users/aidesigner/Columbia Univ Course/CloudComputing/WEBUI"

# 파일 내용 확인
cat whisper-api-server.py > ~/Desktop/whisper-api-server.py
cat requirements-whisper-api.txt > ~/Desktop/requirements-whisper-api.txt
```

## Step 2: GCP 브라우저 SSH로 접속

1. **GCP Console 열기**: https://console.cloud.google.com
2. **Compute Engine** → **VM instances**
3. **whisper-ai-web** 찾기
4. **SSH** 버튼 클릭 → **"Open in browser window"**

## Step 3: VM에서 파일 생성

브라우저 SSH 터미널에서:

### 1) whisper-api-server.py 생성

```bash
cat > ~/whisper-api-server.py << 'ENDOFFILE'
```

**여기서 로컬의 `whisper-api-server.py` 내용 전체를 복사해서 붙여넣기**

```bash
ENDOFFILE
```

### 2) requirements-whisper-api.txt 생성

```bash
cat > ~/requirements-whisper-api.txt << 'ENDOFFILE'
fastapi==0.104.1
uvicorn[standard]==0.24.0
python-multipart==0.0.6
openai==2.8.1
python-dotenv==1.0.0
ENDOFFILE
```

## Step 4: 환경 설정

```bash
# 시스템 업데이트
sudo apt update && sudo apt upgrade -y

# Python 설치
sudo apt install -y python3 python3-pip python3-venv

# 프로젝트 디렉토리 생성
mkdir -p ~/whisper-service
mv ~/whisper-api-server.py ~/whisper-service/
mv ~/requirements-whisper-api.txt ~/whisper-service/
cd ~/whisper-service

# 가상환경 생성
python3 -m venv venv
source venv/bin/activate

# 패키지 설치
pip install --upgrade pip
pip install -r requirements-whisper-api.txt
```

## Step 5: API 키 설정 & 서버 실행

```bash
# API 키 설정 (실제 키로 교체하세요!)
export OPENAI_API_KEY="sk-proj-YOUR-READ-ONLY-API-KEY-HERE"

# 서버 실행 (백그라운드)
nohup python whisper-api-server.py > server.log 2>&1 &

# 프로세스 확인
ps aux | grep whisper

# 로그 확인
tail -f server.log
```

**성공하면 로그에:**

```
INFO:__main__:✅ OpenAI API key configured
INFO:__main__:🚀 Starting Whisper API Server on port 8000
INFO:     Uvicorn running on http://0.0.0.0:8000
```

## Step 6: 방화벽 설정

### GCP 콘솔에서:

1. **VPC Network** → **Firewall**
2. **CREATE FIREWALL RULE**
3. 설정:
   - Name: `allow-whisper-api`
   - Targets: `All instances in the network`
   - Source IP ranges: `0.0.0.0/0`
   - Protocols and ports: `tcp:8000`
4. **CREATE** 클릭

## Step 7: 테스트

브라우저에서:

```
http://34.71.58.225:8000/health
```

응답:

```json
{
  "status": "healthy",
  "service": "transcription",
  "api_configured": true
}
```

**API Docs:**

```
http://34.71.58.225:8000/docs
```

## 🎉 완료!

서비스 URL:

- **Health**: http://34.71.58.225:8000/health
- **Transcribe**: http://34.71.58.225:8000/transcribe
- **Docs**: http://34.71.58.225:8000/docs

## 🔧 서버 관리

### 서버 중지

```bash
pkill -f whisper-api-server
```

### 서버 재시작

```bash
cd ~/whisper-service
source venv/bin/activate
export OPENAI_API_KEY="sk-proj-..."
nohup python whisper-api-server.py > server.log 2>&1 &
```

### 로그 확인

```bash
tail -f ~/whisper-service/server.log
```
