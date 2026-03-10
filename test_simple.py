#!/usr/bin/env python3
"""
简化测试脚本 - 仅测试数据获取
"""
import yfinance as yf
import akshare as ak
from datetime import datetime

def test_us_stock(code):
    """测试美股数据获取"""
    print(f"\n📊 测试美股：{code}")
    ticker = yf.Ticker(code)
    info = ticker.info
    
    print(f"  公司名称：{info.get('shortName', 'N/A')}")
    print(f"  当前价格：{info.get('currentPrice', 'N/A')} USD")
    print(f"  市值：${info.get('marketCap', 0):,.0f}")
    print(f"  PE 比率：{info.get('trailingPE', 'N/A')}")
    print(f"  52 周最高：{info.get('fiftyTwoWeekHigh', 'N/A')}")
    print(f"  52 周最低：{info.get('fiftyTwoWeekLow', 'N/A')}")
    
    return True

def test_cn_stock(code):
    """测试 A 股数据获取"""
    print(f"\n📊 测试 A 股：{code}")
    try:
        df = ak.stock_zh_a_spot_em()
        stock_data = df[df['代码'] == code]
        
        if not stock_data.empty:
            print(f"  公司名称：{stock_data['名称'].values[0]}")
            print(f"  当前价格：{stock_data['最新价'].values[0]} CNY")
            print(f"  涨跌幅：{stock_data['涨跌幅'].values[0]}%")
            print(f"  成交量：{stock_data['成交量'].values[0]}")
            return True
        else:
            print(f"  ❌ 未找到股票：{code}")
            return False
    except Exception as e:
        print(f"  ❌ 错误：{e}")
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("Daily Stock Analysis - 数据获取测试")
    print("=" * 60)
    
    # 测试美股
    test_us_stock('AAPL')
    test_us_stock('MSFT')
    test_us_stock('NVDA')
    
    # 测试 A 股
    test_cn_stock('600519')
    test_cn_stock('300750')
    
    print("\n" + "=" * 60)
    print("✅ 测试完成！")
    print("=" * 60)
