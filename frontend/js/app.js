/**
 * AI视频编辑工具 - 前端应用
 */

const API_BASE_URL = 'http://localhost:5000/api';

const app = {
    // 应用状态
    state: {
        videos: [],
        audios: [],
        script: '',
        settings: {
            language: 'zh-CN',
            voiceSpeed: 1.0,
            subtitlePosition: 'bottom',
            resolution: '1920x1080',
            outputFormat: 'mp4'
        },
        currentTaskId: null,
        isProcessing: false
    },

    /**
     * 初始化应用
     */
    init() {
        console.log('初始化AI视频编辑工具...');
        this.setupEventListeners();
        this.loadFromLocalStorage();
    },

    /**
     * 设置事件监听
     */
    setupEventListeners() {
        // 视频拖拽上传
        const videoDrop = document.getElementById('video-drop');
        const videoInput = document.getElementById('video-input');
        
        videoDrop.addEventListener('click', () => videoInput.click());
        videoDrop.addEventListener('dragover', (e) => this.handleDragOver(e, videoDrop));
        videoDrop.addEventListener('dragleave', (e) => this.handleDragLeave(e, videoDrop));
        videoDrop.addEventListener('drop', (e) => this.handleVideoDrop(e));
        videoInput.addEventListener('change', (e) => this.handleVideoSelect(e));

        // 音频拖拽上传
        const audioDrop = document.getElementById('audio-drop');
        const audioInput = document.getElementById('audio-input');
        
        audioDrop.addEventListener('click', () => audioInput.click());
        audioDrop.addEventListener('dragover', (e) => this.handleDragOver(e, audioDrop));
        audioDrop.addEventListener('dragleave', (e) => this.handleDragLeave(e, audioDrop));
        audioDrop.addEventListener('drop', (e) => this.handleAudioDrop(e));
        audioInput.addEventListener('change', (e) => this.handleAudioSelect(e));

        // 语音速度滑块
        const voiceSpeedSlider = document.getElementById('voice-speed');
        voiceSpeedSlider.addEventListener('input', (e) => {
            this.state.settings.voiceSpeed = parseFloat(e.target.value);
            document.getElementById('speed-display').textContent = e.target.value + 'x';
        });
    },

    /**
     * 显示标签页
     */
    showTab(tabName) {
        // 隐藏所有标签页
        document.querySelectorAll('.tab-content').forEach(tab => {
            tab.classList.remove('active');
        });
        
        // 移除所有导航按钮的active类
        document.querySelectorAll('.nav-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        
        // 显示选中的标签页
        document.getElementById(`tab-${tabName}`).classList.add('active');
        
        // 标记选中的导航按钮
        event.target.classList.add('active');
        
        // 如果是历史页面，加载历史
        if (tabName === 'history') {
            this.loadHistory();
        }
    },

    /**
     * 处理拖拽进入
     */
    handleDragOver(e, element) {
        e.preventDefault();
        e.stopPropagation();
        element.classList.add('drag-over');
    },

    /**
     * 处理拖拽离开
     */
    handleDragLeave(e, element) {
        e.preventDefault();
        e.stopPropagation();
        element.classList.remove('drag-over');
    },

    /**
     * 处理视频文件拖拽
     */
    handleVideoDrop(e) {
        e.preventDefault();
        e.stopPropagation();
        document.getElementById('video-drop').classList.remove('drag-over');
        
        const files = e.dataTransfer.files;
        this.uploadVideoFiles(files);
    },

    /**
     * 处理视频文件选择
     */
    handleVideoSelect(e) {
        const files = e.target.files;
        this.uploadVideoFiles(files);
    },

    /**
     * 上传视频文件
     */
    async uploadVideoFiles(files) {
        for (const file of files) {
            const formData = new FormData();
            formData.append('file', file);
            
            try {
                const response = await fetch(`${API_BASE_URL}/video/upload`, {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                
                if (data.status === 'success') {
                    this.state.videos.push(data.data);
                    this.renderVideoList();
                    this.showNotification(`视频 "${file.name}" 上传成功`, 'success');
                    this.saveToLocalStorage();
                } else {
                    this.showNotification(`上传失败: ${data.message}`, 'error');
                }
            } catch (error) {
                this.showNotification(`上传错误: ${error.message}`, 'error');
            }
        }
    },

    /**
     * 处理音频文件拖拽
     */
    handleAudioDrop(e) {
        e.preventDefault();
        e.stopPropagation();
        document.getElementById('audio-drop').classList.remove('drag-over');
        
        const files = e.dataTransfer.files;
        this.uploadAudioFiles(files);
    },

    /**
     * 处理音频文件选择
     */
    handleAudioSelect(e) {
        const files = e.target.files;
        this.uploadAudioFiles(files);
    },

    /**
     * 上传音频文件
     */
    async uploadAudioFiles(files) {
        for (const file of files) {
            const formData = new FormData();
            formData.append('file', file);
            
            try {
                const response = await fetch(`${API_BASE_URL}/audio/upload`, {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                
                if (data.status === 'success') {
                    this.state.audios.push(data.data);
                    this.renderAudioList();
                    this.showNotification(`音乐 "${file.name}" 上传成功`, 'success');
                    this.saveToLocalStorage();
                } else {
                    this.showNotification(`上传失败: ${data.message}`, 'error');
                }
            } catch (error) {
                this.showNotification(`上传错误: ${error.message}`, 'error');
            }
        }
    },

    /**
     * 渲染视频列表
     */
    renderVideoList() {
        const list = document.getElementById('video-list');
        list.innerHTML = '';
        
        this.state.videos.forEach((video, index) => {
            const item = document.createElement('div');
            item.className = 'file-item';
            item.innerHTML = `
                <div>
                    <div class="file-name">📹 ${video.original_filename}</div>
                    <div class="file-size">${(video.file_size / 1024 / 1024).toFixed(2)} MB</div>
                </div>
                <button class="delete-btn" onclick="app.deleteVideo(${index})">删除</button>
            `;
            list.appendChild(item);
        });
    },

    /**
     * 渲染音频列表
     */
    renderAudioList() {
        const list = document.getElementById('audio-list');
        list.innerHTML = '';
        
        this.state.audios.forEach((audio, index) => {
            const item = document.createElement('div');
            item.className = 'file-item';
            item.innerHTML = `
                <div>
                    <div class="file-name">🎵 ${audio.original_filename}</div>
                    <div class="file-size">${(audio.file_size / 1024 / 1024).toFixed(2)} MB</div>
                </div>
                <button class="delete-btn" onclick="app.deleteAudio(${index})">删除</button>
            `;
            list.appendChild(item);
        });
    },

    /**
     * 删除视频
     */
    deleteVideo(index) {
        this.state.videos.splice(index, 1);
        this.renderVideoList();
        this.saveToLocalStorage();
    },

    /**
     * 删除音频
     */
    deleteAudio(index) {
        this.state.audios.splice(index, 1);
        this.renderAudioList();
        this.saveToLocalStorage();
    },

    /**
     * 保存脚本
     */
    saveScript() {
        const scriptText = document.getElementById('script-text').value;
        if (!scriptText.trim()) {
            this.showNotification('请输入脚本内容', 'error');
            return;
        }
        
        this.state.script = scriptText;
        this.saveToLocalStorage();
        this.showNotification('脚本已保存', 'success');
    },

    /**
     * 更新设置
     */
    updateSettings() {
        this.state.settings.language = document.getElementById('language').value;
        this.state.settings.voiceSpeed = parseFloat(document.getElementById('voice-speed').value);
        this.state.settings.subtitlePosition = document.getElementById('subtitle-position').value;
        this.state.settings.resolution = document.getElementById('resolution').value;
        this.state.settings.outputFormat = document.getElementById('output-format').value;
        
        this.saveToLocalStorage();
    },

    /**
     * 开始处理
     */
    async startProcessing() {
        // 验证
        if (this.state.videos.length === 0) {
            this.showNotification('请至少上传一个视频文件', 'error');
            return;
        }
        
        if (!this.state.script) {
            this.showNotification('请输入脚本内容', 'error');
            return;
        }
        
        // 准备数据
        const processData = {
            video_files: this.state.videos.map(v => v.filename),
            script: this.state.script,
            audio_file: this.state.audios.length > 0 ? this.state.audios[0].filename : null,
            settings: this.state.settings
        };
        
        // 显示进度条
        document.getElementById('progress-modal').classList.remove('hidden');
        this.state.isProcessing = true;
        
        try {
            // 调用处理API
            const response = await fetch(`${API_BASE_URL}/process/start`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(processData)
            });
            
            const data = await response.json();
            
            if (data.status === 'success') {
                this.state.currentTaskId = data.data.task_id;
                this.showNotification('处理任务已启动', 'success');
                
                // 定期检查处理状态
                this.pollTaskStatus();
            } else {
                this.showNotification(`处理失败: ${data.message}`, 'error');
                document.getElementById('progress-modal').classList.add('hidden');
                this.state.isProcessing = false;
            }
        } catch (error) {
            this.showNotification(`错误: ${error.message}`, 'error');
            document.getElementById('progress-modal').classList.add('hidden');
            this.state.isProcessing = false;
        }
    },

    /**
     * 轮询任务状态
     */
    async pollTaskStatus() {
        if (!this.state.isProcessing || !this.state.currentTaskId) return;
        
        try {
            const response = await fetch(`${API_BASE_URL}/process/status/${this.state.currentTaskId}`);
            const data = response.json();
            
            const taskData = data.data;
            
            // 更新进度条
            const progress = taskData.progress || 0;
            document.getElementById('progress-fill').style.width = progress + '%';
            document.getElementById('progress-text').textContent = `处理进度: ${progress}%`;
            
            // 更新步骤状态
            this.updateStepStatus(taskData.steps);
            
            // 检查是否完成
            if (taskData.status === 'completed') {
                this.handleProcessingComplete(taskData);
            } else if (taskData.status === 'failed') {
                this.handleProcessingError(taskData);
            } else {
                // 继续轮询
                setTimeout(() => this.pollTaskStatus(), 2000);
            }
        } catch (error) {
            console.error('获取任务状态失败:', error);
            setTimeout(() => this.pollTaskStatus(), 2000);
        }
    },

    /**
     * 更新步骤状态
     */
    updateStepStatus(steps) {
        Object.keys(steps).forEach(stepName => {
            const stepElement = document.getElementById(`step-${stepName}`);
            if (stepElement) {
                const stepData = steps[stepName];
                stepElement.classList.remove('active', 'completed');
                
                if (stepData.status === 'processing') {
                    stepElement.classList.add('active');
                } else if (stepData.status === 'completed') {
                    stepElement.classList.add('completed');
                }
            }
        });
    },

    /**
     * 处理完成
     */
    handleProcessingComplete(taskData) {
        document.getElementById('progress-fill').style.width = '100%';
        document.getElementById('progress-text').textContent = '处理完成！';
        
        this.state.isProcessing = false;
        
        // 显示完成提示
        setTimeout(() => {
            this.showNotification('视频处理完成！', 'success');
            document.getElementById('progress-modal').classList.add('hidden');
            this.loadHistory();
        }, 1500);
    },

    /**
     * 处理错误
     */
    handleProcessingError(taskData) {
        this.state.isProcessing = false;
        this.showNotification(`处理失败: ${taskData.error}`, 'error');
        document.getElementById('progress-modal').classList.add('hidden');
    },

    /**
     * 取消处理
     */
    async cancelProcessing() {
        if (!this.state.currentTaskId) return;
        
        try {
            const response = await fetch(`${API_BASE_URL}/process/cancel/${this.state.currentTaskId}`, {
                method: 'POST'
            });
            
            const data = await response.json();
            this.showNotification('处理已取消', 'info');
            document.getElementById('progress-modal').classList.add('hidden');
            this.state.isProcessing = false;
        } catch (error) {
            this.showNotification(`取消失败: ${error.message}`, 'error');
        }
    },

    /**
     * 加载处理历史
     */
    async loadHistory() {
        try {
            const response = await fetch(`${API_BASE_URL}/process/history`);
            const data = await response.json();
            
            const historyList = document.getElementById('history-list');
            historyList.innerHTML = '';
            
            if (data.data.tasks.length === 0) {
                historyList.innerHTML = '<p class="empty-message">暂无处理历史</p>';
                return;
            }
            
            data.data.tasks.forEach(task => {
                const item = document.createElement('div');
                item.className = 'history-item';
                
                const statusClass = `status-${task.status}`;
                const statusText = this.getStatusText(task.status);
                
                item.innerHTML = `
                    <div class="history-item-header">
                        <div class="history-item-title">${task.input.script.substring(0, 50)}...</div>
                        <span class="history-item-status ${statusClass}">${statusText}</span>
                    </div>
                    <div class="history-item-details">
                        <p>创建时间: ${new Date(task.created_at).toLocaleString()}</p>
                        <p>进度: ${task.progress}%</p>
                    </div>
                `;
                historyList.appendChild(item);
            });
        } catch (error) {
            console.error('加载历史失败:', error);
        }
    },

    /**
     * 获取状态文本
     */
    getStatusText(status) {
        const statusMap = {
            'processing': '处理中',
            'completed': '已完成',
            'failed': '失败',
            'cancelled': '已取消'
        };
        return statusMap[status] || status;
    },

    /**
     * 显示通知
     */
    showNotification(message, type = 'info') {
        const notification = document.getElementById('notification');
        notification.textContent = message;
        notification.className = `notification ${type}`;
        notification.classList.remove('hidden');
        
        // 3秒后隐藏
        setTimeout(() => {
            notification.classList.add('hidden');
        }, 3000);
    },

    /**
     * 保存到本地存储
     */
    saveToLocalStorage() {
        localStorage.setItem('aiVideoEditorState', JSON.stringify(this.state));
    },

    /**
     * 从本地存储加载
     */
    loadFromLocalStorage() {
        const saved = localStorage.getItem('aiVideoEditorState');
        if (saved) {
            try {
                this.state = JSON.parse(saved);
                this.renderVideoList();
                this.renderAudioList();
                document.getElementById('script-text').value = this.state.script;
            } catch (error) {
                console.error('加载本地存储失败:', error);
            }
        }
    }
};

// 页面加载时初始化
document.addEventListener('DOMContentLoaded', () => {
    app.init();
});
