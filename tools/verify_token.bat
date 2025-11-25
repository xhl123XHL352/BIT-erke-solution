@echo off
chcp 65001 >nul
cd /d %~dp0
python verify_token.py
pause

