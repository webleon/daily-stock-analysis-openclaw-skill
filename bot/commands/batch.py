# -*- coding: utf-8 -*-
"""
===================================
批量分析命令
===================================

批量分析自选股列表中的所有股票。
"""

import logging
import threading
from typing import List

from bot.commands.base import BotCommand
from bot.models import BotMessage, BotResponse

logger = logging.getLogger(__name__)


class BatchCommand(BotCommand):
    """
    批量分析命令
    
    批量分析配置中的自选股列表，生成汇总报告。
    
    用法：
        /batch      - 分析所有自选股
        /batch 3    - 只分析前 3 只
    """
    
    @property
    def name(self) -> str:
        return "batch"
    
    @property
    def aliases(self) -> List[str]:
        return ["b", "批量", "全部"]
    
    @property
    def description(self) -> str:
        return "批量分析自选股"
    
    @property
    def usage(self) -> str:
        return "/batch [数量]"
    
    @property
    def admin_only(self) -> bool:
        """批量分析需要管理员权限（防止滥用）"""
        return False  # 可以根据需要设为 True
    
    def execute(self, message: BotMessage, args: List[str]) -> BotResponse:
        """执行批量分析命令"""
        from src.config import get_config
        
        config = get_config()
        config.refresh_stock_list()
        
        stock_list = config.stock_list
        
        if not stock_list:
            return BotResponse.error_response(
                "自选股列表为空，请先配置 STOCK_LIST"
            )
        
        # 解析数量参数
        limit = None
        if args:
            try:
                limit = int(args[0])
                if limit <= 0:
                    return BotResponse.error_response("数量必须大于 0")
            except ValueError:
                return BotResponse.error_response(f"无效的数量：{args[0]}")
        
        # 限制分析数量
        if limit:
            stock_list = stock_list[:limit]
        
        logger.info(f"[BatchCommand] 开始批量分析 {len(stock_list)} 只股票")
        
        # 在后台线程中执行分析
        thread = threading.Thread(
            target=self._run_batch_analysis,
            args=(stock_list, message),
            daemon=True
        )
        thread.start()
        
        return BotResponse.markdown_response(
            f"✅ **批量分析任务已启动**\n\n"
            f"• 分析数量：{len(stock_list)} 只\n"
            f"• 股票列表：{', '.join(stock_list[:5])}"
            f"{'...' if len(stock_list) > 5 else ''}\n\n"
            f"分析完成后将自动推送汇总报告。"
        )
    
    def _run_batch_analysis(self, stock_list: List[str], message: BotMessage) -> None:
        """后台执行批量分析"""
        from src.analyzer import GeminiAnalyzer
        from src.search_service import SearchService
        from data_provider.manager import DataFetcherManager
        from src.notification import NotificationService
        
        results = []
        failed = []
        
        for i, code in enumerate(stock_list, 1):
            logger.info(f"[BatchCommand] 分析第 {i}/{len(stock_list)} 只股票：{code}")
            
            try:
                # 获取数据
                data_manager = DataFetcherManager()
                stock_data = data_manager.get_stock_data(code)
                
                if not stock_data:
                    failed.append(code)
                    continue
                
                # 分析股票（使用默认策略）
                analyzer = GeminiAnalyzer()
                search_service = SearchService()
                
                analysis = analyzer.analyze_stock_default(stock_data, search_service)
                
                if analysis:
                    results.append({
                        'code': code,
                        'analysis': analysis
                    })
                else:
                    failed.append(code)
                    
            except Exception as e:
                logger.error(f"[BatchCommand] 分析 {code} 失败：{e}")
                failed.append(code)
        
        # 生成汇总报告
        self._send_batch_report(results, failed, message)
    
    def _send_batch_report(self, results: List[dict], failed: List[str], message: BotMessage) -> None:
        """发送批量分析汇总报告"""
        from src.notification import NotificationService
        
        notifier = NotificationService()
        
        # 构建汇总报告
        report = "# 📊 批量分析报告\n\n"
        report += f"✅ 分析完成：{len(results)} 只\n"
        report += f"❌ 分析失败：{len(failed)} 只\n\n"
        
        # 添加每只股票的分析摘要
        for i, result in enumerate(results, 1):
            code = result['code']
            analysis = result['analysis']
            
            # 提取关键信息（第一行）
            first_line = analysis.split('\n')[0] if analysis else "分析失败"
            
            report += f"## {i}. {code}\n{first_line}\n\n"
        
        # 添加失败列表
        if failed:
            report += "## ❌ 分析失败\n\n"
            report += ", ".join(failed)
            report += "\n\n"
        
        # 发送报告
        if notifier.is_available():
            notifier.send(report)
            logger.info(f"[BatchCommand] 汇总报告已发送")
        else:
            logger.warning(f"[BatchCommand] 通知渠道不可用，无法发送报告")
