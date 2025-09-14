#!/usr/bin/env python3
"""
백엔드 API 서버 실행 스크립트
"""

import os
import sys
import subprocess
import uvicorn

def main():
    """백엔드 서버 실행"""
    print("🚀 Airbnb Marketing Dashboard API 서버 시작...")
    
    # 가상환경 활성화 확인
    if not os.path.exists("venv"):
        print("❌ 가상환경을 찾을 수 없습니다. setup.py를 먼저 실행하세요.")
        sys.exit(1)
    
    # 가상환경의 Python 경로
    if os.name == 'nt':  # Windows
        python_path = os.path.join("venv", "Scripts", "python")
    else:  # Unix/Linux/macOS
        python_path = os.path.join("venv", "bin", "python")
    
    # 필요한 패키지 설치
    print("📦 필요한 패키지 설치 중...")
    subprocess.run([python_path, "-m", "pip", "install", "-r", "requirements.txt"])
    
    # API 서버 실행
    print("🌐 API 서버 실행 중...")
    print("📍 서버 주소: http://localhost:8000")
    print("📍 API 문서: http://localhost:8000/docs")
    print("📍 대시보드: http://localhost:8000")
    print("\n종료하려면 Ctrl+C를 누르세요.")
    
    try:
        # 가상환경의 Python을 사용하여 uvicorn 실행
        subprocess.run([
            python_path, "-m", "uvicorn",
            "backend.main:app",
            "--host", "0.0.0.0",
            "--port", "8000",
            "--reload",
            "--log-level", "info"
        ])
    except KeyboardInterrupt:
        print("\n🛑 서버가 중지되었습니다.")

if __name__ == "__main__":
    main()
