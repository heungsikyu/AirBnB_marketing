"""
스케줄링 모듈
자동화된 마케팅 작업을 스케줄링하고 실행
"""

import schedule
import time
import logging
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import os

logger = logging.getLogger(__name__)

class MarketingScheduler:
    """마케팅 스케줄러 클래스"""
    
    def __init__(self):
        """초기화"""
        self.is_running = False
        self.scheduler_thread = None
        self.posting_schedule = self._parse_posting_schedule()
        
    def _parse_posting_schedule(self) -> List[str]:
        """포스팅 스케줄 파싱"""
        schedule_str = os.getenv('POSTING_SCHEDULE', '09:00,15:00,21:00')
        return [time.strip() for time in schedule_str.split(',')]
    
    def start(self):
        """스케줄러 시작"""
        if self.is_running:
            logger.warning("스케줄러가 이미 실행 중입니다")
            return
        
        try:
            # 일일 마케팅 작업 스케줄링
            self._schedule_daily_tasks()
            
            # 포스팅 스케줄링
            self._schedule_posting_tasks()
            
            # 데이터 정리 작업 스케줄링
            self._schedule_cleanup_tasks()
            
            # 스케줄러 실행
            self.is_running = True
            self.scheduler_thread = threading.Thread(target=self._run_scheduler, daemon=True)
            self.scheduler_thread.start()
            
            logger.info("마케팅 스케줄러 시작됨")
            
        except Exception as e:
            logger.error(f"스케줄러 시작 중 오류: {str(e)}")
    
    def stop(self):
        """스케줄러 중지"""
        self.is_running = False
        if self.scheduler_thread:
            self.scheduler_thread.join(timeout=5)
        logger.info("마케팅 스케줄러 중지됨")
    
    def _run_scheduler(self):
        """스케줄러 실행 루프"""
        while self.is_running:
            try:
                schedule.run_pending()
                time.sleep(60)  # 1분마다 체크
            except Exception as e:
                logger.error(f"스케줄러 실행 중 오류: {str(e)}")
                time.sleep(60)
    
    def _schedule_daily_tasks(self):
        """일일 작업 스케줄링"""
        # 매일 오전 6시에 새로운 숙소 데이터 수집
        schedule.every().day.at("06:00").do(self._run_daily_data_collection)
        
        # 매일 오전 7시에 콘텐츠 생성
        schedule.every().day.at("07:00").do(self._run_content_generation)
        
        # 매일 오전 8시에 분석 리포트 생성
        schedule.every().day.at("08:00").do(self._run_analytics_report)
        
        logger.info("일일 작업 스케줄링 완료")
    
    def _schedule_posting_tasks(self):
        """포스팅 작업 스케줄링"""
        for schedule_time in self.posting_schedule:
            schedule.every().day.at(schedule_time).do(self._run_scheduled_posting)
            logger.info(f"포스팅 스케줄 추가: {schedule_time}")
    
    def _schedule_cleanup_tasks(self):
        """정리 작업 스케줄링"""
        # 매주 일요일 오전 2시에 오래된 데이터 정리
        schedule.every().sunday.at("02:00").do(self._run_data_cleanup)
        
        # 매월 1일 오전 3시에 월간 리포트 생성
        schedule.every().month.do(self._run_monthly_report)
        
        logger.info("정리 작업 스케줄링 완료")
    
    def _run_daily_data_collection(self):
        """일일 데이터 수집 실행"""
        try:
            logger.info("일일 데이터 수집 시작")
            
            # 실제 구현에서는 main.py의 AirbnbMarketingBot 인스턴스를 사용
            # 여기서는 시뮬레이션
            from .airbnb_scraper import AirbnbScraper
            from .database import DatabaseManager
            
            scraper = AirbnbScraper()
            db_manager = DatabaseManager()
            
            # 새로운 숙소 데이터 수집
            properties = scraper.get_korean_properties(limit=50)
            
            for property_data in properties:
                db_manager.save_property_data(property_data)
            
            logger.info(f"일일 데이터 수집 완료: {len(properties)}개 숙소")
            
        except Exception as e:
            logger.error(f"일일 데이터 수집 중 오류: {str(e)}")
    
    def _run_content_generation(self):
        """콘텐츠 생성 실행"""
        try:
            logger.info("콘텐츠 생성 시작")
            
            from .content_generator import ContentGenerator
            from .database import DatabaseManager
            
            content_generator = ContentGenerator()
            db_manager = DatabaseManager()
            
            # 미처리된 숙소 데이터 조회
            properties = db_manager.get_all_properties(limit=20)
            
            for property_data in properties:
                # 콘텐츠 생성
                content = content_generator.create_property_content(property_data)
                
                # 데이터베이스에 저장
                db_manager.save_property_data(property_data, content)
            
            logger.info(f"콘텐츠 생성 완료: {len(properties)}개 숙소")
            
        except Exception as e:
            logger.error(f"콘텐츠 생성 중 오류: {str(e)}")
    
    def _run_scheduled_posting(self):
        """스케줄된 포스팅 실행"""
        try:
            logger.info("스케줄된 포스팅 시작")
            
            from .social_media_manager import SocialMediaManager
            from .database import DatabaseManager
            
            social_manager = SocialMediaManager()
            db_manager = DatabaseManager()
            
            # 미게시된 콘텐츠 조회
            pending_content = db_manager.get_pending_content(limit=10)
            
            for content in pending_content:
                try:
                    # 소셜미디어에 게시
                    result = social_manager.post_to_all_platforms(
                        content['content_data'], 
                        content['property_data']
                    )
                    
                    # 게시 이력 저장
                    for platform, platform_result in result.get('platforms', {}).items():
                        db_manager.save_posting_history(
                            content['property_id'], 
                            platform, 
                            platform_result
                        )
                    
                    # 콘텐츠를 게시됨으로 표시
                    db_manager.mark_content_as_posted(content['id'])
                    
                except Exception as e:
                    logger.error(f"포스팅 중 오류 ({content['property_id']}): {str(e)}")
            
            logger.info(f"스케줄된 포스팅 완료: {len(pending_content)}개 콘텐츠")
            
        except Exception as e:
            logger.error(f"스케줄된 포스팅 중 오류: {str(e)}")
    
    def _run_analytics_report(self):
        """분석 리포트 생성 실행"""
        try:
            logger.info("분석 리포트 생성 시작")
            
            from .database import DatabaseManager
            
            db_manager = DatabaseManager()
            
            # 최근 7일간의 분석 데이터 조회
            analytics = db_manager.get_posting_analytics(days=7)
            
            # 리포트 생성
            report = self._generate_analytics_report(analytics)
            
            # 리포트 저장
            self._save_analytics_report(report)
            
            logger.info("분석 리포트 생성 완료")
            
        except Exception as e:
            logger.error(f"분석 리포트 생성 중 오류: {str(e)}")
    
    def _run_data_cleanup(self):
        """데이터 정리 실행"""
        try:
            logger.info("데이터 정리 시작")
            
            from .database import DatabaseManager
            
            db_manager = DatabaseManager()
            
            # 90일 이전 데이터 정리
            db_manager.cleanup_old_data(days=90)
            
            logger.info("데이터 정리 완료")
            
        except Exception as e:
            logger.error(f"데이터 정리 중 오류: {str(e)}")
    
    def _run_monthly_report(self):
        """월간 리포트 생성 실행"""
        try:
            logger.info("월간 리포트 생성 시작")
            
            from .database import DatabaseManager
            
            db_manager = DatabaseManager()
            
            # 최근 30일간의 분석 데이터 조회
            analytics = db_manager.get_posting_analytics(days=30)
            conversions = db_manager.get_conversion_stats()
            
            # 월간 리포트 생성
            report = self._generate_monthly_report(analytics, conversions)
            
            # 리포트 저장
            self._save_monthly_report(report)
            
            logger.info("월간 리포트 생성 완료")
            
        except Exception as e:
            logger.error(f"월간 리포트 생성 중 오류: {str(e)}")
    
    def _generate_analytics_report(self, analytics: List[Dict]) -> Dict:
        """분석 리포트 생성"""
        try:
            total_posts = len(analytics)
            successful_posts = len([a for a in analytics if a['status'] == 'success'])
            failed_posts = total_posts - successful_posts
            
            # 플랫폼별 통계
            platform_stats = {}
            for analytics_data in analytics:
                platform = analytics_data['platform']
                if platform not in platform_stats:
                    platform_stats[platform] = {'total': 0, 'success': 0, 'failed': 0}
                
                platform_stats[platform]['total'] += 1
                if analytics_data['status'] == 'success':
                    platform_stats[platform]['success'] += 1
                else:
                    platform_stats[platform]['failed'] += 1
            
            report = {
                'generated_at': datetime.now().isoformat(),
                'period': '7일',
                'summary': {
                    'total_posts': total_posts,
                    'successful_posts': successful_posts,
                    'failed_posts': failed_posts,
                    'success_rate': (successful_posts / total_posts * 100) if total_posts > 0 else 0
                },
                'platform_stats': platform_stats,
                'top_properties': self._get_top_properties(analytics, limit=5)
            }
            
            return report
            
        except Exception as e:
            logger.error(f"분석 리포트 생성 중 오류: {str(e)}")
            return {}
    
    def _generate_monthly_report(self, analytics: List[Dict], conversions: List[Dict]) -> Dict:
        """월간 리포트 생성"""
        try:
            # 기본 통계
            total_posts = len(analytics)
            total_clicks = sum(c['click_count'] for c in conversions)
            total_conversions = sum(c['conversion_count'] for c in conversions)
            
            # 플랫폼별 성과
            platform_performance = {}
            for analytics_data in analytics:
                platform = analytics_data['platform']
                if platform not in platform_performance:
                    platform_performance[platform] = {
                        'posts': 0, 'clicks': 0, 'conversions': 0
                    }
                
                platform_performance[platform]['posts'] += 1
            
            for conversion in conversions:
                platform = conversion['platform']
                if platform in platform_performance:
                    platform_performance[platform]['clicks'] += conversion['click_count']
                    platform_performance[platform]['conversions'] += conversion['conversion_count']
            
            report = {
                'generated_at': datetime.now().isoformat(),
                'period': '30일',
                'summary': {
                    'total_posts': total_posts,
                    'total_clicks': total_clicks,
                    'total_conversions': total_conversions,
                    'conversion_rate': (total_conversions / total_clicks * 100) if total_clicks > 0 else 0
                },
                'platform_performance': platform_performance,
                'recommendations': self._generate_recommendations(platform_performance)
            }
            
            return report
            
        except Exception as e:
            logger.error(f"월간 리포트 생성 중 오류: {str(e)}")
            return {}
    
    def _get_top_properties(self, analytics: List[Dict], limit: int = 5) -> List[Dict]:
        """상위 성과 숙소 조회"""
        try:
            property_stats = {}
            
            for analytics_data in analytics:
                property_id = analytics_data['property_id']
                if property_id not in property_stats:
                    property_stats[property_id] = {
                        'property_id': property_id,
                        'title': analytics_data.get('title', ''),
                        'city': analytics_data.get('city', ''),
                        'posts': 0,
                        'successful_posts': 0
                    }
                
                property_stats[property_id]['posts'] += 1
                if analytics_data['status'] == 'success':
                    property_stats[property_id]['successful_posts'] += 1
            
            # 성공률 기준으로 정렬
            sorted_properties = sorted(
                property_stats.values(),
                key=lambda x: x['successful_posts'] / x['posts'] if x['posts'] > 0 else 0,
                reverse=True
            )
            
            return sorted_properties[:limit]
            
        except Exception as e:
            logger.error(f"상위 성과 숙소 조회 중 오류: {str(e)}")
            return []
    
    def _generate_recommendations(self, platform_performance: Dict) -> List[str]:
        """추천사항 생성"""
        recommendations = []
        
        try:
            # 플랫폼별 성과 분석
            for platform, stats in platform_performance.items():
                if stats['posts'] > 0:
                    conversion_rate = stats['conversions'] / stats['clicks'] * 100 if stats['clicks'] > 0 else 0
                    
                    if conversion_rate < 5:
                        recommendations.append(f"{platform}: 전환율이 낮습니다. 콘텐츠 품질을 개선해보세요.")
                    elif conversion_rate > 15:
                        recommendations.append(f"{platform}: 전환율이 우수합니다. 더 많은 콘텐츠를 게시해보세요.")
            
            # 일반적인 추천사항
            if not recommendations:
                recommendations.append("모든 플랫폼에서 균형잡힌 성과를 보이고 있습니다.")
                recommendations.append("다양한 콘텐츠 유형을 시도해보세요.")
                recommendations.append("해시태그 전략을 최적화해보세요.")
            
        except Exception as e:
            logger.error(f"추천사항 생성 중 오류: {str(e)}")
            recommendations.append("데이터 분석 중 오류가 발생했습니다.")
        
        return recommendations
    
    def _save_analytics_report(self, report: Dict):
        """분석 리포트 저장"""
        try:
            os.makedirs('reports', exist_ok=True)
            
            filename = f"reports/analytics_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            with open(filename, 'w', encoding='utf-8') as f:
                import json
                json.dump(report, f, ensure_ascii=False, indent=2)
            
            logger.info(f"분석 리포트 저장: {filename}")
            
        except Exception as e:
            logger.error(f"분석 리포트 저장 중 오류: {str(e)}")
    
    def _save_monthly_report(self, report: Dict):
        """월간 리포트 저장"""
        try:
            os.makedirs('reports', exist_ok=True)
            
            filename = f"reports/monthly_report_{datetime.now().strftime('%Y%m')}.json"
            
            with open(filename, 'w', encoding='utf-8') as f:
                import json
                json.dump(report, f, ensure_ascii=False, indent=2)
            
            logger.info(f"월간 리포트 저장: {filename}")
            
        except Exception as e:
            logger.error(f"월간 리포트 저장 중 오류: {str(e)}")
    
    def add_custom_schedule(self, job_func, schedule_time: str, job_name: str = None):
        """커스텀 스케줄 추가"""
        try:
            schedule.every().day.at(schedule_time).do(job_func).tag(job_name or f"custom_{int(time.time())}")
            logger.info(f"커스텀 스케줄 추가: {schedule_time} - {job_name}")
            
        except Exception as e:
            logger.error(f"커스텀 스케줄 추가 중 오류: {str(e)}")
    
    def remove_schedule(self, job_name: str):
        """스케줄 제거"""
        try:
            schedule.clear(job_name)
            logger.info(f"스케줄 제거: {job_name}")
            
        except Exception as e:
            logger.error(f"스케줄 제거 중 오류: {str(e)}")
    
    def get_scheduled_jobs(self) -> List[Dict]:
        """예약된 작업 목록 조회"""
        try:
            jobs = []
            for job in schedule.jobs:
                jobs.append({
                    'job': str(job.job_func),
                    'next_run': job.next_run.isoformat() if job.next_run else None,
                    'interval': job.interval,
                    'unit': job.unit,
                    'tags': job.tags
                })
            
            return jobs
            
        except Exception as e:
            logger.error(f"예약된 작업 조회 중 오류: {str(e)}")
            return []
