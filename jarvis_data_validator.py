#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🔐 JARVIS 데이터 검증 시스템
Phase A에서 수집한 자료의 신뢰도 검증 및 품질 필터링
"""

import json
from datetime import datetime
from pathlib import Path

# 신뢰할 수 있는 출처
TRUSTED_SOURCES = {
    "Nature": 0.99,
    "Science": 0.99,
    "MIT News": 0.98,
    "TechCrunch": 0.95,
    "arXiv": 0.95,
    "IEEE": 0.97,
    "Medical News Today": 0.94,
    "The Verge": 0.92,
    "Reuters": 0.96,
    "BBC": 0.95
}

class JARVISDataValidator:
    """JARVIS 데이터 검증 시스템"""

    def __init__(self):
        self.base_path = Path(r"C:\Users\Desktop\Claude\Projects\kms")
        self.validator_dir = self.base_path / "validation_results"
        self.validator_dir.mkdir(exist_ok=True)

        self.today = datetime.now().strftime("%Y-%m-%d")
        self.log_file = self.validator_dir / f"validation_log_{self.today}.json"

    def calculate_source_credibility(self, source: str) -> float:
        """출처 신뢰도 계산"""
        if source in TRUSTED_SOURCES:
            return TRUSTED_SOURCES[source]
        else:
            return 0.6  # 기본값

    def calculate_content_credibility(self, content: str) -> float:
        """내용 신뢰도 계산"""
        # 간단한 메트릭
        length = len(content.split())

        if length > 500:
            return 0.85
        elif length > 200:
            return 0.75
        else:
            return 0.5

    def calculate_freshness(self, publish_date: str) -> float:
        """최신도 계산"""
        # 모든 자료를 최신으로 간주
        return 0.9

    def calculate_citation_score(self, citations: int = 0) -> float:
        """인용도 계산"""
        if citations > 100:
            return 1.0
        elif citations > 50:
            return 0.9
        elif citations > 10:
            return 0.7
        else:
            return 0.5

    def calculate_trust_score(self, data_item: dict) -> float:
        """통합 신뢰도 점수 계산"""

        source_score = self.calculate_source_credibility(
            data_item.get('source', 'Unknown')
        )
        content_score = self.calculate_content_credibility(
            data_item.get('summary', '')
        )
        freshness_score = self.calculate_freshness(
            data_item.get('publish_date', '')
        )
        citation_score = self.calculate_citation_score(
            data_item.get('citations', 0)
        )

        # 가중치 평균
        trust_score = (
            source_score * 0.3 +
            content_score * 0.3 +
            freshness_score * 0.2 +
            citation_score * 0.2
        )

        return trust_score

    def is_duplicate(self, data_item: dict, existing_items: list) -> bool:
        """중복 검사"""
        title = data_item.get('title', '')

        for item in existing_items:
            if item.get('title', '').lower() == title.lower():
                return True

        return False

    def passes_quality_check(self, data_item: dict) -> bool:
        """품질 검사"""

        # 최소 길이 체크
        title = data_item.get('title', '')
        summary = data_item.get('summary', '')

        if len(title) < 10:
            return False
        if len(summary) < 20:
            return False

        # 스팸 체크
        spam_keywords = ['buy now', 'click here', 'limited offer']
        content = (title + ' ' + summary).lower()

        for keyword in spam_keywords:
            if keyword in content:
                return False

        return True

    def auto_classify(self, data_item: dict) -> str:
        """자동 분류"""

        title = data_item.get('title', '').lower()

        if 'ai' in title or 'machine learning' in title:
            return 'AI/ML'
        elif 'medical' in title or 'health' in title:
            return 'Medical'
        elif 'music' in title or 'audio' in title:
            return 'Music'
        elif 'business' in title or 'market' in title:
            return 'Business'
        else:
            return 'Technology'

    def validate_all_data(self, data_list: list) -> dict:
        """모든 데이터 검증"""

        print("\n" + "="*60)
        print("🔐 JARVIS 데이터 검증 시스템")
        print("="*60 + "\n")

        valid_data = []
        invalid_data = []
        statistics = {
            "total_input": len(data_list),
            "trust_score_passed": 0,
            "duplicate_removed": 0,
            "quality_passed": 0,
            "final_valid": 0
        }

        print(f"📊 입력 데이터: {len(data_list)}개\n")

        # 신뢰도 검사
        print("📊 Step 1: 신뢰도 점수 계산")
        temp_data = []
        for item in data_list:
            trust_score = self.calculate_trust_score(item)
            item['trust_score'] = trust_score

            if trust_score >= 0.7:  # 70점 이상
                temp_data.append(item)
                statistics["trust_score_passed"] += 1
            else:
                invalid_data.append(item)

        print(f"✅ 통과: {statistics['trust_score_passed']}개\n")

        # 중복 제거
        print("📊 Step 2: 중복 제거")
        for item in temp_data:
            if not self.is_duplicate(item, valid_data):
                valid_data.append(item)
            else:
                statistics["duplicate_removed"] += 1
                invalid_data.append(item)

        print(f"✅ 제거: {statistics['duplicate_removed']}개\n")

        # 품질 필터링
        print("📊 Step 3: 품질 필터링")
        final_data = []
        for item in valid_data:
            if self.passes_quality_check(item):
                # 자동 분류
                item['category'] = self.auto_classify(item)
                final_data.append(item)
                statistics["quality_passed"] += 1
            else:
                invalid_data.append(item)

        statistics["final_valid"] = len(final_data)

        print(f"✅ 통과: {statistics['quality_passed']}개\n")
        print(f"📊 최종 유효: {statistics['final_valid']}개\n")

        # 결과 저장
        self.save_results(final_data, statistics)

        return {
            "valid_data": final_data,
            "invalid_data": invalid_data,
            "statistics": statistics
        }

    def save_results(self, valid_data: list, statistics: dict):
        """결과 저장"""

        results = {
            "timestamp": datetime.now().isoformat(),
            "date": self.today,
            "statistics": statistics,
            "valid_count": len(valid_data),
            "valid_data": valid_data
        }

        try:
            with open(self.log_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)

            print(f"✅ 결과 저장: {self.log_file}\n")

        except Exception as e:
            print(f"❌ 저장 오류: {e}\n")

    def create_obsidian_report(self, results: dict):
        """Obsidian 리포트 생성"""

        report_path = self.validator_dir / f"validation_report_{self.today}.md"
        stats = results['statistics']

        content = f"""# 🔐 데이터 검증 보고서

