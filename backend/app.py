#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI视频编辑工具 - 主应用程序
作者: AI Video Editor Team
版本: 1.0.0
"""

import os
import sys
import logging
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import yaml

# 加载环境变量
load_dotenv()

# 创建Flask应��
app = Flask(__name__)
CORS(app)

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 加载配置文件
def load_config():
    """
    从config.yml加载配置
    """
    try:
        with open('../config.yml', 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        return config
    except Exception as e:
        logger.error(f"加载配置文件失败: {e}")
        return {}

config = load_config()

# 应用配置
app.config['MAX_CONTENT_LENGTH'] = config.get('video', {}).get('max_file_size', 5000) * 1024 * 1024
app.config['UPLOAD_FOLDER'] = config.get('storage', {}).get('upload_dir', './uploads')
app.config['OUTPUT_FOLDER'] = config.get('storage', {}).get('output_dir', './outputs')

# 创建必要的文件夹
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)
os.makedirs('logs', exist_ok=True)

# 导入API蓝图
from routes import (
    video_routes,
    audio_routes,
    subtitle_routes,
    process_routes,
    health_routes
)

# 注册蓝图
app.register_blueprint(health_routes.bp, url_prefix='/api')
app.register_blueprint(video_routes.bp, url_prefix='/api/video')
app.register_blueprint(audio_routes.bp, url_prefix='/api/audio')
app.register_blueprint(subtitle_routes.bp, url_prefix='/api/subtitle')
app.register_blueprint(process_routes.bp, url_prefix='/api/process')

# 错误处理
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'status': 'error',
        'message': '请求的资源不存在',
        'code': 404
    }), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"内部错误: {error}")
    return jsonify({
        'status': 'error',
        'message': '服务器内部错误',
        'code': 500
    }), 500

@app.errorhandler(413)
def request_entity_too_large(error):
    return jsonify({
        'status': 'error',
        'message': '文件过大，请检查文件大小限制',
        'code': 413
    }), 413

# 主路由
@app.route('/')
def index():
    return jsonify({
        'status': 'success',
        'message': 'AI视频编辑工具API服务',
        'version': '1.0.0',
        'endpoints': {
            'health': '/api/health',
            'video': '/api/video',
            'audio': '/api/audio',
            'subtitle': '/api/subtitle',
            'process': '/api/process'
        }
    })

if __name__ == '__main__':
    port = config.get('app', {}).get('port', 5000)
    debug = config.get('app', {}).get('debug', True)
    
    logger.info(f"启动AI视频编辑工具 - 端口: {port}")
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug,
        use_reloader=debug
    )
