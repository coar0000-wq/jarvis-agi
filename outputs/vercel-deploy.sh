#!/bin/bash

echo "🚀 JARVIS 통합 대시보드 - Vercel 자동 배포 시작!"
echo "=================================================="

# Step 1: 필요한 파일 확인
echo ""
echo "📍 Step 1: 배포 환경 확인..."

if ! command -v git &> /dev/null; then
    echo "❌ Git이 설치되어 있지 않습니다."
    echo "   https://git-scm.com/download/win 에서 다운로드 후 설치하세요."
    exit 1
fi

if ! command -v npm &> /dev/null; then
    echo "❌ Node.js/npm이 설치되어 있지 않습니다."
    echo "   https://nodejs.org/ 에서 LTS 버전 다운로드 후 설치하세요."
    exit 1
fi

echo "✅ Git 확인됨"
echo "✅ npm 확인됨"

# Step 2: 프로젝트 초기화
echo ""
echo "📍 Step 2: 프로젝트 초기화..."

cd /c/Users/Desktop/Claude/Projects/kms

# Git 초기화
if [ ! -d .git ]; then
    git init
    echo "✅ Git 저장소 생성됨"
else
    echo "✅ Git 저장소 이미 존재"
fi

# Step 3: Vercel CLI 설치
echo ""
echo "📍 Step 3: Vercel CLI 설치 중..."

npm install -g vercel

echo "✅ Vercel CLI 설치 완료"

# Step 4: GitHub에 푸시
echo ""
echo "📍 Step 4: GitHub에 코드 푸시..."

git add .
git commit -m "Add JARVIS Unified Dashboard - Auto Deploy $(date +%Y-%m-%d)" || echo "⚠️ 변경사항 없음"

# GitHub 원격 설정 (사용자가 직접 설정해야 함)
echo ""
echo "⚠️  GitHub 설정 필요:"
echo "   1. https://github.com/new 에서 새 리포지토리 생성 (이름: jarvis-dashboard)"
echo "   2. 다음 명령어 실행:"
echo ""
echo "   git remote add origin https://github.com/[당신의계정]/jarvis-dashboard.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
read -p "GitHub에 푸시 완료했나요? (y/n): " github_done

if [ "$github_done" != "y" ]; then
    echo "❌ GitHub 푸시를 먼저 완료해주세요."
    exit 1
fi

echo "✅ GitHub 푸시 완료"

# Step 5: Vercel 배포
echo ""
echo "📍 Step 5: Vercel에 배포 중..."
echo "   (브라우저에서 로그인 후 프로젝트 생성 선택)"

vercel --prod

# Step 6: 완료!
echo ""
echo "=================================================="
echo "✅ 배포 완료!"
echo ""
echo "📊 대시보드 접속:"
echo "   Vercel이 제공한 URL을 사용하세요"
echo ""
echo "🔄 자동 업데이트 설정:"
echo "   python C:\Users\Desktop\Claude\Projects\kms\outputs\update-dashboard.py"
echo ""
echo "💬 팀에게 공유:"
echo "   Slack #daiso-team에 대시보드 URL을 고정 메시지로 올리세요"
echo ""
echo "완료! 🎉"
