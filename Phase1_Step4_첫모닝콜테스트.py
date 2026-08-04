#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
☀️ Phase 1 Step 4: 첫 모닝콜 테스트
사용방법: python Phase1_Step4_첫모닝콜테스트.py
"""

import os
import sys
from datetime import datetime
import pyttsx3
import requests

def get_weather():
    """OpenWeatherMap API로 현재 날씨 조회"""
    try:
        api_key = os.getenv("OPENWEATHER_API_KEY")
        if not api_key:
            print("⚠️  OPENWEATHER_API_KEY 환경변수 없음")
            return "날씨 정보를 가져올 수 없습니다"

        # 서울 날씨 조회
        url = f"https://api.openweathermap.org/data/2.5/weather?q=Seoul&appid={api_key}&units=metric&lang=ko"
        response = requests.get(url, timeout=5)
        data = response.json()

        if response.status_code == 200:
            temp = int(data['main']['temp'])
            description = data['weather'][0]['description']
            return f"서울은 {description}이고 기온은 {temp}도입니다"
        else:
            return "날씨 정보를 가져올 수 없습니다"
    except Exception as e:
        print(f"⚠️  날씨 조회 오류: {e}")
        return "날씨 정보를 가져올 수 없습니다"

def morning_call():
    """08:00 모닝콜 테스트"""

    print("\n" + "="*60)
    print("☀️ JARVIS Phase 1 - 첫 모닝콜 테스트")
    print("="*60 + "\n")

    # 현재 시간
    now = datetime.now()
    current_time = now.strftime("%H:%M")

    print(f"⏰ 현재 시간: {current_time}")
    print()

    # TTS 엔진 초기화
    engine = pyttsx3.init()

    # 여성음 설정
    voices = engine.getProperty('voices')
    try:
        engine.setProperty('voice', voices[1].id)
        print(f"🎙️ 음성: {voices[1].name}")
    except:
        engine.setProperty('voice', voices[0].id)
        print(f"🎙️ 음성: {voices[0].name}")

    # 음성 속도/크기 설정
    engine.setProperty('rate', 180)
    engine.setProperty('volume', 0.9)

    print()
    print("🎧 모닝콜 재생 시작:")
    print("="*60 + "\n")

    # 모닝콜 메시지 생성
    messages = [
        "좋은 아침입니다, 도현님!",
    ]

    # 날씨 조회
    weather = get_weather()
    print(f"🌤️ 날씨: {weather}")
    messages.append(weather)

    # 응원 메시지
    messages.append("오늘도 최고의 하루가 되길 응원합니다!")

    # 메시지 재생
    for i, msg in enumerate(messages, 1):
        print(f"🔊 [{i}] {msg}")
        engine.say(msg)
        engine.runAndWait()
        print(f"    ✅ 재생 완료\n")

    print("="*60)
    print("✨ Step 4 완료! 첫 모닝콜 테스트 완료")
    print("="*60 + "\n")

    # 다음 단계 안내
    print("📋 다음 단계:")
    print("  1. ✅ 환경변수 설정")
    print("  2. ✅ 패키지 설치")
    print("  3. ✅ pyttsx3 여성음 설정")
    print("  4. ✅ 첫 모닝콜 테스트")
    print("  5. ⏳ Asterisk 설정 (선택사항)")
    print()

if __name__ == "__main__":
    try:
        morning_call()
        print("✨ 모닝콜 테스트가 완료되었습니다!")
        print()
        print("🎉 Phase 1 Week 1 기본 준비 완료!")
        print()
        print("📅 다음 일정:")
        print("  - Week 1 (08-05~08-11): 모닝콜 시스템 완성")
        print("  - Week 2 (08-12~08-19): 뉴스/비즈니스/철학 에이전트 추가")
        print("  - 2026-08-19: Phase 1 정식 출시")
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
