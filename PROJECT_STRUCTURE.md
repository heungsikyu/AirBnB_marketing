# 📁 프로젝트 구조

## 🏗️ 전체 구조

```
AirBnB_marketing/
├── 📁 backend/                    # FastAPI 백엔드 서버
│   ├── 📁 api/                    # API 모듈 (미사용)
│   ├── 📁 models/                 # 데이터 모델 (미사용)
│   ├── 📁 routes/                 # API 라우터
│   │   ├── __init__.py
│   │   ├── dashboard.py           # 대시보드 API
│   │   ├── properties.py          # 숙소 관리 API
│   │   ├── notifications.py       # 알림 API
│   │   ├── analytics.py           # 분석 API
│   │   └── settings.py            # 설정 API
│   ├── 📁 services/               # 비즈니스 로직 (미사용)
│   ├── 📁 static/                 # 정적 파일 (프론트엔드 빌드 결과)
│   ├── main.py                    # FastAPI 메인 서버
│   └── requirements.txt           # 백엔드 의존성 (미사용)
│
├── 📁 frontend/                   # React 프론트엔드
│   ├── 📁 public/                 # 정적 파일
│   ├── 📁 src/
│   │   ├── 📁 components/         # React 컴포넌트
│   │   │   └── Layout.tsx         # 레이아웃 컴포넌트
│   │   ├── 📁 pages/              # 페이지 컴포넌트
│   │   │   ├── Dashboard.tsx      # 대시보드
│   │   │   ├── Properties.tsx     # 숙소 관리
│   │   │   ├── Notifications.tsx  # 알림
│   │   │   ├── Analytics.tsx      # 분석
│   │   │   └── Settings.tsx       # 설정
│   │   ├── 📁 services/           # API 서비스
│   │   │   ├── api.ts             # API 클라이언트
│   │   │   └── websocket.ts       # WebSocket 서비스
│   │   ├── 📁 types/              # TypeScript 타입
│   │   │   └── index.ts           # 타입 정의
│   │   ├── 📁 utils/              # 유틸리티 (미사용)
│   │   ├── App.tsx                # 메인 앱 컴포넌트
│   │   ├── main.tsx               # 앱 진입점
│   │   └── index.css              # 글로벌 스타일
│   ├── index.html                 # HTML 템플릿
│   ├── package.json               # 프론트엔드 의존성
│   ├── tailwind.config.js         # Tailwind CSS 설정
│   ├── tsconfig.json              # TypeScript 설정
│   └── vite.config.ts             # Vite 설정
│
├── 📁 src/                        # 핵심 자동화 모듈
│   ├── __init__.py
│   ├── airbnb_scraper.py          # Airbnb 데이터 수집
│   ├── content_generator.py       # AI 콘텐츠 생성
│   ├── database.py                # 데이터베이스 관리
│   ├── scheduler.py               # 작업 스케줄링
│   └── social_media_manager.py    # 소셜 미디어 포스팅
│
├── 📁 shared/                     # 공유 모듈 (미사용)
├── 📁 generated_images/           # 생성된 이미지
├── 📁 reports/                    # 보고서
├── 📁 logs/                       # 로그 파일
├── 📁 data/                       # 데이터 파일
│
├── 📄 main.py                     # 기존 자동화 프로그램 진입점
├── 📄 config.py                   # 설정 관리
├── 📄 config.env                  # 환경 변수 (실제)
├── 📄 config.env.example          # 환경 변수 (예시)
├── 📄 requirements.txt            # 통합 Python 의존성
├── 📄 setup.py                    # 설치 스크립트
├── 📄 venv_setup.py               # 가상환경 설정
│
├── 🚀 run_dashboard.py            # 통합 실행 (권장)
├── 🚀 run_backend.py              # 백엔드만 실행
├── 🚀 run_frontend.py             # 프론트엔드만 실행
├── 🚀 run.sh                      # 기존 자동화 실행 (Unix)
├── 🚀 run.bat                     # 기존 자동화 실행 (Windows)
├── 🚀 venv_activate.sh            # 가상환경 활성화 (Unix)
└── 🚀 venv_activate.bat           # 가상환경 활성화 (Windows)
│
├── 📁 venv/                       # Python 가상환경
└── 📄 README.md                   # 프로젝트 문서
```

## 🎯 디렉토리별 역할

### **Backend (FastAPI)**
- **`main.py`**: FastAPI 서버 진입점, WebSocket 연결 관리
- **`routes/`**: REST API 엔드포인트 정의
  - `dashboard.py`: 대시보드 통계 및 시스템 상태
  - `properties.py`: 숙소 CRUD 및 관리
  - `notifications.py`: 알림 관리 및 실시간 업데이트
  - `analytics.py`: 성과 분석 및 리포트
  - `settings.py`: 시스템 설정 및 API 키 관리

### **Frontend (React + TypeScript)**
- **`src/pages/`**: 각 기능별 페이지 컴포넌트
- **`src/components/`**: 재사용 가능한 UI 컴포넌트
- **`src/services/`**: 백엔드 API 통신 및 WebSocket
- **`src/types/`**: TypeScript 타입 정의

### **Core Modules (기존 자동화)**
- **`airbnb_scraper.py`**: 한국 15개 도시 숙소 데이터 수집
- **`content_generator.py`**: OpenAI를 활용한 콘텐츠 생성
- **`social_media_manager.py`**: Instagram, YouTube, WordPress 포스팅
- **`database.py`**: SQLite 데이터베이스 관리
- **`scheduler.py`**: 자동화 작업 스케줄링

## 🔄 실행 흐름

### **1. 통합 실행 (권장)**
```bash
python run_dashboard.py
```
- 백엔드 서버 (포트 8000) + 프론트엔드 서버 (포트 3000) 동시 실행
- 대시보드: http://localhost:3000

### **2. 개별 실행**
```bash
# 백엔드만
python run_backend.py

# 프론트엔드만 (별도 터미널)
python run_frontend.py
```

### **3. 기존 자동화만**
```bash
# Unix/Linux/macOS
./run.sh

# Windows
run.bat
```

## 📦 의존성 관리

- **`requirements.txt`**: 통합 Python 의존성 (자동화 + 백엔드)
- **`frontend/package.json`**: 프론트엔드 Node.js 의존성
- **가상환경**: `venv/` 디렉토리에 격리된 Python 환경

## 🗂️ 데이터 저장소

- **`data/`**: SQLite 데이터베이스 파일
- **`generated_images/`**: AI 생성 이미지
- **`reports/`**: 성과 보고서
- **`logs/`**: 시스템 로그

## 🔧 설정 파일

- **`config.env`**: 실제 API 키 및 설정 (Git에서 제외)
- **`config.env.example`**: 설정 예시 템플릿
- **`config.py`**: Python 설정 관리 모듈
