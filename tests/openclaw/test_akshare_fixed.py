#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试修复后的 AkShare 获取器"""

import sys
sys.path.insert(0, '.')

import logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

from data_provider.akshare_fetcher import AkshareFetcher

print("=" * 60)
print("测试修复版 AkShare 获取器")
print("=" * 60)

fetcher = AkshareFetcher()

# 测试 1: 指数行情
print("\n1. 测试指数行情")
print("-" * 40)
indices = fetcher.get_main_indices(region='cn')
if indices:
    print(f"✅ 获取到 {len(indices)} 个指数")
    for idx in indices:
        print(f"   {idx['name']}: {idx['current']:.2f} ({idx['change_pct']:+.2f}%)")
else:
    print("❌ 获取失败")

# 测试 2: 涨跌统计
print("\n2. 测试涨跌统计")
print("-" * 40)
stats = fetcher.get_market_stats()
if stats:
    print(f"✅ 上涨：{stats.get('up_count', 'N/A')} | 下跌：{stats.get('down_count', 'N/A')}")
    print(f"✅ 涨停：{stats.get('limit_up_count', 'N/A')} | 跌停：{stats.get('limit_down_count', 'N/A')}")
else:
    print("❌ 获取失败")

# 测试 3: 板块排行
print("\n3. 测试板块排行")
print("-" * 40)
sectors = fetcher.get_sector_rankings()
if sectors:
    print(f"✅ 领涨：{', '.join([s['name'] for s in sectors['top'][:3]])}")
    print(f"✅ 领跌：{', '.join([s['name'] for s in sectors['bottom'][:3]])}")
else:
    print("❌ 获取失败")

print("\n" + "=" * 60)
print("测试完成")
print("=" * 60)
