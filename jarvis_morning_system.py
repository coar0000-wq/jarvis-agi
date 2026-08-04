#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🌅 JARVIS Morning Call System - Phase 1 Week 1 Main Implementation
완전 자동화된 아침 음성 비서 시스템
"""

import os
import sys
import pyttsx3
import requests
import schedule
import time
from datetime import datetime
import json

class JARVISMorningSystem:
    """도현님의 24시간 음성 비서 시스템"""

    def __init__(self):
        """시스템 초기화"""
        self.engine = pyttsx3.init()
        self.setup_voice()
        self.load_api_keys()
        self.log_file = "jarvis_morning_log.txt"

    def setup_voice(self):
        """여성음 설정"""
        voices = self.engine.getProperty('voices')
        try:
            # Microsoft Zira (영어 여성음) 설정
            self.engine.setProperty('voice', voices[1].id)
            self.voice_name = voices[1].name
        except:
            self.engine.setProperty('voice', voices[0].id)
            self.voice_name = voices[0].name

        self.engine.setProperty('rate', 180)  # 속도
        self.engine.setProperty('volume', 0.9)  # 크기

    def load_api_keys(self):
        """API 키 로드"""
        self.newsapi_key = os.getenv("NEWSAPI_KEY")
        self.alpha_vantage_key = os.getenv("ALPHA_VANTAGE_KEY")
        self.openweather_key = os.getenv("OPENWEATHER_API_KEY")

    def get_weather(self):
        """서울 날씨 조회"""
        try:
            if not self.openweather_key:
                return "날씨 정보를 가져올 수 없습니다"

            url = f"https://api.openweathermap.org/data/2.5/weather?q=Seoul&appid={self.openweather_key}&units=metric&lang=ko"
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

    def speak(self, message):
        """메시지 음성 재생"""
        print(f"🎙️ {message}")
        self.engine.say(message)
        self.engine.runAndWait()

    def log(self, message):
        """로그 기록"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}"
        print(log_message)

        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_message + '\n')

    def morning_call(self):
        """08:00 모닝콜 실행"""
        current_time = datetime.now().strftime("%H:%M")

        print("\n" + "="*60)
        print("🌅 JARVIS 모닝콜 시스템")
        print("="*60)
        self.log(f"✨ 모닝콜 시작 ({current_time})")

        # 1단계: 인사
        self.speak("좋은 아침입니다, 도현님!")
        time.sleep(1)

        # 2단계: 날씨
        weather = self.get_weather()
        self.speak(weather)
        time.sleep(1)

        # 3단계: 응원
        self.speak("오늘도 최고의 하루가 되길 응원합니다!")
        time.sleep(1)

        print("="*60)
        self.log("✨ 모닝콜 완료")
        print()

    def schedule_morning_call(self):
        """매일 08:00에 모닝콜 예약"""
        schedule.every().day.at("08:00").do(self.morning_call)
        self.log("📅 08:00 모닝콜 자동 스케줄링 완료")

    def run(self):
        """시스템 실행"""
        print("\n" + "="*60)
        print("🤖 JARVIS Phase 1 Week 1 - 모닝콜 시스템 시작")
        print("="*60 + "\n")

        self.log("🚀 JARVIS 시스템 시작")
        self.log(f"음성: {self.voice_name}")
        self.log(f"API 키 상태: NewsAPI={bool(self.newsapi_key)}, AlphaVantage={bool(self.alpha_vantage_key)}, OpenWeather={bool(self.openweather_key)}")

        # 스케줄링 설정
        self.schedule_morning_call()

        # 테스트: 지금 바로 모닝콜 실행
        print("📌 테스트: 지금 바로 모닝콜 재생...\n")
        self.morning_call()

        # 스케줄러 실행
        print("⏰ 스케줄러 시작 (매일 08:00에 자동 실행)")
        print("💡 Ctrl+C로 종료할 수 있습니다\n")

        try:
            while True:
                schedule.run_pending()
                time.sleep(60)
        except KeyboardInterrupt:
            print("\n\n🛑 시스템 종료")
            self.log("🛑 JARVIS 시스템 종료")

if __name__ == "__main__":
    system = JARVISMorningSystem()
    system.run()
