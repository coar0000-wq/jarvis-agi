@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo.
echo ================================================================
echo 🤖 JARVIS 노드 자동 연결 시작
echo ================================================================
echo.
python connect_nodes_auto.py
echo.
pause
