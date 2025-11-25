@echo off
chcp 65001 >nul
echo ========================================
echo 清除系统代理设置
echo ========================================
echo.

echo 正在清除系统代理设置...
netsh winhttp reset proxy

if errorlevel 1 (
    echo ⚠️ 清除代理失败，可能需要管理员权限
    echo 请以管理员身份运行此脚本
) else (
    echo ✅ 系统代理已清除
)

echo.
echo 当前代理设置：
netsh winhttp show proxy

echo.
pause

