"""
数据获取模块
支持 AkShare、Tushare、Yahoo Finance 等多数据源
带故障切换、重试、速率限制等高级功能
"""

# 基础类
from .base import (
    BaseFetcher,
    DataFetcherManager,
    DataFetchError,
    RateLimitError,
)

# 具体数据源
from .akshare_fetcher import AkshareFetcher
from .tushare_fetcher import TushareFetcher
from .efinance_fetcher import EfinanceFetcher
from .yfinance_fetcher import YFinanceFetcher

__all__ = [
    'BaseFetcher',
    'DataFetcherManager',
    'DataFetchError',
    'RateLimitError',
    'AkshareFetcher',
    'TushareFetcher',
    'EfinanceFetcher',
    'YFinanceFetcher',
]
