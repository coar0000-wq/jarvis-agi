@echo off
setlocal enabledelayedexpansion

echo.
echo =========================================================
echo  JARVIS Cloud Auto Deploy
echo =========================================================
echo.

cd /d C:\Users\Desktop\Claude\Projects\kms

echo [1/4] Checking Git repository...

if not exist .git (
    echo Initializing Git repository...
    git init
    git config user.email "coar0000@naver.com"
    git config user.name "JARVIS"
    echo Git repository created
) else (
    echo Git repository found
)

echo.
echo [2/4] Adding files...

git add .github/workflows/jarvis-auto-collect.yml
git add jarvis_auto_collect.py
git add app.yaml
git add deploy_cloud.bat

echo Files added

echo.
echo [3/4] Committing...

git commit -m "JARVIS Cloud Automation Deployment"

echo.
echo [4/4] Pushing to GitHub...

git push origin main

if %errorLevel% neq 0 (
    echo Trying master branch...
    git push origin master
)

echo.
echo =========================================================
echo  DONE - Cloud Deployment Ready!
echo =========================================================
echo.
echo Next steps:
echo  1. Go to GitHub Settings - Secrets
echo  2. Add CLAUDE_API_KEY
echo  3. Add YOUTUBE_API_KEY
echo  4. Enable Google Cloud App Engine
echo.
echo Daily automation will run at 08:00 KST
echo.

pause
