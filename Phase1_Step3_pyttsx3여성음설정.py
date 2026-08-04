#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🎙️ Phase 1 Step 3: pyttsx3 여성음 설정 및 테스트
사용방법: python Phase1_Step3_pyttsx3여성음설정.py
"""

import pyttsx3
import sys

def setup_female_voice():
    """여성음 설정 및 테스트"""

    print("\n" + "="*60)
    print("🎙️ JARVIS Phase 1 - pyttsx3 여성음 설정")
    print("="*60 + "\n")

    # TTS 엔진 초기화
    engine = pyttsx3.init()

    # 사용 가능한 음성 출력
    print("🔍 사용 가능한 음성:")
    voices = engine.getProperty('voices')
    for i, voice in enumerate(voices):
        print(f"  {i}: {voice.name}")

    print()

    # 여성음 설정 (보통 여성음은 인덱스 1)
    try:
        # Windows: 일반적으로 여성음이 인덱스 1
        # Mac: 여성음이 인덱스 1 또는 2
        female_voice_id = voices[1].id
        engine.setProperty('voice', female_voice_id)
        print(f"✅ 여성음 설정: {voices[1].name}")
    except (IndexError, AttributeError):
        print("⚠️  여성음 자동 설정 실패, 기본 음성 사용")
        female_voice_id = voices[0].id
        engine.setProperty('voice', female_voice_id)

    # 음성 속도 설정 (기본값: 200)
    engine.setProperty('rate', 180)  # 좀 더 천천히
    print("📊 음성 속도: 180 (느림)")

    # 음성 볼륨 설정 (0.0 ~ 1.0)
    engine.setProperty('volume', 0.9)
    print("🔊 음성 크기: 0.9 (큼)")

    print("\n" + "="*60)
    print("🎧 음성 테스트 재생:")
    print("="*60 + "\n")

    # 테스트 텍스트
    test_messages = [
        "좋은 아침입니다, 도현님!",
        "오늘은 화창한 날씨입니다.",
        "JARVIS 음성 비서 시스템입니다."
    ]

    for i, msg in enumerate(test_messages, 1):
        print(f"🔊 [{i}] {msg}")
        engine.say(msg)
        engine.runAndWait()
        print(f"    ✅ 재생 완료\n")

    print("="*60)
    print("✨ Step 3 완료! pyttsx3 여성음 설정 완료")
    print("="*60 + "\n")

    # 설정 저장
    print("💾 설정 정보:")
    print(f"  - 음성: {voices[1].name}")
    print(f"  - 속도: 180")
    print(f"  - 크기: 0.9")
    print()

    return engine

if __name__ == "__main__":
    try:
        engine = setup_female_voice()
        print("✨ pyttsx3 여성음 설정이 완료되었습니다!")
        print("다음은 첫 모닝콜 테스트입니다.")
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        sys.exit(1)
