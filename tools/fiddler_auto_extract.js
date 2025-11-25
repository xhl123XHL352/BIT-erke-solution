// FiddlerScript - 自动提取Token脚本
// 使用方法：
// 1. 在Fiddler中：Rules → Customize Rules...
// 2. 将以下代码添加到 OnBeforeRequest 函数中
// 3. 修改 filePath 为你的实际路径
// 4. 保存（Ctrl+S）

static function OnBeforeRequest(oSession: Session) {
    // 检查是否是目标API
    if (oSession.hostname.Contains("qcbldekt.bit.edu.cn")) {
        // 获取Authorization头
        var authHeader = oSession.oRequest.headers["Authorization"];
        if (authHeader != null && authHeader != "") {
            try {
                // 修改为你的实际路径
                var filePath = "C:\\Users\\你的用户名\\Desktop\\erke\\tools\\token.txt";
                
                // 写入文件
                System.IO.File.WriteAllText(filePath, authHeader, System.Text.Encoding.UTF8);
                
                // 显示提示（可选，如果觉得烦可以注释掉）
                // FiddlerObject.alert("Token已保存: " + authHeader);
                
                // 在Fiddler日志中显示
                FiddlerObject.log("🎉 Token已自动保存: " + authHeader);
            } catch (e) {
                FiddlerObject.log("❌ 保存Token失败: " + e);
            }
        }
    }
}

// 可选：在响应时也检查（用于调试）
static function OnBeforeResponse(oSession: Session) {
    if (oSession.hostname.Contains("qcbldekt.bit.edu.cn")) {
        // 如果响应是401或403，说明Token可能过期
        if (oSession.responseCode == 401 || oSession.responseCode == 403) {
            FiddlerObject.log("⚠️ 警告: Token可能已过期 (HTTP " + oSession.responseCode + ")");
        }
    }
}

