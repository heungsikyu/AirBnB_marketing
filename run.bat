@echo off
echo 🏠 Airbnb 마케팅 자동화 프로그램 시작...
echo ================================================

REM 가상환경 활성화
if exist "venv\Scripts\activate.bat" (
    echo 🐍 가상환경 활성화 중...
    call venv\Scripts\activate.bat
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
