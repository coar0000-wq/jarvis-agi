#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
💬 JARVIS Phase 1 Week 1 - 카카오톡 자동 메시지 시스템
매일 08:00에 카카오톡으로 음성 메시지 발송 (완전 무료!)
"""

import os
import sys
import requests
import schedule
import time
from datetime import datetime
import json

# ============================================================================
# 카카오 봇 설정
# ============================================================================

# 🔑 카카오 Open Builder에서 발급받은 정보
KAKAO_BOT_ID = os.getenv("KAKAO_BOT_ID", "YOUR_BOT_ID")  # 나중에 설정
KAKAO_USER_ID = os.getenv("KAKAO_USER_ID", "YOUR_USER_ID")  # 테스트용

# OpenWeather API
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

# ============================================================================
# 날씨 정보 조회
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
# 카카오톡 메시지 발송
# ============================================================================

class JARVISKakaoSystem:
    """카카오톡 기반 음성 비서 시스템"""

    def __init__(self):
        """시스템 초기화"""
        self.log_file = "jarvis_kakao_message_log.txt"

        # ⚠️ 주의: 카카오 설정 필수
        if KAKAO_BOT_ID == "YOUR_BOT_ID":
            print("\n⚠️  카카오 Bot ID가 설정되지 않았습니다!")
            print("다음 단계를 진행해주세요:")
            print("1. https://developers.kakao.com/ 접속")
            print("2. Open Builder에서 봇 생성")
            print("3. 봇 ID 확인 후 KAKAO_BOT_ID 환경변수 설정")
            print("환경변수 설정 방법:")
            print('  $env:KAKAO_BOT_ID = "YOUR_BOT_ID"')
            print('  $env:KAKAO_USER_ID = "YOUR_USER_ID"\n')

    def log(self, message):
        """로그 기록"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}"
        print(log_message)

        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_message + '\n')

    def send_kakao_message(self, text, image_url=None):
        """카카오톡 메시지 발송 (여러 방식)"""

        print(f"\n📨 카카오톡 메시지 발송 시도...")
        self.log(f"📨 메시지 발송: {text}")

        # ============================================================
        # 방식 1: Kakao Chatbot API (권장)
        # ============================================================
        self.send_via_chatbot_api(text)

        # ============================================================
        # 방식 2: 카카오톡 Plus Friend (유료 - 선택)
        # ============================================================
        # self.send_via_plus_friend(text)

    def send_via_chatbot_api(self, text):
        """방식 1: Kakao Chatbot API로 발송

        💡 작동 방식:
        1. 사용자가 봇과 채팅 시작
        2. 봇이 자동으로 메시지 전송
        3. 카카오톡 앱에서 수신
        """

        try:
            # Kakao Chatbot Message API
            url = "https://kapi.kakao.com/v2/bot/message/send"

            headers = {
                "Authorization": f"Bearer {KAKAO_BOT_ID}",
                "Content-Type": "application/json"
            }

            # 메시지 포맷 (BasicCard)
            payload = {
                "user_key": KAKAO_USER_ID,
                "message": {
                    "text": text
                }
            }

            response = requests.post(url, json=payload, headers=headers, timeout=10)

            if response.status_code in [200, 201]:
                print(f"✅ 카카오톡 메시지 발송 성공!")
                self.log(f"✅ 카카오톡 메시지 전송 완료")
                return True
            else:
                print(f"⚠️ 상태 코드: {response.status_code}")
                print(f"응답: {response.text}")
                self.log(f"❌ 발송 실패: {response.status_code}")
                return False

        except Exception as e:
            print(f"❌ 발송 오류: {e}")
            self.log(f"❌ 오류: {e}")
            return False

    def send_via_plus_friend(self, text):
        """방식 2: 카카오톡 플러스친구 (유료)

        💡 비용: 월 수천원대
        💡 장점: 일반 계정에서 메시지 발송 가능
        """

        print("\n📝 카카오톡 Plus Friend API (유료 - 선택사항)")
        print("- 월간 수천원 비용")
        print("- 공식 비즈니스 메시지 발송 가능")
        self.log("ℹ️ Plus Friend는 유료 서비스입니다")

    def send_morning_message(self):
        """아침 메시지 발송"""

        current_time = datetime.now().strftime("%H:%M")

        print("\n" + "="*60)
        print("💬 JARVIS 카카오톡 메시지 시스템")
        print("="*60)
        self.log(f"✨ 메시지 발송 시작 ({current_time})")

        try:
            # 메시지 구성
            greeting = "좋은 아침입니다, 도현님! 🌅"
            weather = get_weather()
            encouragement = "오늘도 최고의 하루가 되길 응원합니다! 💪"

            # 전체 메시지
            full_message = f"{greeting}\n\n{weather}\n\n{encouragement}"

            print(f"\n📨 발송 메시지:")
            print(f"  {greeting}")
            print(f"  {weather}")
            print(f"  {encouragement}")

            # 카카오톡 발송
            self.send_kakao_message(full_message)

            print("="*60)
            self.log("✨ 메시지 발송 완료")
            print()

        except Exception as e:
            error_msg = f"❌ 메시지 발송 실패: {e}"
            print(error_msg)
            self.log(error_msg)

    def schedule_morning_message(self):
        """매일 08:00에 메시지 발송 예약"""
        schedule.every().day.at("08:00").do(self.send_morning_message)
        self.log("📅 08:00 카카오톡 메시지 자동 스케줄링 완료")

    def run(self):
        """시스템 실행"""
        print("\n" + "="*60)
        print("🤖 JARVIS Phase 1 Week 1 - 카카오톡 메시지 시스템")
        print("="*60 + "\n")

        self.log("🚀 JARVIS 카카오톡 시스템 시작")

        # 스케줄링 설정
        self.schedule_morning_message()

        # 테스트: 지금 바로 메시지 발송
        print("📌 테스트: 지금 바로 카카오톡 메시지 발송...\n")
        self.send_morning_message()

        # 스케줄러 실행
        print("⏰ 스케줄러 시작 (매일 08:00에 자동 실행)")
        print("💡 Ctrl+C로 종료할 수 있습니다\n")

        try:
            while True:
                schedule.run_pending()
                time.sleep(60)
        except KeyboardInterrupt:
            print("\n\n🛑 시스템 종료")
            self.log("🛑 JARVIS 카카오톡 시스템 종료")

if __name__ == "__main__":
    system = JARVISKakaoSystem()
    system.run()
