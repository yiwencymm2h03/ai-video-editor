#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动剪辑模块
"""

import os
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class AutoEditor:
    """
    自动视频剪辑类
    """
    
    def __init__(self, output_folder='./outputs'):
        self.output_folder = output_folder
        os.makedirs(output_folder, exist_ok=True)
    
    def analyze_script(self, script_text):
        """
        分析脚本文本
        
        Args:
            script_text: 脚本文本
        
        Returns:
            dict: 脚本分析结果
        """
        try:
            # 按段落分割脚本
            segments = script_text.strip().split('\n\n')
            
            script_segments = []
            for i, segment in enumerate(segments):
                script_segments.append({
                    'index': i,
                    'text': segment.strip(),
                    'duration': len(segment.split()) * 0.5  # 算法: 每个字~0.5秒
                })
            
            logger.info(f"分析脚本成功: {len(script_segments)}个段落")
            return {
                'total_segments': len(script_segments),
                'total_duration': sum([s['duration'] for s in script_segments]),
                'segments': script_segments
            }
        
        except Exception as e:
            logger.error(f"脚本分析失败: {e}")
            return None
    
    def match_clips_to_script(self, video_files, script_segments):
        """
        将视频片段匹配到脚本
        
        Args:
            video_files: 视频文件列表
            script_segments: 脚本段落
        
        Returns:
            list: 匹配结果
        """
        try:
            from video_processor import VideoProcessor
            
            processor = VideoProcessor()
            matches = []
            
            for i, segment in enumerate(script_segments):
                if i < len(video_files):
                    video_info = processor.get_video_info(video_files[i])
                    
                    matches.append({
                        'script_index': segment['index'],
                        'script_text': segment['text'],
                        'script_duration': segment['duration'],
                        'video_file': video_files[i],
                        'video_duration': video_info['duration'] if video_info else 0,
                        'match_score': 0.8  # 简化的匹配分数
                    })
            
            logger.info(f"匹配成功: {len(matches)}条匹配记录")
            return matches
        
        except Exception as e:
            logger.error(f"片段匹配失败: {e}")
            return []
    
    def create_composition(self, matches, audio_file=None, subtitle_file=None):
        """
        根据匹配结果创建简会
        
        Args:
            matches: 匹配结果列表
            audio_file: 背景音乐文件
            subtitle_file: 字幕文件
        
        Returns:
            dict: 简会信息
        """
        try:
            from moviepy.editor import VideoFileClip, concatenate_videoclips, AudioFileClip
            
            clips = []
            
            # 加载视频片段
            for match in matches:
                video_clip = VideoFileClip(match['video_file'])
                # 根据脚本执行时间调整视频或剪辑
                clips.append(video_clip)
            
            if not clips:
                logger.error("不有有效的视频片段")
                return None
            
            # 简会视频
            final_clip = concatenate_videoclips(clips)
            
            # 添加音频
            if audio_file and os.path.exists(audio_file):
                audio = AudioFileClip(audio_file)
                final_clip = final_clip.set_audio(audio)
            
            logger.info("简会创建成功")
            return {
                'clip': final_clip,
                'duration': final_clip.duration,
                'width': final_clip.w,
                'height': final_clip.h,
                'fps': final_clip.fps
            }
        
        except Exception as e:
            logger.error(f"简会创建失败: {e}")
            return None
