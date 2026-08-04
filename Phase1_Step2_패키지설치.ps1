# ============================================================================
# 📦 Phase 1 Step 2: 필수 패키지 설치
# ============================================================================
# 사용방법: PowerShell에서 실행
# PS> Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
# PS> .\Phase1_Step2_패키지설치.ps1

Write-Host "📦 JARVIS Phase 1 - 필수 패키지 설치" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

# 설치할 패키지 목록
$packages = @(
    "pyttsx3",      # 음성 합성 (여성음)
    "schedule",     # 작업 스케줄링 (08:00, 12:00, 17:30, 21:00)
    "requests",     # HTTP 요청 (API 호출)
    "anthropic"     # Claude API
)

Write-Host "설치할 패키지:" -ForegroundColor Yellow
foreach ($pkg in $packages) {
    Write-Host "  - $pkg" -ForegroundColor Cyan
}
Write-Host ""

Write-Host "🔧 설치 시작 (약 2-3분 소요)..." -ForegroundColor Yellow
Write-Host ""

# 패키지 설치
foreach ($pkg in $packages) {
    Write-Host "⏳ $pkg 설치 중..." -ForegroundColor Cyan
    pip install $pkg -q
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ $pkg 설치 완료" -ForegroundColor Green
    } else {
        Write-Host "❌ $pkg 설치 실패" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "✨ Step 2 완료! 모든 패키지 설치 완료" -ForegroundColor Green
Write-Host ""
Write-Host "다음은 pyttsx3 여성음 설정입니다." -ForegroundColor Green
Read-Host "엔터를 눌러 계속..."
