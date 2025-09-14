@echo off
echo 🐍 가상환경 활성화 중...

if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
    echo ✅ 가상환경이 활성화되었습니다.
    echo.
    echo 사용 가능한 명령어:
    echo   python main.py          - 메인 프로그램 실행
    echo   python -m src.airbnb_scraper - 데이터 수집 테스트
    echo   python -m src.content_generator - 콘텐츠 생성 테스트
    echo   deactivate              - 가상환경 비활성화
    echo.
    cmd /k
) else (
    echo ❌ 가상환경을 찾을 수 없습니다.
    echo setup.py 또는 venv_setup.py를 먼저 실행하세요.
    pause
)
