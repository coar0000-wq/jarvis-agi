# ============================================================================
# 🤖 Windows Task Scheduler - 매일 08:00 자동 실행 설정
# ============================================================================
# 사용방법: PowerShell 관리자 권한으로 실행
# PS> Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
# PS> .\setup_windows_task.ps1

Write-Host "🔧 JARVIS 자동 스케줄링 설정 시작" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

# 파이썬 경로 설정
$pythonPath = "python"
$scriptPath = "C:\Users\Desktop\Claude\Projects\kms\jarvis_morning_system.py"
$taskName = "JARVIS_MorningCall_08AM"

# 기존 작업 삭제 (있으면)
Write-Host "⏳ 기존 작업 확인 중..." -ForegroundColor Cyan
$existingTask = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
if ($existingTask) {
    Write-Host "⚠️  기존 작업 삭제..." -ForegroundColor Yellow
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
}

Write-Host ""
Write-Host "✅ 새 작업 생성 중..." -ForegroundColor Green

# 작업 설정
$action = New-ScheduledTaskAction `
    -Execute $pythonPath `
    -Argument $scriptPath `
    -WorkingDirectory "C:\Users\Desktop\Claude\Projects\kms"

$trigger = New-ScheduledTaskTrigger `
    -Daily `
    -At "08:00AM"

$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -RunWithoutNetwork:$false

# 작업 등록
$task = Register-ScheduledTask `
    -TaskName $taskName `
    -Action $action `
    -Trigger $trigger `
    -Settings $settings `
    -RunLevel Highest `
    -Description "JARVIS 음성 비서 - 매일 08:00 자동 실행" `
    -Force

Write-Host ""
Write-Host "✨ 작업 등록 완료!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 작업 정보:" -ForegroundColor Cyan
Write-Host "  - 이름: $taskName"
Write-Host "  - 실행 시간: 매일 08:00 AM"
Write-Host "  - 스크립트: $scriptPath"
Write-Host ""
Write-Host "✅ 설정 완료!" -ForegroundColor Green
Write-Host "🎉 이제 매일 08:00에 자동으로 모닝콜이 울릴 것입니다!"
Write-Host ""
