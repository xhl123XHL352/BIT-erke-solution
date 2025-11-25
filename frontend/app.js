// API基础URL
const API_BASE = 'http://localhost:5000/api';

// DOM元素
const statusDot = document.getElementById('statusDot');
const statusText = document.getElementById('statusText');
const startBtn = document.getElementById('startBtn');
const stopBtn = document.getElementById('stopBtn');
const refreshBtn = document.getElementById('refreshBtn');
const configForm = document.getElementById('configForm');
const logsContainer = document.getElementById('logsContainer');
const coursesList = document.getElementById('coursesList');
const historyContainer = document.getElementById('historyContainer');
const clearLogsBtn = document.getElementById('clearLogsBtn');
const clearHistoryBtn = document.getElementById('clearHistoryBtn');
const refreshCoursesBtn = document.getElementById('refreshCoursesBtn');

// 状态更新间隔
let statusInterval = null;
let logsInterval = null;

// 初始化
document.addEventListener('DOMContentLoaded', () => {
    loadConfig();
    loadStatus();
    loadLogs();
    loadHistory();
    loadCourses();
    
    // 设置定时刷新
    statusInterval = setInterval(loadStatus, 2000);
    logsInterval = setInterval(loadLogs, 3000);
    
    // 绑定事件
    configForm.addEventListener('submit', saveConfig);
    startBtn.addEventListener('click', startMonitor);
    stopBtn.addEventListener('click', stopMonitor);
    refreshBtn.addEventListener('click', () => {
        loadStatus();
        loadCourses();
        loadHistory();
    });
    clearLogsBtn.addEventListener('click', clearLogs);
    clearHistoryBtn.addEventListener('click', clearHistory);
    refreshCoursesBtn.addEventListener('click', loadCourses);
});

// 加载配置
async function loadConfig() {
    try {
        const response = await fetch(`${API_BASE}/config`);
        const config = await response.json();
        
        document.getElementById('token').value = config.token || '';
        document.getElementById('sleepTime').value = config.sleep_time || 2;
        document.getElementById('minId').value = config.min_id || 100;
        document.getElementById('maxId').value = config.max_id || 999;
        document.getElementById('autoApply').checked = config.auto_apply !== false;
    } catch (error) {
        console.error('加载配置失败:', error);
        showError('加载配置失败: ' + error.message);
    }
}

// 保存配置
async function saveConfig(e) {
    e.preventDefault();
    
    const config = {
        token: document.getElementById('token').value.trim(),
        sleep_time: parseInt(document.getElementById('sleepTime').value),
        min_id: parseInt(document.getElementById('minId').value),
        max_id: parseInt(document.getElementById('maxId').value),
        auto_apply: document.getElementById('autoApply').checked
    };
    
    try {
        const response = await fetch(`${API_BASE}/config`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(config)
        });
        
        const result = await response.json();
        if (result.success) {
            showSuccess('配置保存成功');
            loadStatus();
        } else {
            showError(result.message || '保存失败');
        }
    } catch (error) {
        console.error('保存配置失败:', error);
        showError('保存配置失败: ' + error.message);
    }
}

// 加载状态
async function loadStatus() {
    try {
        const response = await fetch(`${API_BASE}/status`);
        const status = await response.json();
        
        // 更新状态指示器
        if (status.running) {
            statusDot.className = 'dot running';
            statusText.textContent = '运行中';
            startBtn.disabled = true;
            stopBtn.disabled = false;
        } else {
            statusDot.className = 'dot stopped';
            statusText.textContent = '已停止';
            startBtn.disabled = false;
            stopBtn.disabled = true;
        }
        
        // 更新统计信息
        document.getElementById('scanCount').textContent = status.stats.scan_count || 0;
        document.getElementById('successCount').textContent = status.stats.success_count || 0;
        document.getElementById('failCount').textContent = status.stats.fail_count || 0;
        document.getElementById('lastScanTime').textContent = status.stats.last_scan_time || '-';
    } catch (error) {
        console.error('加载状态失败:', error);
    }
}

// 启动监控
async function startMonitor() {
    try {
        const response = await fetch(`${API_BASE}/start`, {
            method: 'POST'
        });
        
        const result = await response.json();
        if (result.success) {
            showSuccess('监控已启动');
            loadStatus();
        } else {
            showError(result.message || '启动失败');
        }
    } catch (error) {
        console.error('启动监控失败:', error);
        showError('启动监控失败: ' + error.message);
    }
}

