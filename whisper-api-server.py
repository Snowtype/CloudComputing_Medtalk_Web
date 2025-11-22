#!/usr/bin/env python3
"""
Whisper API Server - OpenAI Whisper API 사용
너의 담당 백엔드: 음성 → 텍스트 변환
"""

import os
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from openai import OpenAI
from typing import Optional
import logging
from datetime import datetime

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI 앱 생성
app = FastAPI(
    title="Whisper API Transcription Service",
    description="OpenAI Whisper API를 사용한 음성 인식 서비스 for MedTalk Assist",
    version="1.0.0"
)

# CORS 설정 - 프론트엔드에서 접근 가능하도록
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 프로덕션에서는 특정 도메인으로 제한
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OpenAI 클라이언트 초기화
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", "your_api_key_here"))

@app.get("/")
async def root():
    """서버 상태 확인"""
    return {
        "service": "Whisper API Transcription Service",
        "status": "running",
        "provider": "OpenAI Whisper API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "transcribe": "/transcribe",
            "batch": "/batch-transcribe"
        }
    }

@app.get("/health")
async def health_check():
    """헬스 체크 엔드포인트 - 프론트엔드에서 서비스 상태 확인용"""
    api_key_configured = client.api_key != "your_api_key_here"
    
    return {
        "status": "healthy",
        "service": "transcription",
        "api_configured": api_key_configured,
        "timestamp": datetime.now().isoformat()
    }

@app.post("/transcribe")
async def transcribe_audio(
    file: UploadFile = File(...),
    language: Optional[str] = None,
    prompt: Optional[str] = None
):
    """
    오디오 파일을 텍스트로 변환 (OpenAI Whisper API 사용)
    
    Args:
        file: 오디오 파일 (mp3, wav, m4a, webm 등)
        language: 언어 코드 (선택사항, 예: 'en', 'ko')
        prompt: 컨텍스트 프롬프트 (선택사항)
    
    Returns:
        JSON 응답:
        {
            "success": true,
            "text": "변환된 텍스트",
            "language": "en",
            "filename": "audio.wav",
            "duration": 120.5,
            "timestamp": "2025-11-22T..."
        }
    """
    
    try:
        # 파일 크기 확인 (25MB 제한)
        content = await file.read()
        file_size_mb = len(content) / (1024 * 1024)
        
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
        
        # OpenAI API 키 확인
        if client.api_key == "your_api_key_here":
            raise HTTPException(
                status_code=500,
                detail="OpenAI API key not configured. Please set OPENAI_API_KEY environment variable."
            )
        
        # OpenAI Whisper API 호출 (v2.x 방식)
        file.file.seek(0)  # 파일 포인터를 처음으로
        
        # OpenAI API 호출
        logger.info(f"Calling OpenAI Whisper API for {file.filename}")
        
        # Create a file-like object from bytes
        from io import BytesIO
        audio_file = BytesIO(content)
        audio_file.name = file.filename
        
        # API 호출 파라미터
        transcribe_params = {
            "model": "whisper-1",
            "file": audio_file
        }
        
        if language:
            transcribe_params["language"] = language
        
        if prompt:
            transcribe_params["prompt"] = prompt
        
        response = client.audio.transcriptions.create(**transcribe_params)
        
        # 응답 처리
        transcribed_text = response.text
        detected_language = language or "unknown"
        
        # 성공 응답
        response_data = {
            "success": True,
            "text": transcribed_text.strip(),
            "language": detected_language,
            "filename": file.filename,
            "file_size_mb": round(file_size_mb, 2),
            "model": "whisper-1",
            "provider": "OpenAI",
            "timestamp": datetime.now().isoformat() + "Z"
        }
        
        logger.info(f"Transcription completed: {len(transcribed_text)} characters")
        return JSONResponse(content=response_data)
        
    except Exception as api_error:
        if "authentication" in str(api_error).lower():
            logger.error("OpenAI API authentication failed")
            raise HTTPException(
                status_code=401,
                detail="OpenAI API authentication failed. Please check your API key."
            )
        elif "rate" in str(api_error).lower():
            logger.error("OpenAI API rate limit exceeded")
            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded. Please try again later."
            )
        else:
            logger.error(f"OpenAI API error: {str(api_error)}")
            raise HTTPException(
                status_code=502,
                detail=f"OpenAI API error: {str(api_error)}"
            )
    
    except Exception as e:
        logger.error(f"Transcription error: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Transcription failed: {str(e)}"
        )

@app.post("/batch-transcribe")
async def batch_transcribe(files: list[UploadFile] = File(...)):
    """
    여러 파일 일괄 처리
    
    Args:
        files: 오디오 파일 목록
    
    Returns:
        각 파일의 처리 결과 배열
    """
    results = []
    
    for idx, file in enumerate(files, 1):
        try:
            logger.info(f"Processing batch file {idx}/{len(files)}: {file.filename}")
            
            # 개별 파일 처리
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
    
    # 통계
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
    port = int(os.getenv("PORT", 8000))
    
    # API 키 확인
    if client.api_key == "your_api_key_here" or not client.api_key:
        logger.warning("⚠️  OpenAI API key not configured!")
        logger.warning("Set OPENAI_API_KEY environment variable before starting")
    else:
        logger.info("✅ OpenAI API key configured")
    
    logger.info(f"🚀 Starting Whisper API Server on port {port}")
    logger.info(f"📝 Docs: http://localhost:{port}/docs")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info"
    )

