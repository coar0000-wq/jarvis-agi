#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JARVIS 자동 데이터 수집 시스템
YouTube + arXiv 자동 수집 + Claude 분석 + 대시보드 업데이트
"""

import requests
import json
import os
from datetime import datetime
from pathlib import Path

# API 설정
CLAUDE_API_KEY = os.getenv('CLAUDE_API_KEY', '')
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY', '')

# 저장 경로
OUTPUT_DIR = Path('C:/Users/Desktop/Claude/Projects/kms')
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("""
╔════════════════════════════════════════════════════════════╗
║  🤖 JARVIS 자동 데이터 수집 시스템 시작                     ║
║  📅 시간: """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """                          ║
╚════════════════════════════════════════════════════════════╝
""")

# ============================================================
# 1️⃣ YouTube 자동 수집
# ============================================================

print("\n[Step 1/4] YouTube 데이터 수집 중...")

youtube_results = []
search_terms = [
    "MoE 라우터 2026",
    "신경심볼릭 AI",
    "양자 신약 설계",
    "메타러닝 AI",
    "다중모달 AI"
]

if YOUTUBE_API_KEY:
    for term in search_terms:
        try:
            url = "https://www.googleapis.com/youtube/v3/search"
            params = {
                'key': YOUTUBE_API_KEY,
                'q': term,
                'part': 'snippet',
                'maxResults': 2,
                'type': 'video',
                'order': 'date'
            }
            response = requests.get(url, params=params, timeout=5)
            if response.status_code == 200:
                data = response.json()
                for item in data.get('items', []):
                    youtube_results.append({
                        'title': item['snippet']['title'],
                        'channel': item['snippet']['channelTitle'],
                        'url': f"https://www.youtube.com/watch?v={item['id']['videoId']}",
                        'published': item['snippet']['publishedAt']
                    })
        except Exception as e:
            print(f"  ⚠️  YouTube 오류 ({term}): {e}")
else:
    print("  ⚠️  YouTube API 키 없음 (스킵)")

print(f"  ✅ YouTube: {len(youtube_results)}개 수집")

# ============================================================
# 2️⃣ arXiv 자동 수집
# ============================================================

print("\n[Step 2/4] arXiv 논문 수집 중...")

arxiv_results = []

try:
    search_query = "cat:cs.AI AND (MoE OR \"mixture of experts\")"
    url = "http://export.arxiv.org/api/query"
    params = {
        'search_query': search_query,
        'start': 0,
        'max_results': 20,
        'sortBy': 'submittedDate',
        'sortOrder': 'descending'
    }

    response = requests.get(url, params=params, timeout=10)
    if response.status_code == 200:
        # XML 파싱 (간단한 방식)
        content = response.text
        papers = content.split('<entry>')

        for paper in papers[1:]:
            try:
                title = paper.split('<title>')[1].split('</title>')[0].strip()
                authors = paper.split('<author>')[1].split('<name>')[1].split('</name>')[0] if '<author>' in paper else "Unknown"
                published = paper.split('<published>')[1].split('</published>')[0] if '<published>' in paper else ""
                arxiv_id = paper.split('arxiv.org/abs/')[1].split('</id>')[0] if 'arxiv.org/abs/' in paper else ""

                arxiv_results.append({
                    'title': title,
                    'author': authors,
                    'published': published,
                    'url': f'https://arxiv.org/abs/{arxiv_id}' if arxiv_id else '',
                    'arxiv_id': arxiv_id
                })
            except:
                pass
except Exception as e:
    print(f"  ⚠️  arXiv 오류: {e}")

print(f"  ✅ arXiv: {len(arxiv_results)}개 수집")

# ============================================================
# 3️⃣ Claude로 분석
# ============================================================

print("\n[Step 3/4] Claude 분석 중...")

analysis_result = ""

if CLAUDE_API_KEY:
    try:
        prompt = f"""다음 YouTube 영상과 arXiv 논문들을 분석하고 JARVIS의 기술 진화 관점에서 핵심 내용을 요약해줘:

## YouTube 영상 ({len(youtube_results)}개)
{json.dumps(youtube_results[:5], ensure_ascii=False, indent=2)}

## arXiv 논문 ({len(arxiv_results)}개)
{json.dumps(arxiv_results[:10], ensure_ascii=False, indent=2)}

