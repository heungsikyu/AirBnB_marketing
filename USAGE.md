# 📖 사용법 가이드

## 🎯 프로그램 개요

Airbnb 한국 숙소 마케팅 자동화 프로그램은 다음과 같은 워크플로우로 작동합니다:

1. **데이터 수집** → 2. **콘텐츠 생성** → 3. **소셜미디어 게시** → 4. **분석 및 추적**

## 🚀 첫 실행하기

### 1단계: 환경 설정

```bash
# 1. Python 3.8+ 설치 확인
python --version

# 2. 프로젝트 디렉토리로 이동
cd AirBnB_marketing

# 3. 설치 스크립트 실행
python setup.py
```

### 2단계: API 키 설정

`config.env` 파일을 열어서 필요한 API 키를 입력하세요:

```env
# 필수 설정
OPENAI_API_KEY=sk-your-openai-api-key-here
INSTAGRAM_USERNAME=your_instagram_username
INSTAGRAM_PASSWORD=your_instagram_password

# 선택 설정 (해당 플랫폼을 사용하지 않으면 비워두세요)
YOUTUBE_CLIENT_ID=your_youtube_client_id
YOUTUBE_CLIENT_SECRET=your_youtube_client_secret
YOUTUBE_REFRESH_TOKEN=your_youtube_refresh_token
WORDPRESS_URL=https://your-blog.com
WORDPRESS_USERNAME=your_wordpress_username
WORDPRESS_PASSWORD=your_wordpress_password
```

### 3단계: 프로그램 실행

```bash
# Windows
run.bat

# Unix/Linux/macOS
./run.sh

# 또는 직접 실행
python main.py
```

## 📋 상세 사용법

### 1. 수동 실행

#### 일일 마케팅 작업 실행
```python
from main import AirbnbMarketingBot

# 봇 인스턴스 생성
bot = AirbnbMarketingBot()

# 일일 마케팅 작업 실행
bot.run_daily_marketing()
```

#### 특정 숙소 콘텐츠 생성
```python
from src.content_generator import ContentGenerator

# 콘텐츠 생성기 초기화
generator = ContentGenerator()

# 숙소 데이터 (예시)
property_data = {
    'id': 'test_property_1',
    'title': '서울 강남의 아름다운 아파트',
    'city': '서울',
    'price_per_night': 150000,
    'rating': 4.8,
    'max_guests': 4,
    'amenities': ['WiFi', '주차장', '에어컨'],
    'description': '강남 중심가의 편리한 위치에 있는 아파트입니다.'
}

# 콘텐츠 생성
content = generator.create_property_content(property_data)
print(content)
```

#### 소셜미디어 게시
```python
from src.social_media_manager import SocialMediaManager

# 소셜미디어 매니저 초기화
manager = SocialMediaManager()

# 모든 플랫폼에 게시
result = manager.post_to_all_platforms(content, property_data)
print(result)
```

### 2. 스케줄링 설정

#### 포스팅 시간 변경
`config.env` 파일에서 `POSTING_SCHEDULE` 값을 수정하세요:

```env
# 하루 2번 포스팅 (10:00, 18:00)
POSTING_SCHEDULE=10:00,18:00

# 하루 1번 포스팅 (14:00)
POSTING_SCHEDULE=14:00

# 하루 4번 포스팅 (09:00, 12:00, 15:00, 18:00)
POSTING_SCHEDULE=09:00,12:00,15:00,18:00
```

#### 커스텀 스케줄 추가
```python
from src.scheduler import MarketingScheduler
from datetime import datetime

# 스케줄러 초기화
scheduler = MarketingScheduler()

# 커스텀 작업 함수 정의
def custom_marketing_task():
    print("커스텀 마케팅 작업 실행!")

# 매일 오후 2시에 실행되는 스케줄 추가
scheduler.add_custom_schedule(
    job_func=custom_marketing_task,
    schedule_time="14:00",
    job_name="custom_marketing"
)
```

### 3. 데이터 관리

#### 숙소 데이터 조회
```python
from src.database import DatabaseManager

# 데이터베이스 매니저 초기화
db = DatabaseManager()

# 모든 숙소 조회
properties = db.get_all_properties(limit=10)
for prop in properties:
    print(f"{prop['title']} - {prop['city']} - {prop['price_per_night']:,}원")

# 특정 숙소 조회
property_data = db.get_property_data('property_id_here')
if property_data:
    print(property_data['title'])
```

#### 미게시 콘텐츠 조회
```python
# 미게시된 콘텐츠 조회
pending_content = db.get_pending_content(limit=5)
for content in pending_content:
    print(f"미게시 콘텐츠: {content['property_id']} - {content['content_type']}")
```

#### 게시 이력 조회
```python
# 최근 7일간 게시 이력 조회
analytics = db.get_posting_analytics(days=7)
for analytics_data in analytics:
    print(f"{analytics_data['platform']}: {analytics_data['status']} - {analytics_data['posted_at']}")
```

### 4. 분석 및 모니터링

#### 실시간 로그 확인
```bash
# 전체 로그 확인
tail -f airbnb_marketing.log

# 에러만 확인
grep "ERROR" airbnb_marketing.log

# 특정 모듈 로그 확인
grep "content_generator" airbnb_marketing.log
```

#### 성과 분석
```python
from src.social_media_manager import SocialMediaManager

# 소셜미디어 매니저 초기화
manager = SocialMediaManager()

# 특정 숙소의 분석 데이터 조회
analytics = manager.get_posting_analytics('property_id_here')
print(analytics)

# 전환 추적 URL 생성
tracking_result = manager.track_conversion('property_id_here', 'instagram')
print(f"추적 URL: {tracking_result['tracking_url']}")
```

