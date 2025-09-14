"""
분석 API 라우터
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import sys
import os

# 프로젝트 루트를 Python 경로에 추가
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from src.database import DatabaseManager

router = APIRouter()

def get_db_manager():
    """데이터베이스 매니저 의존성"""
    return DatabaseManager()

@router.get("/overview")
async def get_analytics_overview(
    days: int = Query(30, ge=1, le=365),
    db: DatabaseManager = Depends(get_db_manager)
) -> Dict[str, Any]:
    """분석 개요 조회"""
    try:
        # 게시 이력 조회
        posting_history = db.get_posting_analytics(days=days)
        
        # 전환 통계
        conversions = db.get_conversion_stats()
        
        # 기본 통계
        total_posts = len(posting_history)
        successful_posts = len([p for p in posting_history if p['status'] == 'success'])
        failed_posts = total_posts - successful_posts
        
        total_clicks = sum(c['click_count'] for c in conversions)
        total_conversions = sum(c['conversion_count'] for c in conversions)
        
        # 일별 통계
        daily_stats = {}
        for post in posting_history:
            date = post['posted_at'][:10]
            if date not in daily_stats:
                daily_stats[date] = {'posts': 0, 'success': 0, 'error': 0}
            
            daily_stats[date]['posts'] += 1
            if post['status'] == 'success':
                daily_stats[date]['success'] += 1
            else:
                daily_stats[date]['error'] += 1
        
        # 플랫폼별 통계
        platform_stats = {}
        for post in posting_history:
            platform = post['platform']
            if platform not in platform_stats:
                platform_stats[platform] = {'posts': 0, 'success': 0, 'error': 0}
            
            platform_stats[platform]['posts'] += 1
            if post['status'] == 'success':
                platform_stats[platform]['success'] += 1
            else:
                platform_stats[platform]['error'] += 1
        
        return {
            "period": f"{days}일",
            "totalPosts": total_posts,
            "successfulPosts": successful_posts,
            "failedPosts": failed_posts,
            "successRate": (successful_posts / total_posts * 100) if total_posts > 0 else 0,
            "totalClicks": total_clicks,
            "totalConversions": total_conversions,
            "conversionRate": (total_conversions / total_clicks * 100) if total_clicks > 0 else 0,
            "dailyStats": daily_stats,
            "platformStats": platform_stats
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"분석 개요 조회 중 오류 발생: {str(e)}")

@router.get("/performance")
async def get_performance_analytics(
    days: int = Query(30, ge=1, le=365),
    db: DatabaseManager = Depends(get_db_manager)
) -> Dict[str, Any]:
    """성과 분석 조회"""
    try:
        # 게시 이력 조회
        posting_history = db.get_posting_analytics(days=days)
        
        # 숙소별 성과
        property_performance = {}
        for post in posting_history:
            prop_id = post['property_id']
            if prop_id not in property_performance:
                property_performance[prop_id] = {
                    'property_id': prop_id,
                    'posts': 0,
                    'success': 0,
                    'error': 0,
                    'platforms': set()
                }
            
            property_performance[prop_id]['posts'] += 1
            property_performance[prop_id]['platforms'].add(post['platform'])
            
            if post['status'] == 'success':
                property_performance[prop_id]['success'] += 1
            else:
                property_performance[prop_id]['error'] += 1
        
        # 플랫폼을 리스트로 변환
        for prop_id in property_performance:
            property_performance[prop_id]['platforms'] = list(property_performance[prop_id]['platforms'])
            property_performance[prop_id]['successRate'] = (
                property_performance[prop_id]['success'] / property_performance[prop_id]['posts'] * 100
            ) if property_performance[prop_id]['posts'] > 0 else 0
        
        # 성과순 정렬
        top_performers = sorted(
            property_performance.values(),
            key=lambda x: x['successRate'],
            reverse=True
        )[:10]
        
        return {
            "topPerformers": top_performers,
            "totalProperties": len(property_performance),
            "averageSuccessRate": sum(p['successRate'] for p in property_performance.values()) / len(property_performance) if property_performance else 0
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"성과 분석 조회 중 오류 발생: {str(e)}")

@router.get("/trends")
async def get_trend_analytics(
    days: int = Query(30, ge=7, le=365),
    db: DatabaseManager = Depends(get_db_manager)
) -> Dict[str, Any]:
    """트렌드 분석 조회"""
    try:
        # 게시 이력 조회
        posting_history = db.get_posting_analytics(days=days)
        
        # 주간 통계
        weekly_stats = {}
        for post in posting_history:
            # ISO 주차 계산
            date = datetime.fromisoformat(post['posted_at'].replace('Z', '+00:00'))
            year, week, _ = date.isocalendar()
            week_key = f"{year}-W{week:02d}"
            
            if week_key not in weekly_stats:
                weekly_stats[week_key] = {'posts': 0, 'success': 0, 'error': 0}
            
            weekly_stats[week_key]['posts'] += 1
            if post['status'] == 'success':
                weekly_stats[week_key]['success'] += 1
            else:
                weekly_stats[week_key]['error'] += 1
        
        # 성장률 계산
        weeks = sorted(weekly_stats.keys())
        growth_rates = []
        
        for i in range(1, len(weeks)):
            prev_week = weekly_stats[weeks[i-1]]
            curr_week = weekly_stats[weeks[i]]
            
            if prev_week['posts'] > 0:
                growth_rate = ((curr_week['posts'] - prev_week['posts']) / prev_week['posts']) * 100
                growth_rates.append({
                    'week': weeks[i],
                    'growthRate': growth_rate,
                    'posts': curr_week['posts']
                })
        
        return {
            "weeklyStats": weekly_stats,
            "growthRates": growth_rates,
            "averageGrowthRate": sum(g['growthRate'] for g in growth_rates) / len(growth_rates) if growth_rates else 0
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"트렌드 분석 조회 중 오류 발생: {str(e)}")

@router.get("/export")
async def export_analytics(
    format: str = Query("json", regex="^(json|csv)$"),
    days: int = Query(30, ge=1, le=365),
    db: DatabaseManager = Depends(get_db_manager)
) -> Dict[str, Any]:
    """분석 데이터 내보내기"""
    try:
        # 게시 이력 조회
        posting_history = db.get_posting_analytics(days=days)
        
        if format == "json":
            return {
                "data": posting_history,
                "exported_at": datetime.now().isoformat(),
                "format": "json"
            }
        elif format == "csv":
            # CSV 형식으로 변환
            csv_data = "id,property_id,platform,status,posted_at,error_message\n"
            for post in posting_history:
                csv_data += f"{post['id']},{post['property_id']},{post['platform']},{post['status']},{post['posted_at']},{post.get('error_message', '')}\n"
            
            return {
                "data": csv_data,
                "exported_at": datetime.now().isoformat(),
                "format": "csv"
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"데이터 내보내기 중 오류 발생: {str(e)}")
