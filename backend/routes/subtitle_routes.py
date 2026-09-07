#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
字幕处理路由
"""

from flask import Blueprint, request, jsonify, current_app
import os
from datetime import datetime, timedelta
import uuid
from werkzeug.utils import secure_filename

bp = Blueprint('subtitle', __name__)

ALLOWED_EXTENSIONS = {'srt', 'vtt', 'ass', 'ssa'}

def allowed_file(filename):
    """
    检查字幕文件是否允许
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/upload', methods=['POST'])
def upload_subtitle():
    """
    上传字幕文件
    """
    try:
        if 'file' not in request.files:
            return jsonify({
                'status': 'error',
                'message': '未找到文件'
            }), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({
                'status': 'error',
                'message': '未选择文件'
            }), 400
        
        if not allowed_file(file.filename):
            return jsonify({
                'status': 'error',
                'message': f'不支持的文件格式。支持的格式: {ALLOWED_EXTENSIONS}'
            }), 400
        
        filename = secure_filename(file.filename)
        file_id = str(uuid.uuid4())
        file_ext = filename.rsplit('.', 1)[1].lower()
        new_filename = f"subtitle_{file_id}.{file_ext}"
        
        upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], new_filename)
        file.save(upload_path)
        
        file_size = os.path.getsize(upload_path)
        
        return jsonify({
            'status': 'success',
            'message': '字幕上传成功',
            'data': {
                'file_id': file_id,
                'filename': new_filename,
                'original_filename': filename,
                'file_size': file_size,
                'upload_time': datetime.now().isoformat()
            }
        }), 200
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'上传失败: {str(e)}'
        }), 500

@bp.route('/generate', methods=['POST'])
def generate_subtitle():
    """
    自动生成字幕
    
    请求示例:
    {
        "audio_file": "audio.wav",
        "language": "zh-CN",
        "format": "srt"
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'audio_file' not in data:
            return jsonify({
                'status': 'error',
                'message': '缺少必要参数: audio_file'
            }), 400
        
        audio_file = data.get('audio_file')
        language = data.get('language', 'zh-CN')
        output_format = data.get('format', 'srt')
        
        # TODO: 实现实际的字幕生成逻辑
        subtitle_id = str(uuid.uuid4())
        output_filename = f"subtitle_{subtitle_id}.{output_format}"
        
        return jsonify({
            'status': 'success',
            'message': '字幕生成中',
            'data': {
                'subtitle_id': subtitle_id,
                'filename': output_filename,
                'audio_file': audio_file,
                'language': language,
                'format': output_format,
                'status': 'generating'
            }
        }), 200
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'字幕生成失败: {str(e)}'
        }), 500
