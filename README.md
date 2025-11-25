# 🎓 自动抢课监控系统

一个完整的自动监控与自动抢课系统，包含现代化的Web前端界面和Flask后端API服务。

## ✨ 功能特性

- 🔄 **自动监控**: 定时扫描课程列表，自动检测符合条件的课程
- ⚡ **自动抢课**: 发现目标课程后自动抢课
- 🎨 **现代化界面**: 美观的Web前端，实时显示监控状态和日志
- ⚙️ **灵活配置**: 可配置Token、扫描频率、课程ID范围等
- 📊 **实时统计**: 显示扫描次数、成功/失败次数等统计信息
- 📋 **日志记录**: 完整的运行日志，支持不同级别的日志显示
- 📜 **历史记录**: 记录已抢课程ID，防止重复抢课
- 🎯 **手动抢课**: 支持手动选择课程进行抢课
- 🔍 **Token工具**: 提供自动抓包和验证工具

## 📁 项目结构

```
erke/
├── backend/              # 后端服务
│   ├── app.py           # Flask主应用
│   ├── requirements.txt # Python依赖
│   └── config.json      # 配置文件（自动生成）
├── frontend/            # 前端界面
│   ├── index.html       # 主页面
│   ├── style.css        # 样式文件
│   └── app.js           # 前端逻辑
├── tools/               # 工具脚本
│   ├── verify_token.py        # Token验证脚本
│   ├── setup_fiddler.bat      # Fiddler配置助手
│   ├── remove_proxy.bat       # 清除系统代理
│   ├── fiddler_capture_guide.md  # Fiddler抓包详细指南
│   ├── fiddler_auto_extract.js   # Fiddler自动提取Token脚本
│   └── README.md               # 工具使用说明
├── start_backend.bat    # 后端启动脚本（Windows）
├── start_backend.sh     # 后端启动脚本（Linux/Mac）
├── start_frontend.bat   # 前端启动脚本（Windows）
├── start_frontend.sh    # 前端启动脚本（Linux/Mac）
└── README.md            # 项目说明
```

## 🚀 快速开始

### 环境要求

- Python 3.7+
- 现代浏览器（Chrome、Edge、Firefox等）
- 微信PC版（用于获取Token）
- Fiddler Classic（免费版，用于抓包）

### 第一步：安装依赖

**Windows用户：**
```bash
cd backend
pip install -r requirements.txt
```

**Linux/Mac用户：**
```bash
cd backend
pip3 install -r requirements.txt
```

### 第二步：获取Token（重要！）

由于课程系统是微信小程序，需要使用Fiddler在电脑微信中抓包获取Token。

#### 使用Fiddler抓包（推荐）✨

1. **安装Fiddler**
   - 下载地址：https://www.telerik.com/fiddler
   - 安装Fiddler Classic（免费版）

2. **配置Fiddler**
   - 启动Fiddler
   - 菜单栏：`Tools` → `Options` → `HTTPS` 标签
   - 勾选 `Decrypt HTTPS traffic`
   - 勾选 `Ignore server certificate errors`
   - 点击 `Actions` → `Export Root Certificate to Desktop`（导出证书到桌面）

3. **安装证书到系统**
   - 双击桌面上的 `FiddlerRoot.cer` 文件
   - 点击"安装证书" → 选择"本地计算机" → 下一步
   - 选择"将所有证书都放入下列存储" → 浏览 → 选择"受信任的根证书颁发机构" → 确定 → 完成

4. **配置系统代理（自动配置）**
   - 以管理员身份运行 `tools/setup_fiddler.bat`
   - 或手动设置：
     - Windows设置 → 网络和Internet → 代理
     - 手动代理设置：地址 `127.0.0.1`，端口 `8888`

5. **重启微信**
   - 完全关闭微信（包括后台进程）
   - 重新启动微信

6. **捕获Token**
   - 在Fiddler底部输入框输入：`qcbldekt.bit.edu.cn`（用于过滤）
   - 在微信中打开课程系统小程序，访问课程列表页面
   - 在Fiddler中找到 `qcbldekt.bit.edu.cn` 的请求
   - 点击请求，在右侧 `Headers` 标签中找到 `Authorization` 字段
   - 复制完整内容（例如：`Bearer 517196|E8m5blSrtgMfwYzu34rklcaSdamO34gwUWReRIPd`）

7. **保存Token**
   - 将Token保存到 `tools/token.txt` 文件
   - 或直接复制到抢课系统配置中

