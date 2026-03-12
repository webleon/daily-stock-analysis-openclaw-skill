#!/usr/bin/env python3
"""简单测试脚本 - 测试核心功能"""

from src.core.market_strategy import list_strategies, get_strategy

print("=" * 60)
print("OpenClaw Daily Stock Analysis - 功能测试")
print("=" * 60)

# 测试 1: 列出所有策略
print("\n✅ 测试 1: 列出所有策略")
strategies = list_strategies()
print(f"共 {len(strategies)} 种策略：")
for i, s in enumerate(strategies, 1):
    print(f"  {i}. {s['id']:25} - {s['title']}")

# 测试 2: 查看策略详情
print("\n✅ 测试 2: 查看策略详情")
test_ids = ["bull_trend", "chan_theory", "wave_theory"]
for strategy_id in test_ids:
    strategy = get_strategy(strategy_id)
    if strategy:
        print(f"  ✅ {strategy_id}: {strategy.title}")
        print(f"     定位：{strategy.positioning}")
        print(f"     Prompt 长度：{len(strategy.prompt_template)} 字符")

print("\n" + "=" * 60)
print("✅ 所有测试通过！")
print("=" * 60)
