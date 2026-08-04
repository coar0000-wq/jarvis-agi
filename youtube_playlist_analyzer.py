#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🎬 YouTube 재생목록 분석 스크립트
yt-dlp를 사용해서 재생목록의 모든 영상 정보 수집
"""

import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime

def get_playlist_info(playlist_url):
    """재생목록 정보 수집"""

    print("\n📥 YouTube 재생목록 정보 수집 중...\n")

    # yt-dlp 명령어
    cmd = [
        "yt-dlp",
        "--dump-json",
        "--flat-playlist",
        playlist_url
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)

        if result.returncode != 0:
            print(f"❌ 오류: {result.stderr}")
            return None

        # JSON 파싱
        videos = []
        for line in result.stdout.strip().split('\n'):
            if line.strip():
                try:
                    data = json.loads(line)
                    videos.append(data)
                except json.JSONDecodeError:
                    pass

        return videos

    except subprocess.TimeoutExpired:
        print("❌ 타임아웃: 재생목록이 너무 큽니다")
        return None
    except Exception as e:
        print(f"❌ 오류: {e}")
        return None

def save_analysis(videos, output_dir):
    """분석 결과 저장"""

    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)

    print(f"\n📊 {len(videos)}개 영상 분석 결과 저장 중...\n")

    # 1. 재생목록 인덱스 생성
    index_md = f"""# 🎬 YouTube 재생목록 분석

**날짜**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**영상 개수**: {len(videos)}개
**상태**: ✅ 분석 완료

---

## 📋 영상 목록

"""

    for i, video in enumerate(videos, 1):
        title = video.get('title', 'Unknown')
        video_id = video.get('id', '')
        duration = video.get('duration', 0)

        duration_str = f"{duration//60}:{duration%60:02d}" if duration else "Unknown"

        index_md += f"### {i}. {title}\n"
        index_md += f"- **Video ID**: `{video_id}`\n"
        index_md += f"- **길이**: {duration_str}\n"
        index_md += f"- **문서**: [[youtube-{i:02d}-{title.replace(' ', '-')[:30].lower()}]]\n\n"

    # 인덱스 저장
    index_path = output_dir / "youtube_playlist_index.md"
    index_path.write_text(index_md, encoding='utf-8')
    print(f"✅ 저장: {index_path}")

    # 2. 각 영상별 분석 문서 생성
    for i, video in enumerate(videos, 1):
        title = video.get('title', 'Unknown')
        video_id = video.get('id', '')
        duration = video.get('duration', 0)
        description = video.get('description', 'No description')
        url = f"https://www.youtube.com/watch?v={video_id}"

        duration_str = f"{duration//60}:{duration%60:02d}" if duration else "Unknown"

        video_md = f"""# 🎬 {title}

**비디오 ID**: {video_id}
**URL**: {url}
**길이**: {duration_str}
**날짜**: {datetime.now().strftime('%Y-%m-%d')}

---

## 📝 설명

{description}

---

## 🎯 주요 내용

### 핵심 개념
- (분석 필요)

### 기술 스택
- (분석 필요)

### 타임스탬프
- 0:00 - 시작
- (분석 필요)

---

## 💡 배운 점

(분석 필요)

---

## 🔗 관련 자료

[[youtube_playlist_index]]

---

**상태**: ⏳ 분석 대기
**담당**: JARVIS 학습 시스템
"""

        filename = f"youtube-{i:02d}-{title.replace(' ', '-')[:30].lower()}.md"
        filepath = output_dir / filename
        filepath.write_text(video_md, encoding='utf-8')
        print(f"✅ 생성: {filepath.name}")

    print(f"\n✅ 분석 완료! {len(videos)}개 파일 생성됨\n")
    return output_dir

def main():
    """메인 함수"""

    playlist_url = "https://www.youtube.com/watch?v=HL0J-KN9gd0&list=PLFZNgUMeL3yt9LoS6CRA3epZFNvTMNxlO"
    output_dir = r"C:\Users\Desktop\Claude\Projects\kms\youtube_analysis"

    print("=" * 60)
    print("🎬 YouTube 재생목록 분석기")
    print("=" * 60)

    # 재생목록 정보 수집
    videos = get_playlist_info(playlist_url)

    if not videos:
        print("❌ 재생목록을 가져올 수 없습니다")
        sys.exit(1)

    print(f"✅ {len(videos)}개 영상 발견!\n")

    # 분석 결과 저장
    output_path = save_analysis(videos, output_dir)

    print(f"📂 저장 경로: {output_path}")
    print("\n🎉 분석 완료!")

if __name__ == "__main__":
    main()
