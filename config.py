"""
설정 관리 모듈
환경 변수와 설정값을 관리
"""

import os
from dotenv import load_dotenv
from typing import Dict, Any

# 환경 변수 로드
load_dotenv()

class Config:
    """설정 클래스"""
    
    # 기본 설정
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    # 데이터베이스 설정
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///airbnb_marketing.db')
    
    # Airbnb API 설정
    AIRBNB_API_KEY = os.getenv('AIRBNB_API_KEY')
    AIRBNB_API_SECRET = os.getenv('AIRBNB_API_SECRET')
    
    # OpenAI API 설정
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')
    
    # Instagram 설정
    INSTAGRAM_USERNAME = os.getenv('INSTAGRAM_USERNAME')
    INSTAGRAM_PASSWORD = os.getenv('INSTAGRAM_PASSWORD')
    
    # YouTube 설정
    YOUTUBE_CLIENT_ID = os.getenv('YOUTUBE_CLIENT_ID')
    YOUTUBE_CLIENT_SECRET = os.getenv('YOUTUBE_CLIENT_SECRET')
    YOUTUBE_REFRESH_TOKEN = os.getenv('YOUTUBE_REFRESH_TOKEN')
    
    # WordPress 블로그 설정
    WORDPRESS_URL = os.getenv('WORDPRESS_URL')
    WORDPRESS_USERNAME = os.getenv('WORDPRESS_USERNAME')
    WORDPRESS_PASSWORD = os.getenv('WORDPRESS_PASSWORD')
    
    # 스케줄링 설정
    POSTING_SCHEDULE = os.getenv('POSTING_SCHEDULE', '09:00,15:00,21:00').split(',')
    
    # 한국 도시 설정
    KOREAN_CITIES = {
        '서울': {'lat': 37.5665, 'lng': 126.9780, 'priority': 1},
        '부산': {'lat': 35.1796, 'lng': 129.0756, 'priority': 2},
        '인천': {'lat': 37.4563, 'lng': 126.7052, 'priority': 3},
        '대구': {'lat': 35.8714, 'lng': 128.6014, 'priority': 4},
        '대전': {'lat': 36.3504, 'lng': 127.3845, 'priority': 5},
        '광주': {'lat': 35.1595, 'lng': 126.8526, 'priority': 6},
        '울산': {'lat': 35.5384, 'lng': 129.3114, 'priority': 7},
        '세종': {'lat': 36.4800, 'lng': 127.2890, 'priority': 8},
        '제주': {'lat': 33.4996, 'lng': 126.5312, 'priority': 9},
        '수원': {'lat': 37.2636, 'lng': 127.0286, 'priority': 10},
        '고양': {'lat': 37.6584, 'lng': 126.8320, 'priority': 11},
        '용인': {'lat': 37.2411, 'lng': 127.1776, 'priority': 12},
        '성남': {'lat': 37.4201, 'lng': 127.1267, 'priority': 13},
        '부천': {'lat': 37.5034, 'lng': 126.7660, 'priority': 14},
        '화성': {'lat': 37.1995, 'lng': 126.8314, 'priority': 15},
    }
    
    # 콘텐츠 생성 설정
    CONTENT_SETTINGS = {
        'max_title_length': 50,
        'max_description_length': 500,
        'hashtag_limit': 15,
        'image_quality': 95,
        'image_formats': ['jpg', 'png'],
        'video_formats': ['mp4', 'mov'],
        'max_video_duration': 60,  # 초
        'max_image_size': (1080, 1080),  # 픽셀
        'story_image_size': (1080, 1920),
        'thumbnail_size': (1280, 720),
    }
    
    # 소셜미디어 설정
    SOCIAL_MEDIA_SETTINGS = {
        'instagram': {
            'max_caption_length': 2200,
            'max_hashtags': 30,
            'story_duration': 15,  # 초
            'reels_duration': 30,  # 초
        },
        'youtube': {
            'max_title_length': 100,
            'max_description_length': 5000,
            'max_tags': 15,
            'shorts_duration': 60,  # 초
        },
        'blog': {
            'max_title_length': 100,
            'min_content_length': 500,
            'max_content_length': 5000,
            'max_tags': 10,
        }
    }
    
    # 스크래핑 설정
    SCRAPING_SETTINGS = {
        'request_delay': (1, 3),  # 요청 간 지연 시간 (초)
        'max_retries': 3,
        'timeout': 30,
        'user_agents': [
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        ],
        'headers': {
            'Accept': 'application/json',
            'Accept-Language': 'ko-KR,ko;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
    }
    
    # 분석 설정
    ANALYTICS_SETTINGS = {
        'tracking_period_days': 30,
        'report_generation_hour': 8,
        'data_cleanup_days': 90,
        'conversion_tracking': True,
        'performance_metrics': [
            'likes', 'comments', 'shares', 'views', 'clicks', 'conversions'
        ]
    }
    
    # 에러 처리 설정
    ERROR_SETTINGS = {
        'max_retries': 3,
        'retry_delay': 5,  # 초
        'error_notification': True,
        'log_errors': True,
        'save_failed_content': True,
    }
    
    @classmethod
    def validate_config(cls) -> Dict[str, Any]:
        """설정 유효성 검사"""
        errors = []
        warnings = []
        
        # 필수 설정 확인
        required_settings = [
            ('OPENAI_API_KEY', 'OpenAI API 키'),
            ('INSTAGRAM_USERNAME', '인스타그램 사용자명'),
            ('INSTAGRAM_PASSWORD', '인스타그램 비밀번호'),
        ]
        
        for setting, description in required_settings:
            if not getattr(cls, setting):
                errors.append(f"{description}이 설정되지 않았습니다: {setting}")
        
        # 선택적 설정 확인
        optional_settings = [
            ('AIRBNB_API_KEY', 'Airbnb API 키'),
            ('YOUTUBE_CLIENT_ID', 'YouTube 클라이언트 ID'),
            ('WORDPRESS_URL', 'WordPress URL'),
        ]
        
        for setting, description in optional_settings:
            if not getattr(cls, setting):
                warnings.append(f"{description}이 설정되지 않았습니다: {setting}")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings
        }
    
    @classmethod
    def get_city_priority(cls, city_name: str) -> int:
        """도시 우선순위 반환"""
        return cls.KOREAN_CITIES.get(city_name, {}).get('priority', 999)
    
    @classmethod
    def get_city_coordinates(cls, city_name: str) -> tuple:
        """도시 좌표 반환"""
        city_data = cls.KOREAN_CITIES.get(city_name, {})
        return city_data.get('lat', 0), city_data.get('lng', 0)
    
    @classmethod
    def get_priority_cities(cls, limit: int = 10) -> list:
        """우선순위가 높은 도시 목록 반환"""
        cities = sorted(
            cls.KOREAN_CITIES.items(),
            key=lambda x: x[1]['priority']
        )
        return [city[0] for city in cities[:limit]]
    
    @classmethod
    def get_random_user_agent(cls) -> str:
        """랜덤 User-Agent 반환"""
        import random
        return random.choice(cls.SCRAPING_SETTINGS['user_agents'])
    
    @classmethod
    def get_request_delay(cls) -> float:
        """요청 지연 시간 반환"""
        import random
        delay_range = cls.SCRAPING_SETTINGS['request_delay']
        return random.uniform(delay_range[0], delay_range[1])
    
    @classmethod
    def is_platform_enabled(cls, platform: str) -> bool:
        """플랫폼 활성화 상태 확인"""
        platform_settings = {
            'instagram': bool(cls.INSTAGRAM_USERNAME and cls.INSTAGRAM_PASSWORD),
            'youtube': bool(cls.YOUTUBE_CLIENT_ID and cls.YOUTUBE_CLIENT_SECRET),
            'blog': bool(cls.WORDPRESS_URL and cls.WORDPRESS_USERNAME and cls.WORDPRESS_PASSWORD),
        }
        return platform_settings.get(platform, False)
    
    @classmethod
    def get_enabled_platforms(cls) -> list:
        """활성화된 플랫폼 목록 반환"""
        platforms = ['instagram', 'youtube', 'blog']
        return [platform for platform in platforms if cls.is_platform_enabled(platform)]
    
    @classmethod
    def print_config_status(cls):
        """설정 상태 출력"""
        validation = cls.validate_config()
        
        print("🔧 설정 상태:")
        
        if validation['valid']:
            print("✅ 모든 필수 설정이 완료되었습니다.")
        else:
            print("❌ 필수 설정이 누락되었습니다:")
            for error in validation['errors']:
                print(f"  - {error}")
        
        if validation['warnings']:
            print("⚠️ 선택적 설정이 누락되었습니다:")
            for warning in validation['warnings']:
                print(f"  - {warning}")
        
        print(f"\n📱 활성화된 플랫폼: {', '.join(cls.get_enabled_platforms())}")
        print(f"🏙️ 대상 도시: {len(cls.KOREAN_CITIES)}개")
        print(f"⏰ 포스팅 스케줄: {', '.join(cls.POSTING_SCHEDULE)}")

# 설정 인스턴스 생성
config = Config()

if __name__ == "__main__":
    config.print_config_status()
