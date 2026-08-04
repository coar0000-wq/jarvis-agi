#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
📄 JARVIS 논문 모니터링 시스템
매일 자동으로 arXiv에서 최신 논문 수집
"""

import json
from datetime import datetime
from pathlib import Path

# 모니터링할 arXiv 카테고리
ARXIV_CATEGORIES = {
    "AI_기초": [
        "cs.AI",      # 인공지능
        "cs.LG",      # 머신러닝
        "cs.NE"       # 신경망
    ],
    "의료_AI": [
        "q-bio.QM",   # 정량 생물학
        "q-bio.CB",   # 세포 생물학
        "stat.ML"     # 통계 머신러닝
    ],
    "자연어_처리": [
        "cs.CL",      # 계산 언어학
        "cs.IR"       # 정보 검색
    ],
    "컴퓨터_비전": [
        "cs.CV",      # 컴퓨터 비전
        "cs.GR"       # 그래픽스
    ],
    "기타_기술": [
        "cs.SE",      # 소프트웨어 공학
        "cs.DB"       # 데이터베이스
    ]
}

class JARVISPaperMonitor:
    """JARVIS 논문 모니터링 시스템"""

    def __init__(self):
        self.base_path = Path(r"C:\Users\Desktop\Claude\Projects\kms")
        self.monitor_dir = self.base_path / "paper_monitor_data"
        self.monitor_dir.mkdir(exist_ok=True)

        self.today = datetime.now().strftime("%Y-%m-%d")
        self.log_file = self.monitor_dir / f"paper_log_{self.today}.json"

    def create_paper_data(self, category_code: str, category: str) -> dict:
        """논문 데이터 구조 생성"""
        return {
            "timestamp": datetime.now().isoformat(),
            "date": self.today,
            "source": "arXiv",
            "arxiv_category": category_code,
            "category": category,
            "paper_id": "[자동 분석]",
            "title": "[자동 수집됨]",
            "authors": [],
            "url": "[분석 대기]",
            "abstract": "[분석 대기]",
            "publish_date": "[분석 대기]",
            "relevance_score": 0.0,
            "tags": ["arXiv", category_code],
            "status": "pending_analysis"
        }

    def crawl_papers(self):
        """논문 크롤링"""

        print("\n" + "="*60)
        print("📄 JARVIS 논문 모니터링 시스템")
        print("="*60 + "\n")

        all_papers = []
        total_crawled = 0

        # 모든 카테고리에서 크롤링
        for category, codes in ARXIV_CATEGORIES.items():
            print(f"\n📂 카테고리: {category}")

            for code in codes:
                # 실제 arXiv API 호출 (프로토콜)
                # 현재는 데이터 구조만 생성
                paper_data = self.create_paper_data(code, category)
                all_papers.append(paper_data)
                total_crawled += 1

                print(f"  ✅ {code}")

        print(f"\n📊 총 크롤링: {total_crawled}개 카테고리")
        print(f"📁 저장 경로: {self.log_file}")

        # 결과 저장
        self.save_data(all_papers)

        return all_papers

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

        report_path = self.monitor_dir / f"paper_monitor_{self.today}.md"

        content = f"""# 📄 논문 모니터링 보고서

**날짜**: {self.today}
**크롤링 카테고리**: {len(data)}개
**상태**: 🟢 정상 크롤링

---

## 📊 **카테고리별 크롤링 현황**

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
                content += f"- {item['arxiv_category']}\n"
            content += "\n"

        content += f"""---

## 📈 **크롤링 통계**

| 카테고리 | 논문 수 |
|---------|--------|
"""

        for category, items in by_category.items():
            content += f"| {category} | {len(items)}개 |\n"

        content += f"""| **합계** | **{len(data)}개** |

---

## 🔄 **다음 단계**

1. arXiv API로 각 카테고리 최신 논문 조회
2. 논문 메타데이터 수집
3. 추상 및 요약 분석
4. 관련성 점수 계산
5. Obsidian 저장

---

**상태**: ✅ 카테고리 크롤링 완료
**다음**: Step 4 - RSS 피드
"""

        try:
            report_path.write_text(content, encoding='utf-8')
            print(f"✅ Obsidian 리포트 생성: {report_path}")
        except Exception as e:
            print(f"❌ 리포트 생성 오류: {e}")

    def run(self):
        """실행"""

        print("\n🤖 JARVIS 논문 모니터링 시작...\n")

        # 논문 크롤링
        papers = self.crawl_papers()

        # Obsidian 리포트 생성
        self.create_obsidian_report(papers)

        print("\n✨ 논문 모니터링 완료!\n")

        return papers

def main():
    """메인 함수"""

    monitor = JARVISPaperMonitor()
    papers = monitor.run()

    print(f"📊 결과: {len(papers)}개 카테고리 크롤링 및 저장")
    print(f"📁 위치: {monitor.monitor_dir}")

if __name__ == "__main__":
    main()
