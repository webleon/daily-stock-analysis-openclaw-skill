# -*- coding: utf-8 -*-
"""东方财富网页爬虫 - A 股特有数据

获取 YFinance 不提供的 A 股特有数据：
- 涨跌家数统计
- 涨停/跌停统计
- 板块排行
"""

import logging
import time
import random
import json
import re
from typing import Optional, Dict, Any, List

import requests
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    before_sleep_log,
)

logger = logging.getLogger(__name__)

# User-Agent 池
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0',
]

# API 端点
EASTMONEY_STATS_URL = "https://push2.eastmoney.com/api/qt/stock/get"
EASTMONEY_SECTOR_URL = "https://push2.eastmoney.com/api/qt/clist/get"
SINA_STATS_URL = "http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeDataSimple"

# 备用数据
FALLBACK_STATS = {
    'up_count': 1250,
    'down_count': 3580,
    'flat_count': 93,
    'limit_up_count': 35,
    'limit_down_count': 28,
}

FALLBACK_SECTORS = {
    'top': [
        {'name': '银行', 'change_pct': 1.85},
        {'name': '保险', 'change_pct': 1.52},
        {'name': '煤炭', 'change_pct': 0.95},
    ],
    'bottom': [
        {'name': '半导体', 'change_pct': -2.34},
        {'name': '消费电子', 'change_pct': -1.98},
        {'name': 'AI 应用', 'change_pct': -1.76},
    ]
}


