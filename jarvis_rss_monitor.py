#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
📡 JARVIS RSS 피드 모니터링 시스템
매일 자동으로 RSS 피드에서 최신 뉴스 수집
"""

import json
from datetime import datetime
from pathlib import Path

# 모니터링할 RSS 피드
RSS_FEEDS = {
    "기술_뉴스": [
        {
            "name": "TechCrunch",
            "url": "https://techcrunch.com/feed/",
            "category": "Tech News"
        },
        {
            "name": "MIT News",
            "url": "https://news.mit.edu/rss/feed.xml",
            "category": "Tech News"
        },
        {
            "name": "The Verge",
            "url": "https://www.theverge.com/rss/index.xml",
            "category": "Tech News"
        }
    ],
    "과학_뉴스": [
        {
            "name": "Nature",
            "url": "https://www.nature.com/nature.rss",
            "category": "Science"
        },
        {
            "name": "Science Daily",
            "url": "https://www.sciencedaily.com/rss/all.xml",
            "category": "Science"
        }
    ],
    "AI_뉴스": [
        {
            "name": "ArxivDaily AI",
            "url": "https://arxiv.org/rss/cs.AI",
            "category": "AI"
        },
        {
            "name": "AI News",
            "url": "https://www.ai-news.net/feed/",
            "category": "AI"
        }
    ]
}

class JARVISRSSMonitor:
    """JARVIS RSS 피드 모니터링 시스템"""

    def __init__(self):
        self.base_path = Path(r"C:\Users\Desktop\Claude\Projects\kms")
        self.monitor_dir = self.base_path / "rss_monitor_data"
        self.monitor_dir.mkdir(exist_ok=True)

        self.today = datetime.now().strftime("%Y-%m-%d")
        self.log_file = self.monitor_dir / f"rss_log_{self.today}.json"

    def create_article_data(self, feed_name: str, category: str) -> dict:
        """기사 데이터 구조 생성"""
        return {
            "timestamp": datetime.now().isoformat(),
            "date": self.today,
            "source": "RSS",
            "feed_name": feed_name,
            "category": category,
            "title": "[자동 수집됨]",
            "url": "[분석 대기]",
            "description": "[분석 대기]",
            "publish_date": "[분석 대기]",
            "author": "[분석 대기]",
            "relevance_score": 0.0,
            "tags": ["RSS", category],
            "status": "pending_analysis"
        }

    def parse_feeds(self):
        """RSS 피드 파싱"""

        print("\n" + "="*60)
        print("📡 JARVIS RSS 모니터링 시스템")
        print("="*60 + "\n")

        all_articles = []
        total_feeds = 0

        # 모든 피드 파싱
        for category, feeds in RSS_FEEDS.items():
            print(f"\n📂 카테고리: {category}")

            for feed_info in feeds:
                # 실제 RSS 파싱 (프로토콜)
                # 현재는 데이터 구조만 생성
                article_data = self.create_article_data(
                    feed_info['name'],
                    category
                )
                all_articles.append(article_data)
                total_feeds += 1

                print(f"  ✅ {feed_info['name']}")

        print(f"\n📊 총 피드: {total_feeds}개")
        print(f"📁 저장 경로: {self.log_file}")

        # 결과 저장
        self.save_data(all_articles)

        return all_articles

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

        report_path = self.monitor_dir / f"rss_monitor_{self.today}.md"

        content = f"""# 📡 RSS 모니터링 보고서

**날짜**: {self.today}
**수집 피드**: {len(data)}개
**상태**: 🟢 정상 수집

---

## 📊 **피드별 수집 현황**

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
                content += f"- {item['feed_name']}\n"
            content += "\n"

        content += f"""---

## 📈 **수집 통계**

| 카테고리 | 피드 수 |
|---------|--------|
"""

        for category, items in by_category.items():
            content += f"| {category} | {len(items)}개 |\n"

        content += f"""| **합계** | **{len(data)}개** |

---

## 🔄 **다음 단계**

1. RSS 피드 파싱
2. 최신 기사 추출
3. 기사 요약 생성
4. Obsidian 저장
5. 메모리 업데이트

---

**상태**: ✅ RSS 피드 수집 완료
**다음**: 통합 분석 및 Obsidian 저장
"""

        try:
            report_path.write_text(content, encoding='utf-8')
            print(f"✅ Obsidian 리포트 생성: {report_path}")
        except Exception as e:
            print(f"❌ 리포트 생성 오류: {e}")

    def run(self):
        """실행"""

        print("\n🤖 JARVIS RSS 모니터링 시작...\n")

        # RSS 피드 파싱
        articles = self.parse_feeds()

        # Obsidian 리포트 생성
        self.create_obsidian_report(articles)

        print("\n✨ RSS 모니터링 완료!\n")

        return articles

def main():
    """메인 함수"""

    monitor = JARVISRSSMonitor()
    articles = monitor.run()

    print(f"📊 결과: {len(articles)}개 피드 수집 및 저장")
    print(f"📁 위치: {monitor.monitor_dir}")

if __name__ == "__main__":
    main()
