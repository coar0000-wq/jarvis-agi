#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🤖 JARVIS 노드 자동 연결 스크립트 (자동 경로)
모든 고립 노드를 JARVIS 중심으로 일괄 연결
"""

import os
import sys
from pathlib import Path
from datetime import datetime

# ============================================================================
# 📊 노드 분류 매핑
# ============================================================================

NODE_CLASSIFICATION = {
    "의료 전문가": [
        "healthcare", "medical", "clinical", "biomedical",
        "diagnosis", "treatment", "patient", "disease",
        "health", "hospital", "drug", "medication", "health"
    ],
    "기술 전문가": [
        "ai", "ml", "deep learning", "neural", "algorithm",
        "software", "architecture", "system", "performance",
        "optimization", "cloud", "devops", "database",
        "agent", "skill", "implementation", "code",
        "api", "framework", "library", "tool", "learning"
    ],
    "과학 전문가": [
        "research", "paper", "arxiv", "science", "physics",
        "biology", "chemistry", "quantum", "theory",
        "experiment", "model", "data", "analysis"
    ],
    "철학 전문가": [
        "ethics", "privacy", "bias", "fairness", "transparency",
        "responsibility", "trust", "security", "preserve",
        "federated", "moral", "philosophy", "principle"
    ],
    "음악 전문가": [
        "music", "audio", "sound", "synthesis", "composition",
        "instrument", "melody", "harmony", "song"
    ],
    "비즈니스 전문가": [
        "business", "market", "strategy", "revenue", "growth",
        "competition", "intelligence", "analytics", "sales"
    ],
    "경제 전문가": [
        "economic", "finance", "investment", "market", "exchange",
        "indicator", "trends", "analysis", "price"
    ],
    "교육 전문가": [
        "learning", "education", "training", "skill", "course",
        "assessment", "development", "knowledge"
    ],
    "예술 전문가": [
        "design", "art", "creative", "visual", "aesthetic",
        "color", "ui", "ux", "graphic"
    ]
}

# ============================================================================
# 🎯 함수들
# ============================================================================

def classify_node(filename):
    """파일명으로 노드 분류"""
    filename_lower = filename.lower()

    for expert, keywords in NODE_CLASSIFICATION.items():
        for keyword in keywords:
            if keyword in filename_lower:
                return expert

    return "기술 전문가"

def add_frontmatter(filepath, expert):
    """파일에 YAML 프론트매터 추가"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # 기존 프론트매터 제거
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                content = parts[2].lstrip('\n')

        # 새 프론트매터 추가
        frontmatter = f"""---
type: [[JARVIS]]
connected_to: [[JARVIS]], [[{expert}]]
domain: [[{expert.split('(')[0].strip()}]]
links_added: true
updated: {datetime.now().strftime('%Y-%m-%d')}
---

"""

        new_content = frontmatter + content

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)

        return True
    except Exception as e:
        print(f"❌ {filepath}: {e}")
        return False

def add_backlinks(filepath, expert):
    """파일 끝에 백링크 섹션 추가"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # 기존 백링크 섹션 확인
        if "## 🔗 JARVIS 네트워크 노드" in content:
            return True

        # 새 백링크 섹션 추가
        backlinks = f"""

---

## 🔗 JARVIS 네트워크 노드

### 상위 연결
- [[JARVIS]] - 중심 시스템
- [[{expert}]] - 담당 전문가

### 관련 노드
(자동으로 채워집니다)

---

**이 노드는 JARVIS 중심 그래프의 일부입니다.**
"""

        new_content = content + backlinks

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)

        return True
    except Exception as e:
        print(f"❌ {filepath}: {e}")
        return False

def process_vault(vault_path):
    """Obsidian vault의 모든 마크다운 파일 처리"""
    vault_path = Path(vault_path)

    if not vault_path.exists():
        print(f"❌ 경로를 찾을 수 없습니다: {vault_path}")
        return 0, {}

    files = list(vault_path.rglob("*.md"))

    if not files:
        print(f"⚠️  마크다운 파일을 찾을 수 없습니다: {vault_path}")
        return 0, {}

    print(f"📂 발견된 파일: {len(files)}개\n")
    print("🔄 처리 중...\n")

    success_count = 0
    expert_counts = {}

    for i, md_file in enumerate(files, 1):
        filename = md_file.name

        # 기본 파일 제외
        if filename in ["README.md", "MEMORY.md", "connect_nodes.py", "connect_nodes_auto.py"]:
            continue

        # 분류
        expert = classify_node(filename)
        expert_counts[expert] = expert_counts.get(expert, 0) + 1

        # 연결
        if add_frontmatter(str(md_file), expert):
            if add_backlinks(str(md_file), expert):
                status = "✅"
                success_count += 1
            else:
                status = "⚠️ "
        else:
            status = "❌"

        print(f"{status} [{i:3d}] {filename[:50]:<50} → {expert}")

    return success_count, expert_counts

def print_summary(success_count, expert_counts):
    """최종 요약 출력"""
    print("\n" + "="*70)
    print("✅ JARVIS 노드 연결 완료!")
    print("="*70)

    total = sum(expert_counts.values())
    print(f"\n📊 통계:")
    print(f"  총 처리: {success_count}개 파일")
    print(f"  성공: {success_count}개")

    print(f"\n📈 전문가별 분류:")
    for expert, count in sorted(expert_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {expert:<15} : {count:3d}개")

    print(f"\n🎯 다음 단계:")
    print(f"  1. Obsidian을 새로고침하세요 (Cmd/Ctrl + Shift + R)")
    print(f"  2. Graph View를 열어서 확인하세요")
    print(f"  3. JARVIS가 중심에 있고 모든 노드가 연결되었는지 확인")

    print(f"\n✨ 모든 노드가 JARVIS와 연결되었습니다!")
    print("="*70 + "\n")

# ============================================================================
# 🚀 실행
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("🤖 JARVIS 노드 자동 연결 스크립트 (자동 경로)")
    print("="*70 + "\n")

    # 자동 경로 설정
    vault_path = Path("C:/Users/Desktop/Obsidian").expanduser()

    print(f"📂 Obsidian Vault: {vault_path}")
    print(f"   (자동 감지됨)\n")

    if not vault_path.exists():
        print(f"❌ 경로를 찾을 수 없습니다: {vault_path}")
        print(f"\n다른 경로를 시도해봅시다...")

        alt_paths = [
            Path.home() / "Obsidian",
            Path.home() / "Documents" / "Obsidian",
            Path("C:/Users/Desktop/Obsidian"),
        ]

        for alt in alt_paths:
            if alt.exists():
                vault_path = alt
                print(f"✅ 발견됨: {vault_path}\n")
                break

    # 처리 시작
    print(f"🔄 처리 중: {vault_path}\n")
    success_count, expert_counts = process_vault(str(vault_path))

    # 결과 출력
    print_summary(success_count, expert_counts)
