"""
대시보드 API 라우터
"""

from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any
import sys
import os

# 프로젝트 루트를 Python 경로에 추가
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from src.database import DatabaseManager

router = APIRouter()

def get_db_manager():
    """데이터베이스 매니저 의존성"""
    return DatabaseManager()

@router.get("/stats")
async def get_dashboard_stats(db: DatabaseManager = Depends(get_db_manager)) -> Dict[str, Any]:
    """대시보드 통계 조회"""
    try:
        # 기본 통계
        properties = db.get_all_properties()
        active_properties = [p for p in properties if p.get('is_active', True)]
        
        # 게시 이력 조회
        posting_history = db.get_posting_analytics(days=30)
        successful_posts = len([p for p in posting_history if p['status'] == 'success'])
        failed_posts = len([p for p in posting_history if p['status'] == 'failed'])
        
        # 전환 통계
        conversions = db.get_conversion_stats()
        total_clicks = sum(c['click_count'] for c in conversions)
        total_conversions = sum(c['conversion_count'] for c in conversions)
        
        return {
            "totalProperties": len(properties),
            "activeProperties": len(active_properties),
            "totalPosts": len(posting_history),
            "successfulPosts": successful_posts,
            "failedPosts": failed_posts,
            "totalClicks": total_clicks,
            "totalConversions": total_conversions,
            "conversionRate": (total_conversions / total_clicks * 100) if total_clicks > 0 else 0,
            "errorCount": failed_posts,
            "successRate": (successful_posts / len(posting_history) * 100) if posting_history else 0
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"통계 조회 중 오류 발생: {str(e)}")

@router.get("/system-status")
async def get_system_status() -> Dict[str, Any]:
    """시스템 상태 조회"""
    try:
        # 실제로는 스케줄러 상태를 확인해야 함
        return {
            "isRunning": True,
            "lastExecution": "2024-01-15T14:30:00",
            "nextExecution": "2024-01-15T17:30:00",
            "activeWorkflows": ["data_collection", "content_generation", "social_posting"],
            "errorCount": 0,
            "uptime": "2 days, 5 hours, 30 minutes"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"시스템 상태 조회 중 오류 발생: {str(e)}")

@router.post("/start")
async def start_system():
    """시스템 시작"""
    try:
        # 실제로는 스케줄러를 시작해야 함
        return {"message": "시스템이 시작되었습니다.", "status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"시스템 시작 중 오류 발생: {str(e)}")

@router.post("/stop")
async def stop_system():
    """시스템 중지"""
    try:
        # 실제로는 스케줄러를 중지해야 함
        return {"message": "시스템이 중지되었습니다.", "status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"시스템 중지 중 오류 발생: {str(e)}")

@router.get("/recent-activities")
async def get_recent_activities(db: DatabaseManager = Depends(get_db_manager)) -> Dict[str, Any]:
    """최근 활동 조회"""
    try:
        # 최근 게시 이력
        recent_posts = db.get_posting_analytics(days=7)
        
        # 최근 숙소 추가
        recent_properties = db.get_all_properties(limit=5)
        
        activities = []
        
        # 게시 활동 추가
        for post in recent_posts[:10]:
            activities.append({
                "type": "post",
                "message": f"{post['platform']}에 게시됨",
                "status": post['status'],
                "timestamp": post['posted_at'],
                "property_id": post['property_id']
            })
        
        # 숙소 추가 활동
        for prop in recent_properties[:5]:
            activities.append({
                "type": "property_added",
                "message": f"새 숙소 추가: {prop['title']}",
                "status": "success",
                "timestamp": prop['created_at'],
                "property_id": prop['id']
            })
        
        # 시간순 정렬
        activities.sort(key=lambda x: x['timestamp'], reverse=True)
        
        return {
            "activities": activities[:20],  # 최근 20개만
            "total": len(activities)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"최근 활동 조회 중 오류 발생: {str(e)}")
