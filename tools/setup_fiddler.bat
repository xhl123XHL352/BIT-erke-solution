@echo off
chcp 65001 >nul
echo ========================================
echo Fiddler配置助手
echo ========================================
echo.

echo 本脚本将帮助您配置Fiddler和系统代理
echo.

echo [步骤1] 检查Fiddler是否已安装...
where fiddler >nul 2>&1
if errorlevel 1 (
    echo ⚠️ 未检测到Fiddler，请先安装Fiddler
    echo 下载地址: https://www.telerik.com/fiddler
    echo.
    pause
    exit /b 1
) else (
    echo ✅ Fiddler已安装
)

echo.
echo [步骤2] 配置系统代理...
echo 正在设置系统代理为 127.0.0.1:8888
echo.

REM 使用netsh设置代理
netsh winhttp set proxy 127.0.0.1:8888
if errorlevel 1 (
    echo ⚠️ 设置代理失败，可能需要管理员权限
    echo 请以管理员身份运行此脚本
    pause
    exit /b 1
) else (
    echo ✅ 系统代理已设置为 127.0.0.1:8888
)

echo.
echo [步骤3] 检查当前代理设置...
netsh winhttp show proxy

echo.
echo ========================================
echo 配置完成！
echo ========================================
echo.
echo 接下来的步骤：
echo 1. 启动Fiddler
echo 2. 在Fiddler中：Tools → Options → HTTPS
echo    勾选 "Decrypt HTTPS traffic"
echo    点击 "Actions" → "Export Root Certificate to Desktop"
echo 3. 双击导出的证书文件，安装到"受信任的根证书颁发机构"
echo 4. 重启微信
echo 5. 在微信中打开小程序，访问课程列表
echo 6. 在Fiddler中查找 qcbldekt.bit.edu.cn 的请求
echo 7. 查看Request Headers中的Authorization字段
echo.
echo 详细说明请查看: tools\fiddler_capture_guide.md
echo.
pause

