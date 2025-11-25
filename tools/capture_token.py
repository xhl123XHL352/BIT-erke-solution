#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动抓包脚本 - 用于捕获微信小程序中的Token
使用方法：
1. 安装依赖: pip install mitmproxy
2. 运行脚本: python capture_token.py
3. 配置手机代理指向电脑IP:8080
4. 在微信中打开小程序，访问课程列表
5. Token会自动保存到 token.txt
"""

import sys
from mitmproxy import http
from mitmproxy.tools.dump import DumpMaster
from mitmproxy.options import Options
import os
from datetime import datetime

# 目标域名
TARGET_DOMAIN = "qcbldekt.bit.edu.cn"
# Token保存路径
TOKEN_FILE = "token.txt"
# 日志文件
LOG_FILE = "capture_log.txt"

class TokenCapture:
    def __init__(self):
        self.token_found = False
        self.captured_tokens = set()
        
    def log(self, message):
        """记录日志"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_msg = f"[{timestamp}] {message}\n"
        print(log_msg, end='')
        
        # 同时写入日志文件
        try:
            with open(LOG_FILE, "a", encoding="utf-8") as f:
                f.write(log_msg)
        except:
            pass
    
    def request(self, flow: http.HTTPFlow) -> None:
        """拦截HTTP请求"""
        try:
            # 检查是否是目标API
            host = flow.request.pretty_host
            path = flow.request.path
            
            if TARGET_DOMAIN in host:
                # 获取Authorization头
                auth_header = flow.request.headers.get("Authorization", "")
                
                if auth_header:
                    # 检查是否是新Token
                    if auth_header not in self.captured_tokens:
                        self.captured_tokens.add(auth_header)
                        
                        # 保存Token
                        try:
                            with open(TOKEN_FILE, "w", encoding="utf-8") as f:
                                f.write(auth_header)
                            
                            self.log("=" * 60)
                            self.log("🎉 成功捕获Token！")
                            self.log("=" * 60)
                            self.log(f"请求URL: {flow.request.pretty_url}")
                            self.log(f"请求方法: {flow.request.method}")
                            self.log(f"Authorization: {auth_header}")
                            self.log(f"Token已保存到: {os.path.abspath(TOKEN_FILE)}")
                            self.log("=" * 60)
                            
                            if not self.token_found:
                                self.token_found = True
                                self.log("\n✅ 首次捕获Token成功！")
                                self.log("💡 提示：你可以继续使用小程序，脚本会持续监控")
                                self.log("💡 如果Token更新，会自动保存最新的Token\n")
                        except Exception as e:
                            self.log(f"❌ 保存Token失败: {e}")
                
                # 显示所有请求信息（用于调试）
                self.log(f"📡 捕获请求: {flow.request.method} {path}")
                
        except Exception as e:
            self.log(f"⚠️ 处理请求时出错: {e}")
    
    def response(self, flow: http.HTTPFlow) -> None:
        """拦截HTTP响应（可选，用于调试）"""
        try:
            if TARGET_DOMAIN in flow.request.pretty_host:
                status = flow.response.status_code
                if status == 401 or status == 403:
                    self.log(f"⚠️ 警告: 收到 {status} 响应，Token可能已过期")
        except:
            pass

def main():
    """主函数"""
    print("=" * 60)
    print("🚀 Token自动捕获工具")
    print("=" * 60)
    print(f"目标域名: {TARGET_DOMAIN}")
    print(f"监听端口: 8080")
    print(f"Token保存路径: {os.path.abspath(TOKEN_FILE)}")
    print("=" * 60)
    print("\n📋 使用步骤：")
    print("1. 确保手机和电脑连接同一WiFi")
    print("2. 查看本机IP地址（脚本会显示）")
    print("3. 在手机WiFi设置中配置代理：")
    print("   - 服务器: 本机IP地址")
    print("   - 端口: 8080")
    print("4. 在手机浏览器访问: http://mitm.it")
    print("   下载并安装证书（iOS需要在设置中信任证书）")
    print("5. 在微信中打开小程序，访问课程列表")
    print("6. Token会自动捕获并保存")
    print("\n" + "=" * 60)
    print("⏳ 等待捕获Token...")
    print("按 Ctrl+C 停止捕获")
    print("=" * 60 + "\n")
    
    # 获取本机IP（简单方法）
    try:
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        print(f"💡 本机IP地址: {local_ip}")
        print(f"💡 手机代理设置: {local_ip}:8080\n")
    except:
        print("⚠️ 无法自动获取IP地址，请手动查看\n")
    
    # 创建mitmproxy选项
    opts = Options(listen_port=8080)
    
    # 创建捕获实例
    capture = TokenCapture()
    
    # 创建DumpMaster
    master = DumpMaster(opts)
    master.addons.add(capture)
    
    try:
        # 启动mitmproxy
        master.run()
    except KeyboardInterrupt:
        print("\n\n" + "=" * 60)
        print("🛑 捕获已停止")
        if capture.token_found:
            print(f"✅ Token已保存到: {os.path.abspath(TOKEN_FILE)}")
        else:
            print("⚠️ 未捕获到Token，请检查：")
            print("   1. 手机代理是否正确配置")
            print("   2. 证书是否已安装并信任")
            print("   3. 是否在微信中访问了课程列表")
        print("=" * 60)

if __name__ == "__main__":
    main()

