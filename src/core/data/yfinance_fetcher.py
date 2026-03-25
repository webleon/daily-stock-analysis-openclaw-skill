# -*- coding: utf-8 -*-
"""YFinance 数据获取器 - A 股指数专用

使用 YFinance 获取 A 股指数行情（稳定可靠）
"""

import logging
from typing import Optional, List, Dict, Any

import yfinance as yf

from .base import BaseFetcher

logger = logging.getLogger(__name__)

# A 股指数 Yahoo Finance 代码映射
A_SHARE_INDICES = {
    "000001": {"name": "上证指数", "yf_code": "000001.SS"},
    "399001": {"name": "深证成指", "yf_code": "399001.SZ"},
    "399006": {"name": "创业板指", "yf_code": "399006.SZ"},
    "000016": {"name": "上证 50", "yf_code": "000016.SS"},
    "000300": {"name": "沪深 300", "yf_code": "000300.SS"},
    "000688": {"name": "科创 50", "yf_code": "000688.SS"},
}


class YFinanceFetcher:
    """
    Yahoo Finance 数据源实现
    
    优先级：4
    数据来源：Yahoo Finance API
    特点：支持美股、港股
    
    注意：此类不继承 BaseFetcher，因为它是专用数据源
    """
    name = "YFinanceFetcher"
    priority = 4  # 默认优先级
    """YFinance A 股指数获取器"""
    
    def __init__(self):
        self.timeout = 30
    
    def get_main_indices(self) -> Optional[List[Dict[str, Any]]]:
        """获取 A 股主要指数行情"""
        logger.info("[YFinance] 获取 A 股指数行情...")
        
        indices = []
        
        for code, info in A_SHARE_INDICES.items():
            try:
                ticker = yf.Ticker(info["yf_code"])
                hist = ticker.history(period="1d", timeout=self.timeout)
                
                if hist is not None and not hist.empty:
                    latest = hist.iloc[-1]
                    current = float(latest['Close'])
                    
                    # 获取前一日收盘价计算涨跌幅
                    prev_close = float(latest.get('Previous Close', 0))
                    if prev_close <= 0 and len(hist) > 1:
                        prev_close = float(hist.iloc[-2]['Close'])
                    if prev_close <= 0:
                        prev_close = current
                    
                    change = current - prev_close
                    change_pct = (change / prev_close * 100) if prev_close else 0
                    
                    indices.append({
                        'code': code,
                        'name': info['name'],
                        'current': current,
                        'change': change,
                        'change_pct': round(change_pct, 2),
                        'open': float(latest.get('Open', current)),
                        'high': float(latest.get('High', current)),
                        'low': float(latest.get('Low', current)),
                        'prev_close': prev_close,
                        'volume': float(latest.get('Volume', 0)),
                        'amount': 0,  # YFinance 不提供成交额
                    })
                    
                    logger.debug(f"[YFinance] {info['name']}: {current:.2f} ({change_pct:+.2f}%)")
                    
            except Exception as e:
                logger.warning(f"[YFinance] 获取 {info['name']} 失败：{e}")
                continue
        
        if indices:
            logger.info(f"[YFinance] 获取到 {len(indices)} 个指数")
            return indices
        
        logger.error("[YFinance] 获取指数行情完全失败")
        return None
    
    def get_index_quote(self, code: str) -> Optional[Dict[str, Any]]:
        """获取单个指数行情"""
        if code not in A_SHARE_INDICES:
            logger.warning(f"[YFinance] 未知指数代码：{code}")
            return None
        
        info = A_SHARE_INDICES[code]
        
        try:
            ticker = yf.Ticker(info["yf_code"])
            hist = ticker.history(period="1d", timeout=self.timeout)
            
            if hist is not None and not hist.empty:
                latest = hist.iloc[-1]
                current = float(latest['Close'])
                
                if len(hist) > 1:
                    prev_close = float(hist.iloc[-2]['Close'])
                else:
                    prev_close = float(latest.get('Previous Close', current))
                
                change = current - prev_close
                change_pct = (change / prev_close * 100) if prev_close else 0
                
                return {
                    'code': code,
                    'name': info['name'],
                    'current': current,
                    'change': change,
                    'change_pct': round(change_pct, 2),
                    'open': float(latest.get('Open', current)),
                    'high': float(latest.get('High', current)),
                    'low': float(latest.get('Low', current)),
                    'prev_close': prev_close,
                }
        except Exception as e:
            logger.warning(f"[YFinance] 获取 {info['name']} 失败：{e}")
        
        return None


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    
    fetcher = YFinanceFetcher()
    
    print("=== YFinance A 股指数测试 ===\n")
    
    indices = fetcher.get_main_indices()
    if indices:
        print(f"✅ 获取到 {len(indices)} 个指数\n")
        for idx in indices:
            print(f"{idx['name']}: {idx['current']:.2f} ({idx['change_pct']:+.2f}%)")
    else:
        print("❌ 获取失败")
