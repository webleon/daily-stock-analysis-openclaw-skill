"""
原项目核心功能包装器
将原项目代码封装为统一的 API 接口
"""

from .analysis import SixteenModulesAnalyzer, SixPerspectivesAnalyzer
from .data import DataFetcherManager
# TODO: 报告生成模块待完善
# from .report import HTMLReportGenerator, MarkdownReportGenerator


class StockAnalysisCore:
    """股票分析核心引擎"""
    
    def __init__(self, config=None):
        self.config = config or {}
        
        # 初始化分析器
        self.sixteen_modules = SixteenModulesAnalyzer()
        self.six_perspectives = SixPerspectivesAnalyzer()
        
        # 初始化数据获取器
        self.data_manager = DataFetcherManager()
    
    def fetch_data(self, stock_code, source='auto'):
        """
        获取股票数据（自动故障切换）
        
        Args:
            stock_code: 股票代码
            source: 数据源（'auto' 表示自动切换）
        
        Returns:
            股票数据字典
        """
        try:
            # 使用数据源管理器自动获取
            data = self.data_manager.get_realtime_quote(stock_code)
            
            if data is None:
                return {
                    "stock_code": stock_code,
                    "error": "所有数据源均失败"
                }
            
            return data
            
        except Exception as e:
            return {
                "stock_code": stock_code,
                "error": str(e)
            }
    
    def analyze(self, stock_code, data):
        """执行分析"""
        # 16 模块分析
        sixteen_modules_result = self.sixteen_modules.analyze(data)
        
        # 6 大投资视角
        six_perspectives_result = self.six_perspectives.analyze(data)
        
        return {
            "stock_code": stock_code,
            "sixteen_modules": sixteen_modules_result,
            "six_perspectives": six_perspectives_result
        }
    
    def generate_report(self, analysis_result, fmt='html', lang='zh'):
        """生成报告"""
        # TODO: 实现实际的报告生成
        return {
            "format": fmt,
            "language": lang,
            "content": ""
        }
