#!/usr/bin/env python3
"""
Airbnb Marketing Dashboard 통합 실행 스크립트
"""

import os
import sys
import subprocess
import threading
import time
import signal

def run_backend():
    """백엔드 서버 실행"""
    print("🚀 백엔드 API 서버 시작...")
    try:
        subprocess.run([sys.executable, "run_backend.py"])
    except KeyboardInterrupt:
        print("백엔드 서버 중지됨")

def run_frontend():
    """프론트엔드 서버 실행"""
    print("🎨 프론트엔드 개발 서버 시작...")
    try:
        subprocess.run([sys.executable, "run_frontend.py"])
    except KeyboardInterrupt:
        print("프론트엔드 서버 중지됨")

def main():
    """통합 실행"""
    print("🏠 Airbnb Marketing Dashboard 시작...")
    print("=" * 50)
    
    # 가상환경 확인
    if not os.path.exists("venv"):
        print("❌ 가상환경을 찾을 수 없습니다. setup.py를 먼저 실행하세요.")
        sys.exit(1)
    
    # 백엔드와 프론트엔드를 별도 스레드에서 실행
    backend_thread = threading.Thread(target=run_backend)
    frontend_thread = threading.Thread(target=run_frontend)
    
    try:
        # 백엔드 먼저 시작
        backend_thread.start()
        time.sleep(3)  # 백엔드 시작 대기
        
        # 프론트엔드 시작
        frontend_thread.start()
        
        print("\n✅ 모든 서비스가 시작되었습니다!")
        print("📍 대시보드: http://localhost:3000")
        print("📍 API 서버: http://localhost:8000")
        print("📍 API 문서: http://localhost:8000/docs")
        print("\n종료하려면 Ctrl+C를 누르세요.")
        
        # 메인 스레드 대기
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 서비스 중지 중...")
        sys.exit(0)

if __name__ == "__main__":
    main()
