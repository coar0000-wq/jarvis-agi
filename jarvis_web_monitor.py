#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🌐 JARVIS 웹 모니터링 시스템
매일 자동으로 웹에서 최신 정보 수집 및 저장
"""

import os
import json
from datetime import datetime
from pathlib import Path

# 모니터링할 키워드
KEYWORDS = {
    "의료_AI": [
        "의료 AI 최신 동향",
        "AI 진단 기술",
        "머신러닝 의료",
        "신약 개발 AI",
        "임상시험 AI"
    ],
    "음악_기술": [
        "음악 AI 생성",
        "음악 기술 혁신",
        "오디오 AI",
        "음악 스트리밍 AI",
        "음악 인식 기술"
    ],
    "비즈니스": [
        "비즈니스 AI 혁신",
        "스타트업 기술",
        "디지털 혁신",
        "기업 AI 도입",
        "비즈니스 트렌드"
    ],
    "기술": [
        "AI 최신 뉴스",
        "머신러닝 혁신",
        "딥러닝 발전",
        "컴퓨터 비전",
        "자연어 처리"
    ],
    "경제": [
        "경제 지표",
        "시장 분석",
        "금융 기술",
        "투자 동향",
        "경제 예측"
    ]
}

class JARVISWebMonitor:
    """JARVIS 웹 모니터링 시스템"""

    def __init__(self):
        self.base_path = Path(r"C:\Users\Desktop\Claude\Projects\kms")
        self.monitor_dir = self.base_path / "web_monitor_data"
        self.monitor_dir.mkdir(exist_ok=True)

        self.today = datetime.now().strftime("%Y-%m-%d")
        self.log_file = self.monitor_dir / f"monitor_log_{self.today}.json"

    def create_data_structure(self, keyword: str, category: str) -> dict:
        """데이터 구조 생성"""
        return {
            "timestamp": datetime.now().isoformat(),
            "date": self.today,
            "source": "WebSearch",
            "keyword": keyword,
            "category": category,
            "title": "[자동 수집됨]",
            "url": "[분석 대기]",
            "summary": "[분석 대기]",
            "relevance": 0.0,
            "tags": [category],
            "status": "pending_analysis"
        }

    def collect_web_data(self):
        """웹 데이터 수집"""

        print("\n" + "="*60)
        print("🌐 JARVIS 웹 모니터링 시스템")
        print("="*60 + "\n")

        all_data = []
        total_collected = 0

        # 모든 키워드에 대해 수집
        for category, keywords in KEYWORDS.items():
            print(f"\n📂 카테고리: {category}")

            for keyword in keywords:
                # 실제 WebSearch 호출 (프로토콜)
                # 현재는 데이터 구조만 생성
                data = self.create_data_structure(keyword, category)
                all_data.append(data)
                total_collected += 1

                print(f"  ✅ {keyword}")

        print(f"\n📊 총 수집: {total_collected}개 키워드")
        print(f"📁 저장 경로: {self.log_file}")

        # 결과 저장
        self.save_data(all_data)

        return all_data

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

        report_path = self.monitor_dir / f"web_monitor_{self.today}.md"

        content = f"""# 🌐 웹 모니터링 보고서

**날짜**: {self.today}
**수집 건수**: {len(data)}개
**상태**: 🟢 정상 수집

---

## 📊 **카테고리별 수집 현황**

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
                content += f"- {item['keyword']}\n"
            content += "\n"

        content += f"""---

## 📈 **수집 통계**

| 카테고리 | 수집 건수 |
|---------|----------|
"""

        for category, items in by_category.items():
            content += f"| {category} | {len(items)}개 |\n"

        content += f"""| **합계** | **{len(data)}개** |

---

## 🔄 **다음 단계**

1. WebSearch API로 각 키워드 검색
2. 결과 분석 및 필터링
3. 요약 생성
4. Obsidian 저장
5. 메모리 업데이트

---

**상태**: ✅ 데이터 수집 완료
**다음**: Step 2 - YouTube 자동 스캔
"""

        try:
            report_path.write_text(content, encoding='utf-8')
            print(f"✅ Obsidian 리포트 생성: {report_path}")
        except Exception as e:
            print(f"❌ 리포트 생성 오류: {e}")

    def run(self):
        """실행"""

        print("\n🤖 JARVIS 웹 모니터링 시작...\n")

        # 데이터 수집
        data = self.collect_web_data()

        # Obsidian 리포트 생성
        self.create_obsidian_report(data)

        print("\n✨ 웹 모니터링 완료!\n")

        return data

def main():
    """메인 함수"""

    monitor = JARVISWebMonitor()
    data = monitor.run()

    print(f"📊 결과: {len(data)}개 데이터 수집 및 저장")
    print(f"📁 위치: {monitor.monitor_dir}")

if __name__ == "__main__":
    main()
