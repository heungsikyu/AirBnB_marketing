"""
콘텐츠 생성 모듈
숙소 정보를 기반으로 소셜미디어용 콘텐츠 생성
"""

import os
import json
import logging
from typing import Dict, List, Optional
from datetime import datetime
import openai
from PIL import Image, ImageDraw, ImageFont
import textwrap
import random

logger = logging.getLogger(__name__)

class ContentGenerator:
    """콘텐츠 생성 클래스"""
    
    def __init__(self):
        """초기화"""
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        if self.openai_api_key:
            openai.api_key = self.openai_api_key
        
        # 한국어 폰트 경로 (시스템에 따라 조정 필요)
        self.font_paths = [
            '/System/Library/Fonts/AppleGothic.ttf',  # macOS
            '/usr/share/fonts/truetype/nanum/NanumGothic.ttf',  # Linux
            'C:/Windows/Fonts/malgun.ttf',  # Windows
        ]
        
        self.font = self._get_available_font()
        
        # 해시태그 템플릿
        self.hashtag_templates = {
            'instagram': [
                "#에어비앤비", "#한국여행", "#숙소추천", "#여행", "#휴가",
                "#관광", "#호텔", "#펜션", "#게스트하우스", "#여행스타그램",
                "#인스타여행", "#여행일기", "#여행사진", "#여행코스", "#여행팁"
            ],
            'youtube': [
                "#에어비앤비", "#한국여행", "#숙소리뷰", "#여행브이로그", "#숙소추천",
                "#여행가이드", "#한국관광", "#여행정보", "#숙소후기", "#여행팁"
            ],
            'blog': [
                "에어비앤비", "한국여행", "숙소추천", "여행정보", "관광지",
                "여행코스", "숙소리뷰", "여행팁", "한국관광", "여행가이드"
            ]
        }
    
    def _get_available_font(self):
        """사용 가능한 한국어 폰트 찾기"""
        for font_path in self.font_paths:
            if os.path.exists(font_path):
                try:
                    return ImageFont.truetype(font_path, 24)
                except:
                    continue
        
        # 기본 폰트 사용
        try:
            return ImageFont.load_default()
        except:
            return None
    
    def create_property_content(self, property_data: Dict) -> Dict:
        """숙소 정보를 기반으로 콘텐츠 생성"""
        try:
            logger.info(f"콘텐츠 생성 시작: {property_data.get('title', 'Unknown')}")
            
            content = {
                'property_id': property_data['id'],
                'created_at': datetime.now().isoformat(),
                'platforms': {}
            }
            
            # 각 플랫폼별 콘텐츠 생성
            content['platforms']['instagram'] = self._create_instagram_content(property_data)
            content['platforms']['youtube'] = self._create_youtube_content(property_data)
            content['platforms']['blog'] = self._create_blog_content(property_data)
            
            # 이미지 생성
            content['images'] = self._create_property_images(property_data)
            
            logger.info("콘텐츠 생성 완료")
            return content
            
        except Exception as e:
            logger.error(f"콘텐츠 생성 중 오류: {str(e)}")
            return {}
    
    def _create_instagram_content(self, property_data: Dict) -> Dict:
        """인스타그램용 콘텐츠 생성"""
        try:
            # AI를 사용한 캡션 생성
            caption = self._generate_ai_caption(property_data, 'instagram')
            
            # 해시태그 추가
            hashtags = self._generate_hashtags(property_data, 'instagram')
            
            return {
                'caption': f"{caption}\n\n{hashtags}",
                'hashtags': hashtags,
                'story_text': self._create_story_text(property_data),
                'reels_script': self._create_reels_script(property_data)
            }
            
        except Exception as e:
            logger.error(f"인스타그램 콘텐츠 생성 중 오류: {str(e)}")
            return {}
    
    def _create_youtube_content(self, property_data: Dict) -> Dict:
        """유튜브용 콘텐츠 생성"""
        try:
            title = self._generate_youtube_title(property_data)
            description = self._generate_youtube_description(property_data)
            tags = self._generate_hashtags(property_data, 'youtube')
            
            return {
                'title': title,
                'description': description,
                'tags': tags,
                'shorts_script': self._create_shorts_script(property_data),
                'thumbnail_text': self._create_thumbnail_text(property_data)
            }
            
        except Exception as e:
            logger.error(f"유튜브 콘텐츠 생성 중 오류: {str(e)}")
            return {}
    
    def _create_blog_content(self, property_data: Dict) -> Dict:
        """블로그용 콘텐츠 생성"""
        try:
            title = self._generate_blog_title(property_data)
            content_text = self._generate_blog_content(property_data)
            tags = self._generate_hashtags(property_data, 'blog')
            
            return {
                'title': title,
                'content': content_text,
                'excerpt': self._create_blog_excerpt(property_data),
                'tags': tags,
                'meta_description': self._create_meta_description(property_data)
            }
            
        except Exception as e:
            logger.error(f"블로그 콘텐츠 생성 중 오류: {str(e)}")
            return {}
    
    def _generate_ai_caption(self, property_data: Dict, platform: str) -> str:
        """AI를 사용한 캡션 생성"""
        if not self.openai_api_key:
            return self._generate_fallback_caption(property_data, platform)
        
        try:
            prompt = f"""
            다음 Airbnb 숙소 정보를 바탕으로 {platform}용 매력적인 한국어 캡션을 작성해주세요:
            
            숙소명: {property_data.get('title', '')}
            도시: {property_data.get('city', '')}
            가격: {property_data.get('price_per_night', 0):,}원/박
            평점: {property_data.get('rating', 0)}/5
            최대 인원: {property_data.get('max_guests', 0)}명
            편의시설: {', '.join(property_data.get('amenities', [])[:5])}
            
            요구사항:
            - 감정적이고 매력적인 문구 사용
            - 여행의 즐거움을 강조
            - 2-3문장으로 구성
            - 이모지 적절히 사용
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"AI 캡션 생성 중 오류: {str(e)}")
            return self._generate_fallback_caption(property_data, platform)
    
    def _generate_fallback_caption(self, property_data: Dict, platform: str) -> str:
        """AI 없이 기본 캡션 생성"""
        templates = [
            f"🏠 {property_data.get('city', '')}의 숨은 보석 같은 숙소를 발견했어요! ✨",
            f"💫 {property_data.get('city', '')} 여행의 완벽한 숙소, {property_data.get('title', '')}",
            f"🌟 {property_data.get('price_per_night', 0):,}원으로 즐기는 {property_data.get('city', '')} 여행!",
            f"🏡 {property_data.get('max_guests', 0)}명이 함께 즐길 수 있는 완벽한 숙소",
            f"⭐ {property_data.get('rating', 0)}점의 높은 평점을 받은 믿을 수 있는 숙소"
        ]
        
        return random.choice(templates)
    
    def _generate_hashtags(self, property_data: Dict, platform: str) -> str:
        """해시태그 생성"""
        base_hashtags = self.hashtag_templates.get(platform, [])
        
        # 숙소 특성에 따른 추가 해시태그
        city = property_data.get('city', '')
        property_type = property_data.get('property_type', '')
        
        additional_hashtags = []
        if city:
            additional_hashtags.append(f"#{city}여행")
        if property_type:
            additional_hashtags.append(f"#{property_type}")
        
        # 가격대별 해시태그
        price = property_data.get('price_per_night', 0)
        if price < 100000:
            additional_hashtags.append("#저렴한숙소")
        elif price > 150000:
            additional_hashtags.append("#럭셔리숙소")
        
        all_hashtags = base_hashtags + additional_hashtags
        selected_hashtags = random.sample(all_hashtags, min(10, len(all_hashtags)))
        
        return " ".join(selected_hashtags)
    
    def _create_story_text(self, property_data: Dict) -> str:
        """인스타그램 스토리용 텍스트"""
        return f"✨ {property_data.get('title', '')}\n📍 {property_data.get('city', '')}\n💰 {property_data.get('price_per_night', 0):,}원/박"
    
    def _create_reels_script(self, property_data: Dict) -> str:
        """릴스용 스크립트"""
        return f"""
        [0-2초] "안녕하세요! {property_data.get('city', '')} 여행 숙소를 소개해드릴게요!"
        [2-4초] "바로 이곳, {property_data.get('title', '')}입니다!"
        [4-6초] "가격은 {property_data.get('price_per_night', 0):,}원이고, 평점은 {property_data.get('rating', 0)}점이에요!"
        [6-8초] "편의시설도 {', '.join(property_data.get('amenities', [])[:3])} 등이 있어요!"
        [8-10초] "예약하시려면 링크를 클릭하세요!"
        """
    
    def _generate_youtube_title(self, property_data: Dict) -> str:
        """유튜브 제목 생성"""
        templates = [
            f"{property_data.get('city', '')} 숨은 보석 숙소 발견! {property_data.get('title', '')} 리뷰",
            f"에어비앤비 {property_data.get('city', '')} 숙소 추천 | {property_data.get('title', '')}",
            f"{property_data.get('price_per_night', 0):,}원으로 즐기는 {property_data.get('city', '')} 여행 숙소",
            f"평점 {property_data.get('rating', 0)}점! {property_data.get('city', '')} 최고의 숙소는?",
            f"{property_data.get('city', '')} 여행 필수 숙소 {property_data.get('title', '')} 완전 리뷰"
        ]
        
        return random.choice(templates)
    
    def _generate_youtube_description(self, property_data: Dict) -> str:
        """유튜브 설명 생성"""
        return f"""
        안녕하세요! 오늘은 {property_data.get('city', '')}의 숨은 보석 같은 숙소를 소개해드릴게요!

        📍 숙소명: {property_data.get('title', '')}
        💰 가격: {property_data.get('price_per_night', 0):,}원/박
        ⭐ 평점: {property_data.get('rating', 0)}/5 ({property_data.get('review_count', 0)}개 리뷰)
        👥 최대 인원: {property_data.get('max_guests', 0)}명
        🛏️ 침실: {property_data.get('bedrooms', 0)}개
        🚿 욕실: {property_data.get('bathrooms', 0)}개

        🏠 편의시설:
        {chr(10).join([f"• {amenity}" for amenity in property_data.get('amenities', [])])}

        📖 숙소 설명:
        {property_data.get('description', '')}

        🔗 예약하기: {property_data.get('booking_url', '')}

        #에어비앤비 #한국여행 #숙소추천 #여행브이로그 #숙소리뷰
        """
    
    def _create_shorts_script(self, property_data: Dict) -> str:
        """쇼츠용 스크립트"""
        return f"""
        [0-1초] "이 숙소 어때요?"
        [1-2초] "가격: {property_data.get('price_per_night', 0):,}원"
        [2-3초] "평점: {property_data.get('rating', 0)}점"
        [3-4초] "위치: {property_data.get('city', '')}"
        [4-5초] "예약 링크 클릭!"
        """
    
    def _create_thumbnail_text(self, property_data: Dict) -> str:
        """썸네일용 텍스트"""
        return f"{property_data.get('city', '')}\n{property_data.get('price_per_night', 0):,}원"
    
    def _generate_blog_title(self, property_data: Dict) -> str:
        """블로그 제목 생성"""
        return f"{property_data.get('city', '')} 여행 숙소 추천: {property_data.get('title', '')} 완전 리뷰"
    
    def _generate_blog_content(self, property_data: Dict) -> str:
        """블로그 본문 생성"""
        return f"""
        <h2>{property_data.get('title', '')} - {property_data.get('city', '')} 여행의 완벽한 선택</h2>
        
        <p>안녕하세요! 오늘은 {property_data.get('city', '')}에서 발견한 숨은 보석 같은 숙소를 소개해드리려고 합니다. 
        바로 <strong>{property_data.get('title', '')}</strong>입니다!</p>
        
        <h3>📍 숙소 기본 정보</h3>
        <ul>
            <li><strong>위치:</strong> {property_data.get('city', '')}</li>
            <li><strong>가격:</strong> {property_data.get('price_per_night', 0):,}원/박</li>
            <li><strong>평점:</strong> {property_data.get('rating', 0)}/5 ({property_data.get('review_count', 0)}개 리뷰)</li>
            <li><strong>최대 인원:</strong> {property_data.get('max_guests', 0)}명</li>
            <li><strong>침실:</strong> {property_data.get('bedrooms', 0)}개</li>
            <li><strong>욕실:</strong> {property_data.get('bathrooms', 0)}개</li>
            <li><strong>숙소 유형:</strong> {property_data.get('property_type', '')}</li>
        </ul>
        
        <h3>🏠 편의시설</h3>
        <p>이 숙소는 다음과 같은 편의시설을 제공합니다:</p>
        <ul>
            {''.join([f'<li>{amenity}</li>' for amenity in property_data.get('amenities', [])])}
        </ul>
        
        <h3>⭐ 리뷰 및 평점</h3>
        <p>이 숙소는 {property_data.get('rating', 0)}점의 높은 평점을 받았으며, 
        총 {property_data.get('review_count', 0)}개의 리뷰가 있습니다. 
        게스트들은 특히 깨끗함과 위치의 편리함을 높이 평가했습니다.</p>
        
        <h3>💰 가격 및 가치</h3>
        <p>{property_data.get('price_per_night', 0):,}원/박의 가격으로 {property_data.get('city', '')}에서 
        이만한 편의시설과 위치를 제공하는 숙소는 정말 찾기 어렵습니다. 
        특히 {property_data.get('max_guests', 0)}명까지 수용 가능한 넓은 공간을 고려하면 
        가족이나 친구들과 함께 여행하기에 최적의 선택이라고 할 수 있습니다.</p>
        
        <h3>📍 위치 및 접근성</h3>
        <p>{property_data.get('city', '')}의 중심가에 위치한 이 숙소는 
        주요 관광지와의 접근성이 뛰어납니다. 
        대중교통을 이용한 이동도 편리하며, 
        주변에 편의시설과 맛집들이 많아 여행하기에 최적의 환경을 제공합니다.</p>
        
        <h3>🎯 총평</h3>
        <p><strong>{property_data.get('title', '')}</strong>는 {property_data.get('city', '')} 여행을 계획하고 계신다면 
        강력히 추천드리는 숙소입니다. 합리적인 가격, 우수한 편의시설, 
        그리고 편리한 위치까지 모든 조건을 만족하는 숙소라고 할 수 있습니다.</p>
        
        <p>예약을 원하신다면 아래 링크를 클릭해주세요!</p>
        <p><a href="{property_data.get('booking_url', '')}" target="_blank">예약하기</a></p>
        
        <p>더 많은 여행 정보와 숙소 추천이 필요하시다면 
        저희 블로그를 계속 방문해주세요! 😊</p>
        """
    
    def _create_blog_excerpt(self, property_data: Dict) -> str:
        """블로그 요약 생성"""
        return f"{property_data.get('city', '')} 여행의 완벽한 선택! {property_data.get('title', '')}의 상세 리뷰와 예약 정보를 확인해보세요."
    
    def _create_meta_description(self, property_data: Dict) -> str:
        """메타 설명 생성"""
        return f"{property_data.get('city', '')} 여행 숙소 추천: {property_data.get('title', '')} - {property_data.get('price_per_night', 0):,}원/박, 평점 {property_data.get('rating', 0)}점"
    
    def _create_property_images(self, property_data: Dict) -> List[Dict]:
        """숙소 이미지 생성"""
        try:
            images = []
            
            # 메인 이미지 생성
            main_image = self._create_main_image(property_data)
            if main_image:
                images.append({
                    'type': 'main',
                    'path': main_image,
                    'platforms': ['instagram', 'youtube', 'blog']
                })
            
            # 스토리용 이미지 생성
            story_image = self._create_story_image(property_data)
            if story_image:
                images.append({
                    'type': 'story',
                    'path': story_image,
                    'platforms': ['instagram']
                })
            
            # 썸네일 이미지 생성
            thumbnail_image = self._create_thumbnail_image(property_data)
            if thumbnail_image:
                images.append({
                    'type': 'thumbnail',
                    'path': thumbnail_image,
                    'platforms': ['youtube']
                })
            
            return images
            
        except Exception as e:
            logger.error(f"이미지 생성 중 오류: {str(e)}")
            return []
    
    def _create_main_image(self, property_data: Dict) -> Optional[str]:
        """메인 이미지 생성"""
        try:
            # 1080x1080 인스타그램 포스트 크기
            width, height = 1080, 1080
            image = Image.new('RGB', (width, height), color='white')
            draw = ImageDraw.Draw(image)
            
            if self.font:
                # 제목
                title = property_data.get('title', '')[:30] + '...' if len(property_data.get('title', '')) > 30 else property_data.get('title', '')
                draw.text((50, 100), title, fill='black', font=self.font)
                
                # 가격
                price_text = f"{property_data.get('price_per_night', 0):,}원/박"
                draw.text((50, 150), price_text, fill='red', font=self.font)
                
                # 위치
                location_text = f"📍 {property_data.get('city', '')}"
                draw.text((50, 200), location_text, fill='blue', font=self.font)
                
                # 평점
                rating_text = f"⭐ {property_data.get('rating', 0)}/5"
                draw.text((50, 250), rating_text, fill='orange', font=self.font)
            
            # 이미지 저장
            image_path = f"generated_images/{property_data['id']}_main.jpg"
            os.makedirs(os.path.dirname(image_path), exist_ok=True)
            image.save(image_path)
            
            return image_path
            
        except Exception as e:
            logger.error(f"메인 이미지 생성 중 오류: {str(e)}")
            return None
    
    def _create_story_image(self, property_data: Dict) -> Optional[str]:
        """스토리용 이미지 생성"""
        try:
            # 1080x1920 인스타그램 스토리 크기
            width, height = 1080, 1920
            image = Image.new('RGB', (width, height), color='lightblue')
            draw = ImageDraw.Draw(image)
            
            if self.font:
                # 제목
                title = property_data.get('title', '')[:20] + '...' if len(property_data.get('title', '')) > 20 else property_data.get('title', '')
                draw.text((50, 200), title, fill='white', font=self.font)
                
                # 가격
                price_text = f"{property_data.get('price_per_night', 0):,}원"
                draw.text((50, 300), price_text, fill='yellow', font=self.font)
            
            # 이미지 저장
            image_path = f"generated_images/{property_data['id']}_story.jpg"
            os.makedirs(os.path.dirname(image_path), exist_ok=True)
            image.save(image_path)
            
            return image_path
            
        except Exception as e:
            logger.error(f"스토리 이미지 생성 중 오류: {str(e)}")
            return None
    
    def _create_thumbnail_image(self, property_data: Dict) -> Optional[str]:
        """썸네일 이미지 생성"""
        try:
            # 1280x720 유튜브 썸네일 크기
            width, height = 1280, 720
            image = Image.new('RGB', (width, height), color='darkblue')
            draw = ImageDraw.Draw(image)
            
            if self.font:
                # 제목
                title = property_data.get('title', '')[:25] + '...' if len(property_data.get('title', '')) > 25 else property_data.get('title', '')
                draw.text((100, 200), title, fill='white', font=self.font)
                
                # 가격
                price_text = f"{property_data.get('price_per_night', 0):,}원/박"
                draw.text((100, 300), price_text, fill='red', font=self.font)
            
            # 이미지 저장
            image_path = f"generated_images/{property_data['id']}_thumbnail.jpg"
            os.makedirs(os.path.dirname(image_path), exist_ok=True)
            image.save(image_path)
            
            return image_path
            
        except Exception as e:
            logger.error(f"썸네일 이미지 생성 중 오류: {str(e)}")
            return None
