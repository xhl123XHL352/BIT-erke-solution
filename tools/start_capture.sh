#!/bin/bash

echo "========================================"
echo "Token自动捕获工具"
echo "========================================"
echo ""

cd "$(dirname "$0")"

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "[错误] 未找到Python3，请先安装Python"
    exit 1
fi

# 检查mitmproxy
if ! python3 -c "import mitmproxy" 2>/dev/null; then
    echo "[提示] 未安装mitmproxy，正在安装..."
    pip3 install mitmproxy
    if [ $? -ne 0 ]; then
        echo "[错误] 安装mitmproxy失败"
        exit 1
    fi
fi

echo ""
echo "启动Token捕获工具..."
echo ""
python3 capture_token.py

