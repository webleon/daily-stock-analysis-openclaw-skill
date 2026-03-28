#!/usr/bin/env python3
"""
统一路径配置

核心原则：
1. 所有输出路径统一在此定义
2. 敏感信息 (API Keys) 从环境变量读取
3. 其他配置使用简单常量
"""

from pathlib import Path
import os


# ==================== 统一输出路径 ====================

# 统一输出根目录
OUTPUT_ROOT = Path.home() / ".openclaw" / "workspace" / "output"

# 各模块输出子目录
OUTPUT_BACKUPS = OUTPUT_ROOT / "backups"
OUTPUT_CACHE = OUTPUT_ROOT / "cache"
OUTPUT_ACCURACY = OUTPUT_ROOT / "accuracy"
OUTPUT_REPORTS = OUTPUT_ROOT / "daily-stock-analysis"
OUTPUT_LOGS = OUTPUT_ROOT / "logs"


# ==================== 敏感信息 (从环境变量读取) ====================

# AI API Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# 数据源
TUSHARE_TOKEN = os.getenv("TUSHARE_TOKEN")


# ==================== 简单配置常量 ====================

# 缓存配置 (秒)
CACHE_TTL = 3600

# 分析超时 (秒)
ANALYSIS_TIMEOUT = 300


# ==================== 自动初始化 ====================

def init():
    """创建所有输出目录"""
    for dir_path in [OUTPUT_ROOT, OUTPUT_BACKUPS, OUTPUT_CACHE, 
                     OUTPUT_ACCURACY, OUTPUT_REPORTS, OUTPUT_LOGS]:
        dir_path.mkdir(parents=True, exist_ok=True)

# 自动执行
init()


# ==================== 便捷函数 ====================

def get_cache_db() -> Path:
    """获取缓存数据库路径"""
    OUTPUT_CACHE.mkdir(parents=True, exist_ok=True)
    return OUTPUT_CACHE / "analysis.db"


def get_accuracy_db() -> Path:
    """获取准确率数据库路径"""
    OUTPUT_ACCURACY.mkdir(parents=True, exist_ok=True)
    return OUTPUT_ACCURACY / "accuracy.db"
