#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多 Agent 升级提示演示脚本
演示普通分析后主动提示深度分析功能
"""

import sys
from pathlib import Path

# 添加模块路径
sys.path.insert(0, str(Path(__file__).parent))

from src.analyzer import GeminiAnalyzer


def demo_upgrade_prompt():
    """演示升级提示功能"""
    
    print("=" * 70)
    print("多 Agent 升级提示演示")
    print("=" * 70)
    print()
    
    # 测试用例
    test_cases = [
        ("AAPL", None, "无评分提示"),
        ("NVDA", 55, "低评分提示"),
        ("TSLA", 68, "中评分提示"),
        ("MSFT", 82, "高评分提示"),
    ]
    
    for stock_code, score, description in test_cases:
        print(f"\n### {description}: {stock_code}")
        print("-" * 70)
        
        prompt = GeminiAnalyzer.get_multi_agent_upgrade_prompt(stock_code, score)
        print(prompt)
        
        if score:
            print(f"(当前评分：{score}/100)")
        print()


def demo_full_flow():
    """演示完整流程"""
    
    print("\n" + "=" * 70)
    print("完整流程演示")
    print("=" * 70)
    print()
    
    # 模拟用户请求
    user_request = "分析 AAPL"
    print(f"用户：{user_request}")
    print()
    
    # 普通分析
    print("AI: 正在进行普通分析...（30 秒）")
    print("AI: 分析完成！")
    print()
    print("AI: AAPL 综合评分：72/100")
    print("AI: 操作建议：买入")
    print("AI: 第一买点：$168.80")
    print()
    
    # 主动提示
    print("AI: " + "-" * 60)
    prompt = GeminiAnalyzer.get_multi_agent_upgrade_prompt("AAPL", score=72)
    print(prompt)


if __name__ == "__main__":
    # 演示升级提示
    demo_upgrade_prompt()
    
    # 演示完整流程
    demo_full_flow()
    
    print("\n" + "=" * 70)
    print("演示完成！")
    print("=" * 70)
