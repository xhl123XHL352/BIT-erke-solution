# Token自动捕获工具

这个工具可以帮助你自动从微信小程序中捕获Token，无需手动抓包。

## 🚀 快速开始

### Windows用户

1. **安装依赖**
   ```bash
   cd tools
   pip install mitmproxy
   ```

2. **运行捕获工具**
   - 双击运行 `start_capture.bat`
   - 或命令行运行：
     ```bash
     python capture_token.py
     ```

### Linux/Mac用户

1. **安装依赖**
   ```bash
   cd tools
   pip3 install mitmproxy
   ```

2. **运行捕获工具**
   ```bash
   chmod +x start_capture.sh
   ./start_capture.sh
   ```
   或：
   ```bash
   python3 capture_token.py
   ```

## 📋 详细步骤

### 第一步：启动捕获工具

运行脚本后，会显示：
- 本机IP地址
- 监听端口（默认8080）
- Token保存路径

### 第二步：配置手机代理

1. **确保手机和电脑连接同一WiFi**

2. **查看本机IP**
   - 脚本会自动显示，或手动查看：
   - Windows: `ipconfig` 查看IPv4地址
   - Mac/Linux: `ifconfig` 或 `ip addr`

3. **在手机WiFi设置中配置代理**
   - 打开WiFi设置
   - 长按当前连接的WiFi
   - 选择"修改网络"或"高级选项"
   - 代理选择"手动"
   - 服务器：输入电脑IP地址
   - 端口：8080
   - 保存

### 第三步：安装证书（重要！）

1. **在手机浏览器中访问**
   ```
   http://mitm.it
   ```

2. **下载证书**
   - 根据手机系统选择对应的证书下载
   - Android: 下载并安装证书
   - iOS: 下载后需要在"设置-通用-关于本机-证书信任设置"中信任证书

3. **验证证书**
   - 安装证书后，再次访问 `http://mitm.it` 应该显示绿色提示

### 第四步：捕获Token

1. **在微信中打开小程序**
   - 打开课程系统小程序
   - 访问课程列表页面

2. **查看捕获结果**
   - 脚本会自动捕获Token
   - Token会保存到 `token.txt` 文件
   - 控制台会显示捕获信息

3. **使用Token**
   - 打开 `token.txt` 文件
   - 复制Token内容
   - 粘贴到抢课系统的配置中

## ⚠️ 注意事项

1. **证书信任（iOS）**
   - iOS系统需要在"设置-通用-关于本机-证书信任设置"中信任mitmproxy证书
   - 否则无法抓取HTTPS请求

2. **防火墙设置**
   - 确保防火墙允许8080端口
   - Windows可能会弹出防火墙提示，选择"允许访问"

3. **网络环境**
   - 手机和电脑必须在同一局域网
   - 建议关闭VPN等代理工具

4. **Token格式**
   - 捕获的Token格式通常是：`Bearer xxxxx`
   - 直接复制完整内容即可使用

5. **停止捕获**
   - 按 `Ctrl+C` 停止捕获
   - 停止后记得关闭手机代理设置

## 🔧 故障排除

### 问题1：无法捕获Token

**可能原因：**
- 手机代理未正确配置
- 证书未安装或未信任
- 防火墙阻止了连接

**解决方法：**
1. 检查手机代理设置是否正确
2. 重新安装并信任证书
3. 检查防火墙设置
4. 确保手机和电脑在同一WiFi

### 问题2：证书安装失败

**解决方法：**
1. 确保手机浏览器可以访问 `http://mitm.it`
2. 如果无法访问，检查代理设置
3. iOS需要额外在系统设置中信任证书

### 问题3：捕获到但Token无效

**可能原因：**
- Token已过期
- 捕获的不是正确的请求

**解决方法：**
1. 重新捕获Token
2. 确保在访问课程列表时捕获
3. 检查Token格式是否正确

### 问题4：端口被占用

**解决方法：**
1. 修改脚本中的端口号（默认8080）
2. 或关闭占用端口的程序

## 📝 输出文件

- `token.txt`: 保存捕获的Token
- `capture_log.txt`: 捕获过程的日志

## 💡 提示

1. **首次使用建议先测试**
   - 可以先访问其他HTTPS网站测试代理是否正常
   - 确认能正常抓包后再使用小程序

2. **Token有效期**
   - Token可能会过期，需要定期重新捕获
   - 建议保存多个Token备用

3. **安全提示**
   - 抓包工具会拦截所有HTTPS流量
   - 使用完毕后记得关闭代理
   - 不要在不安全的网络环境中使用

## 🎯 快速验证

捕获Token后，可以使用验证脚本快速验证Token是否有效：

**Windows:**
```bash
verify_token.bat
```

**Linux/Mac:**
```bash
chmod +x verify_token.sh
./verify_token.sh
```

**或直接运行:**
```bash
python verify_token.py
```

验证脚本会：
- 自动读取 `token.txt` 文件
- 测试Token是否有效
- 显示课程列表（如果Token有效）
- 给出明确的验证结果

## 📦 工具文件说明

- `capture_token.py` - Token自动捕获主脚本
- `verify_token.py` - Token验证脚本
- `start_capture.bat/sh` - 启动捕获工具的便捷脚本
- `verify_token.bat/sh` - 启动验证工具的便捷脚本
- `token.txt` - 保存捕获的Token（自动生成）
- `capture_log.txt` - 捕获过程日志（自动生成）

祝使用愉快！🎉

