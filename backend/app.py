from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import time
import datetime
import threading
import urllib3
import json
import os

# 禁用 SSL 安全警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 全局状态
monitor_status = {
    "running": False,
    "thread": None,
    "config": {
        "token": "",
        "sleep_time": 2,
        "min_id": 100,
        "max_id": 999,
        "auto_apply": True
    },
    "logs": [],
    "applied_history": [],
    "stats": {
        "scan_count": 0,
        "success_count": 0,
        "fail_count": 0,
        "last_scan_time": None
    }
}

# 配置文件路径
CONFIG_FILE = "config.json"

# API 端点
LIST_URL = "https://qcbldekt.bit.edu.cn/api/course/list"
APPLY_URL = "https://qcbldekt.bit.edu.cn/api/course/apply"

def get_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def add_log(message, level="info"):
    """添加日志"""
    log_entry = {
        "time": get_time(),
        "message": message,
        "level": level
    }
    monitor_status["logs"].append(log_entry)
    # 只保留最近500条日志
    if len(monitor_status["logs"]) > 500:
        monitor_status["logs"] = monitor_status["logs"][-500:]
    print(f"[{log_entry['time']}] {message}")

def load_config():
    """加载配置"""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                saved_config = json.load(f)
                monitor_status["config"].update(saved_config)
                add_log("配置加载成功", "info")
        except Exception as e:
            add_log(f"加载配置失败: {e}", "error")

def save_config():
    """保存配置"""
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(monitor_status["config"], f, ensure_ascii=False, indent=2)
        add_log("配置保存成功", "info")
    except Exception as e:
        add_log(f"保存配置失败: {e}", "error")

def get_headers():
    """获取请求头"""
    token = monitor_status["config"]["token"]
    return {
        "Host": "qcbldekt.bit.edu.cn",
        "Authorization": token if token.startswith("Bearer") else f"Bearer {token}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF",
        "Content-Type": "application/json",
        "Referer": "https://servicewechat.com/wx89b19258915c9585/25/page-frame.html"
    }

def apply_course(course_id, title):
    """执行抢课"""
    add_log(f"⚡ 发现目标 ID:{course_id} ({title}) -> 正在秒杀...", "warning")
    
    try:
        payload = {"course_id": course_id}
        headers = get_headers()
        res = requests.post(APPLY_URL, headers=headers, json=payload, verify=False, timeout=5)
        res_json = res.json()
        
        # 判断结果
        if res.status_code == 200 and (res_json.get("code") == 200 or "成功" in str(res_json)):
            add_log(f"🎉🎉🎉 抢课成功！ID: {course_id} | {title}", "success")
            add_log(f"服务器回执: {json.dumps(res_json, ensure_ascii=False)}", "info")
            monitor_status["stats"]["success_count"] += 1
            return True
        else:
            msg = res_json.get("message", "未知错误")
            add_log(f"❌ 失败: {msg}", "error")
            monitor_status["stats"]["fail_count"] += 1
            
            # 如果提示已报名，加入历史记录
            if "已报名" in str(msg) or "重复" in str(msg):
                if course_id not in monitor_status["applied_history"]:
                    monitor_status["applied_history"].append(course_id)
            return False
            
    except Exception as e:
        add_log(f"抢课请求异常: {e}", "error")
        monitor_status["stats"]["fail_count"] += 1
        return False

def monitor_loop():
    """监控循环"""
    config = monitor_status["config"]
    min_id = config.get("min_id", 100)
    max_id = config.get("max_id", 999)
    auto_apply = config.get("auto_apply", True)
    sleep_time = config.get("sleep_time", 2)
    
    add_log("🚀 监控脚本启动！", "info")
    add_log(f"筛选条件: [状态=进行中] AND [有名额] AND [{min_id} <= ID <= {max_id}]", "info")
    
    while monitor_status["running"]:
        try:
            # 获取课程列表
            params = {
                "page": 1,
                "limit": 100,
                "sign_status": 2
            }
            
            headers = get_headers()
            resp = requests.get(LIST_URL, headers=headers, params=params, verify=False, timeout=5)
            
            # 检查 Token
            if resp.status_code == 401 or resp.status_code == 403:
                add_log("⛔ Token 过期了！请更新Token", "error")
                monitor_status["running"] = False
                break
            
            data = resp.json()
            items = data.get("data", {}).get("items", [])
            
            monitor_status["stats"]["scan_count"] += 1
            monitor_status["stats"]["last_scan_time"] = get_time()
            
            # 遍历筛选
            if items:
                for item in items:
                    if not monitor_status["running"]:
                        break
                        
                    try:
                        cid = int(item['id'])
                        title = item['title']
                        curr = int(item.get('course_apply_count', 0))
                        maxx = int(item.get('max', 0))
                        
                        # 筛选逻辑
                        is_in_range = (min_id <= cid <= max_id)
                        has_quota = (curr < maxx)
                        not_applied = (cid not in monitor_status["applied_history"])
                        
                        if is_in_range and has_quota and not_applied:
                            add_log(f"🎯 命中规则! ID:{cid} | {title} | 名额:{curr}/{maxx}", "warning")
                            
                            if auto_apply:
                                success = apply_course(cid, title)
                                if success:
                                    monitor_status["applied_history"].append(cid)
                            else:
                                add_log(f"⚠️ 自动抢课已关闭，仅记录目标: ID:{cid}", "info")
                                
                    except (ValueError, KeyError) as e:
                        continue
            
        except Exception as e:
            add_log(f"监控异常: {e}", "error")
            time.sleep(sleep_time)
        
        if monitor_status["running"]:
            time.sleep(sleep_time)
    
    add_log("监控已停止", "info")

