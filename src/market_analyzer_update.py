import re

# 读取原文件
with open('src/market_analyzer.py', 'r') as f:
    content = f.read()

# 1. 添加 Tavily 导入
if 'from tavily import TavilyClient' not in content:
    content = content.replace(
        'from data_provider.base import DataFetcherManager',
        'from data_provider.base import DataFetcherManager\ntry:\n    from tavily import TavilyClient\n    TAVILY_AVAILABLE = True\nexcept ImportError:\n    TAVILY_AVAILABLE = False'
    )

# 2. 添加东方财富导入
if 'from data_provider.eastmoney_fetcher import EastmoneyFetcher' not in content:
    content = content.replace(
        'from data_provider.base import DataFetcherManager',
        'from data_provider.base import DataFetcherManager\nfrom data_provider.eastmoney_fetcher import EastmoneyFetcher'
    )

# 写入
with open('src/market_analyzer.py', 'w') as f:
    f.write(content)

print("✅ 已更新 market_analyzer.py 导入")
