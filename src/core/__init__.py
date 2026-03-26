"""
原项目核心功能包装器
将原项目代码封装为统一的 API 接口
"""

from .analysis import SixteenModulesAnalyzer, SixPerspectivesAnalyzer
from .data import DataFetcherManager
from .report import HTMLReportGenerator
from datetime import datetime
from pathlib import Path


class StockAnalysisCore:
    """股票分析核心引擎"""
    
    def __init__(self, config=None):
        self.config = config or {}
        
        # 初始化分析器
        self.sixteen_modules = SixteenModulesAnalyzer()
        self.six_perspectives = SixPerspectivesAnalyzer()
        
        # 初始化数据获取器
        self.data_manager = DataFetcherManager()
        
        # 初始化报告生成器
        self.report_generator = HTMLReportGenerator()
    
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
    
    def generate_report(self, analysis_result, fmt='html', lang='zh', output_path=None):
        """
        生成报告（默认输出到统一目录）
        
        Args:
            analysis_result: 分析结果字典
            fmt: 报告格式 ('html' 或 'md')
            lang: 语言 ('zh' 或 'en')
            output_path: 输出文件路径（可选，默认使用统一目录）
        
        Returns:
            报告内容字符串
        """
        # 统一输出目录
        default_output_dir = Path.home() / '.openclaw' / 'workspace' / 'output' / 'reports'
        default_output_dir.mkdir(parents=True, exist_ok=True)
        
        # 如果没有指定输出路径，使用默认路径
        if output_path is None:
            stock_code = analysis_result.get('stock_code', 'unknown')
            report_date = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_path = default_output_dir / f"{stock_code}_{report_date}_report.html"
        
        if fmt == 'html':
            generator = HTMLReportGenerator()
            return generator.generate(analysis_result, str(output_path))
        else:
            # TODO: Markdown 报告生成
            return f"# {analysis_result.get('stock_name', '股票')} 分析报告\n\n报告内容..."
