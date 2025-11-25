@echo off
echo 正在启动前端服务器...
cd frontend
python -m http.server 8000
pause