# ==================== API 路由 ====================

@app.route('/api/status', methods=['GET'])
def get_status():
    """获取监控状态"""
    return jsonify({
        "running": monitor_status["running"],
        "config": monitor_status["config"],
        "stats": monitor_status["stats"]
    })

@app.route('/api/config', methods=['GET'])
def get_config():
    """获取配置"""
    return jsonify(monitor_status["config"])

@app.route('/api/config', methods=['POST'])
def update_config():
    """更新配置"""
    data = request.json
    monitor_status["config"].update(data)
    save_config()
    add_log("配置已更新", "info")
    return jsonify({"success": True, "message": "配置已更新"})

@app.route('/api/start', methods=['POST'])
def start_monitor():
    """启动监控"""
    if monitor_status["running"]:
        return jsonify({"success": False, "message": "监控已在运行中"})
    
    if not monitor_status["config"]["token"]:
        return jsonify({"success": False, "message": "请先配置Token"})
    
    monitor_status["running"] = True
    monitor_status["stats"] = {
        "scan_count": 0,
        "success_count": 0,
        "fail_count": 0,
        "last_scan_time": None
    }
    
    thread = threading.Thread(target=monitor_loop, daemon=True)
    thread.start()
    monitor_status["thread"] = thread
    
    add_log("监控已启动", "info")
    return jsonify({"success": True, "message": "监控已启动"})

@app.route('/api/stop', methods=['POST'])
def stop_monitor():
    """停止监控"""
    if not monitor_status["running"]:
        return jsonify({"success": False, "message": "监控未运行"})
    
    monitor_status["running"] = False
    add_log("正在停止监控...", "info")
    return jsonify({"success": True, "message": "监控已停止"})

@app.route('/api/logs', methods=['GET'])
def get_logs():
    """获取日志"""
    limit = request.args.get('limit', 100, type=int)
    logs = monitor_status["logs"][-limit:]
    return jsonify(logs)

@app.route('/api/logs/clear', methods=['POST'])
def clear_logs():
    """清空日志"""
    monitor_status["logs"] = []
    add_log("日志已清空", "info")
    return jsonify({"success": True, "message": "日志已清空"})

@app.route('/api/history', methods=['GET'])
def get_history():
    """获取抢课历史"""
    return jsonify(monitor_status["applied_history"])

@app.route('/api/history/clear', methods=['POST'])
def clear_history():
    """清空历史记录"""
    monitor_status["applied_history"] = []
    add_log("历史记录已清空", "info")
    return jsonify({"success": True, "message": "历史记录已清空"})

@app.route('/api/courses', methods=['GET'])
def get_courses():
    """获取课程列表"""
    try:
        params = {
            "page": request.args.get('page', 1, type=int),
            "limit": request.args.get('limit', 100, type=int),
            "sign_status": request.args.get('sign_status', 2, type=int)
        }
        
        headers = get_headers()
        resp = requests.get(LIST_URL, headers=headers, params=params, verify=False, timeout=5)
        
        if resp.status_code == 401 or resp.status_code == 403:
            return jsonify({"success": False, "message": "Token过期，请更新Token"}), 401
        
        data = resp.json()
        return jsonify({"success": True, "data": data})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/api/apply', methods=['POST'])
def manual_apply():
    """手动抢课"""
    data = request.json
    course_id = data.get('course_id')
    
    if not course_id:
        return jsonify({"success": False, "message": "缺少course_id参数"}), 400
    
    try:
        # 先获取课程信息
        headers = get_headers()
        params = {"page": 1, "limit": 100, "sign_status": 2}
        resp = requests.get(LIST_URL, headers=headers, params=params, verify=False, timeout=5)
        data = resp.json()
        items = data.get("data", {}).get("items", [])
        
        course_info = None
        for item in items:
            if int(item['id']) == course_id:
                course_info = item
                break
        
        if not course_info:
            return jsonify({"success": False, "message": "未找到该课程"}), 404
        
        title = course_info.get('title', '')
        success = apply_course(course_id, title)
        
        if success:
            if course_id not in monitor_status["applied_history"]:
                monitor_status["applied_history"].append(course_id)
        
        return jsonify({"success": success, "message": "抢课成功" if success else "抢课失败"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

if __name__ == '__main__':
    # 加载配置
    load_config()
    
    # 启动Flask应用
    app.run(host='0.0.0.0', port=5000, debug=True)

