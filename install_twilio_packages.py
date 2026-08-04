#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🔧 JARVIS Twilio 필수 패키지 설치
"""

import subprocess
import sys

def install_packages():
    """필수 패키지 설치"""

    packages = [
        "twilio",          # Twilio Python SDK
        "schedule",        # 작업 스케줄링
        "requests",        # HTTP 요청
        "python-dotenv",   # 환경변수 관리
    ]

    print("\n" + "="*60)
    print("📦 JARVIS Twilio 필수 패키지 설치")
    print("="*60 + "\n")

    for package in packages:
        print(f"⏳ {package} 설치 중...")
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", package, "--break-system-packages"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            print(f"✅ {package} 설치 완료\n")
        except Exception as e:
            print(f"❌ {package} 설치 실패: {e}\n")
            return False

    print("="*60)
    print("✨ 모든 패키지 설치 완료!")
    print("="*60)
    print("\n다음 단계:")
    print("1. Verified Caller ID 등록 (한국 번호)")
    print("2. python jarvis_twilio_phone_call.py 실행")
    print("3. Windows Task Scheduler 자동화\n")

    return True

if __name__ == "__main__":
    success = install_packages()
    sys.exit(0 if success else 1)