#### 리포트 생성
```python
from src.scheduler import MarketingScheduler

# 스케줄러 초기화
scheduler = MarketingScheduler()

# 수동으로 분석 리포트 생성
scheduler._run_analytics_report()

# 수동으로 월간 리포트 생성
scheduler._run_monthly_report()
```

## 🔧 고급 설정

### 1. 콘텐츠 생성 커스터마이징

`config.py` 파일에서 콘텐츠 설정을 수정할 수 있습니다:

```python
# 콘텐츠 설정 수정
CONTENT_SETTINGS = {
    'max_title_length': 60,        # 제목 최대 길이
    'max_description_length': 600, # 설명 최대 길이
    'hashtag_limit': 20,           # 해시태그 개수 제한
    'image_quality': 90,           # 이미지 품질 (1-100)
    'max_image_size': (1200, 1200), # 이미지 최대 크기
}
```

### 2. 대상 도시 설정

`config.py`에서 `KOREAN_CITIES` 딕셔너리를 수정하여 대상 도시를 변경할 수 있습니다:

```python
KOREAN_CITIES = {
    '서울': {'lat': 37.5665, 'lng': 126.9780, 'priority': 1},
    '부산': {'lat': 35.1796, 'lng': 129.0756, 'priority': 2},
    # 새로운 도시 추가
    '춘천': {'lat': 37.8813, 'lng': 127.7298, 'priority': 3},
}
```

### 3. 스크래핑 설정 조정

```python
SCRAPING_SETTINGS = {
    'request_delay': (2, 5),  # 요청 간 지연 시간 (초)
    'max_retries': 5,         # 최대 재시도 횟수
    'timeout': 60,            # 타임아웃 (초)
}
```

## 🐛 문제 해결

### 1. 일반적인 오류

#### ModuleNotFoundError
```bash
# 필요한 패키지 설치
pip install -r requirements.txt

# 가상환경 사용
python -m venv venv
source venv/bin/activate  # Unix/Linux/macOS
venv\Scripts\activate     # Windows
```

#### API 키 오류
```python
from config import config

# 설정 상태 확인
config.print_config_status()

# 특정 설정 확인
print(f"OpenAI API 키: {'설정됨' if config.OPENAI_API_KEY else '설정 안됨'}")
```

#### 데이터베이스 오류
```bash
# 데이터베이스 파일 삭제 후 재생성
rm airbnb_marketing.db
python -c "from src.database import DatabaseManager; DatabaseManager()"
```

### 2. 로그 분석

#### 에러 로그 분석
```bash
# 최근 에러 확인
grep -i "error" airbnb_marketing.log | tail -10

# 특정 시간대 에러 확인
grep "2024-01-01 14:" airbnb_marketing.log | grep -i "error"
```

#### 성능 모니터링
```bash
# 처리 속도 확인
grep "완료" airbnb_marketing.log | tail -5

# 메모리 사용량 확인 (Linux/macOS)
ps aux | grep python
```

### 3. 데이터 정리

#### 오래된 데이터 정리
```python
from src.database import DatabaseManager

db = DatabaseManager()
# 90일 이전 데이터 정리
db.cleanup_old_data(days=90)
```

#### 로그 파일 정리
```bash
# 7일 이전 로그 파일 삭제
find logs/ -name "*.log" -mtime +7 -delete

# 로그 파일 압축
gzip airbnb_marketing.log
```

## 📊 성능 최적화

### 1. 메모리 사용량 최적화

```python
# 대량 데이터 처리 시 배치 처리
def process_properties_in_batches(properties, batch_size=10):
    for i in range(0, len(properties), batch_size):
        batch = properties[i:i+batch_size]
        process_batch(batch)
```

### 2. API 호출 최적화

```python
# 요청 간 지연 시간 조정
import time
import random

def optimized_request():
    time.sleep(random.uniform(1, 3))  # 1-3초 지연
    # API 호출
```

### 3. 데이터베이스 최적화

```python
# 인덱스 생성 (필요시)
from src.database import DatabaseManager

db = DatabaseManager()
# 인덱스 생성 쿼리 실행
```

## 🔒 보안 고려사항

### 1. API 키 보안

```python
# 환경 변수 사용
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
```

### 2. 로그 보안

```python
# 민감한 정보 마스킹
def mask_sensitive_data(data):
    if 'password' in data:
        data['password'] = '***'
    return data
```

### 3. 데이터 암호화

```python
# 중요 데이터 암호화 (필요시)
import hashlib

def encrypt_data(data):
    return hashlib.sha256(data.encode()).hexdigest()
```

## 📈 모니터링 대시보드

### 1. 기본 모니터링

```python
# 프로그램 상태 확인
def check_program_status():
    from src.database import DatabaseManager
    from config import config
    
    db = DatabaseManager()
    
    # 데이터베이스 연결 확인
    properties_count = len(db.get_all_properties(limit=1))
    
    # 설정 상태 확인
    config_status = config.validate_config()
    
    return {
        'database_connected': properties_count >= 0,
        'config_valid': config_status['valid'],
        'enabled_platforms': config.get_enabled_platforms()
    }
```

### 2. 성과 지표 모니터링

```python
# 일일 성과 지표
def get_daily_metrics():
    from src.database import DatabaseManager
    
    db = DatabaseManager()
    analytics = db.get_posting_analytics(days=1)
    
    total_posts = len(analytics)
    successful_posts = len([a for a in analytics if a['status'] == 'success'])
    
    return {
        'total_posts': total_posts,
        'successful_posts': successful_posts,
        'success_rate': (successful_posts / total_posts * 100) if total_posts > 0 else 0
    }
```

이제 프로그램을 사용할 준비가 완료되었습니다! 🎉
