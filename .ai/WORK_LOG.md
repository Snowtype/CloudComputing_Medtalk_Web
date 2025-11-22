# 📝 Work Log - MedTalk Assist Whisper Service

> 작업 일지: 주요 변경사항, 결정사항, 이슈 해결 내역을 시간순으로 기록

---

## 2025-11-22 (금) - 프로젝트 완료 및 배포

### ✅ 완료된 작업

#### 1. OpenAI Whisper API 연동
- **시간**: 오전 10:00 - 11:00
- **작업**: `whisper-api-server.py` FastAPI 백엔드 구현
- **결과**: 
  - POST /transcribe 엔드포인트 구현
  - POST /batch-transcribe 엔드포인트 구현
  - GET /health 엔드포인트 구현
  - CORS 미들웨어 추가

#### 2. 의존성 버전 문제 해결
- **시간**: 오전 11:00 - 12:00
- **문제**: `openai` 라이브러리 버전 호환성 이슈
  - `openai==0.28.1` → `ImportError: cannot import name 'OpenAI'`
  - `openai==1.35.1` → `TypeError: httpx proxies argument`
- **해결**: `openai==1.57.4`로 업데이트
- **변경 파일**: `requirements-whisper-api.txt`

#### 3. GCP VM 배포
- **시간**: 오후 1:00 - 3:00
- **작업**:
  - GitHub 저장소 새로 생성: `CloudComputing_Medtalk_Web`
  - 기존 저장소 (WEBUI)에서 필요한 파일만 분리
  - GCP VM SSH 접속 및 환경 설정
  - Python venv 설정 (Debian python3-venv 패키지 설치 필요했음)
  - 의존성 설치
  - 서버 실행 및 테스트
- **VM 정보**:
  - 인스턴스: whisper-ai-web
  - IP: 34.71.58.225
  - 위치: /home/mk4434/whisper-service/
- **문제**:
  - Debian에서 `python` 명령어 없음 → `python3` 사용
  - `venv` 생성 실패 → `python3.11-venv` 패키지 설치 필요
  - Port 8000 Docker와 충돌 → 방화벽 규칙 추가로 해결

#### 4. 방화벽 설정
- **시간**: 오후 3:00 - 3:30
- **작업**: GCP 방화벽 규칙 추가
  - Port 8000: Whisper API 접근 허용
  - Source: 0.0.0.0/0 (모든 IP)
- **결과**: API 외부 접근 가능 (`http://34.71.58.225:8000`)

#### 5. Web UI 업데이트
- **시간**: 오후 3:30 - 4:30
- **작업**:
  - 기존 Web UI가 mock 데이터만 표시
  - 실제 API 호출하도록 `transcribeAudio()` 함수 수정
  - `http://34.71.58.225:8000/transcribe`로 POST 요청
  - 응답 결과를 UI에 표시
- **배포**:
  - VM의 `/home/aidesigner/medtalk-project/index.html` 업데이트
  - `npx serve` 재시작

#### 6. 문서 정리
- **시간**: 오후 4:30 - 6:00
- **작업**:
  - 불필요한 파일 삭제 (13개 파일 제거)
    - 중복 문서: DEPLOY-GCP.md, INTEGRATION-GUIDE.md 등
    - 사용 안 하는 파일: whisper-free-server.py, requirements-free.txt
    - 불필요한 스크립트: start-server.sh, test-server.sh 등
  - README.md 한국어로 재작성
    - 지환님(팀원)이 보실 핵심 내용을 최상단에 배치
    - 부가 정보는 `<details>` 태그로 접을 수 있게 구성
  - `.ai/` 디렉토리 생성 및 문서화
    - PROJECT_CONTEXT.md: 프로젝트 전체 개요
    - WORK_LOG.md: 작업 일지 (현재 파일)

---

## 🔧 기술적 결정 사항

### 1. OpenAI Whisper API 선택 이유
- **대안 고려**: Hugging Face Inference API (무료)
- **결정**: OpenAI Whisper API 사용
- **이유**:
  - 높은 정확도 (의료 분야에 중요)
  - 안정적인 서비스 (SLA 보장)
  - Hugging Face API 엔드포인트 변경 (deprecated)
  - 비용 합리적 ($0.006/분)

### 2. 가상환경 필수 사용
- **이유**: Debian 12의 externally-managed-environment 정책
- **방법**: `python3 -m venv venv` + `source venv/bin/activate`
- **대안 거부**: `--break-system-packages` (시스템 패키지 오염 위험)

### 3. API 키 관리 방식
- **방법**: 환경 변수 (`export OPENAI_API_KEY=...`)
- **보안**:
  - Git에 커밋 안 됨 (`.gitignore`)
  - Read-only 권한 키 사용
  - GitHub Push Protection 통과
