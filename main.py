#!/usr/bin/env python3
"""
Airbnb 한국 숙소 마케팅 자동화 프로그램
Instagram, YouTube, 블로그에 자동으로 콘텐츠를 게시하고 예약으로 연결
"""

import os
import sys
import logging
from datetime import datetime
from dotenv import load_dotenv

# 프로젝트 루트를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.airbnb_scraper import AirbnbScraper
from src.content_generator import ContentGenerator
from src.social_media_manager import SocialMediaManager
from src.scheduler import MarketingScheduler
from src.database import DatabaseManager

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('airbnb_marketing.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class AirbnbMarketingBot:
    """Airbnb 마케팅 자동화 메인 클래스"""
    
    def __init__(self):
        """초기화"""
        load_dotenv()
        self.db_manager = DatabaseManager()
        self.airbnb_scraper = AirbnbScraper()
        self.content_generator = ContentGenerator()
        self.social_manager = SocialMediaManager()
        self.scheduler = MarketingScheduler()
        
    def run_daily_marketing(self):
        """일일 마케팅 작업 실행"""
        try:
            logger.info("일일 마케팅 작업 시작")
            
            # 1. 새로운 숙소 데이터 수집
            logger.info("숙소 데이터 수집 중...")
            properties = self.airbnb_scraper.get_korean_properties()
            
            if not properties:
                logger.warning("수집된 숙소가 없습니다.")
                return
                
            # 2. 콘텐츠 생성
            logger.info("콘텐츠 생성 중...")
            for property_data in properties:
                content = self.content_generator.create_property_content(property_data)
                
                # 3. 소셜미디어에 게시
                logger.info(f"소셜미디어 게시 중: {property_data.get('title', 'Unknown')}")
                self.social_manager.post_to_all_platforms(content, property_data)
                
                # 4. 데이터베이스에 저장
                self.db_manager.save_property_data(property_data, content)
                
            logger.info("일일 마케팅 작업 완료")
            
        except Exception as e:
            logger.error(f"마케팅 작업 중 오류 발생: {str(e)}")
            
    def run_scheduled_posting(self):
        """스케줄된 포스팅 실행"""
        try:
            logger.info("스케줄된 포스팅 시작")
            
            # 데이터베이스에서 미게시된 콘텐츠 조회
            pending_content = self.db_manager.get_pending_content()
            
            for content in pending_content:
                self.social_manager.post_to_all_platforms(content, content['property_data'])
                self.db_manager.mark_content_as_posted(content['id'])
                
            logger.info("스케줄된 포스팅 완료")
            
        except Exception as e:
            logger.error(f"스케줄된 포스팅 중 오류 발생: {str(e)}")
            
    def start_scheduler(self):
        """스케줄러 시작"""
        logger.info("마케팅 스케줄러 시작")
        self.scheduler.start()
        
    def stop_scheduler(self):
        """스케줄러 중지"""
        logger.info("마케줄러 중지")
        self.scheduler.stop()

def main():
    """메인 함수"""
    bot = AirbnbMarketingBot()
    
    try:
        # 스케줄러 시작
        bot.start_scheduler()
        
        # 즉시 일일 마케팅 실행
        bot.run_daily_marketing()
        
        # 스케줄러가 실행되는 동안 대기
        import time
        while True:
            time.sleep(60)  # 1분마다 체크
            
    except KeyboardInterrupt:
        logger.info("프로그램 종료 요청")
        bot.stop_scheduler()
    except Exception as e:
        logger.error(f"프로그램 실행 중 오류: {str(e)}")
    finally:
        logger.info("프로그램 종료")

if __name__ == "__main__":
    main()
