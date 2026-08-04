#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🔧 Windows Task Scheduler - JARVIS Twilio 자동 실행 설정
매일 08:00에 자동으로 전화 발신
"""

import subprocess
import sys
import os
import ctypes

def request_admin():
    """자동으로 관리자 권한 상승"""
    try:
        if not ctypes.windll.shell.IsUserAnAdmin():
            print("\n⚠️  관리자 권한이 필요합니다.")
            print("🔄 자동으로 관리자 권한으로 재실행 중...\n")

            # 관리자 권한으로 다시 실행
            ctypes.windll.shell.ShellExecuteW(
                None,
                "runas",
                sys.executable,
                " ".join(sys.argv),
                None,
                1
            )
            sys.exit()
    except Exception as e:
        print(f"⚠️  권한 상승 오류: {e}")
        print("수동으로 관리자 권한으로 실행해주세요.")

def setup_task():
    """Windows Task Scheduler에 자동 실행 작업 등록"""

    print("\n" + "="*60)
    print("🔧 Windows Task Scheduler 설정 시작")
    print("="*60 + "\n")

    # 경로 설정
    script_path = r"C:\Users\Desktop\Claude\Projects\kms\jarvis_twilio_phone_call.py"
    task_name = "JARVIS_Twilio_MorningCall_08AM"
    work_dir = r"C:\Users\Desktop\Claude\Projects\kms"

    # PowerShell 명령어
    ps_command = f'''
# 기존 작업 삭제 (있으면)
$taskName = '{task_name}'
$existingTask = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
if ($existingTask) {{
    Write-Host "⚠️  기존 작업 삭제 중..." -ForegroundColor Yellow
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
}}

# 새 작업 생성
Write-Host "✅ 새 작업 생성 중..." -ForegroundColor Green

$action = New-ScheduledTaskAction `
    -Execute "python" `
    -Argument '{script_path}' `
    -WorkingDirectory '{work_dir}'

$trigger = New-ScheduledTaskTrigger `
    -Daily `
    -At "08:00AM"

$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -RunWithoutNetwork:$false

$task = Register-ScheduledTask `
    -TaskName $taskName `
    -Action $action `
    -Trigger $trigger `
    -Settings $settings `
    -RunLevel Highest `
    -Description "JARVIS Twilio 음성 비서 - 매일 08:00 자동 전화" `
    -Force

Write-Host ""
Write-Host "✨ 작업 등록 완료!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 작업 정보:" -ForegroundColor Cyan
Write-Host "  - 이름: $taskName"
Write-Host "  - 실행 시간: 매일 08:00 AM"
Write-Host "  - 스크립트: {script_path}"
Write-Host ""
Write-Host "✅ JARVIS Twilio 자동화 설정 완료!" -ForegroundColor Green
Write-Host "🎉 이제 매일 08:00에 자동으로 전화가 울릴 것입니다!" -ForegroundColor Cyan
Write-Host ""
'''

    try:
        print("⏳ PowerShell 실행 중...")

        # PowerShell 실행
        result = subprocess.run(
            ["powershell", "-NoProfile", "-Command", ps_command],
            capture_output=True,
            text=True,
            shell=False
        )

        print(result.stdout)

        if result.returncode == 0:
            print("\n" + "="*60)
            print("✅ Task Scheduler 설정 완료!")
            print("="*60)
            print("\n🎉 모든 설정이 완료되었습니다!")
            print("📅 내일 (또는 오늘) 08:00에 자동으로 전화가 울릴 것입니다.")
            print("\n💡 테스트하려면:")
            print("   1. Task Scheduler 열기 (Win+R → 'taskschd.msc' 입력)")
            print("   2. 'JARVIS_Twilio_MorningCall_08AM' 찾기")
            print("   3. 우클릭 → '실행' 선택")
            print("\n💰 비용: 0원 (영구 무료!)")
            print("   - Verified Caller ID로의 호출은 Twilio Free Trial에서도 무료")
            print("   - 30일 후 Pay as You Go 전환 후에도 무료 (pre-registered 번호)")
            return True
        else:
            print("\n❌ 오류 발생!")
            print(result.stderr)
            return False

    except Exception as e:
        print(f"\n❌ 오류: {e}")
        return False

if __name__ == "__main__":
    # 관리자 권한 자동 상승
    request_admin()

    success = setup_task()
    sys.exit(0 if success else 1)