**날짜**: {self.today}
**상태**: ✅ 검증 완료

---

## 📊 **검증 통계**

| 단계 | 입력 | 출력 | 통과율 |
|------|------|------|--------|
| **입력** | {stats['total_input']}개 | - | - |
| **신뢰도** | {stats['total_input']}개 | {stats['trust_score_passed']}개 | {(stats['trust_score_passed']/stats['total_input']*100):.1f}% |
| **중복 제거** | {stats['trust_score_passed']}개 | {stats['trust_score_passed']-stats['duplicate_removed']}개 | {((stats['trust_score_passed']-stats['duplicate_removed'])/stats['trust_score_passed']*100):.1f}% |
| **품질 필터** | {stats['trust_score_passed']-stats['duplicate_removed']}개 | {stats['final_valid']}개 | {(stats['quality_passed']/(stats['trust_score_passed']-stats['duplicate_removed'])*100):.1f}% |

---

## ✅ **최종 결과**

- **입력**: {stats['total_input']}개
- **신뢰도 통과**: {stats['trust_score_passed']}개 ({(stats['trust_score_passed']/stats['total_input']*100):.1f}%)
- **중복 제거**: {stats['duplicate_removed']}개
- **품질 통과**: {stats['quality_passed']}개
- **최종 유효**: {stats['final_valid']}개

---

## 🎯 **다음 단계**

1. Obsidian에 유효 자료 저장
2. Phase C 자동 요약 시스템 개발
3. 메모리 업데이트

---

**상태**: ✅ 검증 완료
"""

        report_path.write_text(content, encoding='utf-8')
        print(f"✅ 리포트 생성: {report_path}")

    def run(self, data_list: list = None):
        """실행"""

        # 테스트 데이터
        if data_list is None:
            data_list = [
                {
                    "source": "TechCrunch",
                    "title": "AI 최신 기술 발전",
                    "summary": "이 기사는 인공지능의 최신 발전 방향을 설명합니다.",
                    "publish_date": "2026-08-04",
                    "citations": 50
                },
                {
                    "source": "Unknown",
                    "title": "Buy Now!",
                    "summary": "Limited offer",
                    "publish_date": "2026-08-04",
                    "citations": 0
                },
                {
                    "source": "Nature",
                    "title": "의료 AI 혁신",
                    "summary": "의료 분야에서 인공지능을 활용한 새로운 진단 기술이 개발되었습니다.",
                    "publish_date": "2026-08-03",
                    "citations": 100
                }
            ]

        print("\n🤖 JARVIS 데이터 검증 시작...\n")

        # 검증 실행
        results = self.validate_all_data(data_list)

        # 리포트 생성
        self.create_obsidian_report(results)

        print("\n✨ 데이터 검증 완료!")

        return results

def main():
    """메인 함수"""

    validator = JARVISDataValidator()
    results = validator.run()

    print(f"\n📊 결과 요약:")
    print(f"  - 입력: {results['statistics']['total_input']}개")
    print(f"  - 유효: {results['statistics']['final_valid']}개")
    print(f"  - 통과율: {(results['statistics']['final_valid']/results['statistics']['total_input']*100):.1f}%")

if __name__ == "__main__":
    main()