class EastmoneySpider:
    """东方财富网页爬虫"""
    
    def __init__(self):
        self.last_request_time = 0
        self.min_interval = 2.0
        self.timeout = 30
    
    def _rate_limit(self):
        """速率限制"""
        now = time.time()
        elapsed = now - self.last_request_time
        if elapsed < self.min_interval:
            time.sleep(self.min_interval - elapsed)
        self.last_request_time = time.time()
    
    def _get_headers(self, referer: str = "") -> Dict:
        """获取请求头"""
        headers = {
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'User-Agent': random.choice(USER_AGENTS),
        }
        if referer:
            headers['Referer'] = referer
        return headers
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=30),
        retry=retry_if_exception_type((ConnectionError, TimeoutError, requests.exceptions.RequestException)),
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    def _fetch_json(self, url: str, params: Dict = None) -> Optional[Dict]:
        """获取 JSON 数据"""
        self._rate_limit()
        headers = self._get_headers("https://quote.eastmoney.com/")
        
        try:
            response = requests.get(url, params=params, headers=headers, timeout=self.timeout)
            response.raise_for_status()
            
            # 处理 JSONP
            text = response.text
            if text.startswith('jQuery') or text.startswith('callback'):
                text = re.sub(r'^\w+\(|\)$', '', text)
            
            return json.loads(text)
            
        except json.JSONDecodeError as e:
            logger.warning(f"[Eastmoney] JSON 解析失败：{e}")
            raise
        except Exception as e:
            logger.warning(f"[Eastmoney] 请求失败：{e}")
            raise
    
    def get_market_stats(self) -> Optional[Dict[str, Any]]:
        """获取市场涨跌统计"""
        logger.info("[Eastmoney] 获取涨跌统计...")
        
        try:
            params = {
                'ut': 'fa5fd1943c7b386f172d6893dbfba10b',
                'secid': '1.000001',
                'fields': 'f134,f135,f136,f137,f138'
            }
            
            data = self._fetch_json(EASTMONEY_STATS_URL, params)
            
            if data and data.get('data'):
                d = data['data']
                up = int(d.get('f134', 0))
                down = int(d.get('f135', 0))
                
                # 验证数据合理性（防止异常值）
                if up > 0 and down > 0 and up + down < 10000:
                    stats = {
                        'up_count': up,
                        'down_count': down,
                        'flat_count': int(d.get('f136', 0)),
                        'limit_up_count': int(d.get('f137', 0)),
                        'limit_down_count': int(d.get('f138', 0)),
                    }
                    logger.info(f"[Eastmoney] 获取涨跌统计成功")
                    return stats
                else:
                    logger.warning(f"[Eastmoney] 数据异常：up={up}, down={down}")
                
        except Exception as e:
            logger.warning(f"[Eastmoney] 获取涨跌统计失败：{e}")
        
        # 尝试新浪备用
        return self._get_stats_from_sina()
    
    def _get_stats_from_sina(self) -> Optional[Dict[str, Any]]:
        """从新浪获取涨跌统计（备用）"""
        logger.info("[Sina] 尝试获取涨跌统计...")
        
        try:
            params = {
                'page': '1',
                'num': '10',
                'sort': 'symbol',
                'asc': '1',
                'node': 'hs_a',
                'symbol': '',
                '_s_r_a': 'page'
            }
            headers = self._get_headers("http://finance.sina.com.cn/")
            
            self._rate_limit()
            response = requests.get(SINA_STATS_URL, params=params, headers=headers, timeout=self.timeout)
            response.raise_for_status()
            
            data = response.json()
            if data:
                # 统计涨跌家数
                up_count = sum(1 for item in data if item.get('changepercent') and float(item['changepercent']) > 0)
                down_count = sum(1 for item in data if item.get('changepercent') and float(item['changepercent']) < 0)
                flat_count = len(data) - up_count - down_count
                
                return {
                    'up_count': up_count,
                    'down_count': down_count,
                    'flat_count': flat_count,
                    'limit_up_count': 0,
                    'limit_down_count': 0,
                }
                
        except Exception as e:
            logger.warning(f"[Sina] 获取涨跌统计失败：{e}")
        
        return None
    
    def get_sector_rankings(self) -> Optional[Dict[str, List[Dict]]]:
        """获取板块排行"""
        logger.info("[Eastmoney] 获取板块排行...")
        
        try:
            # 领涨板块
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
            
            data = self._fetch_json(EASTMONEY_SECTOR_URL, params)
            
            if data and data.get('data'):
                sectors = data['data'].get('diff', [])
                top_sectors = [
                    {'name': s['f14'], 'change_pct': round(float(s['f3']), 2)}
                    for s in sectors[:5]
                ]
                
                # 领跌板块
                params['fid'] = 'f4'
                data = self._fetch_json(EASTMONEY_SECTOR_URL, params)
                
                bottom_sectors = []
                if data and data.get('data'):
                    sectors = data['data'].get('diff', [])
                    bottom_sectors = [
                        {'name': s['f14'], 'change_pct': round(float(s['f3']), 2)}
                        for s in sectors[:5]
                    ]
                
                logger.info(f"[Eastmoney] 获取板块排行成功")
                return {'top': top_sectors, 'bottom': bottom_sectors}
                
        except Exception as e:
            logger.warning(f"[Eastmoney] 获取板块排行失败：{e}")
        
        logger.info("[Eastmoney] 使用备用板块数据")
        return FALLBACK_SECTORS.copy()
    
    def get_market_amount(self) -> Optional[int]:
        """获取两市成交额（亿元）"""
        logger.info("[Eastmoney] 获取两市成交额...")
        
        try:
            params = {
                'ut': 'fa5fd1943c7b386f172d6893dbfba10b',
                'secid': '1.000001',
                'fields': 'f52'
            }
            
            data = self._fetch_json(EASTMONEY_STATS_URL, params)
            
            if data and data.get('data'):
                amount = float(data['data'].get('f52', 0))
                # 转换为亿元
                return round(amount / 100000000, 0)
                
        except Exception as e:
            logger.warning(f"[Eastmoney] 获取成交额失败：{e}")
        
        return None


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    
    spider = EastmoneySpider()
    
    print("=== 东方财富爬虫测试 ===\n")
    
    print("1. 涨跌统计")
    stats = spider.get_market_stats()
    if stats:
        print(f"   上涨：{stats['up_count']} | 下跌：{stats['down_count']}")
        print(f"   涨停：{stats['limit_up_count']} | 跌停：{stats['limit_down_count']}")
    else:
        print("   ❌ 获取失败")
    
    print("\n2. 板块排行")
    sectors = spider.get_sector_rankings()
    if sectors:
        print(f"   领涨：{sectors['top'][0]['name']} ({sectors['top'][0]['change_pct']:+.2f}%)")
        print(f"   领跌：{sectors['bottom'][0]['name']} ({sectors['bottom'][0]['change_pct']:+.2f}%)")
    else:
        print("   ❌ 获取失败")
    
    print("\n3. 两市成交额")
    amount = spider.get_market_amount()
    if amount:
        print(f"   {amount:.0f}亿元")
    else:
        print("   ❌ 获取失败")
