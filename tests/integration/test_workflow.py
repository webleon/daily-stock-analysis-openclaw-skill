"""
集成测试 - 完整工作流测试
"""

import pytest
from src.agents.analysis_agent import AnalysisAgent
from src.agents.scheduler_agent import SchedulerAgent
from src.agents.report_agent import ReportAgent


class TestWorkflow:
    """工作流集成测试"""
    
    def test_full_workflow(self):
        """测试完整工作流"""
        # 1. 分析 Agent
        analysis_agent = AnalysisAgent()
        analysis_result = analysis_agent.analyze({"stock_code": "AAPL"})
        
        # 2. 调度 Agent
        scheduler_agent = SchedulerAgent()
        scheduler_result = scheduler_agent.analyze({
            "tasks": [{"name": "analysis", "type": "analysis"}]
        })
        
        # 3. 报告 Agent
        report_agent = ReportAgent()
        report_result = report_agent.analyze({
            "analysis_result": analysis_result,
            "stock_code": "AAPL"
        })
        
        # 验证结果
        assert analysis_result is not None
        assert scheduler_result is not None
        assert report_result is not None
