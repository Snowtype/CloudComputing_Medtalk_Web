# 🎤 MedTalk Assist - Whisper Transcription Service

**Audio-to-Text Transcription Microservice using OpenAI Whisper API**

[![Status](https://img.shields.io/badge/status-production-brightgreen)]()
[![API](https://img.shields.io/badge/API-FastAPI-009688)]()
[![Deployed](https://img.shields.io/badge/deployed-GCP-4285F4)]()

---

## 🚀 **Live Service**

- **Production API**: `http://34.71.58.225:8000`
- **Web Interface**: `http://34.71.58.225:5000`
- **API Documentation**: `http://34.71.58.225:8000/docs`
- **Health Check**: `http://34.71.58.225:8000/health`

---

## 📋 **Quick Start for Integration (Jihwan)**

### **1. Test the API**

```bash
# Health check
curl http://34.71.58.225:8000/health

# Expected response:
# {"status":"healthy","service":"transcription","api_configured":true,"timestamp":"..."}
```

### **2. Transcribe Audio**

```bash
curl -X POST http://34.71.58.225:8000/transcribe \
  -F "file=@your_audio.wav" \
  -F "language=en"
```

**Response:**
```json
{
  "success": true,
  "text": "This is the transcribed text from your audio file.",
  "language": "en",
  "filename": "your_audio.wav",
  "file_size_mb": 2.5,
  "model": "whisper-1",
  "provider": "OpenAI",
  "timestamp": "2025-11-22T10:30:00.000000Z"
}
```

### **3. Integration with Your Composite Service**

#### **Python Example:**

```python
import requests

def transcribe_audio(audio_file_path):
    url = "http://34.71.58.225:8000/transcribe"
    
    with open(audio_file_path, 'rb') as f:
        files = {'file': f}
        data = {'language': 'en'}
        
        response = requests.post(url, files=files, data=data)
        
    if response.status_code == 200:
        result = response.json()
        return result['text']
    else:
        raise Exception(f"Transcription failed: {response.text}")

# Usage
transcribed_text = transcribe_audio("patient_audio.wav")
print(transcribed_text)
```

#### **JavaScript/Node.js Example:**

```javascript
const FormData = require('form-data');
const fs = require('fs');
const axios = require('axios');

async function transcribeAudio(audioFilePath) {
    const form = new FormData();
    form.append('file', fs.createReadStream(audioFilePath));
    form.append('language', 'en');
    
    const response = await axios.post('http://34.71.58.225:8000/transcribe', form, {
        headers: form.getHeaders()
    });
    
    return response.data.text;
}

// Usage
transcribeAudio('patient_audio.wav')
    .then(text => console.log(text))
    .catch(error => console.error(error));
```

---

## 🛠 **API Specification**

### **Endpoint: `POST /transcribe`**

**Parameters:**
- `file` (required): Audio file (multipart/form-data)
  - Supported formats: MP3, WAV, M4A, MPEG, MPGA, WebM, OGG, FLAC
  - Max size: 25MB
- `language` (optional): Language code (default: auto-detect)
  - Example: `en`, `ko`, `es`, `fr`
- `prompt` (optional): Context hint for better accuracy

**Response (Success - 200):**
```json
{
  "success": true,
  "text": "transcribed text",
  "language": "en",
  "filename": "audio.wav",
  "file_size_mb": 2.5,
  "model": "whisper-1",
  "provider": "OpenAI",
  "timestamp": "2025-11-22T10:30:00.000000Z"
}
```

**Response (Error - 4xx/5xx):**
```json
{
  "detail": "Error message description"
}
```

### **Endpoint: `GET /health`**

**Response:**
```json
{
  "status": "healthy",
  "service": "transcription",
  "api_configured": true,
  "timestamp": "2025-11-22T10:30:00.000000"
}
```

### **Endpoint: `POST /batch-transcribe`**

**Parameters:**
- `files` (required): Multiple audio files

**Response:**
```json
{
  "batch_results": [
    {"filename": "file1.wav", "success": true, "result": {...}},
    {"filename": "file2.wav", "success": true, "result": {...}}
  ],
  "total_files": 2,
  "successful": 2,
  "failed": 0,
  "timestamp": "2025-11-22T10:30:00.000000Z"
}
```

---

## 📂 **Project Structure**

```
WEBUI/
├── whisper-api-server.py          # Main FastAPI backend server
├── requirements-whisper-api.txt   # Python dependencies
├── env.whisper.example            # Environment variables template
├── start-server.sh                # Server startup script
├── test-server.sh                 # Local testing script
├── deployed-version/              # Frontend files
│   ├── index.html                 # Production Web UI
│   └── index-local.html           # Local development Web UI
├── INTEGRATION-GUIDE.md           # Detailed integration guide
├── DEPLOY-GCP.md                  # GCP deployment instructions
├── LOCAL-TEST-GUIDE.md            # Local testing guide
├── MANUAL-DEPLOY.md               # Manual deployment steps
└── README.md                      # This file
```

---

## 🏗 **Tech Stack**

- **Backend Framework**: FastAPI 0.115.6
- **Server**: Uvicorn 0.34.0
- **AI Model**: OpenAI Whisper API (whisper-1)
- **Language**: Python 3.11
- **Deployment**: GCP Compute Engine (Debian 12)
- **Frontend**: Vanilla HTML/CSS/JavaScript

---

## 🔧 **Local Development Setup**

### **Prerequisites**
- Python 3.11+
- OpenAI API Key (read-only access is sufficient)

### **Installation**

```bash
# Clone repository
git clone https://github.com/Snowtype/CloudComputing_Medtalk_Web.git
cd CloudComputing_Medtalk_Web

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements-whisper-api.txt

# Set API key
export OPENAI_API_KEY="your-api-key-here"

# Run server
python3 whisper-api-server.py
```

Server will start at:
- API: `http://localhost:8000`
- Docs: `http://localhost:8000/docs`

### **Testing Locally**

```bash
# Terminal 1: Run backend
./test-server.sh

# Terminal 2: Run frontend
cd deployed-version
python3 -m http.server 8080

# Open browser: http://localhost:8080
```

---

## 🌐 **Production Deployment (GCP)**

### **Current Deployment**
- **VM Instance**: `whisper-ai-web`
- **External IP**: `34.71.58.225`
- **Region**: us-central1
- **Machine Type**: e2-micro
- **OS**: Debian 12

### **Services Running**
1. **Backend API** (Port 8000)
   - `/home/mk4434/whisper-service/`
   - Managed by: `nohup python3 whisper-api-server.py`
   
2. **Frontend Web UI** (Port 5000)
   - `/home/aidesigner/medtalk-project/`
   - Managed by: `npx serve`

### **Firewall Rules**
- Port `8000`: Whisper API
- Port `5000`: Web UI
- Port `22`: SSH

---

## 🔐 **Security Notes**

- ✅ OpenAI API key is **read-only** (safer)
- ✅ API key stored as **environment variable** (not in code)
- ✅ API key **not committed to Git** (`.gitignore` protected)
- ✅ CORS enabled for cross-origin requests
- ⚠️ Production API is **public** (consider adding authentication for sensitive use)

---

## 📊 **Monitoring & Logs**

### **Check Backend Status**

```bash
# SSH to VM
gcloud compute ssh whisper-ai-web --zone=us-central1-a

# Check if server is running
ps aux | grep whisper-api-server

# View logs
tail -f ~/whisper-service/server.log

# Check health
curl http://localhost:8000/health
```

### **Check Frontend Status**

```bash
# Check if serving
ps aux | grep "npx serve"

# View logs
tail -f ~/medtalk-project/server.log
```

---

## 🐛 **Troubleshooting**

### **API Not Responding**

```bash
# Restart backend
cd ~/whisper-service
source venv/bin/activate
export OPENAI_API_KEY="your-key-here"
nohup python3 whisper-api-server.py > server.log 2>&1 &
```

### **Web UI Not Loading**

```bash
# Restart frontend
cd ~/medtalk-project
nohup npx serve -s . -p 5000 > server.log 2>&1 &
```

### **Firewall Issues**

```bash
# Check firewall rules
gcloud compute firewall-rules list | grep whisper

# Add firewall rule if missing
gcloud compute firewall-rules create allow-whisper-8000 \
    --allow tcp:8000 \
    --source-ranges 0.0.0.0/0
```

---

## 📚 **Additional Documentation**

- **[INTEGRATION-GUIDE.md](./INTEGRATION-GUIDE.md)**: Complete integration guide for composite service
- **[DEPLOY-GCP.md](./DEPLOY-GCP.md)**: Automated deployment scripts
- **[LOCAL-TEST-GUIDE.md](./LOCAL-TEST-GUIDE.md)**: Local testing instructions
- **[MANUAL-DEPLOY.md](./MANUAL-DEPLOY.md)**: Step-by-step manual deployment

---

## 🤝 **Team Integration**

### **For Jihwan (Composite Service)**

Your composite service should call our `/transcribe` endpoint:

```
POST http://34.71.58.225:8000/transcribe
```

**What you need:**
1. ✅ Endpoint URL (above)
2. ✅ Audio file from user/system
3. ✅ HTTP client (requests, axios, fetch, etc.)

**What you get back:**
- Transcribed text
- Language detected
- File metadata
- Timestamp

**Error Handling:**
- HTTP 200: Success (check `response.json()['text']`)
- HTTP 400: Bad request (invalid file format/size)
- HTTP 413: File too large (>25MB)
- HTTP 500: Server error (check our logs)
- HTTP 502: OpenAI API error (rate limit, API down, etc.)

---

## 📞 **Contact & Support**

- **GitHub**: [CloudComputing_Medtalk_Web](https://github.com/Snowtype/CloudComputing_Medtalk_Web)
- **Issues**: Open a GitHub issue or contact team directly
- **API Status**: Check `/health` endpoint

---

## 📝 **License & Credits**

- OpenAI Whisper API
- FastAPI Framework
- GCP Compute Engine
- MedTalk Assist Team

---

**Last Updated**: November 22, 2025
**Status**: ✅ Production Ready
**Version**: 1.0.0
