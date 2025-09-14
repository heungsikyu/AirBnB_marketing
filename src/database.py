"""
데이터베이스 관리 모듈
숙소 데이터, 콘텐츠, 게시 이력 등을 저장하고 관리
"""

import sqlite3
import json
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
import os

logger = logging.getLogger(__name__)

class DatabaseManager:
    """데이터베이스 관리 클래스"""
    
    def __init__(self, db_path: str = "airbnb_marketing.db"):
        """초기화"""
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """데이터베이스 초기화"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # 숙소 테이블
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS properties (
                        id TEXT PRIMARY KEY,
                        title TEXT NOT NULL,
                        description TEXT,
                        city TEXT,
                        latitude REAL,
                        longitude REAL,
                        price_per_night INTEGER,
                        property_type TEXT,
                        max_guests INTEGER,
                        bedrooms INTEGER,
                        bathrooms INTEGER,
                        amenities TEXT,  -- JSON string
                        rating REAL,
                        review_count INTEGER,
                        host_name TEXT,
                        host_rating REAL,
                        images TEXT,  -- JSON string
                        availability TEXT,  -- JSON string
                        booking_url TEXT,
                        created_at TIMESTAMP,
                        scraped_at TIMESTAMP,
                        is_active BOOLEAN DEFAULT 1
                    )
                ''')
                
                # 콘텐츠 테이블
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS content (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        property_id TEXT,
                        content_type TEXT,  -- 'instagram', 'youtube', 'blog'
                        content_data TEXT,  -- JSON string
                        created_at TIMESTAMP,
                        is_posted BOOLEAN DEFAULT 0,
                        posted_at TIMESTAMP,
                        FOREIGN KEY (property_id) REFERENCES properties (id)
                    )
                ''')
                
                # 게시 이력 테이블
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS posting_history (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        property_id TEXT,
                        platform TEXT,  -- 'instagram', 'youtube', 'blog'
                        post_id TEXT,
                        post_url TEXT,
                        status TEXT,  -- 'success', 'failed', 'pending'
                        error_message TEXT,
                        posted_at TIMESTAMP,
                        analytics_data TEXT,  -- JSON string
                        FOREIGN KEY (property_id) REFERENCES properties (id)
                    )
                ''')
                
                # 전환 추적 테이블
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS conversions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        property_id TEXT,
                        platform TEXT,
                        tracking_url TEXT,
                        click_count INTEGER DEFAULT 0,
                        conversion_count INTEGER DEFAULT 0,
                        created_at TIMESTAMP,
                        last_updated TIMESTAMP,
                        FOREIGN KEY (property_id) REFERENCES properties (id)
                    )
                ''')
                
                # 스케줄 테이블
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS schedules (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        property_id TEXT,
                        platform TEXT,
                        content_id INTEGER,
                        scheduled_time TIMESTAMP,
                        status TEXT,  -- 'pending', 'completed', 'failed'
                        created_at TIMESTAMP,
                        FOREIGN KEY (property_id) REFERENCES properties (id),
                        FOREIGN KEY (content_id) REFERENCES content (id)
                    )
                ''')
                
                conn.commit()
                logger.info("데이터베이스 초기화 완료")
                
        except Exception as e:
            logger.error(f"데이터베이스 초기화 중 오류: {str(e)}")
    
    def save_property_data(self, property_data: Dict, content_data: Dict = None) -> bool:
        """숙소 데이터 저장"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # 기존 데이터 확인
                cursor.execute('SELECT id FROM properties WHERE id = ?', (property_data['id'],))
                existing = cursor.fetchone()
                
                if existing:
                    # 업데이트
                    cursor.execute('''
                        UPDATE properties SET
                            title = ?, description = ?, city = ?, latitude = ?, longitude = ?,
                            price_per_night = ?, property_type = ?, max_guests = ?, bedrooms = ?,
                            bathrooms = ?, amenities = ?, rating = ?, review_count = ?,
                            host_name = ?, host_rating = ?, images = ?, availability = ?,
                            booking_url = ?, scraped_at = ?, is_active = 1
                        WHERE id = ?
                    ''', (
                        property_data.get('title', ''),
                        property_data.get('description', ''),
                        property_data.get('city', ''),
                        property_data.get('latitude', 0),
                        property_data.get('longitude', 0),
                        property_data.get('price_per_night', 0),
                        property_data.get('property_type', ''),
                        property_data.get('max_guests', 0),
                        property_data.get('bedrooms', 0),
                        property_data.get('bathrooms', 0),
                        json.dumps(property_data.get('amenities', [])),
                        property_data.get('rating', 0),
                        property_data.get('review_count', 0),
                        property_data.get('host_name', ''),
                        property_data.get('host_rating', 0),
                        json.dumps(property_data.get('images', [])),
                        json.dumps(property_data.get('availability', {})),
                        property_data.get('booking_url', ''),
                        property_data.get('scraped_at', datetime.now().isoformat()),
                        property_data['id']
                    ))
                else:
                    # 새로 삽입
                    cursor.execute('''
                        INSERT INTO properties (
                            id, title, description, city, latitude, longitude,
                            price_per_night, property_type, max_guests, bedrooms,
                            bathrooms, amenities, rating, review_count, host_name,
                            host_rating, images, availability, booking_url,
                            created_at, scraped_at
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        property_data['id'],
                        property_data.get('title', ''),
                        property_data.get('description', ''),
                        property_data.get('city', ''),
                        property_data.get('latitude', 0),
                        property_data.get('longitude', 0),
                        property_data.get('price_per_night', 0),
                        property_data.get('property_type', ''),
                        property_data.get('max_guests', 0),
                        property_data.get('bedrooms', 0),
                        property_data.get('bathrooms', 0),
                        json.dumps(property_data.get('amenities', [])),
                        property_data.get('rating', 0),
                        property_data.get('review_count', 0),
                        property_data.get('host_name', ''),
                        property_data.get('host_rating', 0),
                        json.dumps(property_data.get('images', [])),
                        json.dumps(property_data.get('availability', {})),
                        property_data.get('booking_url', ''),
                        property_data.get('created_at', datetime.now().isoformat()),
                        property_data.get('scraped_at', datetime.now().isoformat())
                    ))
                
                # 콘텐츠 데이터 저장
                if content_data:
                    self._save_content_data(property_data['id'], content_data, cursor)
                
                conn.commit()
                logger.info(f"숙소 데이터 저장 완료: {property_data['id']}")
                return True
                
        except Exception as e:
            logger.error(f"숙소 데이터 저장 중 오류: {str(e)}")
            return False
    
    def _save_content_data(self, property_id: str, content_data: Dict, cursor):
        """콘텐츠 데이터 저장"""
        try:
            platforms = content_data.get('platforms', {})
            
            for platform, content in platforms.items():
                cursor.execute('''
                    INSERT INTO content (property_id, content_type, content_data, created_at)
                    VALUES (?, ?, ?, ?)
                ''', (
                    property_id,
                    platform,
                    json.dumps(content),
                    datetime.now().isoformat()
                ))
                
        except Exception as e:
            logger.error(f"콘텐츠 데이터 저장 중 오류: {str(e)}")
    
    def get_property_data(self, property_id: str) -> Optional[Dict]:
        """숙소 데이터 조회"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM properties WHERE id = ?', (property_id,))
                row = cursor.fetchone()
                
                if row:
                    columns = [description[0] for description in cursor.description]
                    property_data = dict(zip(columns, row))
                    
                    # JSON 필드 파싱
                    property_data['amenities'] = json.loads(property_data['amenities'] or '[]')
                    property_data['images'] = json.loads(property_data['images'] or '[]')
                    property_data['availability'] = json.loads(property_data['availability'] or '{}')
                    
                    return property_data
                
                return None
                
        except Exception as e:
            logger.error(f"숙소 데이터 조회 중 오류: {str(e)}")
            return None
    
    def get_all_properties(self, limit: int = 100, offset: int = 0) -> List[Dict]:
        """모든 숙소 데이터 조회"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT * FROM properties 
                    WHERE is_active = 1 
                    ORDER BY scraped_at DESC 
                    LIMIT ? OFFSET ?
                ''', (limit, offset))
                
                rows = cursor.fetchall()
                columns = [description[0] for description in cursor.description]
                
                properties = []
                for row in rows:
                    property_data = dict(zip(columns, row))
                    property_data['amenities'] = json.loads(property_data['amenities'] or '[]')
                    property_data['images'] = json.loads(property_data['images'] or '[]')
                    property_data['availability'] = json.loads(property_data['availability'] or '{}')
                    properties.append(property_data)
                
                return properties
                
        except Exception as e:
            logger.error(f"숙소 데이터 조회 중 오류: {str(e)}")
            return []
    
    def get_pending_content(self, limit: int = 50) -> List[Dict]:
        """미게시된 콘텐츠 조회"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT c.*, p.title, p.city, p.price_per_night, p.rating
                    FROM content c
                    JOIN properties p ON c.property_id = p.id
                    WHERE c.is_posted = 0
                    ORDER BY c.created_at ASC
                    LIMIT ?
                ''', (limit,))
                
                rows = cursor.fetchall()
                columns = [description[0] for description in cursor.description]
                
                content_list = []
                for row in rows:
                    content_data = dict(zip(columns, row))
                    content_data['content_data'] = json.loads(content_data['content_data'] or '{}')
                    content_data['property_data'] = {
                        'id': content_data['property_id'],
                        'title': content_data['title'],
                        'city': content_data['city'],
                        'price_per_night': content_data['price_per_night'],
                        'rating': content_data['rating']
                    }
                    content_list.append(content_data)
                
                return content_list
                
        except Exception as e:
            logger.error(f"미게시 콘텐츠 조회 중 오류: {str(e)}")
            return []
    
    def mark_content_as_posted(self, content_id: int) -> bool:
        """콘텐츠를 게시됨으로 표시"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE content 
                    SET is_posted = 1, posted_at = ?
                    WHERE id = ?
                ''', (datetime.now().isoformat(), content_id))
                
                conn.commit()
                return True
                
        except Exception as e:
            logger.error(f"콘텐츠 상태 업데이트 중 오류: {str(e)}")
            return False
    
    def save_posting_history(self, property_id: str, platform: str, post_data: Dict) -> bool:
        """게시 이력 저장"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO posting_history (
                        property_id, platform, post_id, post_url, status,
                        error_message, posted_at, analytics_data
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    property_id,
                    platform,
                    post_data.get('post_id', ''),
                    post_data.get('url', ''),
                    'success' if post_data.get('success', False) else 'failed',
                    post_data.get('error', ''),
                    datetime.now().isoformat(),
                    json.dumps(post_data.get('analytics', {}))
                ))
                
                conn.commit()
                return True
                
        except Exception as e:
            logger.error(f"게시 이력 저장 중 오류: {str(e)}")
            return False
    
    def get_posting_analytics(self, property_id: str = None, platform: str = None, days: int = 30) -> List[Dict]:
        """게시 분석 데이터 조회"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                query = '''
                    SELECT ph.*, p.title, p.city
                    FROM posting_history ph
                    JOIN properties p ON ph.property_id = p.id
                    WHERE ph.posted_at >= datetime('now', '-{} days')
                '''.format(days)
                
                params = []
                if property_id:
                    query += ' AND ph.property_id = ?'
                    params.append(property_id)
                
                if platform:
                    query += ' AND ph.platform = ?'
                    params.append(platform)
                
                query += ' ORDER BY ph.posted_at DESC'
                
                cursor.execute(query, params)
                rows = cursor.fetchall()
                columns = [description[0] for description in cursor.description]
                
                analytics = []
                for row in rows:
                    data = dict(zip(columns, row))
                    data['analytics_data'] = json.loads(data['analytics_data'] or '{}')
                    analytics.append(data)
                
                return analytics
                
        except Exception as e:
            logger.error(f"분석 데이터 조회 중 오류: {str(e)}")
            return []
    
    def save_conversion_tracking(self, property_id: str, platform: str, tracking_url: str) -> bool:
        """전환 추적 데이터 저장"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # 기존 추적 데이터 확인
                cursor.execute('''
                    SELECT id FROM conversions 
                    WHERE property_id = ? AND platform = ?
                ''', (property_id, platform))
                
                existing = cursor.fetchone()
                
                if existing:
                    # 업데이트
                    cursor.execute('''
                        UPDATE conversions 
                        SET tracking_url = ?, last_updated = ?
                        WHERE property_id = ? AND platform = ?
                    ''', (tracking_url, datetime.now().isoformat(), property_id, platform))
                else:
                    # 새로 삽입
                    cursor.execute('''
                        INSERT INTO conversions (property_id, platform, tracking_url, created_at, last_updated)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (property_id, platform, tracking_url, datetime.now().isoformat(), datetime.now().isoformat()))
                
                conn.commit()
                return True
                
        except Exception as e:
            logger.error(f"전환 추적 데이터 저장 중 오류: {str(e)}")
            return False
    
    def update_conversion_stats(self, property_id: str, platform: str, click_count: int = 0, conversion_count: int = 0) -> bool:
        """전환 통계 업데이트"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE conversions 
                    SET click_count = click_count + ?, 
                        conversion_count = conversion_count + ?,
                        last_updated = ?
                    WHERE property_id = ? AND platform = ?
                ''', (click_count, conversion_count, datetime.now().isoformat(), property_id, platform))
                
                conn.commit()
                return True
                
        except Exception as e:
            logger.error(f"전환 통계 업데이트 중 오류: {str(e)}")
            return False
    
    def get_conversion_stats(self, property_id: str = None) -> List[Dict]:
        """전환 통계 조회"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                query = '''
                    SELECT c.*, p.title, p.city
                    FROM conversions c
                    JOIN properties p ON c.property_id = p.id
                '''
                
                params = []
                if property_id:
                    query += ' WHERE c.property_id = ?'
                    params.append(property_id)
                
                query += ' ORDER BY c.last_updated DESC'
                
                cursor.execute(query, params)
                rows = cursor.fetchall()
                columns = [description[0] for description in cursor.description]
                
                stats = []
                for row in rows:
                    stats.append(dict(zip(columns, row)))
                
                return stats
                
        except Exception as e:
            logger.error(f"전환 통계 조회 중 오류: {str(e)}")
            return []
    
    def cleanup_old_data(self, days: int = 90) -> bool:
        """오래된 데이터 정리"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # 오래된 게시 이력 삭제
                cursor.execute('''
                    DELETE FROM posting_history 
                    WHERE posted_at < datetime('now', '-{} days')
                '''.format(days))
                
                # 비활성 숙소 정리
                cursor.execute('''
                    UPDATE properties 
                    SET is_active = 0 
                    WHERE scraped_at < datetime('now', '-{} days')
                '''.format(days))
                
                conn.commit()
                logger.info(f"{days}일 이전 데이터 정리 완료")
                return True
                
        except Exception as e:
            logger.error(f"데이터 정리 중 오류: {str(e)}")
            return False
