# ============================================================================
# 🔑 Phase 1 Step 1: 환경변수 설정
# ============================================================================
# 사용방법: PowerShell에서 실행
# PS> Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
# PS> .\Phase1_Step1_환경변수설정.ps1

Write-Host "🔑 JARVIS Phase 1 - API 키 환경변수 설정" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

# API 키 설정
$newsapi_key = "51a641bc42eb40fa9f0022969b58aca9"
$alpha_vantage_key = "GVD1R10Z7YTYBCMF"
$openweather_key = "56393288cc71f2fab8dza53846fcb51f31"

# 현재 세션에 설정
Write-Host "📝 현재 세션에 환경변수 설정 중..." -ForegroundColor Yellow
$env:NEWSAPI_KEY = $newsapi_key
$env:ALPHA_VANTAGE_KEY = $alpha_vantage_key
$env:OPENWEATHER_API_KEY = $openweather_key

Write-Host "✅ NewsAPI: $($env:NEWSAPI_KEY)" -ForegroundColor Green
Write-Host "✅ Alpha Vantage: $($env:ALPHA_VANTAGE_KEY)" -ForegroundColor Green
Write-Host "✅ OpenWeatherMap: $($env:OPENWEATHER_API_KEY)" -ForegroundColor Green
Write-Host ""

# 영구 설정 (선택사항)
$response = Read-Host "영구 설정하시겠습니까? (Y/N)"
if ($response -eq "Y" -or $response -eq "y") {
    Write-Host "🔧 시스템 환경변수에 영구 설정 중..." -ForegroundColor Yellow
    [Environment]::SetEnvironmentVariable("NEWSAPI_KEY", $newsapi_key, "User")
    [Environment]::SetEnvironmentVariable("ALPHA_VANTAGE_KEY", $alpha_vantage_key, "User")
    [Environment]::SetEnvironmentVariable("OPENWEATHER_API_KEY", $openweather_key, "User")
    Write-Host "✅ 영구 설정 완료! (시스템 재시작 권장)" -ForegroundColor Green
} else {
    Write-Host "⚠️  현재 세션에만 적용됨 (재시작 시 초기화)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "✨ Step 1 완료! 다음은 패키지 설치입니다." -ForegroundColor Green
Read-Host "엔터를 눌러 계속..."
