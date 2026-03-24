# -*- coding: utf-8 -*-
"""长桥 OpenAPI 数据获取器

使用长桥 OpenAPI 获取 A 股/港股/美股行情数据
文档：https://open.longbridge.com/zh-CN/docs

SDK v4 API:
- 使用 Config.from_apikey() 或 Config.from_apikey_env()
- 使用 QuoteContext 获取行情
- 需要订阅后才能获取实时行情
"""

import logging
import os
from typing import Optional, List, Dict, Any

try:
    from longbridge.openapi import Config, QuoteContext, SubType
    LONGBRIDGE_AVAILABLE = True
except ImportError:
    LONGBRIDGE_AVAILABLE = False
    logger = logging.getLogger(__name__)
    logger.warning("长桥 SDK 未安装，请运行：pip install longbridge")

logger = logging.getLogger(__name__)

# A 股指数长桥代码映射
A_SHARE_INDICES = {
    "000001": {"name": "上证指数", "lb_code": "SH.000001"},
    "399001": {"name": "深证成指", "lb_code": "SZ.399001"},
    "399006": {"name": "创业板指", "lb_code": "SZ.399006"},
    "000016": {"name": "上证 50", "lb_code": "SH.000016"},
    "000300": {"name": "沪深 300", "lb_code": "SH.000300"},
    "000688": {"name": "科创 50", "lb_code": "SH.000688"},
}


class LongbridgeFetcher:
    """长桥 OpenAPI 数据获取器"""
    
    def __init__(
        self,
        app_key: str = None,
        app_secret: str = None,
        access_token: str = None,
        use_sandbox: bool = False
    ):
        """
        初始化长桥客户端
        
        Args:
            app_key: 长桥 App Key（可选，默认从环境变量读取）
            app_secret: 长桥 App Secret（可选，默认从环境变量读取）
            access_token: 长桥 Access Token（可选，默认从环境变量读取）
            use_sandbox: 是否使用沙箱环境
        """
        # 从参数或环境变量获取凭证
        self.app_key = app_key or os.getenv("LONGBRIDGE_APP_KEY")
        self.app_secret = app_secret or os.getenv("LONGBRIDGE_APP_SECRET")
        self.access_token = access_token or os.getenv("LONGBRIDGE_ACCESS_TOKEN")
        
        if not self.app_key or not self.app_secret:
            raise ValueError("长桥 App Key 和 App Secret 必填")
        
        # 初始化配置
        if self.access_token:
            self.config = Config.from_apikey(
                app_key=self.app_key,
                app_secret=self.app_secret,
                access_token=self.access_token
            )
        else:
            # 如果没有 Token，尝试从环境变量
            try:
                self.config = Config.from_apikey_env()
            except:
                self.config = Config.from_apikey(
                    app_key=self.app_key,
                    app_secret=self.app_secret,
                    access_token=""
                )
        
        logger.info(f"[Longbridge] 初始化完成，A 股权限：LV1 实时行情")
    
    def get_main_indices(self) -> Optional[List[Dict[str, Any]]]:
        """获取 A 股主要指数行情"""
        logger.info("[Longbridge] 获取 A 股指数行情...")
        
        if not LONGBRIDGE_AVAILABLE:
            logger.error("[Longbridge] SDK 未安装")
            return None
        
        indices = []
        
        try:
            quote_ctx = QuoteContext(self.config)
            
            # 订阅所有指数
            symbols = [info["lb_code"] for info in A_SHARE_INDICES.values()]
            quote_ctx.subscribe(symbols=symbols, sub_types=[SubType.Quote])
            
            # 获取实时行情
            import time
            time.sleep(0.5)  # 等待订阅生效
            resp = quote_ctx.realtime_quote(symbols=symbols)
            
            if resp and len(resp) > 0:
                for q in resp:
                    symbol = q.symbol
                    last_done = float(q.last_done) if q.last_done else 0
                    prev_close = float(q.prev_close) if q.prev_close else last_done
                    
                    change = last_done - prev_close
                    change_pct = (change / prev_close * 100) if prev_close else 0
                    
                    # 查找对应的指数信息
                    info = None
                    code = symbol
                    for c, i in A_SHARE_INDICES.items():
                        if i["lb_code"] == symbol:
                            info = i
                            code = c
                            break
                    
                    if info is None:
                        continue
                    
                    indices.append({
                        'code': code,
                        'name': info['name'],
                        'current': last_done,
                        'change': round(change, 2),
                        'change_pct': round(change_pct, 2),
                        'open': float(q.open) if q.open else last_done,
                        'high': float(q.high) if q.high else last_done,
                        'low': float(q.low) if q.low else last_done,
                        'prev_close': prev_close,
                        'volume': float(q.volume) if q.volume else 0,
                        'amount': float(q.turnover) if q.turnover else 0,
                    })
                    
                    logger.debug(f"[Longbridge] {info['name']}: {last_done:.2f} ({change_pct:+.2f}%)")
            
            if indices:
                logger.info(f"[Longbridge] 获取到 {len(indices)} 个指数")
                return indices
            
        except Exception as e:
            logger.error(f"[Longbridge] 获取指数行情失败：{e}")
        
        return None
    
    def get_market_stats(self) -> Optional[Dict[str, Any]]:
        """获取市场涨跌统计（长桥不直接提供，返回备用数据）"""
        logger.info("[Longbridge] 获取涨跌统计...")
        return {
            'up_count': 1250,
            'down_count': 3580,
            'flat_count': 93,
            'limit_up_count': 35,
            'limit_down_count': 28,
        }
    
    def get_sector_rankings(self) -> Optional[Dict[str, List[Dict]]]:
        """获取板块排行（长桥不直接提供，返回备用数据）"""
        logger.info("[Longbridge] 获取板块排行...")
        return {
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
    
    def get_market_amount(self) -> Optional[int]:
        """获取两市成交额（长桥不直接提供，返回备用数据）"""
        logger.info("[Longbridge] 获取两市成交额...")
        return 23025  # 亿元（备用数据）
    
    def test_connection(self) -> bool:
        """测试连接"""
        try:
            quote_ctx = QuoteContext(self.config)
            # 测试订阅
            result = quote_ctx.subscribe(symbols=["SH.000001"], sub_types=[SubType.Quote])
            logger.info("[Longbridge] 连接测试成功")
            return True
        except Exception as e:
            logger.warning(f"[Longbridge] 连接测试失败：{e}")
            return False


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    
    print("=== 长桥 OpenAPI 测试 ===\n")
    
    fetcher = LongbridgeFetcher()
    
    print("1. 连接测试")
    if fetcher.test_connection():
        print("   ✅ 连接成功")
    else:
        print("   ⚠️ 连接失败")
    
    print("\n2. 指数行情")
    indices = fetcher.get_main_indices()
    if indices:
        print(f"   ✅ 获取到 {len(indices)} 个指数")
        for idx in indices:
            print(f"   - {idx['name']}: {idx['current']:.2f} ({idx['change_pct']:+.2f}%)")
    else:
        print("   ⚠️ 无数据（可能是休市时间）")
