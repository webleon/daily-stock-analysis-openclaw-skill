#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
大盘复盘 - 直接输出到控制台
"""

import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.config import get_config
from src.notification import NotificationService
from src.market_analyzer import MarketAnalyzer
from src.analyzer import GeminiAnalyzer
from src.search_service import SearchService

def main():
    config = get_config()
    
    # 创建必要的服务
    notifier = NotificationService(config)
    analyzer = GeminiAnalyzer(config) if hasattr(config, 'gemini_api_key') and config.gemini_api_key else None
    search_service = SearchService(config) if hasattr(config, 'tavily_api_key') and config.tavily_api_key else None
    
    # 执行 A 股大盘复盘
    print("=" * 60)
    print("📊 正在生成 A 股大盘复盘报告...")
    print("=" * 60)
    
    cn_analyzer = MarketAnalyzer(
        search_service=search_service,
        analyzer=analyzer,
        region='cn'
    )
    cn_report = cn_analyzer.run_daily_review()
    
    if cn_report:
        print("\n" + cn_report)
    else:
        print("\n❌ A 股大盘复盘生成失败")
    
    print("\n" + "=" * 60)
    print("📊 正在生成美股大盘复盘报告...")
    print("=" * 60)
    
    # 执行美股大盘复盘
    us_analyzer = MarketAnalyzer(
        search_service=search_service,
        analyzer=analyzer,
        region='us'
    )
    us_report = us_analyzer.run_daily_review()
    
    if us_report:
        print("\n" + us_report)
    else:
        print("\n❌ 美股大盘复盘生成失败")

if __name__ == "__main__":
    main()
