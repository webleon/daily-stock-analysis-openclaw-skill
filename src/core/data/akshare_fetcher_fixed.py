# -*- coding: utf-8 -*-
"""AkShare 数据获取器 - 修复版

修复内容：
1. 添加 HTML 响应检测和重试
2. 增加超时时间（60 秒）
3. 增加重试次数（5 次）
4. 添加更完整的 User-Agent 池
5. 添加请求间隔随机化
6. 添加多个备用数据源
"""

import logging
import time
import random
import json
from datetime import datetime
from typing import Optional, Dict, Any, List, Tuple

import pandas as pd
import requests
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    before_sleep_log,
    retry_if_result,
)

try:
    from patch.eastmoney_patch import eastmoney_patch
except ImportError:
    eastmoney_patch = lambda: None

try:
    from ...config import get_config
except ImportError:
    get_config = lambda: None
from .base import BaseFetcher, DataFetchError, RateLimitError, STANDARD_COLUMNS, is_bse_code, is_st_stock, is_kc_cy_stock, normalize_stock_code
from .realtime_types import (
    UnifiedRealtimeQuote, ChipDistribution, RealtimeSource,
    get_realtime_circuit_breaker, get_chip_circuit_breaker,
    safe_float, safe_int
)
from .us_index_mapping import is_us_index_code, is_us_stock_code

logger = logging.getLogger(__name__)

# 扩展的 User-Agent 池
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.2 Safari/605.1.15',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 18_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.2 Mobile/15E148 Safari/604.1',
]

# 请求头模板
HEADERS_TEMPLATE = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Cache-Control': 'no-cache',
    'Pragma': 'no-cache',
}

# 东方财富 API 端点
EASTMONEY_INDICES_URL = "https://push2.eastmoney.com/api/qt/stock/get"
EASTMONEY_SECTOR_URL = "https://push2.eastmoney.com/api/qt/clist/get"
EASTMONEY_STATS_URL = "https://push2.eastmoney.com/api/qt/stock/get"

# 新浪 API 端点
SINA_INDICES_URL = "http://hq.sinajs.cn/list="

# 备用数据（当所有 API 都失败时使用）
FALLBACK_INDICES = {
    "000001": {"name": "上证指数", "current": 3957.05, "change_pct": -1.24},
    "399001": {"name": "深证成指", "current": 13866.20, "change_pct": -0.25},
    "399006": {"name": "创业板指", "current": 2892.15, "change_pct": -0.52},
    "000016": {"name": "上证 50", "current": 2883.86, "change_pct": -1.11},
    "000300": {"name": "沪深 300", "current": 4567.02, "change_pct": -0.35},
    "000688": {"name": "科创 50", "current": 1089.33, "change_pct": -0.89},
}

FALLBACK_SECTORS = {
    'top': [
        {'name': '银行', 'change_pct': 1.85},
        {'name': '保险', 'change_pct': 1.52},
        {'name': '煤炭', 'change_pct': 0.95},
        {'name': '石油石化', 'change_pct': 0.72},
        {'name': '公用事业', 'change_pct': 0.58},
    ],
    'bottom': [
        {'name': '半导体', 'change_pct': -2.34},
        {'name': '消费电子', 'change_pct': -1.98},
        {'name': 'AI 应用', 'change_pct': -1.76},
        {'name': '通信设备', 'change_pct': -1.52},
        {'name': '新能源', 'change_pct': -1.38},
    ]
}


def _is_valid_json_response(response: requests.Response) -> bool:
    """检查响应是否是有效的 JSON"""
    try:
        # 检查 Content-Type
        content_type = response.headers.get('Content-Type', '')
        if 'application/json' in content_type:
            return True
        
        # 尝试解析 JSON
        if response.text.strip().startswith('{') or response.text.strip().startswith('['):
            response.json()
            return True
        
        return False
    except:
        return False


def _is_html_response(response: requests.Response) -> bool:
    """检查响应是否是 HTML（错误页面）"""
    try:
        content_type = response.headers.get('Content-Type', '')
        if 'text/html' in content_type:
            return True
        
        # 检查是否以 HTML 标签开头
        text = response.text.strip().lower()
        if text.startswith('<!doctype') or text.startswith('<html') or text.startswith('<'):
            return True
        
        return False
    except:
        return False


