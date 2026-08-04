# 🚀 JARVIS 자동 배포 스크립트
# PowerShell에서 실행: powershell -ExecutionPolicy Bypass -File JARVIS_Auto_Deploy.ps1

Write-Host "`n" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "🚀 JARVIS 자동 배포 시작" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Git 설치 확인
Write-Host "📍 Step 1: Git 설치 확인" -ForegroundColor Yellow
Write-Host "----------------------------------------" -ForegroundColor Yellow

try {
    $gitVersion = git --version
    Write-Host "✅ Git 설치됨: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Git이 설치되지 않았습니다!" -ForegroundColor Red
    Write-Host "📥 다운로드: https://git-scm.com/download/win" -ForegroundColor Cyan
    exit
}

# Step 2: 필요한 파일 확인
Write-Host "`n📍 Step 2: 필수 파일 확인" -ForegroundColor Yellow
Write-Host "----------------------------------------" -ForegroundColor Yellow

$requiredFiles = @(
    "jarvis_web_monitor.py",
    "jarvis_youtube_monitor.py",
    "jarvis_paper_monitor.py",
    "jarvis_rss_monitor.py",
    "jarvis_phase_a_orchestrator.py",
    "jarvis_data_validator.py",
    "jarvis_phase_b_integrated.py",
    "jarvis_cloud_orchestrator.py",
    ".github\workflows\jarvis_auto_monitor.yml"
)

$allExist = $true
foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "  ✅ $file" -ForegroundColor Green
    } else {
        Write-Host "  ❌ $file (없음)" -ForegroundColor Red
        $allExist = $false
    }
}

if (-not $allExist) {
    Write-Host "`n❌ 필수 파일 부족!" -ForegroundColor Red
    exit
}

Write-Host "`n✅ 모든 필수 파일 확인됨" -ForegroundColor Green

# Step 3: GitHub 정보 입력
Write-Host "`n📍 Step 3: GitHub 정보 입력" -ForegroundColor Yellow
Write-Host "----------------------------------------" -ForegroundColor Yellow
Write-Host ""

$username = Read-Host "📝 GitHub 사용자명"
if ([string]::IsNullOrWhiteSpace($username)) {
    Write-Host "❌ 사용자명이 필요합니다!" -ForegroundColor Red
    exit
}

$email = Read-Host "📝 GitHub 이메일"
if ([string]::IsNullOrWhiteSpace($email)) {
    Write-Host "❌ 이메일이 필요합니다!" -ForegroundColor Red
    exit
}

Write-Host ""
Write-Host "✅ 입력 완료:" -ForegroundColor Green
Write-Host "  사용자명: $username" -ForegroundColor Cyan
Write-Host "  이메일: $email" -ForegroundColor Cyan

# Step 4: Git 설정
Write-Host "`n📍 Step 4: Git 전역 설정" -ForegroundColor Yellow
Write-Host "----------------------------------------" -ForegroundColor Yellow

git config --global user.email "$email"
git config --global user.name "$username"

Write-Host "✅ Git 설정 완료" -ForegroundColor Green

# Step 5: GitHub 저장소 초기화
Write-Host "`n📍 Step 5: 로컬 저장소 초기화" -ForegroundColor Yellow
Write-Host "----------------------------------------" -ForegroundColor Yellow

if (Test-Path ".git") {
    Write-Host "⚠️ 이미 Git 저장소입니다. 스킵." -ForegroundColor Yellow
} else {
    git init
    Write-Host "✅ Git 저장소 초기화 완료" -ForegroundColor Green
}

# Step 6: 모든 파일 추가
Write-Host "`n📍 Step 6: 파일 추가 및 커밋" -ForegroundColor Yellow
Write-Host "----------------------------------------" -ForegroundColor Yellow

git add .
$commitDate = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
git commit -m "🤖 JARVIS 초기 배포 ($commitDate)"

Write-Host "✅ 파일 커밋 완료" -ForegroundColor Green

# Step 7: GitHub 저장소 연결
Write-Host "`n📍 Step 7: GitHub 저장소 연결" -ForegroundColor Yellow
Write-Host "----------------------------------------" -ForegroundColor Yellow
Write-Host ""

$repoUrl = "https://github.com/$username/jarvis-agi.git"
Write-Host "📌 저장소 URL: $repoUrl" -ForegroundColor Cyan
Write-Host ""

$proceed = Read-Host "이 URL이 맞습니까? (y/n)"
if ($proceed -ne "y") {
    Write-Host "❌ 취소되었습니다." -ForegroundColor Red
    exit
}

# 기존 원격 제거
git remote remove origin -ErrorAction SilentlyContinue

# 새 원격 추가
git remote add origin $repoUrl

# main 브랜치로 변경
git branch -M main

Write-Host "✅ GitHub 원격 저장소 연결됨" -ForegroundColor Green

