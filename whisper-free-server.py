#!/usr/bin/env python3
"""
Whisper Transcription Server - FREE VERSION
Hugging Face Inference API 사용 (완전 무료!)
"""

import os
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import requests
from typing import Optional
import logging
from datetime import datetime

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI 앱 생성
app = FastAPI(
    title="Whisper Transcription Service (FREE)",
    description="Hugging Face Inference API를 사용한 무료 음성 인식 서비스",
    version="2.0.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Hugging Face API 설정 (새 URL)
HF_API_URL = "https://api-inference.huggingface.co/models/openai/whisper-large-v3"  
# Note: Hugging Face deprecated old URL, but model endpoint still works
HF_TOKEN = os.getenv("HUGGINGFACE_TOKEN", "")  # Optional, for higher rate limits

@app.get("/")
async def root():
    """서버 상태 확인"""
    return {
        "service": "Whisper Transcription Service (FREE)",
        "status": "running",
        "provider": "Hugging Face",
        "model": "openai/whisper-large-v3",
        "version": "2.0.0",
        "cost": "FREE! 🎉"
    }

@app.get("/health")
async def health_check():
    """헬스 체크 엔드포인트"""
    return {
        "status": "healthy",
        "service": "transcription",
        "provider": "huggingface",
        "free": True,
        "timestamp": datetime.now().isoformat()
    }

@app.post("/transcribe")
async def transcribe_audio(
    file: UploadFile = File(...),
    language: Optional[str] = None,
    prompt: Optional[str] = None
):
    """
    오디오 파일을 텍스트로 변환 (Hugging Face 무료 API 사용)
    """
    
    try:
        # 파일 읽기
        content = await file.read()
        file_size_mb = len(content) / (1024 * 1024)
        
        # 파일 크기 확인 (25MB 제한)
        if file_size_mb > 25:
            raise HTTPException(
                status_code=413,
                detail=f"File too large ({file_size_mb:.2f}MB). Maximum size is 25MB."
            )
        
        # 지원되는 파일 형식 확인
        allowed_extensions = {'.mp3', '.mp4', '.mpeg', '.mpga', '.m4a', '.wav', '.webm', '.ogg', '.flac'}
        file_extension = os.path.splitext(file.filename)[1].lower()
        
        if file_extension not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file format '{file_extension}'. Allowed: {', '.join(allowed_extensions)}"
            )
        
        logger.info(f"Processing file: {file.filename} ({file_size_mb:.2f}MB)")
        
        # Hugging Face API 호출
        headers = {}
        if HF_TOKEN:
            headers["Authorization"] = f"Bearer {HF_TOKEN}"
        
        logger.info(f"Calling Hugging Face Inference API for {file.filename}")
        
        response = requests.post(
            HF_API_URL,
            headers=headers,
            data=content,
            timeout=120  # 2분 타임아웃
        )
        
        if response.status_code == 503:
            # 모델 로딩 중
            raise HTTPException(
                status_code=503,
                detail="Model is loading, please try again in 20 seconds. (This is normal for the first request)"
            )
        
        if response.status_code != 200:
            try:
                error_msg = response.json().get('error', 'Unknown error')
            except:
                error_msg = response.text
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Hugging Face API error: {error_msg}"
            )
        
        # Hugging Face 응답 처리
        try:
            result = response.json()
            if isinstance(result, dict):
                transcribed_text = result.get("text", "")
            elif isinstance(result, str):
                transcribed_text = result
            else:
                transcribed_text = str(result)
        except Exception as e:
            logger.error(f"Failed to parse response: {response.text[:200]}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to parse API response: {str(e)}"
            )
        
        # 성공 응답
        response_data = {
            "success": True,
            "text": transcribed_text.strip(),
            "language": language or "auto-detected",
            "filename": file.filename,
            "file_size_mb": round(file_size_mb, 2),
            "model": "whisper-large-v3",
            "provider": "Hugging Face (FREE)",
            "cost": "$0.00 🎉",
            "timestamp": datetime.now().isoformat() + "Z"
        }
        
        logger.info(f"Transcription completed: {len(transcribed_text)} characters")
        return JSONResponse(content=response_data)
        
    except HTTPException:
        raise
    except requests.exceptions.Timeout:
        logger.error("Request timeout")
        raise HTTPException(
            status_code=504,
            detail="Request timeout. Try with a smaller audio file."
        )
    except Exception as e:
        logger.error(f"Transcription error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Transcription failed: {str(e)}"
        )

@app.post("/batch-transcribe")
async def batch_transcribe(files: list[UploadFile] = File(...)):
    """여러 파일 일괄 처리"""
    results = []
    
    for idx, file in enumerate(files, 1):
        try:
            logger.info(f"Processing batch file {idx}/{len(files)}: {file.filename}")
            result = await transcribe_audio(file)
            results.append({
                "filename": file.filename,
                "success": True,
                "result": result
            })
        except HTTPException as e:
            results.append({
                "filename": file.filename,
                "success": False,
                "error": e.detail,
                "status_code": e.status_code
            })
        except Exception as e:
            results.append({
                "filename": file.filename,
                "success": False,
                "error": str(e)
            })
    
    successful = sum(1 for r in results if r["success"])
    failed = len(results) - successful
    
    return {
        "batch_results": results,
        "total_files": len(files),
        "successful": successful,
        "failed": failed,
        "timestamp": datetime.now().isoformat() + "Z"
    }

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8002))
    
    logger.info("🎉 Starting FREE Whisper Transcription Service!")
    logger.info("📌 Provider: Hugging Face Inference API")
    logger.info("💰 Cost: $0.00 (Completely FREE!)")
    logger.info(f"🚀 Starting server on port {port}")
    logger.info(f"📝 Docs: http://localhost:{port}/docs")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info"
    )

