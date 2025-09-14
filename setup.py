#!/usr/bin/env python3
"""
Airbnb 마케팅 자동화 프로그램 설치 스크립트
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_python_version():
    """Python 버전 확인"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 이상이 필요합니다.")
        print(f"현재 버전: {sys.version}")
        sys.exit(1)
    print(f"✅ Python 버전 확인: {sys.version}")

def create_virtual_environment():
    """가상환경 생성"""
    print("🐍 가상환경을 생성하는 중...")
    try:
        # 가상환경 생성
        subprocess.check_call([sys.executable, "-m", "venv", "venv"])
        print("✅ 가상환경 생성 완료")
        
        # 가상환경 활성화 스크립트 경로 설정
        if os.name == 'nt':  # Windows
            pip_path = os.path.join("venv", "Scripts", "pip")
            python_path = os.path.join("venv", "Scripts", "python")
        else:  # Unix/Linux/macOS
            pip_path = os.path.join("venv", "bin", "pip")
            python_path = os.path.join("venv", "bin", "python")
        
        # pip 업그레이드
        subprocess.check_call([pip_path, "install", "--upgrade", "pip"])
        
        return pip_path, python_path
        
    except subprocess.CalledProcessError as e:
        print(f"❌ 가상환경 생성 실패: {e}")
        sys.exit(1)

def install_requirements(pip_path):
    """필요한 패키지 설치"""
    print("📦 필요한 패키지를 설치하는 중...")
    try:
        subprocess.check_call([pip_path, "install", "-r", "requirements.txt"])
        print("✅ 패키지 설치 완료")
    except subprocess.CalledProcessError as e:
        print(f"❌ 패키지 설치 실패: {e}")
        sys.exit(1)

def create_directories():
    """필요한 디렉토리 생성"""
    print("📁 필요한 디렉토리를 생성하는 중...")
    directories = [
        "generated_images",
        "reports",
        "logs",
        "data"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"  ✅ {directory}/ 디렉토리 생성")
    
    print("✅ 디렉토리 생성 완료")

def create_config_file():
    """설정 파일 생성"""
    print("⚙️ 설정 파일을 생성하는 중...")
    
    config_path = "config.env"
    example_path = "config.env.example"
    
    if not os.path.exists(config_path):
        if os.path.exists(example_path):
            shutil.copy(example_path, config_path)
            print(f"✅ {config_path} 파일 생성 (예제 파일 복사)")
            print(f"📝 {config_path} 파일을 편집하여 실제 API 키를 입력하세요.")
        else:
            print(f"❌ {example_path} 파일을 찾을 수 없습니다.")
    else:
        print(f"✅ {config_path} 파일이 이미 존재합니다.")

def setup_database():
    """데이터베이스 초기화"""
    print("🗄️ 데이터베이스를 초기화하는 중...")
    try:
        from src.database import DatabaseManager
        db_manager = DatabaseManager()
        print("✅ 데이터베이스 초기화 완료")
    except Exception as e:
        print(f"❌ 데이터베이스 초기화 실패: {e}")

def setup_database_with_venv(python_path):
    """가상환경에서 데이터베이스 초기화"""
    print("🗄️ 데이터베이스를 초기화하는 중...")
    try:
        # 가상환경의 Python을 사용하여 데이터베이스 초기화
        subprocess.check_call([python_path, "-c", "from src.database import DatabaseManager; DatabaseManager()"])
        print("✅ 데이터베이스 초기화 완료")
    except subprocess.CalledProcessError as e:
        print(f"❌ 데이터베이스 초기화 실패: {e}")
        # 폴백으로 일반 데이터베이스 초기화 시도
        setup_database()

def create_run_scripts():
    """실행 스크립트 생성"""
    print("🚀 실행 스크립트를 생성하는 중...")
    
    # Windows용 배치 파일 (가상환경 사용)
    windows_script = """@echo off
echo 🏠 Airbnb 마케팅 자동화 프로그램 시작...
echo ================================================

REM 가상환경 활성화
if exist "venv\\Scripts\\activate.bat" (
    echo 🐍 가상환경 활성화 중...
    call venv\\Scripts\\activate.bat
) else (
    echo ❌ 가상환경을 찾을 수 없습니다. setup.py를 먼저 실행하세요.
    pause
    exit /b 1
)

REM 필요한 디렉토리 생성
if not exist "generated_images" mkdir generated_images
if not exist "reports" mkdir reports
if not exist "logs" mkdir logs
if not exist "data" mkdir data

REM 설정 파일 확인
if not exist "config.env" (
    echo ⚠️ config.env 파일이 없습니다. config.env.example을 복사하여 설정하세요.
    if exist "config.env.example" (
        copy config.env.example config.env
        echo ✅ config.env 파일을 생성했습니다. API 키를 설정하세요.
    )
    pause
    exit /b 1
)

REM 메인 프로그램 실행
echo 🚀 프로그램 실행 중...
python main.py

echo 프로그램이 종료되었습니다.
pause
"""
    with open("run.bat", "w", encoding="utf-8") as f:
        f.write(windows_script)
    
    # Unix/Linux/macOS용 셸 스크립트 (가상환경 사용)
    unix_script = """#!/bin/bash
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
"""
    with open("run.sh", "w", encoding="utf-8") as f:
        f.write(unix_script)
    
    # 실행 권한 부여 (Unix 계열)
    if os.name != 'nt':
        os.chmod("run.sh", 0o755)
    
    print("✅ 실행 스크립트 생성 완료")
    print("  - Windows: run.bat")
    print("  - Unix/Linux/macOS: ./run.sh")

def main():
    """메인 설치 함수"""
    print("🏠 Airbnb 마케팅 자동화 프로그램 설치를 시작합니다...\n")
    
    # 1. Python 버전 확인
    check_python_version()
    
    # 2. 가상환경 생성
    pip_path, python_path = create_virtual_environment()
    
    # 3. 패키지 설치 (가상환경 내에서)
    install_requirements(pip_path)
    
    # 4. 디렉토리 생성
    create_directories()
    
    # 5. 설정 파일 생성
    create_config_file()
    
    # 6. 데이터베이스 초기화 (가상환경 내에서)
    setup_database_with_venv(python_path)
    
    # 7. 실행 스크립트 생성
    create_run_scripts()
    
    print("\n🎉 설치가 완료되었습니다!")
    print("\n📋 다음 단계:")
    print("1. config.env 파일을 편집하여 API 키를 입력하세요.")
    print("2. run.bat (Windows) 또는 ./run.sh (Unix)를 실행하세요.")
    print("3. 로그 파일을 확인하여 프로그램이 정상 작동하는지 확인하세요.")
    print("\n📚 자세한 사용법은 README.md 파일을 참조하세요.")
    print("\n🐍 가상환경 사용법:")
    print("  - Windows: venv\\Scripts\\activate")
    print("  - Unix/Linux/macOS: source venv/bin/activate")
    print("  - 비활성화: deactivate")

if __name__ == "__main__":
    main()
