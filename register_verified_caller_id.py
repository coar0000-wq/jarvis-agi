#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
📱 Verified Caller ID 자동 등록 스크립트
당신의 한국 번호(01066627063)를 Twilio에 등록 → 영구 무료!
REST API를 직접 사용하여 등록
"""

import sys
import requests
from base64 import b64encode
import json

# Twilio 계정 정보
ACCOUNT_SID = "AC92221a15842adab097c91701b98bc695"
AUTH_TOKEN = "f786d63cc589d29e8b5e1b2bf8a5ea47"  # 계정 전체 권한

# 등록할 번호 (한국)
PHONE_NUMBER = "+8201066627063"  # 국제 형식
FRIENDLY_NAME = "도현님의 핸드폰"

def register_verified_caller_id():
    """Verified Caller ID REST API로 등록"""

    print("\n" + "="*60)
    print("📱 Verified Caller ID 자동 등록 (REST API)")
    print("="*60 + "\n")

    try:
        # REST API 인증 헤더 준비 (Account SID + Auth Token)
        print(f"🔌 REST API 인증 준비 중...")
        auth_string = f"{ACCOUNT_SID}:{AUTH_TOKEN}"
        encoded_auth = b64encode(auth_string.encode()).decode()

        # Twilio REST API URL
        url = f"https://api.twilio.com/2010-04-01/Accounts/{ACCOUNT_SID}/OutgoingCallerIds.json"

        # 등록 데이터
        data = {
            "PhoneNumber": PHONE_NUMBER,
            "FriendlyName": FRIENDLY_NAME
        }

        # HTTP 헤더
        headers = {
            "Authorization": f"Basic {encoded_auth}",
            "Content-Type": "application/x-www-form-urlencoded"
        }

        # Verified Caller ID 등록
        print(f"\n📝 등록 정보:")
        print(f"  - 번호: {PHONE_NUMBER}")
        print(f"  - 이름: {FRIENDLY_NAME}")
        print(f"\n⏳ Twilio REST API로 등록 중...\n")

        response = requests.post(url, data=data, headers=headers, timeout=10)

        # 응답 확인
        if response.status_code in [200, 201]:
            result = response.json()
            print(f"✅ Verified Caller ID 등록 성공!")
            print(f"\n📌 등록 정보:")
            print(f"  - SID: {result.get('sid', 'N/A')}")
            print(f"  - 번호: {result.get('phone_number', 'N/A')}")
            print(f"  - 이름: {result.get('friendly_name', 'N/A')}")
            print(f"  - 생성일: {result.get('date_created', 'N/A')}")

            print("\n" + "="*60)
            print("✨ 등록 완료!")
            print("="*60)
            print("\n💡 다음 단계:")
            print("1. python jarvis_twilio_phone_call.py 실행")
            print("2. 테스트 전화가 울림 (당신의 번호로 발신)")
            print("3. Windows Task Scheduler 자동화\n")

            return True
        else:
            print(f"\n❌ 등록 실패!")
            print(f"상태 코드: {response.status_code}")
            print(f"응답: {response.text}")

            # 한국 번호 미지원 가능성
            if "invalid" in response.text.lower() or "not support" in response.text.lower():
                print(f"\n⚠️  한국 번호 미지원 가능성:")
                print(f"  - Twilio가 해당 국가/번호를 지원하지 않을 수 있음")
                print(f"  - 대신 Twilio 가상 번호 구매 필요 (약 $1/월)")
                print(f"  - 또는 관리자에게 문의\n")

            return False

    except requests.exceptions.RequestException as e:
        print(f"\n❌ 네트워크 오류: {e}")
        print(f"\n⚠️  문제 해결:")
        print(f"  1. 인터넷 연결 확인")
        print(f"  2. 방화벽/프록시 확인")
        print(f"  3. Twilio API 상태 확인\n")
        return False

    except Exception as e:
        print(f"\n❌ 등록 실패: {e}")
        print(f"\n⚠️  문제 해결:")
        print(f"  1. 번호 형식 확인: +8201066627063 (띄어쓰기 없음)")
        print(f"  2. Twilio Account SID & API Key 확인")
        print(f"  3. Trial 계정은 기본 제한이 있을 수 있음\n")

        return False

if __name__ == "__main__":
    success = register_verified_caller_id()
    sys.exit(0 if success else 1)