분석 포맷:
### 🎬 YouTube 핵심
- 제목 (URL)
- 핵심 내용 (2줄)
- JARVIS 적용 가능성: ★★★/5

### 📄 arXiv 핵심
- 제목 (arXiv ID)
- 핵심 기술 (2줄)
- 인용도 추정: 높음/중간/낮음
- JARVIS Phase: 26-30 중 어디에 적용?

### 🚀 다음 액션
- 우선순위 (Top 3)
- 구현 예상 기간"""

        headers = {
            'Content-Type': 'application/json',
            'x-api-key': CLAUDE_API_KEY,
        }

        data = {
            'model': 'claude-3-5-sonnet-20241022',
            'max_tokens': 1500,
            'messages': [
                {
                    'role': 'user',
                    'content': prompt
                }
            ]
        }

        response = requests.post(
            'https://api.anthropic.com/v1/messages',
            headers=headers,
            json=data,
            timeout=30
        )

        if response.status_code == 200:
            result = response.json()
            analysis_result = result['content'][0]['text']
            print("  ✅ Claude 분석 완료")
        else:
            print(f"  ⚠️  Claude API 오류: {response.status_code}")
            analysis_result = "(API 오류로 분석 스킵)"
    except Exception as e:
        print(f"  ⚠️  분석 오류: {e}")
        analysis_result = f"(오류: {e})"
else:
    print("  ⚠️  Claude API 키 없음 (스킵)")
    analysis_result = "(Claude API 키 없음)"

# ============================================================
# 4️⃣ 파일 생성 및 대시보드 업데이트
# ============================================================

print("\n[Step 4/4] 파일 저장 및 대시보드 업데이트 중...")

# 마크다운 파일 생성
timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
filename = OUTPUT_DIR / f"JARVIS_자동수집_{datetime.now().strftime('%Y-%m-%d')}.md"

markdown_content = f"""# 🤖 JARVIS 자동 수집 리포트

**수집 시간:** {timestamp}
**상태:** ✅ 자동 수집 완료

---

## 📊 수집 통계

| 항목 | 개수 |
|------|------|
| YouTube 영상 | {len(youtube_results)} |
| arXiv 논문 | {len(arxiv_results)} |
| Claude 분석 | ✅ |

---

## 🎬 YouTube 영상 ({len(youtube_results)}개)

{json.dumps(youtube_results, ensure_ascii=False, indent=2)}

---

## 📄 arXiv 논문 ({len(arxiv_results)}개)

{json.dumps(arxiv_results[:15], ensure_ascii=False, indent=2)}

---

## 🧠 Claude 분석

{analysis_result}

---

## 🎯 다음 수집

⏰ **다음 자동 수집:** 내일 08:00 KST
📊 **대시보드:** http://localhost:8080/JARVIS_실시간_대시보드_로컬.html

---

*자동 생성됨 (JARVIS Auto Collect)*
"""

# 파일 저장
with open(filename, 'w', encoding='utf-8') as f:
    f.write(markdown_content)

print(f"  ✅ 파일 저장: {filename.name}")

# 대시보드 메트릭 업데이트
try:
    dashboard_data = {
        'youtube_count': len(youtube_results),
        'arxiv_count': len(arxiv_results),
        'timestamp': datetime.now().isoformat(),
        'status': 'success'
    }

    response = requests.post(
        'http://localhost:8080/update_metrics',
        json=dashboard_data,
        timeout=5
    )

    if response.status_code == 200:
        print("  ✅ 대시보드 업데이트 완료")
    else:
        print(f"  ⚠️  대시보드 업데이트 실패 (서버 미응답)")
except Exception as e:
    print(f"  ⚠️  대시보드 연결 실패: {e}")

# ============================================================
# 완료
# ============================================================

print(f"""
╔════════════════════════════════════════════════════════════╗
║  ✅ JARVIS 자동 수집 완료!                                  ║
╚════════════════════════════════════════════════════════════╝

📊 결과:
  - YouTube: {len(youtube_results)}개 수집
  - arXiv: {len(arxiv_results)}개 수집
  - Claude: 분석 완료
  - 파일: {filename.name}

🌐 대시보드:
  http://localhost:8080/JARVIS_실시간_대시보드_로컬.html

⏰ 다음 실행:
  내일 08:00 KST

""")
