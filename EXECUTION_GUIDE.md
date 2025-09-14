# 🚀 실행 가이드

## 📋 스크립트별 역할

### **1. 설치 및 초기 설정**
```bash
# 전체 설치 (가상환경 + 패키지 + 설정)
python setup.py
```

### **2. 실행 방법 (3가지 옵션)**

#### **옵션 1: 통합 대시보드 실행 (권장) 🌟**
```bash
# 백엔드 + 프론트엔드 동시 실행
python run_dashboard.py
```
- **용도**: 관리자 대시보드 사용
- **접속**: http://localhost:3000 (대시보드)
- **API**: http://localhost:8000 (백엔드)

#### **옵션 2: 기존 자동화 프로그램만 실행**
```bash
# Windows
run.bat

# Unix/Linux/macOS
./run.sh
```
- **용도**: 자동화 프로그램만 실행 (대시보드 없음)
- **실행**: `main.py` (기존 자동화 로직)

#### **옵션 3: 개별 실행**
```bash
# 백엔드만 실행
python run_backend.py

# 프론트엔드만 실행 (별도 터미널)
python run_frontend.py
```

### **3. 가상환경 관리 (수동)**

#### **가상환경 활성화**
```bash
# Windows
venv_activate.bat

# Unix/Linux/macOS
./venv_activate.sh

# 또는 수동으로
# Windows
venv\Scripts\activate

# Unix/Linux/macOS
source venv/bin/activate
```

#### **가상환경 비활성화**
```bash
deactivate
```

## 🎯 사용 시나리오별 권장 방법

### **시나리오 1: 처음 설치**
1. `python setup.py` - 전체 설치
2. `config.env` 편집 - API 키 설정
3. `python run_dashboard.py` - 대시보드 실행

### **시나리오 2: 관리자 대시보드 사용**
```bash
python run_dashboard.py
```

### **시나리오 3: 자동화만 실행 (대시보드 불필요)**
```bash
# Windows
run.bat

# Unix/Linux/macOS
./run.sh
```

### **시나리오 4: 개발/디버깅**
```bash
# 가상환경 활성화
venv_activate.bat  # 또는 ./venv_activate.sh

# 개별 모듈 테스트
python -m src.airbnb_scraper
python -m src.content_generator
```

## 📁 스크립트 파일 정리

### **✅ 유지되는 파일들:**
- `setup.py` - 전체 설치 스크립트
- `run_dashboard.py` - 통합 대시보드 실행 (권장)
- `run_backend.py` - 백엔드만 실행
- `run_frontend.py` - 프론트엔드만 실행
- `run.bat` / `run.sh` - 기존 자동화 프로그램 실행
- `venv_activate.bat` / `venv_activate.sh` - 가상환경 활성화 편의 스크립트

### **❌ 제거된 파일들:**
- `venv_setup.py` - `setup.py`와 중복

## 🔧 문제 해결

### **가상환경이 없을 때**
```bash
python setup.py
```

### **패키지 설치 오류**
```bash
# 가상환경 활성화 후
pip install -r requirements.txt
```

### **포트 충돌**
- 대시보드: 3000번 포트
- 백엔드: 8000번 포트
- 다른 프로그램이 사용 중이면 종료 후 재실행

### **Node.js 없을 때 (프론트엔드 실행 시)**
- Node.js 설치: https://nodejs.org/
- 설치 후 `python run_frontend.py` 재실행