# Step 8: Push 준비
Write-Host "`n📍 Step 8: GitHub에 Push" -ForegroundColor Yellow
Write-Host "----------------------------------------" -ForegroundColor Yellow
Write-Host ""
Write-Host "⚠️ 주의:" -ForegroundColor Yellow
Write-Host "  1. GitHub에서 jarvis-agi 저장소를 생성했어야 합니다" -ForegroundColor Yellow
Write-Host "  2. 저장소는 Public으로 설정되어야 합니다" -ForegroundColor Yellow
Write-Host "  3. GitHub Personal Access Token이 필요할 수 있습니다" -ForegroundColor Yellow
Write-Host ""

$pushConfirm = Read-Host "계속 진행하시겠습니까? (y/n)"
if ($pushConfirm -eq "y") {
    try {
        git push -u origin main
        Write-Host "✅ GitHub에 Push 완료!" -ForegroundColor Green
    } catch {
        Write-Host "⚠️ Push 실패" -ForegroundColor Yellow
        Write-Host "   원인: $_" -ForegroundColor Yellow
        Write-Host "`n💡 해결 방법:" -ForegroundColor Cyan
        Write-Host "   1. GitHub에서 jarvis-agi 저장소 생성" -ForegroundColor Cyan
        Write-Host "   2. Personal Access Token 발급: https://github.com/settings/tokens" -ForegroundColor Cyan
        Write-Host "   3. 다시 실행" -ForegroundColor Cyan
    }
} else {
    Write-Host "❌ Push가 취소되었습니다." -ForegroundColor Red
}

# Step 9: API 키 입력
Write-Host "`n📍 Step 9: API 키 입력" -ForegroundColor Yellow
Write-Host "----------------------------------------" -ForegroundColor Yellow
Write-Host ""

Write-Host "📰 NewsAPI 발급:" -ForegroundColor Cyan
Write-Host "   https://newsapi.org → Get API Key" -ForegroundColor Cyan
$newsApiKey = Read-Host "NewsAPI 키 입력"

Write-Host ""
Write-Host "📺 YouTube API 발급:" -ForegroundColor Cyan
Write-Host "   https://console.cloud.google.com" -ForegroundColor Cyan
$youtubeApiKey = Read-Host "YouTube API 키 입력"

# Step 10: .env 파일 생성
Write-Host "`n📍 Step 10: 환경 설정 파일 생성" -ForegroundColor Yellow
Write-Host "----------------------------------------" -ForegroundColor Yellow

$envContent = @"
# JARVIS 환경 변수
NEWS_API_KEY=$newsApiKey
YOUTUBE_API_KEY=$youtubeApiKey
"@

$envContent | Out-File -FilePath ".env" -Encoding UTF8
Write-Host "✅ .env 파일 생성 완료" -ForegroundColor Green
Write-Host "   (이 파일은 GitHub에 업로드되지 않습니다)" -ForegroundColor Cyan

# Step 11: 최종 안내
Write-Host "`n" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host "✨ JARVIS 배포 준비 완료!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "🎯 다음 단계:" -ForegroundColor Cyan
Write-Host ""
Write-Host "1️⃣ GitHub 웹사이트에서 Secrets 등록:" -ForegroundColor Cyan
Write-Host "   저장소 → Settings → Secrets and variables → Actions" -ForegroundColor Cyan
Write-Host "   → New repository secret" -ForegroundColor Cyan
Write-Host ""
Write-Host "   SECRET 1: NEWS_API_KEY" -ForegroundColor Green
Write-Host "   값: $newsApiKey" -ForegroundColor Green
Write-Host ""
Write-Host "   SECRET 2: YOUTUBE_API_KEY" -ForegroundColor Green
Write-Host "   값: $youtubeApiKey" -ForegroundColor Green
Write-Host ""
Write-Host "2️⃣ Actions 탭에서 워크플로우 활성화:" -ForegroundColor Cyan
Write-Host "   저장소 → Actions 탭" -ForegroundColor Cyan
Write-Host "   → 'I understand...' 클릭" -ForegroundColor Cyan
Write-Host ""
Write-Host "3️⃣ 첫 테스트 실행:" -ForegroundColor Cyan
Write-Host "   Actions 탭 → JARVIS 자동 모니터링" -ForegroundColor Cyan
Write-Host "   → Run workflow" -ForegroundColor Cyan
Write-Host ""
Write-Host "✅ 완료 후:" -ForegroundColor Yellow
Write-Host "   매일 자정에 자동 실행됨" -ForegroundColor Yellow
Write-Host "   140개/일 자동 수집" -ForegroundColor Yellow
Write-Host "   Obsidian 자동 업데이트" -ForegroundColor Yellow
Write-Host "   메모리 자동 저장" -ForegroundColor Yellow
Write-Host ""
Write-Host "📊 진행도: GitHub Actions → 24/7 자동 AGI" -ForegroundColor Cyan
Write-Host ""
Write-Host "기간: 2026-08-04 ~ 2026-09-15" -ForegroundColor Cyan
Write-Host "레벨: 2.8 → 3.0 AGI 진화 중!" -ForegroundColor Cyan
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

pause