- **배포**: VM에서 환경 변수로 설정 (코드와 분리)

### 4. GitHub 저장소 분리
- **기존**: `WEBUI` (전체 CloudComputing 폴더 포함)
- **신규**: `CloudComputing_Medtalk_Web` (WEBUI 내용만)
- **이유**:
  - 불필요한 파일 제거 (SimpleMicroservices 등)
  - 깔끔한 프로젝트 구조
  - 팀원이 이해하기 쉽게

### 5. README 구조
- **기존**: 긴 영어 문서, 모든 내용 나열
- **변경**: 한국어, 핵심 내용 최상단 + 부가 정보 접기
- **이유**: 지환님(팀원)이 빠르게 필요한 정보만 확인 가능

---

## 🐛 발생한 이슈 및 해결

### Issue #1: OpenAI 라이브러리 버전 호환성
**날짜**: 2025-11-22  
**증상**: `ImportError: cannot import name 'OpenAI' from 'openai'`  
**원인**: `openai==0.28.1` (구버전) 사용 중  
**해결**: `requirements-whisper-api.txt`에서 `openai==1.57.4`로 업데이트  
**관련 커밋**: `Fix: Update to OpenAI 1.57.4 for httpx compatibility`

### Issue #2: GCP VM Python 환경 설정
**날짜**: 2025-11-22  
**증상**: `ensurepip is not available`  
**원인**: Debian에 `python3-venv` 패키지 미설치  
**해결**:
```bash
sudo apt update
sudo apt install -y python3.11-venv
python3 -m venv venv
```

### Issue #3: 포트 충돌
**날짜**: 2025-11-22  
**증상**: `[Errno 48] Address already in use` (Port 8000)  
**원인**: Docker가 8000번 포트 사용 중  
**해결**: 방화벽 규칙 추가로 외부 접근 허용 (내부 포트는 그대로 유지)

### Issue #4: GitHub Push Protection
**날짜**: 2025-11-22  
**증상**: `GITHUB PUSH PROTECTION - Push cannot contain secrets`  
**원인**: `test-transcription.sh`와 `MANUAL-DEPLOY.md`에 API 키 하드코딩  
**해결**: 해당 파일에서 API 키 제거, 커밋 수정 후 재푸시

### Issue #5: Web UI Mock 데이터만 표시
**날짜**: 2025-11-22  
**증상**: "API key가 설정되지 않음" 메시지만 표시  
**원인**: `transcribeAudio()` 함수가 `setTimeout()` mock 구현  
**해결**: 실제 `fetch()` 호출로 변경, API 엔드포인트 연결  
**관련 커밋**: `Update Web UI to use real Whisper API`

---

## 📊 프로젝트 통계

### 코드 변경 사항
- **추가된 파일**: 5개 (whisper-api-server.py, requirements 등)
- **삭제된 파일**: 13개 (중복 문서, 불필요한 스크립트)
- **최종 파일 수**: 7개 (핵심 파일만 유지)

### Git 커밋
- **총 커밋 수**: 8개
- **주요 커밋**:
  1. `Initial commit - MedTalk Assist Whisper API Service`
  2. `Fix: Update OpenAI library to v1.35.1`
  3. `Fix: Update to OpenAI 1.57.4 for httpx compatibility`
  4. `Update Web UI to use real Whisper API`
  5. `정리: 불필요한 파일 삭제 및 한국어 README 작성`
  6. `docs: README 구조 개선 - 핵심 내용 최상단 배치`

### 배포 정보
- **배포 환경**: GCP Compute Engine (Debian 12)
- **외부 IP**: 34.71.58.225
- **서비스 포트**: 8000 (API), 5000 (Web UI)
- **배포 상태**: ✅ Production

---

## 🚀 다음 작업 (TODO)

### 우선순위 높음
- [ ] API 인증/인가 추가 (보안 강화)
- [ ] 에러 로깅 시스템 구축 (Sentry 또는 GCP Logging)
- [ ] Health check 모니터링 자동화

### 우선순위 중간
- [ ] Redis 캐싱 (동일 파일 중복 처리 방지)
- [ ] Rate Limiting (악용 방지)
- [ ] Batch 처리 성능 최적화

### 우선순위 낮음
- [ ] Docker 컨테이너화
- [ ] CI/CD 파이프라인 (GitHub Actions)
- [ ] 테스트 코드 작성 (pytest)

---

## 📞 팀 커뮤니케이션

### 지환님 (Composite Service 담당)
- **전달 완료**: API 엔드포인트, 사용법, 코드 예제
- **문서 공유**: GitHub README (핵심 내용 최상단 배치)
- **대기 중**: Composite Service 연동 피드백

---

**최종 업데이트**: 2025-11-22 18:00  
**작성자**: AI Developer

