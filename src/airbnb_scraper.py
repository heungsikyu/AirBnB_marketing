"""
Airbnb 숙소 데이터 수집 모듈
한국 내 Airbnb 숙소 정보를 수집하고 처리
"""

import requests
import json
import logging
from typing import List, Dict, Optional
from datetime import datetime
import time
import random

logger = logging.getLogger(__name__)

class AirbnbScraper:
    """Airbnb 숙소 데이터 수집 클래스"""
    
    def __init__(self):
        """초기화"""
        self.base_url = "https://www.airbnb.com/api/v2"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json',
            'Accept-Language': 'ko-KR,ko;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        
        # 한국 주요 도시 좌표
        self.korean_cities = {
            '서울': {'lat': 37.5665, 'lng': 126.9780},
            '부산': {'lat': 35.1796, 'lng': 129.0756},
            '인천': {'lat': 37.4563, 'lng': 126.7052},
            '대구': {'lat': 35.8714, 'lng': 128.6014},
            '대전': {'lat': 36.3504, 'lng': 127.3845},
            '광주': {'lat': 35.1595, 'lng': 126.8526},
            '울산': {'lat': 35.5384, 'lng': 129.3114},
            '세종': {'lat': 36.4800, 'lng': 127.2890},
            '제주': {'lat': 33.4996, 'lng': 126.5312},
            '수원': {'lat': 37.2636, 'lng': 127.0286},
            '고양': {'lat': 37.6584, 'lng': 126.8320},
            '용인': {'lat': 37.2411, 'lng': 127.1776},
            '성남': {'lat': 37.4201, 'lng': 127.1267},
            '부천': {'lat': 37.5034, 'lng': 126.7660},
            '화성': {'lat': 37.1995, 'lng': 126.8314},
        }
        
    def get_korean_properties(self, limit: int = 20) -> List[Dict]:
        """한국 내 숙소 데이터 수집"""
        properties = []
        
        try:
            for city_name, coords in self.korean_cities.items():
                logger.info(f"{city_name} 지역 숙소 수집 중...")
                city_properties = self._search_properties_in_city(
                    city_name, coords['lat'], coords['lng'], limit=5
                )
                properties.extend(city_properties)
                
                # API 호출 간격 조절
                time.sleep(random.uniform(1, 3))
                
        except Exception as e:
            logger.error(f"숙소 데이터 수집 중 오류: {str(e)}")
            
        return properties[:limit]
    
    def _search_properties_in_city(self, city_name: str, lat: float, lng: float, limit: int = 5) -> List[Dict]:
        """특정 도시의 숙소 검색"""
        properties = []
        
        try:
            # Airbnb 검색 API 호출 (실제 API 대신 시뮬레이션)
            # 실제 구현에서는 Airbnb의 공식 API나 웹 스크래핑을 사용해야 함
            mock_properties = self._generate_mock_properties(city_name, lat, lng, limit)
            properties.extend(mock_properties)
            
        except Exception as e:
            logger.error(f"{city_name} 숙소 검색 중 오류: {str(e)}")
            
        return properties
    
    def _generate_mock_properties(self, city_name: str, lat: float, lng: float, limit: int) -> List[Dict]:
        """테스트용 모의 숙소 데이터 생성"""
        property_types = [
            "아파트", "단독주택", "콘도", "펜션", "게스트하우스", 
            "호텔", "리조트", "빌라", "타운하우스", "로프트"
        ]
        
        amenities = [
            "무료 WiFi", "주차장", "에어컨", "세탁기", "주방", 
            "TV", "헤어드라이어", "다리미", "전자레인지", "냉장고"
        ]
        
        properties = []
        
        for i in range(limit):
            property_data = {
                'id': f"airbnb_{city_name}_{i+1}",
                'title': f"{city_name} 중심가의 아름다운 {random.choice(property_types)}",
                'description': f"{city_name}의 핫한 관광지 근처에 위치한 편리한 숙소입니다. 모든 편의시설이 갖춰져 있어 편안한 여행을 즐기실 수 있습니다.",
                'city': city_name,
                'latitude': lat + random.uniform(-0.01, 0.01),
                'longitude': lng + random.uniform(-0.01, 0.01),
                'price_per_night': random.randint(50000, 200000),
                'property_type': random.choice(property_types),
                'max_guests': random.randint(2, 8),
                'bedrooms': random.randint(1, 4),
                'bathrooms': random.randint(1, 3),
                'amenities': random.sample(amenities, random.randint(3, 8)),
                'rating': round(random.uniform(4.0, 5.0), 1),
                'review_count': random.randint(10, 200),
                'host_name': f"호스트{random.randint(1, 100)}",
                'host_rating': round(random.uniform(4.5, 5.0), 1),
                'images': [
                    f"https://example.com/image_{i+1}_1.jpg",
                    f"https://example.com/image_{i+1}_2.jpg",
                    f"https://example.com/image_{i+1}_3.jpg"
                ],
                'availability': {
                    'check_in': '15:00',
                    'check_out': '11:00',
                    'min_nights': random.randint(1, 3),
                    'max_nights': random.randint(7, 30)
                },
                'booking_url': f"https://airbnb.com/rooms/{random.randint(100000, 999999)}",
                'created_at': datetime.now().isoformat(),
                'scraped_at': datetime.now().isoformat()
            }
            
            properties.append(property_data)
            
        return properties
    
    def get_property_details(self, property_id: str) -> Optional[Dict]:
        """특정 숙소의 상세 정보 조회"""
        try:
            # 실제 구현에서는 Airbnb API를 통해 상세 정보 조회
            logger.info(f"숙소 상세 정보 조회: {property_id}")
            
            # 모의 데이터 반환
            return {
                'id': property_id,
                'detailed_description': "상세한 숙소 설명이 여기에 들어갑니다.",
                'house_rules': [
                    "체크인: 15:00 이후",
                    "체크아웃: 11:00 이전",
                    "흡연 금지",
                    "반려동물 동반 불가",
                    "파티 금지"
                ],
                'cancellation_policy': "유연한 취소 정책",
                'safety_features': [
                    "화재경보기",
                    "일산화탄소 경보기",
                    "응급처치키트",
                    "보안카메라"
                ]
            }
            
        except Exception as e:
            logger.error(f"숙소 상세 정보 조회 중 오류: {str(e)}")
            return None
    
    def search_properties_by_keywords(self, keywords: List[str], limit: int = 10) -> List[Dict]:
        """키워드로 숙소 검색"""
        try:
            logger.info(f"키워드 검색: {', '.join(keywords)}")
            
            # 모든 한국 도시에서 키워드 검색
            all_properties = self.get_korean_properties(limit * 2)
            
            # 키워드가 포함된 숙소 필터링
            filtered_properties = []
            for prop in all_properties:
                title_desc = f"{prop['title']} {prop['description']}".lower()
                if any(keyword.lower() in title_desc for keyword in keywords):
                    filtered_properties.append(prop)
                    
            return filtered_properties[:limit]
            
        except Exception as e:
            logger.error(f"키워드 검색 중 오류: {str(e)}")
            return []
