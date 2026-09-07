#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
视频处理路由
"""

from flask import Blueprint, request, jsonify, current_app
import os
from werkzeug.utils import secure_filename
from datetime import datetime
import uuid

bp = Blueprint('video', __name__)

ALLOWED_EXTENSIONS = {'mp4', 'mov', 'avi', 'mkv', 'flv', 'wmv'}

def allowed_file(filename):
    """
    检查文件是否允许
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/upload', methods=['POST'])
def upload_video():
    """
    上传视频文件
    
    请求示例:
    curl -X POST -F 'file=@video.mp4' http://localhost:5000/api/video/upload
    """
    try:
        # 检查是否有文件
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
        
        # 保存文件
        filename = secure_filename(file.filename)
        file_id = str(uuid.uuid4())
        file_ext = filename.rsplit('.', 1)[1].lower()
        new_filename = f"{file_id}.{file_ext}"
        
        upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], new_filename)
        file.save(upload_path)
        
        # 获取文件信息
        file_size = os.path.getsize(upload_path)
        
        return jsonify({
            'status': 'success',
            'message': '视频上传成功',
            'data': {
                'file_id': file_id,
                'filename': new_filename,
                'original_filename': filename,
                'file_size': file_size,
                'upload_time': datetime.now().isoformat(),
                'file_path': f'/uploads/{new_filename}'
            }
        }), 200
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'上传失败: {str(e)}'
        }), 500

@bp.route('/list', methods=['GET'])
def list_videos():
    """
    列出所有已上传的视频
    """
    try:
        upload_folder = current_app.config['UPLOAD_FOLDER']
        videos = []
        
        if os.path.exists(upload_folder):
            for filename in os.listdir(upload_folder):
                file_path = os.path.join(upload_folder, filename)
                if os.path.isfile(file_path):
                    file_size = os.path.getsize(file_path)
                    file_stat = os.stat(file_path)
                    
                    videos.append({
                        'filename': filename,
                        'file_size': file_size,
                        'upload_time': datetime.fromtimestamp(file_stat.st_ctime).isoformat()
                    })
        
        return jsonify({
            'status': 'success',
            'data': {
                'total': len(videos),
                'videos': videos
            }
        }), 200
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'获取视频列表失败: {str(e)}'
        }), 500

@bp.route('/delete/<file_id>', methods=['DELETE'])
def delete_video(file_id):
    """
    删除上传的视频
    """
    try:
        # 在实际应用中，应该使用数据库来存储file_id到filename的映射
        # 这里为了演示，假设file_id就是文件名的前缀
        upload_folder = current_app.config['UPLOAD_FOLDER']
        
        # 查找匹配的文件
        for filename in os.listdir(upload_folder):
            if filename.startswith(file_id):
                file_path = os.path.join(upload_folder, filename)
                os.remove(file_path)
                
                return jsonify({
                    'status': 'success',
                    'message': f'视频 {filename} 删除成功'
                }), 200
        
        return jsonify({
            'status': 'error',
            'message': '找不到该视频'
        }), 404
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'删除失败: {str(e)}'
        }), 500