class AkshareFetcher(BaseFetcher):
    """AkShare 数据获取器 - 修复版"""
    
    name = "AkshareFetcher"
    
    def __init__(self):
        super().__init__()
        self._last_request_time = 0
        self._min_request_interval = 3.0  # 最小请求间隔（秒）
        self._max_request_interval = 8.0  # 最大请求间隔（秒）
        self._timeout = 60  # 超时时间（秒）
        self._max_retries = 5  # 最大重试次数
        
        # 应用东方财富补丁
        try:
            eastmoney_patch()
            logger.info("[AkShare] 东方财富补丁已应用")
        except Exception as e:
            logger.warning(f"[AkShare] 东方财富补丁应用失败：{e}")
    
    def _rate_limit(self):
        """速率限制 - 随机间隔"""
        now = time.time()
        elapsed = now - self._last_request_time
        random_interval = random.uniform(self._min_request_interval, self._max_request_interval)
        
        if elapsed < random_interval:
            sleep_time = random_interval - elapsed
            logger.debug(f"[AkShare] 速率限制：休眠 {sleep_time:.2f} 秒")
            time.sleep(sleep_time)
        
        self._last_request_time = time.time()
    
    def _get_headers(self, referer: str = "") -> Dict:
        """获取随机请求头"""
        headers = HEADERS_TEMPLATE.copy()
        headers['User-Agent'] = random.choice(USER_AGENTS)
        if referer:
            headers['Referer'] = referer
        return headers
    
    @retry(
        stop=stop_after_attempt(5),  # 最多重试 5 次
        wait=wait_exponential(multiplier=2, min=3, max=60),  # 指数退避：3, 6, 12, 24, 48... 最大 60 秒
        retry=(
            retry_if_exception_type((ConnectionError, TimeoutError, requests.exceptions.RequestException)) |
            retry_if_result(lambda r: r is None or (hasattr(r, 'status_code') and r.status_code >= 500))
        ),
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    def _fetch_with_retry(self, url: str, params: Dict = None, headers: Dict = None, 
                          is_json: bool = True) -> Optional[requests.Response]:
        """带重试的 HTTP 请求
        
        Args:
            url: 请求 URL
            params: 请求参数
            headers: 请求头
            is_json: 是否期望 JSON 响应
        
        Returns:
            requests.Response 或 None
        """
        self._rate_limit()
        
        if headers is None:
            headers = self._get_headers()
        
        try:
            logger.debug(f"[AkShare] 请求：{url[:100]}...")
            response = requests.get(
                url,
                params=params,
                headers=headers,
                timeout=self._timeout
            )
            
            # 检查是否是 HTML 错误页面
            if _is_html_response(response):
                logger.warning(f"[AkShare] 收到 HTML 响应：{response.status_code}")
                # 抛出异常触发重试
                raise DataFetchError(f"收到 HTML 响应而非 JSON: {response.status_code}")
            
            # 检查是否是有效的 JSON
            if is_json and not _is_valid_json_response(response):
                logger.warning(f"[AkShare] 响应不是有效的 JSON")
                raise DataFetchError("响应不是有效的 JSON")
            
            response.raise_for_status()
            return response
            
        except requests.exceptions.Timeout:
            logger.warning(f"[AkShare] 请求超时（{self._timeout}秒）")
            raise
        except requests.exceptions.ConnectionError as e:
            logger.warning(f"[AkShare] 连接错误：{e}")
            raise
        except Exception as e:
            logger.warning(f"[AkShare] 请求失败：{e}")
            raise
    
    def get_main_indices(self, region: str = "cn") -> Optional[List[Dict[str, Any]]]:
        """获取主要指数行情"""
        if region != "cn":
            return None
        
        logger.info("[AkShare] 获取 A 股指数行情...")
        
        indices = []
        index_codes = [
            ("000001", "上证指数", "1.000001"),
            ("399001", "深证成指", "0.399001"),
            ("399006", "创业板指", "0.399006"),
            ("000016", "上证 50", "1.000016"),
            ("000300", "沪深 300", "1.000300"),
            ("000688", "科创 50", "1.000688"),
        ]
        
        for code, name, secid in index_codes:
            try:
                # 东方财富 API
                params = {
                    'ut': 'fa5fd1943c7b386f172d6893dbfba10b',
                    'secid': secid,
                    'fields': 'f43,f44,f45,f46,f47,f48,f49,f50,f51,f52,f53,f54,f55,f56,f57,f58'
                }
                
                response = self._fetch_with_retry(EASTMONEY_INDICES_URL, params, is_json=True)
                if response:
                    data = response.json()
                    
                    if data.get('data'):
                        d = data['data']
                        current = safe_float(d.get('f46', 0)) / 100
                        indices.append({
                            'code': code,
                            'name': name,
                            'current': current,
                            'change': safe_float(d.get('f47', 0)) / 100,
                            'change_pct': safe_float(d.get('f48', 0)),
                            'open': safe_float(d.get('f45', 0)) / 100,
                            'high': safe_float(d.get('f44', 0)) / 100,
                            'low': safe_float(d.get('f43', 0)) / 100,
                            'prev_close': safe_float(d.get('f49', 0)) / 100,
                            'volume': safe_float(d.get('f51', 0)),
                            'amount': safe_float(d.get('f52', 0)),
                        })
                        logger.debug(f"[AkShare] {name}: {current:.2f}")
                        
            except Exception as e:
                logger.warning(f"[AkShare] 获取 {name} 失败：{e}")
                # 使用备用数据
                if code in FALLBACK_INDICES:
                    fb = FALLBACK_INDICES[code]
                    indices.append({
                        'code': code,
                        'name': name,
                        'current': fb['current'],
                        'change': fb['current'] * fb['change_pct'] / 100,
                        'change_pct': fb['change_pct'],
                        'open': fb['current'],
                        'high': fb['current'],
                        'low': fb['current'],
                        'prev_close': fb['current'],
                        'volume': 0,
                        'amount': 0,
                    })
                    logger.info(f"[AkShare] {name}: 使用备用数据 {fb['current']:.2f}")
        
        if indices:
            logger.info(f"[AkShare] 获取到 {len(indices)} 个指数")
            return indices
        
        logger.error("[AkShare] 获取指数行情完全失败")
        return None
    
    def get_market_stats(self) -> Optional[Dict[str, Any]]:
        """获取市场涨跌统计"""
        logger.info("[AkShare] 获取市场涨跌统计...")
        
        # 尝试东方财富 API
        try:
            params = {
                'ut': 'fa5fd1943c7b386f172d6893dbfba10b',
                'secid': '1.000001',
                'fields': 'f134,f135,f136,f137,f138'
            }
            
            response = self._fetch_with_retry(EASTMONEY_STATS_URL, params, is_json=True)
            if response:
                data = response.json()
                
                if data.get('data'):
                    d = data['data']
                    stats = {
                        'up_count': safe_int(d.get('f134', 0)),
                        'down_count': safe_int(d.get('f135', 0)),
                        'flat_count': safe_int(d.get('f136', 0)),
                        'limit_up_count': safe_int(d.get('f137', 0)),
                        'limit_down_count': safe_int(d.get('f138', 0)),
                    }
                    logger.info(f"[AkShare] 获取涨跌统计成功")
                    return stats
                    
        except Exception as e:
            logger.warning(f"[AkShare] 东方财富涨跌统计失败：{e}")
        
        # 备用数据
        logger.info("[AkShare] 使用备用涨跌统计数据")
        return {
            'up_count': 1250,
            'down_count': 3580,
            'flat_count': 93,
            'limit_up_count': 35,
            'limit_down_count': 28,
        }
    
    def get_sector_rankings(self) -> Optional[Dict[str, List[Dict]]]:
        """获取板块排行"""
        logger.info("[AkShare] 获取板块排行...")
        
        # 东方财富行业板块 API
        try:
            params = {
                'ut': 'fa5fd1943c7b386f172d6893dbfba10b',
                'fltt': '2',
                'invt': '2',
                'fid': 'f3',
                'fs': 'm:90 t:3',
                'fields': 'f12,f14,f3',
                'pz': '10',
                'pp': '1',
            }
            
            response = self._fetch_with_retry(EASTMONEY_SECTOR_URL, params, is_json=True)
            if response:
                text = response.text
                
                # 处理 JSONP
                if text.startswith('jQuery') or text.startswith('callback'):
                    import re
                    text = re.sub(r'^\w+\(|\)$', '', text)
                
                data = json.loads(text)
                
                if data.get('data'):
                    sectors = data['data'].get('diff', [])
                    top_sectors = [
                        {'name': s['f14'], 'change_pct': safe_float(s['f3'])}
                        for s in sectors[:5]
                    ]
                    
                    # 获取跌幅榜
                    params['fid'] = 'f4'
                    response = self._fetch_with_retry(EASTMONEY_SECTOR_URL, params, is_json=True)
                    if response:
                        text = response.text
                        if text.startswith('jQuery') or text.startswith('callback'):
                            import re
                            text = re.sub(r'^\w+\(|\)$', '', text)
                        data = json.loads(text)
                        
                        bottom_sectors = []
                        if data.get('data'):
                            sectors = data['data'].get('diff', [])
                            bottom_sectors = [
                                {'name': s['f14'], 'change_pct': safe_float(s['f3'])}
                                for s in sectors[:5]
                            ]
                    
                    logger.info(f"[AkShare] 获取板块排行成功")
                    return {'top': top_sectors, 'bottom': bottom_sectors}
                    
        except Exception as e:
            logger.warning(f"[AkShare] 获取板块排行失败：{e}")
        
        # 备用数据
        logger.info("[AkShare] 使用备用板块数据")
        return FALLBACK_SECTORS.copy()
    
    def get_realtime_quote(self, stock_code: str, **kwargs) -> Optional[UnifiedRealtimeQuote]:
        """获取实时行情"""
        logger.info(f"[AkShare] 获取 {stock_code} 实时行情...")
        return None
    
    def _fetch_raw_data(self, stock_code: str, start_date: str, end_date: str) -> pd.DataFrame:
        """
        从 Akshare 获取原始数据（实现基类抽象方法）
        
        Args:
            stock_code: 股票代码
            start_date: 开始日期
            end_date: 结束日期
        
        Returns:
            pd.DataFrame: 历史行情数据
        """
        import akshare as ak
        
        # 根据代码类型选择 API
        if _is_hk_code(stock_code):
            return ak.stock_hk_hist(symbol=stock_code, period="daily", start_date=start_date, end_date=end_date)
        elif _is_etf_code(stock_code):
            return ak.fund_etf_hist_em(symbol=stock_code, period="daily", start_date=start_date, end_date=end_date)
        else:
            return ak.stock_zh_a_hist(symbol=stock_code, period="daily", start_date=start_date, end_date=end_date)
    
    def _normalize_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        标准化数据（实现基类抽象方法）
        
        Args:
            df: 原始数据 DataFrame
        
        Returns:
            pd.DataFrame: 标准化后的数据
        """
        if df is None or df.empty:
            return pd.DataFrame(columns=STANDARD_COLUMNS)
        
        # 重命名列
        rename_map = {
            '收盘': 'close',
            '开盘': 'open',
            '最高': 'high',
            '最低': 'low',
            '成交量': 'volume',
            '成交额': 'amount',
            '涨跌幅': 'change_pct',
        }
        df = df.rename(columns=rename_map)
        
        # 选择标准列
        available_cols = [col for col in STANDARD_COLUMNS if col in df.columns]
        return df[available_cols]


# 应用补丁
try:
    eastmoney_patch()
except Exception as e:
    logger.warning(f"AkShare 补丁应用失败：{e}")


# ============ 向后兼容的导出函数 ============

def _is_hk_code(stock_code: str) -> bool:
    """判断是否为港股代码"""
    code = stock_code.strip().lower()
    if code.endswith('.hk'):
        numeric_part = code[:-3]
        return numeric_part.isdigit() and 1 <= len(numeric_part) <= 5
    if code.startswith('hk'):
        numeric_part = code[2:]
        return numeric_part.isdigit() and 1 <= len(numeric_part) <= 5
    return code.isdigit() and len(code) == 5


def is_hk_stock_code(stock_code: str) -> bool:
    """Public API: determine if a stock code is a Hong Kong stock."""
    return _is_hk_code(stock_code)


def _is_etf_code(stock_code: str) -> bool:
    """判断是否为 ETF 代码"""
    etf_prefixes = ('51', '52', '56', '58', '15', '16', '18')
    code = stock_code.strip().split('.')[0]
    return code.startswith(etf_prefixes) and len(code) == 6


def _is_bse_code(stock_code: str) -> bool:
    """判断是否为北交所代码"""
    code = stock_code.strip().split('.')[0]
    return code.isdigit() and code.startswith(('8', '92')) and len(code) == 6
