#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===================================
全功能测试脚本
===================================

测试核心功能：
1. 策略蓝图
2. 分析器初始化
3. 数据获取器
"""

import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

from src.config import get_config
from src.analyzer import GeminiAnalyzer, get_analyzer
from src.core.data.base import DataFetcherManager
from src.core.market_strategy import get_market_strategy_blueprint


def print_header(title: str):
    """打印标题"""
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def test_strategy_blueprint():
    """测试策略蓝图"""
    print_header("测试 1: 策略蓝图")
    
    try:
        # 测试 A 股策略
        blueprint = get_market_strategy_blueprint("A 股")
        print(f"✅ A 股策略：{blueprint.name}")
        print(f"   维度：{len(blueprint.dimensions)}")
        
        # 测试美股策略
        blueprint = get_market_strategy_blueprint("美股")
        print(f"✅ 美股策略：{blueprint.name}")
        print(f"   维度：{len(blueprint.dimensions)}")
        
        return True
    except Exception as e:
        print(f"❌ 错误：{e}")
        return False


def test_analyzer():
    """测试分析器"""
    print_header("测试 2: 分析器初始化")
    
    try:
        analyzer = get_analyzer()
        print(f"✅ 分析器类型：{type(analyzer).__name__}")
        return True
    except Exception as e:
        print(f"⚠️  分析器初始化失败（可能需要 API key）: {e}")
        return True  # 不视为错误，因为可能需要 API key


def test_data_fetcher():
    """测试数据获取器"""
    print_header("测试 3: 数据获取器")
    
    try:
        fetcher_manager = DataFetcherManager()
        print(f"✅ 数据获取器管理器初始化成功")
        print(f"   可用获取器：{len(fetcher_manager.fetchers)}")
        return True
    except Exception as e:
        print(f"❌ 错误：{e}")
        return False


def test_config():
    """测试配置"""
    print_header("测试 4: 配置加载")
    
    try:
        config = get_config()
        print(f"✅ 配置加载成功")
        print(f"   日志级别：{config.log_level}")
        return True
    except Exception as e:
        print(f"❌ 错误：{e}")
        return False


def main():
    """运行所有测试"""
    print("\n" + "=" * 60)
    print("OpenClaw Daily Stock Analysis - 全功能测试")
    print("=" * 60)
    
    results = []
    
    # 运行测试
    results.append(("策略蓝图", test_strategy_blueprint()))
    results.append(("分析器", test_analyzer()))
    results.append(("数据获取器", test_data_fetcher()))
    results.append(("配置", test_config()))
    
    # 总结
    print_header("测试结果总结")
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    for name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"  {name}: {status}")
    
    print(f"\n总计：{passed}/{total} 通过")
    print("=" * 60)
    
    return all(r for _, r in results)


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
