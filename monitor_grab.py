import requests
import time
import datetime
import sys
import urllib3

# ==================== 🛠️ 用户配置区 ====================

# 您的 Token (如果过期请及时替换)
TOKEN = "Bearer 517196|E8m5blSrtgMfwYzu34rklcaSdamO34gwUWReRIPd"

# 扫描频率 (秒)
SLEEP_TIME = 2

# ==================== ⚙️ 系统配置区 ====================

LIST_URL = "https://qcbldekt.bit.edu.cn/api/course/list"
APPLY_URL = "https://qcbldekt.bit.edu.cn/api/course/apply"

# 禁用 SSL 安全警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

headers = {
    "Host": "qcbldekt.bit.edu.cn",
    "Authorization": TOKEN,
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF",
    "Content-Type": "application/json",
    "Referer": "https://servicewechat.com/wx89b19258915c9585/25/page-frame.html"
}

# 记录已抢过的 ID，防止重复提交
applied_history = []

def get_time():
    return datetime.datetime.now().strftime("%H:%M:%S")

def apply_course(course_id, title):
    """ 执行抢课 """
    print(f"\n[{get_time()}] ⚡ 发现目标 ID:{course_id} ({title}) -> 正在秒杀...")
    
    try:
        payload = {"course_id": course_id}
        # verify=False 必加，否则报错
        res = requests.post(APPLY_URL, headers=headers, json=payload, verify=False, timeout=5)
        res_json = res.json()
        
        # 判断结果
        if res.status_code == 200 and (res_json.get("code") == 200 or "成功" in str(res_json)):
            print(f"[{get_time()}] 🎉🎉🎉 抢课成功！ID: {course_id}")
            print(f"服务器回执: {res_json}")
            return True
        else:
            msg = res_json.get("message", "未知错误")
            print(f"[{get_time()}] ❌ 失败: {msg}")
            
            # 如果提示已报名，加入历史记录
            if "已报名" in str(msg) or "重复" in str(msg):
                applied_history.append(course_id)
            return False
            
    except Exception as e:
        print(f"抢课请求炸了: {e}")
        return False

def monitor():
    print(f"[{get_time()}] 🚀 三位数课程监控脚本启动！")
    print("筛选条件: [状态=进行中] AND [有名额] AND [100 <= ID <= 999]")
    
    scan_count = 0
    
    while True:
        scan_count += 1
        try:
            # 1. 获取列表
            # sign_status=2 表示只看“正在进行中”的课
            # limit=100 尽量一次拉取更多，防止漏掉
            params = {
                "page": 1, 
                "limit": 100, 
                "sign_status": 2 
            }
            
            resp = requests.get(LIST_URL, headers=headers, params=params, verify=False, timeout=5)
            
            # 检查 Token
            if resp.status_code == 401 or resp.status_code == 403:
                print(f"\n[{get_time()}] ⛔ Token 过期了！请去抓个新的填进来！")
                break
            
            data = resp.json()
            items = data.get("data", {}).get("items", [])
            
            # 进度条显示
            sys.stdout.write(f"\r[{get_time()}] 扫描第 {scan_count} 次 | 当前在线课程数: {len(items)} ...")
            sys.stdout.flush()

            # 2. 遍历筛选
            if items:
                for item in items:
                    try:
                        cid = int(item['id']) # 确保转为数字
                        title = item['title']
                        curr = int(item.get('course_apply_count', 0))
                        maxx = int(item.get('max', 0))
                        
                        # === 核心筛选逻辑 ===
                        
                        # 条件 1: 必须是三位数 (100-999)
                        is_three_digits = (100 <= cid <= 999)
                        
                        # 条件 2: 必须有名额
                        has_quota = (curr < maxx)
                        
                        # 条件 3: 没抢过
                        not_applied = (cid not in applied_history)
                        
                        if is_three_digits and has_quota and not_applied:
                            print(f"\n\n[{get_time()}] 🎯 命中规则! ID:{cid} | {title} | 名额:{curr}/{maxx}")
                            
                            # 满足条件，开抢！
                            success = apply_course(cid, title)
                            if success:
                                applied_history.append(cid)
                                
                    except ValueError:
                        continue # ID 转不成数字就算了

        except Exception as e:
            print(f"\n[{get_time()}] 监控异常: {e}")
            time.sleep(SLEEP_TIME)
        
        time.sleep(SLEEP_TIME)

if __name__ == "__main__":
    monitor()