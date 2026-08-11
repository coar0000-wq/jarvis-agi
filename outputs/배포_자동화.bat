@echo off
chcp 65001 > nul
cls

echo.
echo ============================================================
echo  🚀 JARVIS 통합 대시보드 - 완전 자동 배포 시작!
echo ============================================================
echo.

REM Step 1: 관리자 권한 확인
echo 📍 Step 1: 환경 확인 중...

where git >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Git이 설치되어 있지 않습니다.
    echo    https://git-scm.com/download/win 에서 다운로드 후 설치하세요.
    pause
    exit /b 1
)

where node >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Node.js가 설치되어 있지 않습니다.
    echo    https://nodejs.org/ 에서 LTS 버전 다운로드 후 설치하세요.
    pause
    exit /b 1
)

echo ✅ Git 확인됨
echo ✅ Node.js 확인됨
echo.

REM Step 2: 프로젝트 폴더로 이동
echo 📍 Step 2: 프로젝트 폴더 이동...
cd /d "C:\Users\Desktop\Claude\Projects\kms"
if %ERRORLEVEL% NEQ 0 (
    echo ❌ 프로젝트 폴더를 찾을 수 없습니다.
    pause
    exit /b 1
)
echo ✅ 폴더 이동 완료: %CD%
echo.

REM Step 3: Git 초기화
echo 📍 Step 3: Git 저장소 초기화...
if not exist ".git" (
    git init
    echo ✅ Git 저장소 생성됨
) else (
    echo ✅ Git 저장소 이미 존재
)
echo.

REM Step 4: Vercel CLI 설치
echo 📍 Step 4: Vercel CLI 설치 중...
echo    (처음 설치 시 1-2분 소요)
call npm install -g vercel
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Vercel CLI 설치 실패
    pause
    exit /b 1
)
echo ✅ Vercel CLI 설치 완료
echo.

REM Step 5: 코드 커밋
echo 📍 Step 5: 코드 커밋 중...
git add .
for /f "tokens=2-4 delims=/ " %%a in ('date /t') do (set mydate=%%c-%%a-%%b)
for /f "tokens=1-2 delims=/:" %%a in ('time /t') do (set mytime=%%a%%b)
git commit -m "Add JARVIS Dashboard - Auto Deploy %mydate% %mytime%" 2>nul || (
    echo ⚠️  변경사항 없음 (이미 커밋됨)
)
echo ✅ 커밋 완료
echo.

REM Step 6: GitHub 안내
echo ============================================================
echo  📌 GitHub 설정 필요 (중요!)
echo ============================================================
echo.
echo 1️⃣  GitHub 계정에 로그인: https://github.com
echo.
echo 2️⃣  새 리포지토리 생성:
echo     - 이름: jarvis-dashboard
echo     - Public 선택
echo     - "Create repository" 클릭
echo.
echo 3️⃣  다음 명령어를 터미널에 복사-붙여넣기:
echo.
echo     git remote add origin https://github.com/[당신의계정]/jarvis-dashboard.git
echo     git branch -M main
echo     git push -u origin main
echo.
echo ============================================================
echo.
pause /prompt "위 단계를 모두 완료했나요? (아무 키나 눌러서 계속)"
echo.

REM Step 7: Vercel 배포
echo 📍 Step 6: Vercel 배포 시작...
echo    (브라우저가 자동으로 열립니다)
echo    (로그인 후 프로젝트 설정 화면에서 "Deploy" 클릭)
echo.

call vercel --prod

if %ERRORLEVEL% NEQ 0 (
    echo ❌ Vercel 배포 실패
    echo    Vercel에 로그인했는지 확인하세요.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo  ✅ 배포 완료!
echo ============================================================
echo.
echo 🌐 대시보드 접속:
echo    위의 Vercel URL을 사용하세요 (예: jarvis-dashboard-xyz.vercel.app)
echo.
echo 📊 라이브 모니터링:
echo    Slack #daiso-team 채널에 URL을 고정하세요
echo.
echo 🔄 실시간 데이터 업데이트:
echo    자동 업데이트 스크립트를 실행하면 매분 데이터가 갱신됩니다
echo.
echo 🎉 축하합니다! 대시보드가 배포되었습니다!
echo.
pause
