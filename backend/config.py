#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置管理模块
"""

import os
import yaml
from pathlib import Path

class Config:
    """
    基础配置类
    """
    
    # Flask配置
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('DEBUG', True)
    
    # 文件上传配置
    MAX_CONTENT_LENGTH = 5000 * 1024 * 1024  # 5GB
    UPLOAD_FOLDER = './uploads'
    OUTPUT_FOLDER = './outputs'
    TEMP_FOLDER = './temp'
    
    # 支持的文件格式
    ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'mov', 'avi', 'mkv', 'flv', 'wmv'}
    ALLOWED_AUDIO_EXTENSIONS = {'mp3', 'wav', 'aac', 'flac', 'm4a'}
    ALLOWED_SCRIPT_EXTENSIONS = {'txt', 'srt', 'json'}
    
    # 视频处理配置
    VIDEO_FPS = 30
    VIDEO_RESOLUTION = '1920x1080'
    VIDEO_BITRATE = '5000k'
    AUDIO_SAMPLE_RATE = 44100
    AUDIO_CHANNELS = 2
    AUDIO_BITRATE = '192k'
    
    # TTS配置
    TTS_ENGINE = 'coqui'  # 'coqui', 'bark', 'pyttsx3'
    TTS_LANGUAGE = 'zh-CN'
    TTS_VOICE_SPEED = 1.0
    
    # 字幕配置
    SUBTITLE_FONT_SIZE = 24
    SUBTITLE_FONT_FAMILY = 'Arial'
    SUBTITLE_COLOR = '#FFFFFF'
    SUBTITLE_BG_COLOR = '#000000'
    SUBTITLE_OPACITY = 0.8
    
    # 转场效果配置
    TRANSITION_DURATION = 0.5
    TRANSITION_TYPES = ['fade', 'slide', 'wipe', 'crossfade']
    
    @staticmethod
    def load_from_yaml(config_path='../config.yml'):
        """
        从YAML文件加载配置
        """
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config_data = yaml.safe_load(f)
            return config_data
        except Exception as e:
            print(f"加载配置文件失败: {e}")
            return {}

class DevelopmentConfig(Config):
    """
    开发环境配置
    """
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """
    生产环境配置
    """
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    """
    测试环境配置
    """
    DEBUG = True
    TESTING = True
    UPLOAD_FOLDER = './test_uploads'
    OUTPUT_FOLDER = './test_outputs'

# 根据环境变量选择配置
config_env = os.getenv('FLASK_ENV', 'development')

if config_env == 'production':
    config = ProductionConfig()
elif config_env == 'testing':
    config = TestingConfig()
else:
    config = DevelopmentConfig()
