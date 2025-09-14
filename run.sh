#!/bin/bash
echo "🏠 Airbnb 마케팅 자동화 프로그램 시작..."
echo "================================================"

# 가상환경 활성화
if [ -f "venv/bin/activate" ]; then
    echo "🐍 가상환경 활성화 중..."
    source venv/bin/activate
else
    echo "❌ 가상환경을 찾을 수 없습니다. setup.py를 먼저 실행하세요."
    exit 1
fi

# 필요한 디렉토리 생성
mkdir -p generated_images reports logs data

# 설정 파일 확인
if [ ! -f "config.env" ]; then
    echo "⚠️ config.env 파일이 없습니다. config.env.example을 복사하여 설정하세요."
    if [ -f "config.env.example" ]; then
        cp config.env.example config.env
        echo "✅ config.env 파일을 생성했습니다. API 키를 설정하세요."
    fi
    exit 1
fi

# 메인 프로그램 실행
echo "🚀 프로그램 실행 중..."
python main.py

echo "프로그램이 종료되었습니다."
