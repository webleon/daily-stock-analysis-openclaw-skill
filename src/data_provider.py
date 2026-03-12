#!/usr/bin/env python3
"""
数据源适配层
支持多种数据源，自动切换
处理非交易时间数据
"""

import os
from typing import Optional, Dict, Any
from datetime import datetime, time

class StockDataProvider:
    """股票数据提供商 - 支持多数据源"""
    
    def __init__(self):
        self.primary_source = os.getenv('STOCK_DATA_SOURCE', 'akshare')
        self.tushare_token = os.getenv('TUSHARE_TOKEN', '')
        self._tushare_pro = None
    
    def is_trading_time(self) -> bool:
        """判断是否在交易时间"""
        now = datetime.now().time()
        
        # A 股交易时间
        morning_start = time(9, 30)
        morning_end = time(11, 30)
        afternoon_start = time(13, 0)
        afternoon_end = time(15, 0)
        
        is_morning = morning_start <= now <= morning_end
        is_afternoon = afternoon_start <= now <= afternoon_end
        
        # 周末不交易
        is_weekday = datetime.now().weekday() < 5
        
        return is_weekday and (is_morning or is_afternoon)
    
    def get_stock_data(self, stock_code: str) -> Dict[str, Any]:
        """
        获取股票完整数据
        
        Returns:
            包含股票数据的字典
        """
        import akshare as ak
        
        df = ak.stock_zh_a_spot_em()
        stock = df[df['代码'] == stock_code]
        
        if stock.empty:
            return {}
        
        stock_data = stock.iloc[0]
        
        # 判断是否交易时间
        trading_time = self.is_trading_time()
        
        # 处理数据（非交易时间使用昨收数据）
        def safe_float(value, default=None):
            """安全转换 float，处理 NaN"""
            try:
                import pandas as pd
                if pd.isna(value):
                    return default
                return float(value)
            except:
                return default
        
        current_price = safe_float(stock_data['最新价'])
        change_percent = safe_float(stock_data['涨跌幅'])
        
        # 如果最新价是 NaN，使用昨收价
        if current_price is None:
            current_price = safe_float(stock_data['昨收'])
            price_note = '（昨收）'
        else:
            price_note = ''
        
        # 如果涨跌幅是 NaN，设为 0
        if change_percent is None:
            change_percent = 0.0
        
        # 获取 PE（使用适配层）
        pe = self.get_pe(stock_code)
        
        return {
            '代码': stock_code,
            '名称': stock_data['名称'],
            '最新价': current_price,
            '价格备注': price_note,
            '涨跌幅': change_percent,
            '成交量': safe_float(stock_data['成交量'], 0),
            '成交额': safe_float(stock_data['成交额'], 0),
            '总市值': safe_float(stock_data['总市值'], 0),
            '市盈率': pe,
            '市净率': safe_float(stock_data['市净率'], 0),
            '昨收': safe_float(stock_data['昨收'], 0),
            '最高': safe_float(stock_data['最高'], 0),
            '最低': safe_float(stock_data['最低'], 0),
            '今开': safe_float(stock_data['今开'], 0),
            '量比': safe_float(stock_data['量比'], 0),
            '换手率': safe_float(stock_data['换手率'], 0),
            '交易时间': trading_time,
        }
    
    def get_pe(self, stock_code: str) -> Optional[str]:
        """
        获取市盈率（动态）
        
        Args:
            stock_code: 股票代码（如 '603039'）
            
        Returns:
            PE 值（字符串），如果缺失返回 'N/A'，如果亏损返回 '亏损'
        """
        # 尝试配置的数据源
        if self.primary_source == 'tushare' and self.tushare_token:
            pe = self._get_pe_tushare(stock_code)
            if pe:
                return pe
        
        # 默认使用 AkShare
        return self._get_pe_akshare(stock_code)
    
    def _get_pe_akshare(self, stock_code: str) -> Optional[str]:
        """从 AkShare 获取 PE"""
        try:
            import akshare as ak
            import pandas as pd
            
            df = ak.stock_zh_a_spot_em()
            stock = df[df['代码'] == stock_code]
            
            if stock.empty:
                return 'N/A'
            
            pe = stock['市盈率 - 动态'].iloc[0]
            
            # 处理数据
            if pd.isna(pe) or pe == '' or str(pe) == 'nan':
                return 'N/A'
            
            try:
                pe_float = float(pe)
                if pe_float < 0:
                    return '亏损'
                elif pe_float == 0:
                    return 'N/A'
                else:
                    return f'{pe_float:.2f}'
            except:
                return 'N/A'
                
        except Exception as e:
            print(f'⚠️  AkShare 获取 PE 失败：{e}')
            return 'N/A'
    
    def _get_pe_tushare(self, stock_code: str) -> Optional[str]:
        """从 Tushare 获取 PE"""
        try:
            import tushare as ts
            
            if not self._tushare_pro:
                ts.set_token(self.tushare_token)
                self._tushare_pro = ts.pro_api()
            
            # 获取实时行情
            df = self._tushare_pro.daily_basic(
                ts_code=f'{stock_code}.SH' if stock_code.startswith('6') else f'{stock_code}.SZ',
                trade_date=''  # 最新数据
            )
            
            if df.empty:
                return None
            
            pe = df['pe'][0]
            
            if pe is None or pe == '':
                return None
            
            pe_float = float(pe)
            if pe_float < 0:
                return '亏损'
            elif pe_float == 0:
                return None
            else:
                return f'{pe_float:.2f}'
                
        except Exception as e:
            print(f'⚠️  Tushare 获取 PE 失败：{e}')
            return None


# 全局实例
data_provider = StockDataProvider()
