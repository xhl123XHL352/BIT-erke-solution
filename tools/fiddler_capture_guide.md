# Fiddler抓包指南 - 电脑微信小程序

本指南介绍如何使用Fiddler在电脑微信中抓取小程序Token。

## 📋 准备工作

1. **下载安装Fiddler**
   - 访问：https://www.telerik.com/fiddler
   - 下载并安装Fiddler Classic（免费版）

2. **确保已安装微信PC版**
   - 确保微信已登录

## 🚀 详细步骤

### 第一步：配置Fiddler

1. **启动Fiddler**
   - 打开Fiddler应用

2. **配置HTTPS解密**
   - 菜单栏：`Tools` → `Options` → `HTTPS` 标签
   - 勾选 `Decrypt HTTPS traffic`
   - 勾选 `Ignore server certificate errors`
   - 点击 `Actions` → `Export Root Certificate to Desktop`
   - 证书会导出到桌面，文件名为 `FiddlerRoot.cer`

3. **配置监听端口**
   - 菜单栏：`Tools` → `Options` → `Connections` 标签
   - 确认 `Fiddler listens on port` 为 `8888`（默认）
   - 勾选 `Allow remote computers to connect`（如果需要）

4. **安装证书到系统**
   - 双击桌面上的 `FiddlerRoot.cer` 文件
   - 点击"安装证书"
   - 选择"本地计算机" → 下一步
   - 选择"将所有证书都放入下列存储" → 浏览 → 选择"受信任的根证书颁发机构" → 确定
   - 完成安装

### 第二步：配置微信代理

微信PC版需要通过系统代理或环境变量来使用Fiddler。

#### 方法一：通过系统代理（推荐）

1. **设置系统代理**
   - Windows设置 → 网络和Internet → 代理
   - 手动代理设置：
     - 打开"使用代理服务器"
     - 地址：`127.0.0.1`
     - 端口：`8888`
     - 保存

2. **重启微信**
   - 完全关闭微信（包括后台进程）
   - 重新启动微信

#### 方法二：通过环境变量（备选）

如果方法一不行，可以设置环境变量：

1. **设置环境变量**
   - 右键"此电脑" → 属性 → 高级系统设置 → 环境变量
   - 在"用户变量"或"系统变量"中添加：
     - 变量名：`HTTP_PROXY`
     - 变量值：`http://127.0.0.1:8888`
   - 再添加：
     - 变量名：`HTTPS_PROXY`
     - 变量值：`http://127.0.0.1:8888`

2. **重启微信**
   - 完全关闭微信
   - 重新启动微信

### 第三步：在Fiddler中过滤请求

1. **设置过滤器**
   - 在Fiddler底部输入框输入：`qcbldekt.bit.edu.cn`
   - 或使用过滤器：
     - 菜单栏：`Rules` → `Customize Rules...`
     - 在 `OnBeforeRequest` 函数中添加：
     ```javascript
     if (!oSession.hostname.Contains("qcbldekt.bit.edu.cn")) {
         oSession["ui-hide"] = "true";
     }
     ```
   - 保存（Ctrl+S）

2. **清空现有请求**
   - 菜单栏：`Edit` → `Remove` → `All Sessions`
   - 或按 `Ctrl+X`

### 第四步：捕获Token

1. **在微信中打开小程序**
   - 打开微信
   - 找到课程系统小程序
   - 点击进入，访问课程列表页面

2. **在Fiddler中查看请求**
   - 在Fiddler主窗口的请求列表中，找到 `qcbldekt.bit.edu.cn` 的请求
   - 通常会有多个请求，找到 `/api/course/list` 相关的请求

3. **查看请求头**
   - 点击目标请求
   - 在右侧面板切换到 `Headers` 或 `Raw` 标签
   - 找到 `Authorization` 字段
   - 复制完整内容（例如：`Bearer 517196|E8m5blSrtgMfwYzu34rklcaSdamO34gwUWReRIPd`）

4. **保存Token**
   - 将Token保存到 `tools/token.txt` 文件
   - 或直接复制到抢课系统配置中

### 第五步：验证Token

使用验证脚本验证Token是否有效：

```bash
cd tools
python verify_token.py
```

## 🔧 高级技巧

### 使用FiddlerScript自动提取Token

可以编写FiddlerScript自动提取并保存Token：

1. **打开FiddlerScript编辑器**
   - 菜单栏：`Rules` → `Customize Rules...`

2. **添加以下代码到 `OnBeforeRequest` 函数中**
   ```javascript
   static function OnBeforeRequest(oSession: Session) {
       // 检查是否是目标API
       if (oSession.hostname.Contains("qcbldekt.bit.edu.cn")) {
           // 获取Authorization头
           var authHeader = oSession.oRequest.headers["Authorization"];
           if (authHeader != null && authHeader != "") {
               // 保存到文件
               var filePath = "C:\\Users\\你的用户名\\Desktop\\erke\\tools\\token.txt";
               System.IO.File.WriteAllText(filePath, authHeader);
               FiddlerObject.alert("Token已保存: " + authHeader);
           }
       }
   }
   ```

3. **修改文件路径**
   - 将 `filePath` 改为你的实际路径

4. **保存脚本**
   - 按 `Ctrl+S` 保存

### 使用过滤器只显示目标请求

在Fiddler底部过滤器输入：
```
qcbldekt.bit.edu.cn
```

或者使用正则表达式：
```
regex:(?insx).*qcbldekt\.bit\.edu\.cn.*
```

## ⚠️ 常见问题

### 问题1：微信无法连接网络

**原因**：代理配置不正确或证书未安装

**解决方法**：
1. 检查系统代理设置是否正确
2. 确认Fiddler正在运行
3. 重新安装Fiddler证书到系统
4. 重启微信

### 问题2：Fiddler中看不到微信请求

**原因**：微信未使用代理或代理配置错误

**解决方法**：
1. 确认系统代理已设置（127.0.0.1:8888）
2. 完全关闭微信后重新启动
3. 检查Fiddler是否在监听8888端口
4. 尝试设置环境变量方式

### 问题3：HTTPS请求显示Tunnel to

**原因**：证书未正确安装或Fiddler未启用HTTPS解密

**解决方法**：
1. 确认Fiddler中已勾选 `Decrypt HTTPS traffic`
2. 重新安装Fiddler证书到系统
3. 重启Fiddler和微信

### 问题4：找不到Authorization头

**原因**：请求被过滤或查看位置不对

**解决方法**：
1. 清除Fiddler过滤器
2. 在Headers标签中查看Request Headers部分
3. 确认访问了课程列表页面
4. 查看Raw标签查看完整请求

## 💡 提示

1. **使用过滤器**
   - 设置过滤器可以快速找到目标请求
   - 避免在大量请求中查找

2. **保存会话**
   - 可以保存Fiddler会话以便后续分析
   - 菜单栏：`File` → `Save` → `All Sessions`

3. **使用搜索功能**
   - 在Fiddler中按 `Ctrl+F` 搜索 "Authorization"
   - 可以快速定位包含Token的请求

4. **关闭代理**
   - 使用完毕后记得关闭系统代理
   - 避免影响其他应用

## 📝 快速检查清单

- [ ] Fiddler已安装并运行
- [ ] HTTPS解密已启用
- [ ] Fiddler证书已安装到系统
- [ ] 系统代理已设置为 127.0.0.1:8888
- [ ] 微信已重启
- [ ] 在微信中打开了小程序
- [ ] 在Fiddler中找到了目标请求
- [ ] 已复制Authorization头
- [ ] Token已保存或配置到系统

祝使用愉快！🎉

