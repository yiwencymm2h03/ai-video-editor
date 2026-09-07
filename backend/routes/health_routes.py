#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
健康检查路由
"""

from flask import Blueprint, jsonify
import platform
import psutil
from datetime import datetime

bp = Blueprint('health', __name__)

@bp.route('/health', methods=['GET'])
def health_check():
    """
    系统健康检查
    """
    try:
        # 获取系统信息
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'system': {
                'platform': platform.system(),
                'python_version': platform.python_version()
            },
            'resources': {
                'cpu_percent': cpu_percent,
                'memory_percent': memory.percent,
                'disk_percent': disk.percent
            }
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500

@bp.route('/info', methods=['GET'])
def info():
    """
    获取应用信息
    """
    return jsonify({
        'app_name': 'AI Video Editor',
        'version': '1.0.0',
        'description': '智能视频编辑工具，支持自动剪辑、配音、字幕',
        'api_version': 'v1'
    }), 200
