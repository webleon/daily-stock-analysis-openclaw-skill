"""
Agent 单元测试
"""

import pytest
from src.agents.base import BaseAgent
from src.agents.analysis_agent import AnalysisAgent
from src.agents.scheduler_agent import SchedulerAgent
from src.agents.report_agent import ReportAgent


class TestBaseAgent:
    """BaseAgent 测试"""
    
    def test_init(self):
        """测试初始化"""
        agent = BaseAgent()
        assert agent.name == "base_agent"
        assert agent.version == "1.0.0"
    
    def test_validate(self):
        """测试验证"""
        agent = BaseAgent()
        assert agent.validate() == True
    
    def test_get_info(self):
        """测试获取信息"""
        agent = BaseAgent()
        info = agent.get_info()
        assert "name" in info
        assert "version" in info


class TestAnalysisAgent:
    """AnalysisAgent 测试"""
    
    def test_init(self):
        """测试初始化"""
        config = {"model": "qwen3.5-plus", "max_tokens": 4096}
        agent = AnalysisAgent(config)
        assert agent.name == "analysis_agent"
        assert agent.model == "qwen3.5-plus"
    
    def test_analyze_missing_stock_code(self):
        """测试缺少股票代码"""
        agent = AnalysisAgent()
        result = agent.analyze({})
        assert result["success"] == False
        assert "error" in result


class TestSchedulerAgent:
    """SchedulerAgent 测试"""
    
    def test_init(self):
        """测试初始化"""
        config = {"max_workers": 3, "timeout": 300}
        agent = SchedulerAgent(config)
        assert agent.name == "scheduler_agent"
        assert agent.max_workers == 3
    
    def test_analyze_missing_tasks(self):
        """测试缺少任务列表"""
        agent = SchedulerAgent()
        result = agent.analyze({})
        assert result["success"] == False
        assert "error" in result


class TestReportAgent:
    """ReportAgent 测试"""
    
    def test_init(self):
        """测试初始化"""
        config = {"output_formats": ["html", "markdown"], "languages": ["zh", "en"]}
        agent = ReportAgent(config)
        assert agent.name == "report_agent"
        assert "html" in agent.output_formats
    
    def test_analyze_missing_result(self):
        """测试缺少分析结果"""
        agent = ReportAgent()
        result = agent.analyze({})
        assert result["success"] == False
        assert "error" in result
