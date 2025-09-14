#!/usr/bin/env python3
"""
가상환경 설정 및 관리 스크립트
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_virtual_environment():
    """가상환경 존재 여부 확인"""
    venv_path = Path("venv")
    return venv_path.exists()

def create_virtual_environment():
    """가상환경 생성"""
    print("🐍 가상환경을 생성하는 중...")
    
    if check_virtual_environment():
        print("⚠️ 가상환경이 이미 존재합니다.")
        response = input("기존 가상환경을 삭제하고 새로 생성하시겠습니까? (y/N): ")
        if response.lower() == 'y':
            shutil.rmtree("venv")
            print("✅ 기존 가상환경 삭제 완료")
        else:
            print("기존 가상환경을 사용합니다.")
            return get_venv_paths()
    
    try:
        # 가상환경 생성
        subprocess.check_call([sys.executable, "-m", "venv", "venv"])
        print("✅ 가상환경 생성 완료")
        
        # pip 업그레이드
        pip_path, python_path = get_venv_paths()
        subprocess.check_call([pip_path, "install", "--upgrade", "pip"])
        print("✅ pip 업그레이드 완료")
        
        return pip_path, python_path
        
    except subprocess.CalledProcessError as e:
        print(f"❌ 가상환경 생성 실패: {e}")
        sys.exit(1)

def get_venv_paths():
    """가상환경 경로 반환"""
    if os.name == 'nt':  # Windows
        pip_path = os.path.join("venv", "Scripts", "pip")
        python_path = os.path.join("venv", "Scripts", "python")
    else:  # Unix/Linux/macOS
        pip_path = os.path.join("venv", "bin", "pip")
        python_path = os.path.join("venv", "bin", "python")
    
    return pip_path, python_path

def install_packages(pip_path):
    """패키지 설치"""
    print("📦 패키지를 설치하는 중...")
    try:
        subprocess.check_call([pip_path, "install", "-r", "requirements.txt"])
        print("✅ 패키지 설치 완료")
    except subprocess.CalledProcessError as e:
        print(f"❌ 패키지 설치 실패: {e}")
        sys.exit(1)

def activate_instructions():
    """가상환경 활성화 방법 안내"""
    print("\n🐍 가상환경 활성화 방법:")
    if os.name == 'nt':  # Windows
        print("  Windows:")
        print("    venv\\Scripts\\activate")
        print("    # 또는")
        print("    venv\\Scripts\\activate.bat")
    else:  # Unix/Linux/macOS
        print("  Unix/Linux/macOS:")
        print("    source venv/bin/activate")
    
    print("\n  비활성화:")
    print("    deactivate")

def main():
    """메인 함수"""
    print("🏠 Airbnb 마케팅 자동화 프로그램 - 가상환경 설정")
    print("=" * 50)
    
    # 1. 가상환경 생성
    pip_path, python_path = create_virtual_environment()
    
    # 2. 패키지 설치
    install_packages(pip_path)
    
    # 3. 활성화 방법 안내
    activate_instructions()
    
    print("\n🎉 가상환경 설정이 완료되었습니다!")
    print("\n📋 다음 단계:")
    print("1. 가상환경을 활성화하세요.")
    print("2. config.env 파일을 편집하여 API 키를 입력하세요.")
    print("3. run.bat (Windows) 또는 ./run.sh (Unix)를 실행하세요.")

if __name__ == "__main__":
    main()