8. **验证Token（可选）**
   ```bash
   cd tools
   python verify_token.py
   ```

9. **清除代理（使用完毕后）**
   - 运行 `tools/remove_proxy.bat` 清除系统代理
   - 或手动关闭系统代理设置

> 💡 **详细说明**: 完整抓包指南请查看 `tools/fiddler_capture_guide.md`  
> 💡 **自动提取**: 可以使用 `tools/fiddler_auto_extract.js` 脚本自动提取Token（见指南）

### 第三步：启动后端服务

**Windows用户：**
- 双击运行 `start_backend.bat`
- 或命令行运行：
  ```bash
  cd backend
  python app.py
  ```

**Linux/Mac用户：**
```bash
chmod +x start_backend.sh
./start_backend.sh
```
或：
```bash
cd backend
python3 app.py
```

后端服务将在 `http://localhost:5000` 启动。

### 第四步：启动前端界面

**方式一：直接打开（推荐）**
- 直接在浏览器中打开 `frontend/index.html` 文件

**方式二：使用本地服务器**
```bash
cd frontend
python -m http.server 8000
# 或
python3 -m http.server 8000
```
然后在浏览器中访问 `http://localhost:8000`

**Windows用户也可以：**
- 双击运行 `start_frontend.bat`

### 第五步：配置系统

1. **在Web界面中配置Token**
   - 打开"系统配置"面板
   - 将从 `tools/token.txt` 读取的Token粘贴到"Token"输入框
   - 或手动输入Token（格式：`Bearer xxxxx`）

2. **设置扫描参数**
   - **扫描频率**: 建议2-5秒（不要设置太小）
   - **最小课程ID**: 默认100
   - **最大课程ID**: 默认999
   - **自动抢课**: 勾选后满足条件自动抢课

3. **保存配置**
   - 点击"保存配置"按钮
   - 配置会自动保存到 `backend/config.json`

### 第六步：启动监控

1. 点击"启动监控"按钮
2. 系统将开始自动扫描课程
3. 在"运行日志"面板可以查看实时日志
4. 在"统计信息"中可以看到扫描次数、成功/失败次数等

## 📖 使用指南

### 功能说明

#### 自动监控
- 系统会按照设定的扫描频率，定时检查课程列表
- 自动筛选符合条件的课程（ID在范围内、有名额、未抢过）
- 如果启用自动抢课，发现目标后会自动抢课

#### 手动抢课
- 在"课程列表"中，可以看到所有可用课程
- 对于有名额的课程，可以点击"手动抢课"按钮
- 系统会立即尝试抢课

#### 配置管理
- 所有配置会自动保存到 `backend/config.json`
- 下次启动时会自动加载上次的配置
- 可以随时修改配置并保存

#### 日志系统
- 支持不同级别的日志（info、success、warning、error）
- 日志会自动滚动，只保留最近500条
- 可以手动清空日志

#### 历史记录
- 记录所有已抢的课程ID，防止重复抢课
- 可以手动清空历史记录

### 配置参数说明

- **Token**: 认证令牌，必需。从微信小程序中获取
- **扫描频率**: 每次扫描的间隔时间（秒），建议2-5秒，不要设置太小
- **最小课程ID**: 筛选课程的最小ID，默认100
- **最大课程ID**: 筛选课程的最大ID，默认999
- **自动抢课**: 是否在发现目标课程时自动抢课

## 🔧 故障排除

### 问题1：无法连接到后端

**症状**: 前端页面无法加载数据，控制台显示连接错误

**解决方法**:
- 检查后端服务是否正在运行
- 确认后端运行在 `http://localhost:5000`
- 检查防火墙设置，确保5000端口未被阻止
- 尝试在浏览器中直接访问 `http://localhost:5000/api/status` 测试

### 问题2：Token过期或无效

**症状**: 日志显示401或403错误，无法获取课程列表

**解决方法**:
- 重新运行抓包脚本获取新Token
- 检查Token格式是否正确（应该包含"Bearer "前缀）
- 使用 `tools/verify_token.py` 验证Token是否有效
- 确保Token是从正确的API请求中获取的

### 问题3：抢课失败

**症状**: 监控发现目标课程但抢课失败

**解决方法**:
- 检查课程是否还有名额
- 检查网络连接是否稳定
- 查看日志了解具体错误信息
- 尝试手动抢课测试

