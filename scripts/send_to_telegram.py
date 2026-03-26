#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
发送报告到 Telegram
"""

import os
import sys
from pathlib import Path
import requests


def send_to_telegram(file_paths: list, message: str = None):
    """
    发送文件到 Telegram
    
    Args:
        file_paths: 文件路径列表
        message: 附加消息
    """
    # 从环境变量获取配置
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    
    if not bot_token or not chat_id:
        print('❌ 缺少 Telegram 配置')
        print('请设置环境变量:')
        print('  export TELEGRAM_BOT_TOKEN=your_bot_token')
        print('  export TELEGRAM_CHAT_ID=your_chat_id')
        return False
    
    # Telegram API URL
    url = f'https://api.telegram.org/bot{bot_token}/sendDocument'
    
    # 发送每个文件
    for file_path in file_paths:
        try:
            with open(file_path, 'rb') as f:
                files = {'document': f}
                data = {
                    'chat_id': chat_id,
                    'caption': message or f'📊 股票分析报告：{Path(file_path).name}'
                }
                
                response = requests.post(url, files=files, data=data)
                
                if response.status_code == 200:
                    print(f'✅ 发送成功：{file_path}')
                else:
                    print(f'❌ 发送失败：{response.text}')
                    
        except Exception as e:
            print(f'❌ 发送异常：{e}')
            return False
    
    return True


def main():
    """主函数"""
    # 报告文件
    report_files = [
        'output/reports/600519_moutai_report.html',
        'output/reports/000858_wuliangye_report.html'
    ]
    
    # 检查文件是否存在
    for file_path in report_files:
        if not os.path.exists(file_path):
            print(f'❌ 文件不存在：{file_path}')
            return 1
    
    # 发送消息
    message = '''📊 股票分析报告

今日生成 2 份股票分析报告：
1. 贵州茅台 (600519) - 买入评级
2. 五粮液 (000858) - 持有评级

请查收附件中的详细 HTML 报告。

生成时间：2026-03-25
生成工具：Daily Stock Analysis OpenClaw Skill
'''
    
    # 发送到 Telegram
    if send_to_telegram(report_files, message):
        print('✅ 所有报告发送成功')
        return 0
    else:
        print('❌ 发送失败')
        return 1


if __name__ == '__main__':
    sys.exit(main())
