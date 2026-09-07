# AI 视频自动剪辑工具

一个智能的视频编辑工具，能够根据脚本、文字和视频素材自动生成完整的视频作品。

## 主要功能

✅ **视频素材管理** - 上传和管理多个视频片段
✅ **脚本处理** - 导入脚本并自动分析
✅ **自动配音** - 文本转语音（TTS）生成自然配音
✅ **智能字幕** - 自动生成和同步字幕
✅ **自动剪辑** - 根据脚本智能匹配和剪辑视频片段
✅ **转场效果** - 自动添加平滑的转场和过渡效果
✅ **背景音乐** - 自动添加和混音背景音乐
✅ **视频导出** - 支持多种格式和分辨率导出

## 项目结构

```
ai-video-editor/
├── backend/              # Python后端服务
│   ├── app.py           # Flask主应用
│   ├── config.py        # 配置文件
│   ├── requirements.txt  # Python依赖
���   ├── video_processor/  # 视频处理模块
│   ├── tts_engine/       # 语音合成模块
│   ├── subtitle_gen/     # 字幕生成模块
│   └── auto_edit/        # 自动剪辑模块
├── frontend/             # 前端Web应用
│   ├── index.html
│   ├── css/
│   ├── js/
│   └── assets/
├── uploads/              # 上传的文件临时存储
├── outputs/              # 生成的视频输出
└── config.yml            # 全局配置
```

## 快速开始

### 需求
- Python 3.8+
- Node.js 14+
- FFmpeg
- CUDA（可选，用于GPU加速）

### 后端安装

```bash
cd backend
pip install -r requirements.txt
python app.py
```

### 前端安装

```bash
cd frontend
npm install
npm start
```

## 使用流程

1. **上传素材** - 上传视频片段、音乐和图片
2. **导入脚本** - 上传脚本文本文件或直接输入
3. **设置参数** - 配置语言、声音、字幕样式等
4. **自动处理** - 系统自动生成配音、字幕、剪辑
5. **预览编辑** - 预览效果并进行微调
6. **导出视频** - 选择格式和分辨率导出最终视频

## API接口

### POST /api/upload
上传视频素材

### POST /api/process
处理脚本和生成视频

### GET /api/status/:taskId
获取处理进度

### POST /api/export
导出最终视频

## 配置说明

详见 `config.yml`

## 依赖库

- **FFmpeg** - 视频处理
- **MoviePy** - 视频编辑
- **Coqui TTS** - 文本转语音
- **SpeechRecognition** - 音频处理
- **OpenCV** - 视频分析
- **Flask** - Web框架
- **Vue.js/React** - 前端框架

## 许可证

MIT

## 贡献

欢迎提交 Issue 和 Pull Request！
