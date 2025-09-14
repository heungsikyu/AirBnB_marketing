#!/usr/bin/env python3
"""
프론트엔드 개발 서버 실행 스크립트
"""

import os
import sys
import subprocess

def main():
    """프론트엔드 개발 서버 실행"""
    print("🎨 Airbnb Marketing Dashboard 프론트엔드 시작...")
    
    # Node.js 설치 확인
    try:
        subprocess.run(["node", "--version"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Node.js가 설치되지 않았습니다. Node.js를 먼저 설치하세요.")
        print("📥 다운로드: https://nodejs.org/")
        sys.exit(1)
    
    # npm 설치 확인
    try:
        subprocess.run(["npm", "--version"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ npm이 설치되지 않았습니다.")
        sys.exit(1)
    
    # 프론트엔드 디렉토리로 이동
    os.chdir("frontend")
    
    # 패키지 설치
    print("📦 프론트엔드 패키지 설치 중...")
    subprocess.run(["npm", "install"])
    
    # 개발 서버 실행
    print("🌐 프론트엔드 개발 서버 실행 중...")
    print("📍 서버 주소: http://localhost:3000")
    print("\n종료하려면 Ctrl+C를 누르세요.")
    
    try:
        subprocess.run(["npm", "run", "dev"])
    except KeyboardInterrupt:
        print("\n🛑 개발 서버가 중지되었습니다.")

if __name__ == "__main__":
    main()
