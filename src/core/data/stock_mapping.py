"""
股票代码映射和名称验证
简化版本，仅包含基本功能
"""

# A 股指数代码映射
STOCK_NAME_MAP = {
    '000001': '上证指数',
    '399001': '深证成指',
    '399006': '创业板指',
    '000016': '上证 50',
    '000300': '沪深 300',
    '000688': '科创 50',
}


def is_meaningful_stock_name(name: str) -> bool:
    """
    检查股票名称是否有意义
    
    Args:
        name: 股票名称
    
    Returns:
        bool: 是否有意义
    """
    if not name:
        return False
    
    # 排除无意义的名称
    meaningless = ['未知', 'N/A', 'None', '']
    return name not in meaningless
