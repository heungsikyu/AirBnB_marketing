# 🏠 Airbnb 한국 숙소 마케팅 자동화 프로그램

한국 내 Airbnb 숙소를 자동으로 수집하고, 소셜미디어(Instagram, YouTube, 블로그)에 콘텐츠를 자동 게시하여 예약으로 연결하는 마케팅 자동화 프로그램입니다.

## ✨ 주요 기능

### 🏠 숙소 데이터 수집
- 한국 주요 도시의 Airbnb 숙소 정보 자동 수집
- 숙소 상세 정보, 가격, 평점, 편의시설 등 수집
- 실시간 데이터 업데이트 및 중복 방지

### 🤖 AI 콘텐츠 생성
- OpenAI GPT를 활용한 매력적인 한국어 콘텐츠 생성
- 플랫폼별 최적화된 텍스트 및 이미지 생성
- 해시태그 자동 생성 및 최적화

### 📱 소셜미디어 자동 게시
- **Instagram**: 피드, 스토리, 릴스 자동 게시
- **YouTube**: 일반 동영상 및 쇼츠 자동 업로드
- **블로그**: WordPress 자동 포스팅

### 📊 분석 및 추적
- 게시 성과 실시간 분석
- 예약 전환율 추적
- 플랫폼별 성과 리포트 생성

### ⏰ 자동화 스케줄링
- 사용자 정의 포스팅 스케줄
- 일일/주간/월간 자동 작업
- 데이터 정리 및 백업

## 🚀 빠른 시작

### 1. 설치

```bash
# 저장소 클론
git clone <repository-url>
cd AirBnB_marketing

# Python 3.8+ 설치 확인
python --version

# 가상환경을 사용한 설치 (권장)
python setup.py

# 또는 가상환경만 설정
python venv_setup.py
```

### 2. 설정

`config.env` 파일을 편집하여 API 키를 입력하세요:

```env
# OpenAI API 설정 (필수)
OPENAI_API_KEY=your_openai_api_key

# Instagram 설정 (필수)
INSTAGRAM_USERNAME=your_instagram_username
INSTAGRAM_PASSWORD=your_instagram_password

# YouTube 설정 (선택)
YOUTUBE_CLIENT_ID=your_youtube_client_id
YOUTUBE_CLIENT_SECRET=your_youtube_client_secret
YOUTUBE_REFRESH_TOKEN=your_youtube_refresh_token

# WordPress 블로그 설정 (선택)
WORDPRESS_URL=your_wordpress_url
WORDPRESS_USERNAME=your_wordpress_username
WORDPRESS_PASSWORD=your_wordpress_password

# 포스팅 스케줄 설정
POSTING_SCHEDULE=09:00,15:00,21:00
```

### 3. 실행

#### 방법 1: 통합 대시보드 실행 (권장) 🌟
```bash
# 백엔드 + 프론트엔드 동시 실행
python run_dashboard.py
```
- **접속**: http://localhost:3000 (대시보드)
- **API**: http://localhost:8000 (백엔드)

#### 방법 2: 기존 자동화 프로그램만 실행
```bash
# Windows
run.bat

# Unix/Linux/macOS
./run.sh
```
- **용도**: 자동화 프로그램만 실행 (대시보드 없음)

#### 방법 3: 개별 실행 (개발/디버깅용)
```bash
# 백엔드만 실행
python run_backend.py

# 프론트엔드만 실행 (별도 터미널)
python run_frontend.py
```

### 4. 접속 주소

- **대시보드**: http://localhost:3000
- **API 서버**: http://localhost:8000
- **API 문서**: http://localhost:8000/docs

> 📋 **자세한 실행 방법**: [EXECUTION_GUIDE.md](EXECUTION_GUIDE.md) 참조

## 📋 API 키 설정 가이드

