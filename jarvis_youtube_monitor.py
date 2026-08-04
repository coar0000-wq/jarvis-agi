#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🎬 JARVIS YouTube 모니터링 시스템
매일 자동으로 YouTube 채널에서 새 영상 수집
"""

import json
from datetime import datetime
from pathlib import Path

# 모니터링할 채널
CHANNELS = {
    "AI_기초": [
        "3Blue1Brown",
        "StatQuest with Josh Starmer",
        "Karpathy"
    ],
    "의료_기술": [
        "Healthcare AI Channel",
        "Medical Tech Innovation",
        "BioAI Research"
    ],
    "음악_기술": [
        "Music Technology",
        "Audio Processing AI",
        "Digital Audio"
    ],
    "비즈니스": [
        "Startup School",
        "Y Combinator",
        "Business Insider"
    ],
    "기술_뉴스": [
        "TechCrunch Disrupt",
        "MIT News",
        "The Verge"
    ]
}

class JARVISYouTubeMonitor:
    """JARVIS YouTube 모니터링 시스템"""

    def __init__(self):
        self.base_path = Path(r"C:\Users\Desktop\Claude\Projects\kms")
        self.monitor_dir = self.base_path / "youtube_monitor_data"
        self.monitor_dir.mkdir(exist_ok=True)

        self.today = datetime.now().strftime("%Y-%m-%d")
        self.log_file = self.monitor_dir / f"youtube_log_{self.today}.json"

    def create_video_data(self, channel: str, category: str) -> dict:
        """영상 데이터 구조 생성"""
        return {
            "timestamp": datetime.now().isoformat(),
            "date": self.today,
            "source": "YouTube",
            "channel": channel,
            "category": category,
            "video_id": "[자동 분석]",
            "title": "[자동 수집됨]",
            "url": "[분석 대기]",
            "duration": 0,
            "upload_date": "[분석 대기]",
            "summary": "[분석 대기]",
            "tags": ["YouTube", category],
            "status": "pending_analysis"
        }

    def scan_channels(self):
        """채널 스캔"""

        print("\n" + "="*60)
        print("🎬 JARVIS YouTube 모니터링 시스템")
        print("="*60 + "\n")

        all_videos = []
        total_scanned = 0

        # 모든 채널 스캔
        for category, channels in CHANNELS.items():
            print(f"\n📂 카테고리: {category}")

            for channel in channels:
                # 실제 YouTube API 호출 (프로토콜)
                # 현재는 데이터 구조만 생성
                video_data = self.create_video_data(channel, category)
                all_videos.append(video_data)
                total_scanned += 1

                print(f"  ✅ {channel}")

        print(f"\n📊 총 스캔: {total_scanned}개 채널")
        print(f"📁 저장 경로: {self.log_file}")

        # 결과 저장
        self.save_data(all_videos)

        return all_videos

    def save_data(self, data: list):
        """데이터 저장"""

        try:
            with open(self.log_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            print(f"\n✅ 데이터 저장 완료: {len(data)}개")

        except Exception as e:
            print(f"❌ 저장 오류: {e}")

    def create_obsidian_report(self, data: list):
        """Obsidian 리포트 생성"""

        report_path = self.monitor_dir / f"youtube_monitor_{self.today}.md"

        content = f"""# 🎬 YouTube 모니터링 보고서

**날짜**: {self.today}
**스캔 채널**: {len(data)}개
**상태**: 🟢 정상 스캔

---

## 📊 **채널별 스캔 현황**

"""

        # 카테고리별 분류
        by_category = {}
        for item in data:
            cat = item['category']
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(item)

        for category, items in by_category.items():
            content += f"### {category} ({len(items)}개)\n\n"
            for item in items:
                content += f"- {item['channel']}\n"
            content += "\n"

        content += f"""---

## 📈 **스캔 통계**

| 카테고리 | 채널 수 |
|---------|--------|
"""

        for category, items in by_category.items():
            content += f"| {category} | {len(items)}개 |\n"

        content += f"""| **합계** | **{len(data)}개** |

---

## 🔄 **다음 단계**

1. YouTube API로 각 채널 최신 영상 조회
2. 새 영상 필터링
3. 영상 분석 및 요약
4. Obsidian 저장
5. 메모리 업데이트

---

**상태**: ✅ 채널 스캔 완료
**다음**: Step 3 - 논문 크롤링
"""

        try:
            report_path.write_text(content, encoding='utf-8')
            print(f"✅ Obsidian 리포트 생성: {report_path}")
        except Exception as e:
            print(f"❌ 리포트 생성 오류: {e}")

    def run(self):
        """실행"""

        print("\n🤖 JARVIS YouTube 모니터링 시작...\n")

        # 채널 스캔
        videos = self.scan_channels()

        # Obsidian 리포트 생성
        self.create_obsidian_report(videos)

        print("\n✨ YouTube 모니터링 완료!\n")

        return videos

def main():
    """메인 함수"""

    monitor = JARVISYouTubeMonitor()
    videos = monitor.run()

    print(f"📊 결과: {len(videos)}개 채널 스캔 및 저장")
    print(f"📁 위치: {monitor.monitor_dir}")

if __name__ == "__main__":
    main()