// 停止监控
async function stopMonitor() {
    if (!confirm('确定要停止监控吗？')) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/stop`, {
            method: 'POST'
        });
        
        const result = await response.json();
        if (result.success) {
            showSuccess('监控已停止');
            loadStatus();
        } else {
            showError(result.message || '停止失败');
        }
    } catch (error) {
        console.error('停止监控失败:', error);
        showError('停止监控失败: ' + error.message);
    }
}

// 加载日志
async function loadLogs() {
    try {
        const response = await fetch(`${API_BASE}/logs?limit=50`);
        const logs = await response.json();
        
        if (logs.length === 0) {
            logsContainer.innerHTML = '<div class="log-empty">暂无日志</div>';
            return;
        }
        
        logsContainer.innerHTML = logs.reverse().map(log => {
            const levelClass = log.level || 'info';
            return `
                <div class="log-entry ${levelClass}">
                    <span class="log-time">[${log.time}]</span>
                    <span class="log-message">${escapeHtml(log.message)}</span>
                </div>
            `;
        }).join('');
        
        // 自动滚动到底部
        logsContainer.scrollTop = logsContainer.scrollHeight;
    } catch (error) {
        console.error('加载日志失败:', error);
    }
}

// 清空日志
async function clearLogs() {
    if (!confirm('确定要清空所有日志吗？')) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/logs/clear`, {
            method: 'POST'
        });
        
        const result = await response.json();
        if (result.success) {
            showSuccess('日志已清空');
            loadLogs();
        }
    } catch (error) {
        console.error('清空日志失败:', error);
        showError('清空日志失败: ' + error.message);
    }
}

// 加载课程列表
async function loadCourses() {
    coursesList.innerHTML = '<div class="loading">加载中...</div>';
    
    try {
        const response = await fetch(`${API_BASE}/courses?page=1&limit=50&sign_status=2`);
        const result = await response.json();
        
        if (!result.success) {
            coursesList.innerHTML = `<div class="log-empty">${result.message || '加载失败'}</div>`;
            return;
        }
        
        const items = result.data?.data?.items || [];
        
        if (items.length === 0) {
            coursesList.innerHTML = '<div class="log-empty">暂无课程</div>';
            return;
        }
        
        coursesList.innerHTML = items.map(course => {
            const curr = parseInt(course.course_apply_count || 0);
            const max = parseInt(course.max || 0);
            const available = curr < max;
            const quotaClass = available ? 'available' : 'full';
            
            return `
                <div class="course-item">
                    <div class="course-header">
                        <div class="course-title">${escapeHtml(course.title || '未知课程')}</div>
                        <div class="course-id">ID: ${course.id}</div>
                    </div>
                    <div class="course-info">
                        <span>名额: <span class="course-quota ${quotaClass}">${curr}/${max}</span></span>
                        <span>状态: ${course.sign_status === 2 ? '进行中' : '其他'}</span>
                    </div>
                    ${available ? `
                        <div class="course-actions">
                            <button class="btn btn-sm btn-primary" onclick="manualApply(${course.id})">手动抢课</button>
                        </div>
                    ` : ''}
                </div>
            `;
        }).join('');
    } catch (error) {
        console.error('加载课程失败:', error);
        coursesList.innerHTML = `<div class="log-empty">加载失败: ${error.message}</div>`;
    }
}

// 手动抢课
async function manualApply(courseId) {
    if (!confirm(`确定要抢课 ID: ${courseId} 吗？`)) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/apply`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ course_id: courseId })
        });
        
        const result = await response.json();
        if (result.success) {
            showSuccess('抢课成功！');
            loadHistory();
            loadCourses();
        } else {
            showError(result.message || '抢课失败');
        }
    } catch (error) {
        console.error('抢课失败:', error);
        showError('抢课失败: ' + error.message);
    }
}

// 加载历史记录
async function loadHistory() {
    try {
        const response = await fetch(`${API_BASE}/history`);
        const history = await response.json();
        
        if (history.length === 0) {
            historyContainer.innerHTML = '<div class="history-empty">暂无历史记录</div>';
            return;
        }
        
        historyContainer.innerHTML = history.reverse().map(id => {
            return `
                <div class="history-item">
                    <span class="history-id">课程 ID: ${id}</span>
                    <span class="history-time">已抢课</span>
                </div>
            `;
        }).join('');
    } catch (error) {
        console.error('加载历史失败:', error);
    }
}

// 清空历史
async function clearHistory() {
    if (!confirm('确定要清空所有历史记录吗？')) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/history/clear`, {
            method: 'POST'
        });
        
        const result = await response.json();
        if (result.success) {
            showSuccess('历史记录已清空');
            loadHistory();
        }
    } catch (error) {
        console.error('清空历史失败:', error);
        showError('清空历史失败: ' + error.message);
    }
}

// 工具函数
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function showSuccess(message) {
    showNotification(message, 'success');
}

function showError(message) {
    showNotification(message, 'error');
}

function showNotification(message, type = 'info') {
    // 简单的通知实现，可以后续改进
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 12px 24px;
        background: ${type === 'success' ? '#10b981' : '#ef4444'};
        color: white;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        z-index: 1000;
        animation: slideIn 0.3s ease;
    `;
    notification.textContent = message;
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// 添加动画样式
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

