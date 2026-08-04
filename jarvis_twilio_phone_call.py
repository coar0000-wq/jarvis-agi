#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🎙️ JARVIS Phase 1 Week 1 - Twilio 자동 전화 호출 시스템
매일 08:00에 도현님의 핸드폰으로 자동 전화
Twilio Free Trial + Verified Caller ID = 영구 무료
"""

import os
import sys
import requests
import schedule
import time
from datetime import datetime
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse

# ============================================================================
# STEP 1: Twilio 계정 정보 (환경변수로 설정됨)
# ============================================================================

# 당신의 Twilio 계정 정보
ACCOUNT_SID = "AC92221a15842adab097c91701b98bc695"
API_KEY_SID = "SK25178bfe7adf2b2d30c5105096960450"
API_KEY_SECRET = "SKc48cf44beee5f5dab0699c01a14bb10b"

# 전화 정보
FROM_NUMBER = "+8201066627063"  # Verified Caller ID (당신의 번호) - 무료!
TO_NUMBER = "+8201066627063"    # 도현님의 번호 (= FROM_NUMBER일 때 무료)
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

# ============================================================================
# STEP 2: Twilio 클라이언트 초기화
# ============================================================================

def init_twilio():
    """Twilio 클라이언트 생성 (API Key 인증 사용)"""
    try:
        client = Client(
            ACCOUNT_SID,
            API_KEY_SID,
            API_KEY_SECRET
        )
        return client
    except Exception as e:
        print(f"❌ Twilio 클라이언트 초기화 실패: {e}")
        return None

# ============================================================================
# STEP 3: 날씨 정보 조회
# ============================================================================

def get_weather():
    """서울 날씨 조회"""
    try:
        if not OPENWEATHER_API_KEY:
            return "날씨 정보를 가져올 수 없습니다"

        url = f"https://api.openweathermap.org/data/2.5/weather?q=Seoul&appid={OPENWEATHER_API_KEY}&units=metric&lang=ko"
        response = requests.get(url, timeout=5)
        data = response.json()

        if response.status_code == 200:
            temp = int(data['main']['temp'])
            description = data['weather'][0]['description']
            return f"서울은 {description}이고 기온은 {temp}도입니다"
        else:
            return "날씨 정보를 가져올 수 없습니다"
    except Exception as e:
        print(f"⚠️ 날씨 조회 오류: {e}")
        return "날씨 정보를 가져올 수 없습니다"

# ============================================================================
# STEP 4: TwiML 응답 생성 (음성 메시지)
# ============================================================================

def generate_twiml_response(message1, message2, message3):
    """TwiML 음성 응답 생성"""
    response = VoiceResponse()

    # 음성 재생 (Google TTS 사용)
    response.say(message1, voice='alice', language='ko-KR')
    response.pause(length=1)

    response.say(message2, voice='alice', language='ko-KR')
    response.pause(length=1)

    response.say(message3, voice='alice', language='ko-KR')

    return str(response)

# ============================================================================
# STEP 5: 자동 전화 호출
# ============================================================================

class JARVISTwilioSystem:
    """Twilio 기반 음성 전화 비서 시스템"""

    def __init__(self):
        """시스템 초기화"""
        self.client = init_twilio()
        self.log_file = "jarvis_twilio_call_log.txt"

        if not self.client:
            print("❌ Twilio 클라이언트 초기화 실패!")
            sys.exit(1)

    def log(self, message):
        """로그 기록"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}"
        print(log_message)

        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_message + '\n')

    def make_phone_call(self):
        """전화 호출 실행"""
        current_time = datetime.now().strftime("%H:%M")

        print("\n" + "="*60)
        print("📞 JARVIS 모닝콜 시스템 - Twilio 전화")
        print("="*60)
        self.log(f"✨ 모닝콜 시작 ({current_time})")

        try:
            # 메시지 준비
            message1 = "좋은 아침입니다, 도현님!"

            # 날씨 조회
            weather = get_weather()
            message2 = weather

            # 응원 메시지
            message3 = "오늘도 최고의 하루가 되길 응원합니다!"

            # TwiML 생성
            twiml = generate_twiml_response(message1, message2, message3)

            # 전화 걸기
            print(f"\n📱 전화 발신: {FROM_NUMBER} → {TO_NUMBER}")
            print(f"💬 메시지: {message1} / {message2} / {message3}")

            call = self.client.calls.create(
                to=TO_NUMBER,
                from_=FROM_NUMBER,
                twiml=twiml,
                timeout=60
            )

            print(f"✅ 전화 발신 성공!")
            print(f"📌 Call SID: {call.sid}")
            print(f"📊 상태: {call.status}")

            self.log(f"✅ 전화 발신 성공! Call SID: {call.sid}")
            self.log(f"📊 상태: {call.status}")

            print("="*60)
            self.log("✨ 모닝콜 완료")
            print()

        except Exception as e:
            error_msg = f"❌ 전화 호출 실패: {e}"
            print(error_msg)
            self.log(error_msg)

    def schedule_morning_call(self):
        """매일 08:00에 모닝콜 예약"""
        schedule.every().day.at("08:00").do(self.make_phone_call)
        self.log("📅 08:00 모닝콜 자동 스케줄링 완료")

    def run(self):
        """시스템 실행"""
        print("\n" + "="*60)
        print("🤖 JARVIS Phase 1 Week 1 - Twilio 전화 시스템 시작")
        print("="*60 + "\n")

        self.log("🚀 JARVIS Twilio 시스템 시작")
        self.log(f"Account SID: {ACCOUNT_SID}")
        self.log(f"From: {FROM_NUMBER} → To: {TO_NUMBER}")

        # 스케줄링 설정
        self.schedule_morning_call()

        # 테스트: 지금 바로 전화 발신
        print("📌 테스트: 지금 바로 전화 발신...\n")
        self.make_phone_call()

        # 스케줄러 실행
        print("⏰ 스케줄러 시작 (매일 08:00에 자동 실행)")
        print("💡 Ctrl+C로 종료할 수 있습니다\n")

        try:
            while True:
                schedule.run_pending()
                time.sleep(60)
        except KeyboardInterrupt:
            print("\n\n🛑 시스템 종료")
            self.log("🛑 JARVIS Twilio 시스템 종료")

if __name__ == "__main__":
    system = JARVISTwilioSystem()
    system.run()
