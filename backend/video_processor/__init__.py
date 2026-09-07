#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
视频处理模块
"""

import cv2
import os
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class VideoProcessor:
    """
    视频处理类
    """
    
    def __init__(self, output_folder='./outputs'):
        self.output_folder = output_folder
        os.makedirs(output_folder, exist_ok=True)
    
    def get_video_info(self, video_path):
        """
        获取视频信息
        
        Args:
            video_path: 视频文件路径
        
        Returns:
            dict: 视频信息字典
        """
        try:
            cap = cv2.VideoCapture(video_path)
            
            if not cap.isOpened():
                logger.error(f"不能打开视频: {video_path}")
                return None
            
            # 获取视频信息
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            duration = frame_count / fps if fps > 0 else 0
            
            cap.release()
            
            return {
                'fps': fps,
                'frame_count': frame_count,
                'width': width,
                'height': height,
                'duration': duration,
                'resolution': f'{width}x{height}'
            }
        
        except Exception as e:
            logger.error(f"获取视频信息失败: {e}")
            return None
    
    def extract_frames(self, video_path, output_dir, interval=1):
        """
        从视频中提取帧
        
        Args:
            video_path: 视频文件路径
            output_dir: 输出文件夹
            interval: 提取間隔（帧数）
        
        Returns:
            list: 提取的帧文件路径列表
        """
        try:
            os.makedirs(output_dir, exist_ok=True)
            cap = cv2.VideoCapture(video_path)
            
            if not cap.isOpened():
                logger.error(f"不能打开视频: {video_path}")
                return []
            
            frame_list = []
            frame_count = 0
            extracted_count = 0
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                if frame_count % interval == 0:
                    frame_path = os.path.join(output_dir, f'frame_{extracted_count:06d}.jpg')
                    cv2.imwrite(frame_path, frame)
                    frame_list.append(frame_path)
                    extracted_count += 1
                
                frame_count += 1
            
            cap.release()
            logger.info(f"提取{extracted_count}帧，保存到: {output_dir}")
            return frame_list
        
        except Exception as e:
            logger.error(f"提取帧失败: {e}")
            return []
    
    def trim_video(self, video_path, start_time, end_time, output_path):
        """
        剪辑视频
        
        Args:
            video_path: 原视频路径
            start_time: 开始时间（秒）
            end_time: 结束时间（秒）
            output_path: 输出视频路径
        
        Returns:
            bool: 是否成功
        """
        try:
            import subprocess
            
            cmd = [
                'ffmpeg',
                '-i', video_path,
                '-ss', str(start_time),
                '-to', str(end_time),
                '-c', 'copy',
                '-y',
                output_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info(f"视频剪辑成功: {output_path}")
                return True
            else:
                logger.error(f"视频剪辑失败: {result.stderr}")
                return False
        
        except Exception as e:
            logger.error(f"剪辑视频失败: {e}")
            return False
    
    def add_text_overlay(self, video_path, text, output_path, position='center'):
        """
        添加文本水印
        
        Args:
            video_path: 视频路径
            text: 水印文本
            output_path: 输出路径
            position: 水印位置 (top, bottom, center)
        
        Returns:
            bool: 是否成功
        """
        try:
            import subprocess
            
            # 字幕位置映射
            positions = {
                'top': '(W-text_width)/2:10',
                'center': '(W-text_width)/2:(H-text_height)/2',
                'bottom': '(W-text_width)/2:H-30'
            }
            
            fontfile = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
            pos = positions.get(position, positions['center'])
            
            cmd = [
                'ffmpeg',
                '-i', video_path,
                '-vf', f"drawtext=text='{text}':fontfile={fontfile}:fontsize=24:fontcolor=white:x={pos}",
                '-codec:a', 'copy',
                '-y',
                output_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info(f"添加水印成功: {output_path}")
                return True
            else:
                logger.error(f"添加水印失败: {result.stderr}")
                return False
        
        except Exception as e:
            logger.error(f"添加水印失败: {e}")
            return False
