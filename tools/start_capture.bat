@echo off
chcp 65001 >nul
echo ========================================
echo Token自动捕获工具
echo ========================================
echo.

cd /d %~dp0

echo 检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到Python，请先安装Python
    pause
    exit /b 1
)

echo 检查mitmproxy...
python -c "import mitmproxy" >nul 2>&1
if errorlevel 1 (
    echo [提示] 未安装mitmproxy，正在安装...
    pip install mitmproxy
    if errorlevel 1 (
        echo [错误] 安装mitmproxy失败
        pause
        exit /b 1
    )
)

echo.
echo 启动Token捕获工具...
echo.
python capture_token.py

pause

