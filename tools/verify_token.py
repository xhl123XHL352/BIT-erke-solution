#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Token验证脚本
用于验证捕获的Token是否有效
"""

import requests
import urllib3
import os
import sys

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

TOKEN_FILE = "token.txt"
API_URL = "https://qcbldekt.bit.edu.cn/api/course/list"

def verify_token(token):
    """验证Token是否有效"""
    headers = {
        "Host": "qcbldekt.bit.edu.cn",
        "Authorization": token if token.startswith("Bearer") else f"Bearer {token}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF",
        "Content-Type": "application/json",
        "Referer": "https://servicewechat.com/wx89b19258915c9585/25/page-frame.html"
    }
    
    try:
        response = requests.get(
            f"{API_URL}?page=1&limit=10",
            headers=headers,
            verify=False,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get("code") == 200:
                items = data.get("data", {}).get("items", [])
                print("✅ Token有效！")
                print(f"📊 成功获取课程列表，共 {len(items)} 门课程")
                if items:
                    print("\n前3门课程：")
                    for i, course in enumerate(items[:3], 1):
                        print(f"  {i}. [{course.get('id')}] {course.get('title')}")
                return True
            else:
                print(f"❌ API返回错误: {data.get('message', '未知错误')}")
                return False
        elif response.status_code == 401:
            print("❌ Token无效或已过期 (401 Unauthorized)")
            print("💡 请重新捕获Token")
            return False
        elif response.status_code == 403:
            print("❌ Token无权限 (403 Forbidden)")
            print("💡 请检查Token是否正确")
            return False
        else:
            print(f"❌ 请求失败: HTTP {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 网络请求失败: {e}")
        return False

def main():
    print("=" * 60)
    print("🔍 Token验证工具")
    print("=" * 60)
    
    # 检查token.txt文件
    if not os.path.exists(TOKEN_FILE):
        print(f"❌ 未找到 {TOKEN_FILE} 文件")
        print("💡 请先运行 capture_token.py 捕获Token")
        return
    
    # 读取Token
    try:
        with open(TOKEN_FILE, "r", encoding="utf-8") as f:
            token = f.read().strip()
        
        if not token:
            print(f"❌ {TOKEN_FILE} 文件为空")
            return
        
        print(f"📄 读取Token: {token[:50]}...")
        print()
        
        # 验证Token
        if verify_token(token):
            print("\n" + "=" * 60)
            print("✅ 验证通过！可以使用此Token配置抢课系统")
            print("=" * 60)
        else:
            print("\n" + "=" * 60)
            print("❌ 验证失败！请重新捕获Token")
            print("=" * 60)
            
    except Exception as e:
        print(f"❌ 读取Token文件失败: {e}")

if __name__ == "__main__":
    main()

