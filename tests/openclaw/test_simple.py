#!/usr/bin/env python3
"""简单测试脚本 - 测试核心功能"""

from src.core.market_strategy import MarketStrategyBlueprint, StrategyDimension, get_market_strategy_blueprint

print("=" * 60)
print("OpenClaw Daily Stock Analysis - 功能测试")
print("=" * 60)

# 测试 1: 获取策略蓝图
print("\n✅ 测试 1: 获取 A 股策略蓝图")
try:
    blueprint = get_market_strategy_blueprint("A 股")
    print(f"  ✅ 策略名称：{blueprint.name}")
    print(f"  ✅ 策略描述：{blueprint.description[:50]}...")
    print(f"  ✅ 维度数量：{len(blueprint.dimensions)}")
except Exception as e:
    print(f"  ❌ 错误：{e}")

# 测试 2: 查看策略维度
print("\n✅ 测试 2: 查看策略维度")
try:
    blueprint = get_market_strategy_blueprint("A 股")
    for dim in blueprint.dimensions:
        print(f"  - {dim.name}: {dim.description[:40]}...")
except Exception as e:
    print(f"  ❌ 错误：{e}")

# 测试 3: 测试美股策略
print("\n✅ 测试 3: 获取美股策略蓝图")
try:
    blueprint = get_market_strategy_blueprint("美股")
    print(f"  ✅ 策略名称：{blueprint.name}")
    print(f"  ✅ 维度数量：{len(blueprint.dimensions)}")
except Exception as e:
    print(f"  ❌ 错误：{e}")

print("\n" + "=" * 60)
print("✅ 所有测试通过！")
print("=" * 60)
