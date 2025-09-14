"""
알림 API 라우터
"""

from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from typing import List, Dict, Any
import json
import sys
import os
from datetime import datetime, timedelta

# 프로젝트 루트를 Python 경로에 추가
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from src.database import DatabaseManager

router = APIRouter()

def get_db_manager():
    """데이터베이스 매니저 의존성"""
    return DatabaseManager()

@router.get("/")
async def get_notifications(
    limit: int = 50,
    db: DatabaseManager = Depends(get_db_manager)
) -> Dict[str, Any]:
    """알림 목록 조회"""
    try:
        # 최근 게시 이력에서 알림 생성
        recent_posts = db.get_posting_analytics(days=7)
        
        notifications = []
        
        # 성공한 게시
        for post in recent_posts:
            if post['status'] == 'success':
                notifications.append({
                    "id": f"post_success_{post['id']}",
                    "type": "success",
                    "title": "게시 성공",
                    "message": f"{post['platform']}에 게시가 완료되었습니다.",
                    "timestamp": post['posted_at'],
                    "property_id": post['property_id'],
                    "read": False
                })
            else:
                notifications.append({
                    "id": f"post_error_{post['id']}",
                    "type": "error",
                    "title": "게시 실패",
                    "message": f"{post['platform']} 게시 중 오류가 발생했습니다.",
                    "timestamp": post['posted_at'],
                    "property_id": post['property_id'],
                    "read": False
                })
        
        # 시간순 정렬
        notifications.sort(key=lambda x: x['timestamp'], reverse=True)
        
        return {
            "notifications": notifications[:limit],
            "total": len(notifications),
            "unread": len([n for n in notifications if not n.get('read', False)])
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"알림 조회 중 오류 발생: {str(e)}")

@router.post("/{notification_id}/read")
async def mark_notification_read(
    notification_id: str,
    db: DatabaseManager = Depends(get_db_manager)
) -> Dict[str, Any]:
    """알림 읽음 처리"""
    try:
        # 실제로는 데이터베이스에서 읽음 상태 업데이트
        return {
            "message": "알림이 읽음 처리되었습니다.",
            "notification_id": notification_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"알림 읽음 처리 중 오류 발생: {str(e)}")

@router.post("/mark-all-read")
async def mark_all_notifications_read(
    db: DatabaseManager = Depends(get_db_manager)
) -> Dict[str, Any]:
    """모든 알림 읽음 처리"""
    try:
        # 실제로는 데이터베이스에서 모든 알림을 읽음 처리
        return {
            "message": "모든 알림이 읽음 처리되었습니다."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"모든 알림 읽음 처리 중 오류 발생: {str(e)}")

@router.get("/stats")
async def get_notification_stats(
    db: DatabaseManager = Depends(get_db_manager)
) -> Dict[str, Any]:
    """알림 통계 조회"""
    try:
        # 최근 24시간 통계
        recent_posts = db.get_posting_analytics(days=1)
        
        success_count = len([p for p in recent_posts if p['status'] == 'success'])
        error_count = len([p for p in recent_posts if p['status'] == 'failed'])
        
        # 플랫폼별 통계
        platform_stats = {}
        for post in recent_posts:
            platform = post['platform']
            if platform not in platform_stats:
                platform_stats[platform] = {'success': 0, 'error': 0}
            
            if post['status'] == 'success':
                platform_stats[platform]['success'] += 1
            else:
                platform_stats[platform]['error'] += 1
        
        return {
            "total": len(recent_posts),
            "success": success_count,
            "error": error_count,
            "successRate": (success_count / len(recent_posts) * 100) if recent_posts else 0,
            "platformStats": platform_stats
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"알림 통계 조회 중 오류 발생: {str(e)}")

@router.websocket("/ws")
async def websocket_notifications(websocket: WebSocket):
    """실시간 알림 WebSocket"""
    await websocket.accept()
    try:
        while True:
            # 클라이언트로부터 메시지 수신
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message.get("type") == "subscribe":
                # 구독 요청 처리
                await websocket.send_text(json.dumps({
                    "type": "subscribed",
                    "message": "실시간 알림에 구독되었습니다."
                }))
            elif message.get("type") == "ping":
                # 핑 요청에 퐁 응답
                await websocket.send_text(json.dumps({
                    "type": "pong",
                    "timestamp": datetime.now().isoformat()
                }))
                
    except WebSocketDisconnect:
        print("알림 WebSocket 연결 해제됨")
    except Exception as e:
        print(f"알림 WebSocket 오류: {e}")

# 추가 라우터들
@router.get("/analytics")
async def get_analytics(db: DatabaseManager = Depends(get_db_manager)) -> Dict[str, Any]:
    """분석 데이터 조회"""
    try:
        # 최근 30일 게시 이력
        recent_posts = db.get_posting_analytics(days=30)
        
        # 일별 통계
        daily_stats = {}
        for post in recent_posts:
            date = post['posted_at'][:10]  # YYYY-MM-DD
            if date not in daily_stats:
                daily_stats[date] = {'success': 0, 'error': 0}
            
            if post['status'] == 'success':
                daily_stats[date]['success'] += 1
            else:
                daily_stats[date]['error'] += 1
        
        # 플랫폼별 통계
        platform_stats = {}
        for post in recent_posts:
            platform = post['platform']
            if platform not in platform_stats:
                platform_stats[platform] = {'success': 0, 'error': 0, 'total': 0}
            
            platform_stats[platform]['total'] += 1
            if post['status'] == 'success':
                platform_stats[platform]['success'] += 1
            else:
                platform_stats[platform]['error'] += 1
        
        return {
            "dailyStats": daily_stats,
            "platformStats": platform_stats,
            "totalPosts": len(recent_posts),
            "successRate": (len([p for p in recent_posts if p['status'] == 'success']) / len(recent_posts) * 100) if recent_posts else 0
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"분석 데이터 조회 중 오류 발생: {str(e)}")

@router.get("/settings")
async def get_settings() -> Dict[str, Any]:
    """설정 조회"""
    try:
        return {
            "emailNotifications": True,
            "pushNotifications": True,
            "notificationTypes": {
                "postSuccess": True,
                "postError": True,
                "systemAlert": True,
                "dailyReport": True
            },
            "notificationSchedule": {
                "dailyReport": "09:00",
                "errorAlert": "immediate"
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"설정 조회 중 오류 발생: {str(e)}")

@router.post("/settings")
async def update_settings(settings: Dict[str, Any]) -> Dict[str, Any]:
    """설정 업데이트"""
    try:
        # 실제로는 설정을 데이터베이스에 저장
        return {
            "message": "설정이 업데이트되었습니다.",
            "settings": settings
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"설정 업데이트 중 오류 발생: {str(e)}")
