# -*- coding: utf-8 -*-
"""
YFinance Fetcher 测试

测试 YFinance 数据获取器的基本功能
"""

import unittest
from unittest.mock import patch, MagicMock

from src.core.data.yfinance_fetcher import YFinanceFetcher

try:
    import yfinance  # noqa: F401
    HAS_YFINANCE = True
except Exception:
    HAS_YFINANCE = False


class TestYFinanceFetcher(unittest.TestCase):
    """YFinance Fetcher 测试"""
    
    def setUp(self):
        self.fetcher = YFinanceFetcher()

    @unittest.skipUnless(HAS_YFINANCE, "yfinance is required for this test")
    def test_fetcher_initialization(self):
        """测试获取器初始化"""
        self.assertEqual(self.fetcher.timeout, 30)
        self.assertEqual(self.fetcher.name, "YFinanceFetcher")
        self.assertEqual(self.fetcher.priority, 4)

    @unittest.skipUnless(HAS_YFINANCE, "yfinance is required for this test")
    @patch('yfinance.Ticker')
    def test_get_main_indices(self, mock_ticker_class):
        """测试获取主要指数"""
        # 模拟 yfinance 返回数据
        mock_ticker = MagicMock()
        mock_history = MagicMock()
        mock_history.empty = False
        mock_history.iloc = MagicMock()
        mock_latest = MagicMock()
        mock_latest.__getitem__ = lambda self, key: 172.50 if key == 'Close' else 170.0
        mock_latest.get = lambda key, default: 170.0 if key == 'Previous Close' else 0
        mock_history.iloc.__getitem__ = lambda self, idx: mock_latest
        mock_ticker.history.return_value = mock_history
        mock_ticker_class.return_value = mock_ticker

        # 调用方法
        indices = self.fetcher.get_main_indices()
        
        # 验证返回结果
        self.assertIsNotNone(indices)
        self.assertIsInstance(indices, list)

    @unittest.skipUnless(HAS_YFINANCE, "yfinance is required for this test")
    @patch('yfinance.Ticker')
    def test_get_index_quote(self, mock_ticker_class):
        """测试获取单个指数行情"""
        # 模拟 yfinance 返回数据
        mock_ticker = MagicMock()
        mock_history = MagicMock()
        mock_history.empty = False
        mock_history.iloc = MagicMock()
        mock_latest = MagicMock()
        mock_latest.__getitem__ = lambda self, key: 3000.0 if key == 'Close' else 2980.0
        mock_latest.get = lambda key, default: 2980.0 if key == 'Previous Close' else 0
        mock_history.iloc.__getitem__ = lambda self, idx: mock_latest
        mock_ticker.history.return_value = mock_history
        mock_ticker_class.return_value = mock_ticker

        # 调用方法
        quote = self.fetcher.get_index_quote("000001")
        
        # 验证返回结果
        self.assertIsNotNone(quote)
        self.assertIn('code', quote)
        self.assertIn('current', quote)


if __name__ == '__main__':
    unittest.main()
