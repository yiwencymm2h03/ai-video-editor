#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
字幕生成模块
"""

import os
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class SubtitleGenerator:
    """
    自动字幕生成类
    """
    
    def __init__(self, output_folder='./outputs'):
        self.output_folder = output_folder
        os.makedirs(output_folder, exist_ok=True)
    
    def generate_from_audio(self, audio_path, language='zh-CN', output_format='srt'):
        """
        从音频自动生成字幕
        
        Args:
            audio_path: 音频文件路径
            language: 識別語言
            output_format: 输出格式 (srt, vtt, ass)
        
        Returns:
            str: 字幕文件路径
        """
        try:
            import speech_recognition as sr
            
            recognizer = sr.Recognizer()
            
            # 加载音频文件
            with sr.AudioFile(audio_path) as source:
                audio = recognizer.record(source)
            
            # 执行識别
            text = recognizer.recognize_google(audio, language=language)
            
            # 生成字幕文件
            output_path = os.path.join(self.output_folder, f'subtitle.{output_format}')
            
            if output_format == 'srt':
                self._generate_srt(text, output_path)
            elif output_format == 'vtt':
                self._generate_vtt(text, output_path)
            elif output_format == 'ass':
                self._generate_ass(text, output_path)
            
            logger.info(f"字幕生成成功: {output_path}")
            return output_path
        
        except Exception as e:
            logger.error(f"字幕生成失败: {e}")
            return None
    
    def _generate_srt(self, text, output_path):
        """
        生成 SRT 格式字幕
        """
        try:
            srt_content = """1
00:00:00,000 --> 00:00:05,000
{}
""".format(text)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(srt_content)
        
        except Exception as e:
            logger.error(f"SRT字幕生成失败: {e}")
    
    def _generate_vtt(self, text, output_path):
        """
        生成 VTT 格式字幕
        """
        try:
            vtt_content = """WEBVTT

00:00:00.000 --> 00:00:05.000
{}
""".format(text)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(vtt_content)
        
        except Exception as e:
            logger.error(f"VTT字幕生成失败: {e}")
    
    def _generate_ass(self, text, output_path):
        """
        生成 ASS 格式字幕
        """
        try:
            ass_header = """[Script Info]
Title: Generated Subtitle

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,20,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,2,0,2,10,10,10,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
            
            ass_content = ass_header + f"""Dialogue: 0,0:00:00.00,0:00:05.00,Default,,0,0,0,,{text}
"""
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(ass_content)
        
        except Exception as e:
            logger.error(f"ASS字幕生成失败: {e}")
    
    def parse_subtitle_file(self, subtitle_path):
        """
        解析字幕文件
        
        Args:
            subtitle_path: 字幕文件路径
        
        Returns:
            list: 字幕条目列表
        """
        try:
            import pysrt
            
            subtitles = pysrt.open(subtitle_path)
            subtitle_list = []
            
            for sub in subtitles:
                subtitle_list.append({
                    'index': sub.index,
                    'start': str(sub.start),
                    'end': str(sub.end),
                    'text': sub.text
                })
            
            logger.info(f"成功解析{len(subtitle_list)}条字幕")
            return subtitle_list
        
        except Exception as e:
            logger.error(f"字幕文件解析失败: {e}")
            return []
