#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TTS文本转语音模块
"""

import os
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class TTSEngine:
    """
    文本转语音引擎
    """
    
    def __init__(self, engine='coqui', language='zh-CN', speed=1.0):
        """
        创建 TTS 引擎实例
        
        Args:
            engine: TTS引擎 ('coqui', 'bark', 'pyttsx3')
            language: 上程語言 (zh-CN, en-US, etc)
            speed: 语音速度 (0.5-2.0)
        """
        self.engine = engine
        self.language = language
        self.speed = speed
        self.output_folder = './outputs'
        os.makedirs(self.output_folder, exist_ok=True)
        
        logger.info(f"创建 TTS 引擎: {engine} ({language})")
    
    def synthesize(self, text, output_path):
        """
        合成语音
        
        Args:
            text: 要合成的文本
            output_path: 输出音频文件路径
        
        Returns:
            bool: 是否成功
        """
        try:
            if self.engine == 'coqui':
                return self._synthesize_coqui(text, output_path)
            elif self.engine == 'bark':
                return self._synthesize_bark(text, output_path)
            elif self.engine == 'pyttsx3':
                return self._synthesize_pyttsx3(text, output_path)
            else:
                logger.error(f"不支持的TTS引擎: {self.engine}")
                return False
        
        except Exception as e:
            logger.error(f"TTS合成失败: {e}")
            return False
    
    def _synthesize_coqui(self, text, output_path):
        """
        使用 Coqui TTS 合成语音
        """
        try:
            from TTS.api import TTS
            
            # 加载模型
            model_name = f"tts_models/{self.language.split('-')[0]}/glow-tts"
            tts = TTS(model_name=model_name, progress_bar=True, gpu=True)
            
            # 合成语音
            tts.tts_to_file(text=text, file_path=output_path)
            
            logger.info(f"Coqui TTS 合成成功: {output_path}")
            return True
        
        except Exception as e:
            logger.error(f"Coqui TTS 合成失败: {e}")
            return False
    
    def _synthesize_bark(self, text, output_path):
        """
        使用 Bark TTS 合成语音
        """
        try:
            from bark import SAMPLE_RATE, generate_audio, preload_models
            import scipy.io.wavfile as wavfile
            
            # 加载模型
            preload_models()
            
            # 合成语音
            audio_array = generate_audio(text)
            
            # 保存音频
            wavfile.write(output_path, SAMPLE_RATE, audio_array)
            
            logger.info(f"Bark TTS 合成成功: {output_path}")
            return True
        
        except Exception as e:
            logger.error(f"Bark TTS 合成失败: {e}")
            return False
    
    def _synthesize_pyttsx3(self, text, output_path):
        """
        使用 pyttsx3 合成语音
        """
        try:
            import pyttsx3
            
            engine = pyttsx3.init()
            engine.setProperty('rate', 150 * self.speed)  # 控制速度
            engine.save_to_file(text, output_path)
            engine.runAndWait()
            
            logger.info(f"pyttsx3 合成成功: {output_path}")
            return True
        
        except Exception as e:
            logger.error(f"pyttsx3 合成失败: {e}")
            return False
    
    def get_audio_info(self, audio_path):
        """
        获取音频信息
        
        Args:
            audio_path: 音频文件路径
        
        Returns:
            dict: 音频信息字典
        """
        try:
            import librosa
            
            audio, sr = librosa.load(audio_path)
            duration = librosa.get_duration(y=audio, sr=sr)
            
            return {
                'duration': duration,
                'sample_rate': sr,
                'channels': 1 if len(audio.shape) == 1 else audio.shape[0],
                'frame_count': len(audio)
            }
        
        except Exception as e:
            logger.error(f"获取音频信息失败: {e}")
            return None
