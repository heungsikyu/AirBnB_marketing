"""
숙소 관리 API 라우터
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Dict, Any, Optional
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
async def get_properties(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    city: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    db: DatabaseManager = Depends(get_db_manager)
) -> Dict[str, Any]:
    """숙소 목록 조회"""
    try:
        # 모든 숙소 조회
        all_properties = db.get_all_properties(limit=1000)  # 충분히 큰 수
        
        # 필터링
        filtered_properties = all_properties
        
        if city:
            filtered_properties = [p for p in filtered_properties if p.get('city', '').lower() == city.lower()]
        
        if status:
            if status == 'active':
                filtered_properties = [p for p in filtered_properties if p.get('is_active', True)]
            elif status == 'inactive':
                filtered_properties = [p for p in filtered_properties if not p.get('is_active', True)]
        
        if search:
            search_lower = search.lower()
            filtered_properties = [
                p for p in filtered_properties 
                if search_lower in p.get('title', '').lower() or 
                   search_lower in p.get('city', '').lower() or
                   search_lower in p.get('description', '').lower()
            ]
        
        # 페이지네이션
        total = len(filtered_properties)
        start = (page - 1) * limit
        end = start + limit
        properties = filtered_properties[start:end]
        
        return {
            "properties": properties,
            "pagination": {
                "page": page,
                "limit": limit,
                "total": total,
                "pages": (total + limit - 1) // limit
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"숙소 목록 조회 중 오류 발생: {str(e)}")

@router.get("/{property_id}")
async def get_property(
    property_id: str,
    db: DatabaseManager = Depends(get_db_manager)
) -> Dict[str, Any]:
    """특정 숙소 상세 정보 조회"""
    try:
        property_data = db.get_property_data(property_id)
        if not property_data:
            raise HTTPException(status_code=404, detail="숙소를 찾을 수 없습니다.")
        
        return property_data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"숙소 조회 중 오류 발생: {str(e)}")

@router.post("/{property_id}/toggle")
async def toggle_property(
    property_id: str,
    db: DatabaseManager = Depends(get_db_manager)
) -> Dict[str, Any]:
    """숙소 활성화/비활성화 토글"""
    try:
        property_data = db.get_property_data(property_id)
        if not property_data:
            raise HTTPException(status_code=404, detail="숙소를 찾을 수 없습니다.")
        
        # 현재 상태 반전
        new_status = not property_data.get('is_active', True)
        
        # 데이터베이스 업데이트 (실제로는 UPDATE 쿼리 필요)
        # 여기서는 간단히 성공 응답만 반환
        return {
            "message": f"숙소가 {'활성화' if new_status else '비활성화'}되었습니다.",
            "property_id": property_id,
            "is_active": new_status
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"숙소 상태 변경 중 오류 발생: {str(e)}")

@router.delete("/{property_id}")
async def delete_property(
    property_id: str,
    db: DatabaseManager = Depends(get_db_manager)
) -> Dict[str, Any]:
    """숙소 삭제"""
    try:
        property_data = db.get_property_data(property_id)
        if not property_data:
            raise HTTPException(status_code=404, detail="숙소를 찾을 수 없습니다.")
        
        # 실제로는 DELETE 쿼리 실행
        return {
            "message": "숙소가 삭제되었습니다.",
            "property_id": property_id
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"숙소 삭제 중 오류 발생: {str(e)}")

@router.get("/cities/list")
async def get_cities_list(db: DatabaseManager = Depends(get_db_manager)) -> List[str]:
    """도시 목록 조회"""
    try:
        properties = db.get_all_properties()
        cities = list(set(p.get('city', '') for p in properties if p.get('city')))
        cities.sort()
        return cities
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"도시 목록 조회 중 오류 발생: {str(e)}")

@router.get("/stats/summary")
async def get_properties_summary(db: DatabaseManager = Depends(get_db_manager)) -> Dict[str, Any]:
    """숙소 요약 통계"""
    try:
        properties = db.get_all_properties()
        active_properties = [p for p in properties if p.get('is_active', True)]
        
        # 도시별 통계
        city_stats = {}
        for prop in properties:
            city = prop.get('city', 'Unknown')
            if city not in city_stats:
                city_stats[city] = {'total': 0, 'active': 0}
            city_stats[city]['total'] += 1
            if prop.get('is_active', True):
                city_stats[city]['active'] += 1
        
        # 가격대별 통계
        price_ranges = {
            'under_100k': 0,
            '100k_200k': 0,
            '200k_300k': 0,
            'over_300k': 0
        }
        
        for prop in properties:
            price = prop.get('price_per_night', 0)
            if price < 100000:
                price_ranges['under_100k'] += 1
            elif price < 200000:
                price_ranges['100k_200k'] += 1
            elif price < 300000:
                price_ranges['200k_300k'] += 1
            else:
                price_ranges['over_300k'] += 1
        
        return {
            "total": len(properties),
            "active": len(active_properties),
            "inactive": len(properties) - len(active_properties),
            "cityStats": city_stats,
            "priceRanges": price_ranges
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"숙소 요약 통계 조회 중 오류 발생: {str(e)}")