### 问题4：前端页面无法加载

**症状**: 打开HTML文件后页面空白或报错

**解决方法**:
- 如果直接打开HTML文件，确保后端服务正在运行
- 如果使用本地服务器，检查端口是否被占用
- 检查浏览器控制台是否有错误信息
- 尝试使用Chrome或Edge浏览器

### 问题5：Fiddler中看不到微信请求

**症状**: 在Fiddler中看不到微信小程序的请求

**解决方法**:
- 确认系统代理已设置为 127.0.0.1:8888
- 完全关闭微信后重新启动
- 检查Fiddler是否在监听8888端口（Tools → Options → Connections）
- 确认Fiddler中已勾选 `Decrypt HTTPS traffic`
- 尝试以管理员身份运行Fiddler
- 检查防火墙是否阻止了Fiddler

### 问题6：微信无法连接网络

**症状**: 配置代理后微信无法连接网络

**解决方法**:
- 检查系统代理设置是否正确（127.0.0.1:8888）
- 确认Fiddler正在运行
- 重新安装Fiddler证书到系统
- 重启微信
- 如果问题持续，尝试清除代理后重新配置

## 📡 API接口文档

### 获取状态
```
GET /api/status
```
返回监控状态、配置和统计信息

### 获取配置
```
GET /api/config
```
返回当前系统配置

### 更新配置
```
POST /api/config
Content-Type: application/json

{
  "token": "Bearer xxx",
  "sleep_time": 2,
  "min_id": 100,
  "max_id": 999,
  "auto_apply": true
}
```

### 启动监控
```
POST /api/start
```
启动自动监控服务

### 停止监控
```
POST /api/stop
```
停止自动监控服务

### 获取日志
```
GET /api/logs?limit=50
```
获取运行日志，limit参数控制返回数量

### 清空日志
```
POST /api/logs/clear
```
清空所有日志记录

### 获取课程列表
```
GET /api/courses?page=1&limit=50&sign_status=2
```
获取课程列表
- `page`: 页码
- `limit`: 每页数量
- `sign_status`: 课程状态（2=进行中）

### 手动抢课
```
POST /api/apply
Content-Type: application/json

{
  "course_id": 123
}
```
手动抢指定课程

### 获取历史记录
```
GET /api/history
```
获取已抢课程ID列表

### 清空历史记录
```
POST /api/history/clear
```
清空所有历史记录

## ⚠️ 重要注意事项

1. **Token有效期**
   - Token可能会过期，如果出现401或403错误，需要重新获取Token
   - 建议定期检查Token是否有效
   - 可以保存多个Token备用

2. **扫描频率**
   - 不要设置过低的扫描频率（建议≥2秒）
   - 过低的频率可能对服务器造成压力，也可能被限制
   - 建议根据实际情况调整，平衡效率和稳定性

3. **网络连接**
   - 确保网络连接稳定
   - 如果网络不稳定，可能导致抢课失败
   - 建议使用稳定的WiFi网络

4. **合法使用**
   - 请遵守学校相关规定
   - 本系统仅供学习研究使用
   - 不要用于恶意抢课或干扰正常选课
   - 建议合理设置扫描频率，避免对服务器造成压力

5. **浏览器兼容性**
   - 建议使用Chrome、Edge、Firefox等现代浏览器
   - 如果遇到跨域问题，确保后端服务正在运行
   - 某些旧版浏览器可能不支持部分功能

6. **数据安全**
   - Token是敏感信息，请妥善保管
   - 不要将Token分享给他人
   - 配置文件包含Token，注意保护隐私

## 🛠️ 技术栈

- **后端**: Flask + Flask-CORS
- **前端**: 原生HTML/CSS/JavaScript
- **HTTP请求**: requests库
- **抓包工具**: mitmproxy

## 📝 更新日志

### v1.0.0
- ✅ 初始版本
- ✅ 实现自动监控和抢课功能
- ✅ 添加Web前端界面
- ✅ 支持配置管理和日志记录
- ✅ 添加Token自动捕获工具
- ✅ 添加Token验证工具

## 📄 许可证

本项目仅供学习和研究使用。

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📞 技术支持

如遇到问题，请检查：
1. Python版本（建议3.7+）
2. 依赖包是否正确安装
3. 后端服务是否正常运行
4. 浏览器控制台是否有错误
5. Token是否有效

更多工具使用说明请查看 `tools/README.md`

祝您使用愉快！🎉
