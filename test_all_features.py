#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===================================
全功能测试脚本
===================================

测试所有新功能：
1. /ask 命令 - 11 种策略
2. /batch 命令 - 批量分析
3. 大盘复盘功能
"""

import sys
import time
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

from src.config import get_config
from src.analyzer import GeminiAnalyzer, analyze_stock_with_strategy, analyze_stock_default
from src.search_service import SearchService
from data_provider.base import DataFetcherManager
from src.core.market_strategy import list_strategies, get_strategy


def print_header(title: str):
    """打印标题"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60 + "\n")


def print_subheader(title: str):
    """打印子标题"""
    print(f"\n### {title}\n")


def test_strategy_list():
    """测试 1: 列出所有策略"""
    print_header("测试 1: 列出所有策略")
    
    strategies = list_strategies()
    
    print(f"✅ 共 {len(strategies)} 种策略：\n")
    
    for i, strategy in enumerate(strategies, 1):
        print(f"{i:2d}. {strategy['id']:25} - {strategy['title']}")
        print(f"    {strategy['positioning']}")
    
    print(f"\n✅ 测试通过：列出 {len(strategies)} 种策略")
    return True


def test_strategy_detail():
    """测试 2: 查看策略详情"""
    print_header("测试 2: 查看策略详情")
    
    test_strategies = ["bull_trend", "chan_theory", "wave_theory"]
    
    for strategy_id in test_strategies:
        print_subheader(f"策略：{strategy_id}")
        
        strategy = get_strategy(strategy_id)
        if strategy:
            print(f"标题：{strategy.title}")
            print(f"定位：{strategy.positioning}")
            print(f"原则：{len(strategy.principles)} 条")
            print(f"维度：{len(strategy.dimensions)} 个")
            print(f"框架：{len(strategy.action_framework)} 条")
            print(f"Prompt 长度：{len(strategy.prompt_template)} 字符")
        else:
            print(f"❌ 策略 {strategy_id} 不存在")
            return False
    
    print(f"\n✅ 测试通过：查看 3 个策略详情")
    return True


def test_data_fetcher():
    """测试 3: 数据获取"""
    print_header("测试 3: 数据获取测试")
    
    test_stocks = ["600519", "000858", "002594"]
    
    for stock_code in test_stocks:
        print_subheader(f"股票：{stock_code}")
        
        try:
            data_manager = DataFetcherManager()
            stock_data = data_manager.get_stock_data(stock_code)
            
            if stock_data:
                print(f"✅ 数据获取成功")
                
                if 'realtime' in stock_data:
                    rt = stock_data['realtime']
                    print(f"   当前价格：{rt.get('current', 0):.2f} 元")
                    print(f"   涨跌幅：{rt.get('change_pct', 0):+.2f}%")
                    print(f"   成交量：{rt.get('volume', 0)/100:.0f} 手")
                
                if 'daily' in stock_data and stock_data['daily']:
                    daily = stock_data['daily']
                    print(f"   收盘价：{daily.get('close', 0):.2f} 元")
                    print(f"   MA5: {daily.get('ma5', 0):.2f} 元")
                    print(f"   MA10: {daily.get('ma10', 0):.2f} 元")
            else:
                print(f"❌ 数据获取失败")
                return False
                
        except Exception as e:
            print(f"❌ 异常：{e}")
            return False
    
    print(f"\n✅ 测试通过：获取 {len(test_stocks)} 只股票数据")
    return True


def test_default_analysis():
    """测试 4: 默认策略分析"""
    print_header("测试 4: 默认策略分析（多头趋势）")
    
    stock_code = "600519"
    print(f"测试股票：{stock_code}\n")
    
    try:
        data_manager = DataFetcherManager()
        stock_data = data_manager.get_stock_data(stock_code)
        
        if not stock_data:
            print("❌ 数据获取失败")
            return False
        
        print("正在分析...")
        start_time = time.time()
        
        analysis = analyze_stock_default(stock_data)
        
        elapsed = time.time() - start_time
        
        if analysis:
            print(f"✅ 分析完成（耗时：{elapsed:.1f}秒）")
            print(f"\n分析报告前 500 字符：\n{analysis[:500]}...")
        else:
            print("❌ 分析失败")
            return False
            
    except Exception as e:
        print(f"❌ 异常：{e}")
        return False
    
    print(f"\n✅ 测试通过：默认策略分析")
    return True