### OpenAI API
1. [OpenAI Platform](https://platform.openai.com/)에서 계정 생성
2. API 키 생성 및 복사
3. `config.env`에 `OPENAI_API_KEY` 설정

### Instagram API
1. Instagram Business 계정 필요
2. Instagram Basic Display API 또는 Instagram Graph API 사용
3. 또는 Instagram Private API 사용 (주의: 정책 위반 가능성)

### YouTube API
1. [Google Cloud Console](https://console.cloud.google.com/)에서 프로젝트 생성
2. YouTube Data API v3 활성화
3. OAuth 2.0 클라이언트 ID 생성
4. `config.env`에 YouTube 설정 추가

### WordPress API
1. WordPress 사이트에 REST API 활이화
2. Application Password 생성
3. `config.env`에 WordPress 설정 추가

## 🏗️ 프로젝트 구조

```
AirBnB_marketing/
├── main.py                 # 메인 실행 파일
├── config.py              # 설정 관리
├── setup.py               # 설치 스크립트
├── requirements.txt       # Python 패키지 의존성
├── config.env.example     # 설정 파일 예제
├── src/                   # 소스 코드
│   ├── __init__.py
│   ├── airbnb_scraper.py  # Airbnb 데이터 수집
│   ├── content_generator.py # AI 콘텐츠 생성
│   ├── social_media_manager.py # 소셜미디어 관리
│   ├── database.py        # 데이터베이스 관리
│   └── scheduler.py       # 스케줄링
├── generated_images/      # 생성된 이미지
├── reports/              # 분석 리포트
├── logs/                 # 로그 파일
└── data/                 # 데이터 파일
```

## 🐍 가상환경 관리

### 가상환경 생성 및 설정
```bash
# 가상환경 생성 및 패키지 설치
python venv_setup.py

# 또는 전체 설치 (가상환경 포함)
python setup.py
```

### 가상환경 활성화
```bash
# Windows
venv_activate.bat
# 또는
venv\Scripts\activate

# Unix/Linux/macOS
./venv_activate.sh
# 또는
source venv/bin/activate
```

### 가상환경 비활성화
```bash
deactivate
```

### 가상환경 재설정
```bash
# 기존 가상환경 삭제 후 재생성
rm -rf venv  # Unix/Linux/macOS
rmdir /s venv  # Windows
python venv_setup.py
```

## 🔧 설정 옵션

### 포스팅 스케줄
```env
# 하루 3번 포스팅 (09:00, 15:00, 21:00)
POSTING_SCHEDULE=09:00,15:00,21:00

# 하루 1번 포스팅 (12:00)
POSTING_SCHEDULE=12:00
```

### 대상 도시 설정
`config.py`에서 `KOREAN_CITIES` 딕셔너리를 수정하여 대상 도시를 변경할 수 있습니다.

### 콘텐츠 설정
`config.py`에서 `CONTENT_SETTINGS`를 수정하여 콘텐츠 생성 옵션을 조정할 수 있습니다.

## 📊 사용법

### 1. 일일 마케팅 실행
```python
from main import AirbnbMarketingBot

bot = AirbnbMarketingBot()
bot.run_daily_marketing()
```

### 2. 특정 숙소 콘텐츠 생성
```python
from src.content_generator import ContentGenerator

generator = ContentGenerator()
content = generator.create_property_content(property_data)
```

### 3. 소셜미디어 게시
```python
from src.social_media_manager import SocialMediaManager

manager = SocialMediaManager()
result = manager.post_to_all_platforms(content, property_data)
```

### 4. 분석 데이터 조회
```python
from src.database import DatabaseManager

db = DatabaseManager()
analytics = db.get_posting_analytics()
```

## 📈 모니터링 및 분석

### 로그 확인
```bash
# 실시간 로그 확인
tail -f airbnb_marketing.log

# 에러 로그만 확인
grep "ERROR" airbnb_marketing.log
```

### 분석 리포트
- 일일 리포트: `reports/analytics_report_YYYYMMDD_HHMMSS.json`
- 월간 리포트: `reports/monthly_report_YYYYMM.json`

### 데이터베이스 확인
```python
from src.database import DatabaseManager

db = DatabaseManager()
properties = db.get_all_properties()
print(f"총 {len(properties)}개의 숙소 데이터")
```

## ⚠️ 주의사항

### 법적 고려사항
- Airbnb의 이용약관 및 API 사용 정책 준수
- 각 소셜미디어 플랫폼의 정책 준수
- 개인정보보호법 및 관련 법규 준수

### 기술적 제한사항
- Airbnb 공식 API 사용 시 API 호출 제한
- 소셜미디어 API 사용 시 게시 제한
- 웹 스크래핑 시 IP 차단 가능성

### 보안 고려사항
- API 키 및 비밀번호 보안 관리
- 정기적인 비밀번호 변경
- 로그 파일에 민감한 정보 노출 방지

## 🛠️ 문제 해결

### 일반적인 문제

#### 1. 패키지 설치 오류
```bash
# pip 업그레이드
python -m pip install --upgrade pip

# 가상환경 사용
python -m venv venv
source venv/bin/activate  # Unix/Linux/macOS
venv\Scripts\activate     # Windows
```

#### 2. API 키 오류
- `config.env` 파일의 API 키 확인
- API 키 유효성 검사
- 권한 설정 확인

#### 3. 데이터베이스 오류
```bash
# 데이터베이스 파일 삭제 후 재생성
rm airbnb_marketing.db
python setup.py
```

#### 4. 이미지 생성 오류
- 시스템에 한국어 폰트 설치
- PIL/Pillow 패키지 재설치
- 이미지 디렉토리 권한 확인

### 로그 분석
```bash
# 에러 로그 분석
grep -i "error\|exception\|failed" airbnb_marketing.log

# 특정 모듈 로그 확인
grep "content_generator" airbnb_marketing.log
```

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 `LICENSE` 파일을 참조하세요.

## 📞 지원

문제가 발생하거나 질문이 있으시면 다음을 통해 문의하세요:

- Issues: GitHub Issues 페이지
- 이메일: your-email@example.com
- 문서: 프로젝트 Wiki

## 🔄 업데이트 로그

### v1.0.0 (2024-01-01)
- 초기 버전 릴리스
- 기본 마케팅 자동화 기능
- Instagram, YouTube, 블로그 지원
- AI 콘텐츠 생성 기능

---

**면책 조항**: 이 프로그램은 교육 및 연구 목적으로 제작되었습니다. 상업적 사용 시 관련 법규 및 플랫폼 정책을 반드시 확인하고 준수하시기 바랍니다.
