"""
pytest 配置文件
"""

import pytest


@pytest.fixture
def sample_stock_data():
    """示例股票数据"""
    return {
        "stock_code": "AAPL",
        "price": 172.50,
        "change": 1.25,
        "volume": 1000000
    }


@pytest.fixture
def sample_analysis_result():
    """示例分析结果"""
    return {
        "stock_code": "AAPL",
        "sixteen_modules": {},
        "six_perspectives": {},
        "valuation": {}
    }


@pytest.fixture
def sample_config():
    """示例配置"""
    return {
        "model": "qwen3.5-plus",
        "max_tokens": 4096
    }
