"""
Airbnb Marketing Dashboard API Server
"""

import os
import sys
import asyncio
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import uvicorn

# 프로젝트 루트를 Python 경로에 추가
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.database import DatabaseManager
from src.scheduler import MarketingScheduler
from src.airbnb_scraper import AirbnbScraper
from src.content_generator import ContentGenerator
from src.social_media_manager import SocialMediaManager

# 전역 변수
db_manager = None
scheduler = None
scraper = None
content_generator = None
social_manager = None
connected_clients = []

class ConnectionManager:
    """WebSocket 연결 관리"""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        print(f"클라이언트 연결됨. 총 연결: {len(self.active_connections)}")
    
    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        print(f"클라이언트 연결 해제됨. 총 연결: {len(self.active_connections)}")
    
    async def send_personal_message(self, message: str, websocket: WebSocket):
        try:
            await websocket.send_text(message)
        except:
            self.disconnect(websocket)
    
    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                self.disconnect(connection)

manager = ConnectionManager()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """애플리케이션 시작/종료 시 실행"""
    global db_manager, scheduler, scraper, content_generator, social_manager
    
    # 초기화
    print("🚀 API 서버 초기화 중...")
    db_manager = DatabaseManager()
    scraper = AirbnbScraper()
    content_generator = ContentGenerator()
    social_manager = SocialMediaManager()
    scheduler = MarketingScheduler()
    
    # 스케줄러 시작
    scheduler.start()
    print("✅ 모든 서비스 초기화 완료")
    
    yield
    
    # 정리
    print("🛑 서비스 종료 중...")
    scheduler.stop()
    print("✅ 서비스 종료 완료")

# FastAPI 앱 생성
app = FastAPI(
    title="Airbnb Marketing Dashboard API",
    description="Airbnb 마케팅 자동화 대시보드 API",
    version="1.0.0",
    lifespan=lifespan
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 정적 파일 서빙
frontend_dist_path = os.path.join(os.path.dirname(__file__), "..", "frontend", "dist")
app.mount("/static", StaticFiles(directory=frontend_dist_path), name="static")

# API 라우터들
from backend.routes import dashboard, properties, analytics, settings, notifications

app.include_router(dashboard.router, prefix="/api/dashboard", tags=["dashboard"])
app.include_router(properties.router, prefix="/api/properties", tags=["properties"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["analytics"])
app.include_router(settings.router, prefix="/api/settings", tags=["settings"])
app.include_router(notifications.router, prefix="/api/notifications", tags=["notifications"])

@app.get("/")
async def root():
    """메인 페이지"""
    index_path = os.path.join(os.path.dirname(__file__), "..", "frontend", "dist", "index.html")
    return HTMLResponse(open(index_path).read())

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket 연결"""
    await manager.connect(websocket)
    try:
        while True:
            # 클라이언트로부터 메시지 수신 (필요시)
            data = await websocket.receive_text()
            print(f"클라이언트 메시지: {data}")
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# 실시간 알림 함수들
async def send_system_notification(message: str, type: str = "info"):
    """시스템 알림 전송"""
    notification = {
        "type": "notification",
        "data": {
            "message": message,
            "type": type,
            "timestamp": datetime.now().isoformat()
        }
    }
    await manager.broadcast(json.dumps(notification))

async def send_system_update():
    """시스템 상태 업데이트 전송"""
    try:
        stats = await get_dashboard_stats()
        update = {
            "type": "system_update",
            "data": stats
        }
        await manager.broadcast(json.dumps(update))
    except Exception as e:
        print(f"시스템 업데이트 전송 오류: {e}")

# 대시보드 통계 조회
async def get_dashboard_stats() -> Dict[str, Any]:
    """대시보드 통계 조회"""
    try:
        # 기본 통계
        properties = db_manager.get_all_properties()
        active_properties = [p for p in properties if p.get('is_active', True)]
        
        # 게시 이력 조회
        posting_history = db_manager.get_posting_analytics(days=30)
        successful_posts = len([p for p in posting_history if p['status'] == 'success'])
        failed_posts = len([p for p in posting_history if p['status'] == 'failed'])
        
        # 전환 통계
        conversions = db_manager.get_conversion_stats()
        total_clicks = sum(c['click_count'] for c in conversions)
        total_conversions = sum(c['conversion_count'] for c in conversions)
        
        # 시스템 상태
        is_running = scheduler.is_running if scheduler else False
        last_execution = datetime.now() - timedelta(hours=1)  # 임시
        
        return {
            "totalProperties": len(properties),
            "activeProperties": len(active_properties),
            "totalPosts": len(posting_history),
            "successfulPosts": successful_posts,
            "failedPosts": failed_posts,
            "totalClicks": total_clicks,
            "totalConversions": total_conversions,
            "conversionRate": (total_conversions / total_clicks * 100) if total_clicks > 0 else 0,
            "isRunning": is_running,
            "lastExecution": last_execution.isoformat(),
            "nextExecution": (last_execution + timedelta(hours=6)).isoformat(),
            "errorCount": failed_posts,
            "successRate": (successful_posts / len(posting_history) * 100) if posting_history else 0
        }
    except Exception as e:
        print(f"대시보드 통계 조회 오류: {e}")
        return {
            "totalProperties": 0,
            "activeProperties": 0,
            "totalPosts": 0,
            "successfulPosts": 0,
            "failedPosts": 0,
            "totalClicks": 0,
            "totalConversions": 0,
            "conversionRate": 0,
            "isRunning": False,
            "lastExecution": None,
            "nextExecution": None,
            "errorCount": 0,
            "successRate": 0
        }

# 주기적 업데이트 (실제로는 별도 태스크에서 실행)
async def periodic_update():
    """주기적 시스템 업데이트"""
    while True:
        await asyncio.sleep(30)  # 30초마다 업데이트
        await send_system_update()

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