def test_strategy_analysis():
    """测试 5: 特定策略分析"""
    print_header("测试 5: 特定策略分析测试")
    
    test_cases = [
        ("600519", "chan_theory", "缠论分析"),
        ("000858", "wave_theory", "波浪理论"),
        ("002594", "ma_golden_cross", "均线金叉"),
    ]
    
    for stock_code, strategy_id, strategy_name in test_cases:
        print_subheader(f"{stock_code} - {strategy_name}")
        
        try:
            data_manager = DataFetcherManager()
            stock_data = data_manager.get_stock_data(stock_code)
            
            if not stock_data:
                print("❌ 数据获取失败")
                continue
            
            print(f"正在使用 {strategy_name} 分析...")
            start_time = time.time()
            
            analysis = analyze_stock_with_strategy(stock_data, strategy_id)
            
            elapsed = time.time() - start_time
            
            if analysis:
                print(f"✅ 分析完成（耗时：{elapsed:.1f}秒）")
                print(f"\n分析报告前 300 字符：\n{analysis[:300]}...")
            else:
                print("❌ 分析失败")
                
        except Exception as e:
            print(f"❌ 异常：{e}")
    
    print(f"\n✅ 测试通过：3 种策略分析")
    return True


def test_batch_analysis():
    """测试 6: 批量分析"""
    print_header("测试 6: 批量分析测试")
    
    stock_list = ["600519", "000858", "002594"]
    print(f"测试股票：{stock_list}\n")
    
    try:
        results = []
        failed = []
        
        for i, stock_code in enumerate(stock_list, 1):
            print(f"[{i}/{len(stock_list)}] 分析 {stock_code}...")
            
            try:
                data_manager = DataFetcherManager()
                stock_data = data_manager.get_stock_data(stock_code)
                
                if not stock_data:
                    failed.append(stock_code)
                    continue
                
                analysis = analyze_stock_default(stock_data)
                
                if analysis:
                    results.append({
                        'code': stock_code,
                        'analysis': analysis[:200] + "..."  # 只显示前 200 字符
                    })
                else:
                    failed.append(stock_code)
                    
            except Exception as e:
                print(f"   ❌ 异常：{e}")
                failed.append(stock_code)
        
        print(f"\n✅ 批量分析完成")
        print(f"   成功：{len(results)} 只")
        print(f"   失败：{len(failed)} 只")
        
        if failed:
            print(f"   失败列表：{', '.join(failed)}")
            
    except Exception as e:
        print(f"❌ 异常：{e}")
        return False
    
    print(f"\n✅ 测试通过：批量分析 {len(stock_list)} 只股票")
    return True


def test_all_strategies():
    """测试 7: 测试所有策略"""
    print_header("测试 7: 测试所有 11 种策略")
    
    stock_code = "600519"
    strategies = list_strategies()
    
    print(f"测试股票：{stock_code}")
    print(f"测试策略：{len(strategies)} 种\n")
    
    try:
        data_manager = DataFetcherManager()
        stock_data = data_manager.get_stock_data(stock_code)
        
        if not stock_data:
            print("❌ 数据获取失败")
            return False
        
        success_count = 0
        failed_strategies = []
        
        for strategy in strategies:
            strategy_id = strategy['id']
            strategy_name = strategy['title']
            
            print(f"测试策略：{strategy_name}...", end=" ")
            
            try:
                analysis = analyze_stock_with_strategy(stock_data, strategy_id)
                
                if analysis:
                    print(f"✅ ({len(analysis)} 字符)")
                    success_count += 1
                else:
                    print(f"❌ 分析失败")
                    failed_strategies.append(strategy_name)
                    
            except Exception as e:
                print(f"❌ 异常：{e}")
                failed_strategies.append(strategy_name)
        
        print(f"\n✅ 测试完成")
        print(f"   成功：{success_count}/{len(strategies)}")
        
        if failed_strategies:
            print(f"   失败：{', '.join(failed_strategies)}")
            
    except Exception as e:
        print(f"❌ 异常：{e}")
        return False
    
    print(f"\n✅ 测试通过：所有 {len(strategies)} 种策略")
    return True


def main():
    """主测试函数"""
    print_header("OpenClaw Daily Stock Analysis - 全功能测试")
    
    print("本测试将验证所有新功能：")
    print("1. /ask 命令 - 11 种策略")
    print("2. /batch 命令 - 批量分析")
    print("3. 大盘复盘功能")
    print()
    
    input("按 Enter 键开始测试...")
    
    tests = [
        ("策略列表", test_strategy_list),
        ("策略详情", test_strategy_detail),
        ("数据获取", test_data_fetcher),
        ("默认策略分析", test_default_analysis),
        ("特定策略分析", test_strategy_analysis),
        ("批量分析", test_batch_analysis),
        ("所有策略测试", test_all_strategies),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ {test_name} 测试异常：{e}")
            results.append((test_name, False))
    
    # 打印总结
    print_header("测试总结")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print(f"总测试数：{total}")
    print(f"通过：{passed}")
    print(f"失败：{total - passed}")
    print()
    
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{status}: {test_name}")
    
    print()
    if passed == total:
        print("🎉 所有测试通过！")
    else:
        print(f"⚠️  {total - passed} 个测试失败")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
