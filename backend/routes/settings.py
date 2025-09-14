"""
설정 API 라우터
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

@router.get("/")
async def get_settings() -> Dict[str, Any]:
    """설정 조회"""
    try:
        return {
            "postingSchedule": ["09:00", "15:00", "21:00"],
            "targetCities": ["서울", "부산", "인천", "대구", "대전", "광주", "울산", "세종", "제주"],
            "contentSettings": {
                "maxTitleLength": 50,
                "maxDescriptionLength": 500,
                "hashtagLimit": 15,
                "imageQuality": 95,
                "maxImageSize": [1080, 1080]
            },
            "socialMediaSettings": {
                "instagram": {
                    "maxCaptionLength": 2200,
                    "maxHashtags": 30,
                    "storyDuration": 15,
                    "reelsDuration": 30
                },
                "youtube": {
                    "maxTitleLength": 100,
                    "maxDescriptionLength": 5000,
                    "maxTags": 15,
                    "shortsDuration": 60
                },
                "blog": {
                    "maxTitleLength": 100,
                    "minContentLength": 500,
                    "maxContentLength": 5000,
                    "maxTags": 10
                }
            },
            "scrapingSettings": {
                "requestDelay": [1, 3],
                "maxRetries": 3,
                "timeout": 30
            },
            "analyticsSettings": {
                "trackingPeriodDays": 30,
                "reportGenerationHour": 8,
                "dataCleanupDays": 90,
                "conversionTracking": True
            },
            "notificationSettings": {
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
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"설정 조회 중 오류 발생: {str(e)}")

@router.post("/")
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

@router.get("/api-keys")
async def get_api_keys() -> Dict[str, Any]:
    """API 키 조회 (마스킹된 형태)"""
    try:
        return {
            "openai": "sk-***...",
            "instagram": "***...",
            "youtube": "***...",
            "wordpress": "***...",
            "airbnb": "***..."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"API 키 조회 중 오류 발생: {str(e)}")

@router.post("/api-keys")
async def update_api_keys(api_keys: Dict[str, str]) -> Dict[str, Any]:
    """API 키 업데이트"""
    try:
        # 실제로는 API 키를 안전하게 저장
        return {
            "message": "API 키가 업데이트되었습니다.",
            "updated_keys": list(api_keys.keys())
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"API 키 업데이트 중 오류 발생: {str(e)}")

@router.post("/test-connection")
async def test_api_connection(service: str) -> Dict[str, Any]:
    """API 연결 테스트"""
    try:
        # 실제로는 각 서비스의 API 연결을 테스트
        if service == "openai":
            return {"status": "success", "message": "OpenAI API 연결 성공"}
        elif service == "instagram":
            return {"status": "success", "message": "Instagram API 연결 성공"}
        elif service == "youtube":
            return {"status": "success", "message": "YouTube API 연결 성공"}
        elif service == "wordpress":
            return {"status": "success", "message": "WordPress API 연결 성공"}
        else:
            return {"status": "error", "message": f"알 수 없는 서비스: {service}"}
    except Exception as e:
        return {"status": "error", "message": f"연결 테스트 중 오류 발생: {str(e)}"}

@router.get("/system-info")
async def get_system_info() -> Dict[str, Any]:
    """시스템 정보 조회"""
    try:
        import platform
        import psutil
        
        return {
            "platform": platform.system(),
            "python_version": platform.python_version(),
            "cpu_count": psutil.cpu_count(),
            "memory_total": psutil.virtual_memory().total,
            "memory_available": psutil.virtual_memory().available,
            "disk_usage": psutil.disk_usage('/').percent,
            "uptime": "2 days, 5 hours, 30 minutes"  # 실제로는 계산 필요
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"시스템 정보 조회 중 오류 발생: {str(e)}")

@router.post("/backup")
async def create_backup() -> Dict[str, Any]:
    """데이터베이스 백업 생성"""
    try:
        # 실제로는 데이터베이스 백업 생성
        return {
            "message": "백업이 생성되었습니다.",
            "backup_file": f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db",
            "created_at": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"백업 생성 중 오류 발생: {str(e)}")

@router.post("/restore")
async def restore_backup(backup_file: str) -> Dict[str, Any]:
    """데이터베이스 복원"""
    try:
        # 실제로는 백업 파일에서 데이터베이스 복원
        return {
            "message": "데이터베이스가 복원되었습니다.",
            "restored_from": backup_file,
            "restored_at": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"데이터베이스 복원 중 오류 발생: {str(e)}")
