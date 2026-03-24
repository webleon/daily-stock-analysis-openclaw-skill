#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多 Agent 编排模块
实现 Subagent 级联分析架构
"""

import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict

logger = logging.getLogger(__name__)


@dataclass
class AnalysisTask:
    """分析任务定义"""
    type: str  # technical/sentiment/fundamental
    label: str
    task: str
    stock_code: str
    priority: int = 1


@dataclass
class SubagentResult:
    """Subagent 分析结果"""
    analysis_type: str
    stock_code: str
    timestamp: str
    score: int
    conclusion: str
    key_points: List[str]
    data: Dict[str, Any]
    success: bool = True
    error: Optional[str] = None


class MultiAgentOrchestrator:
    """多 Agent 编排器"""
    
    def __init__(self, stock_code: str):
        self.stock_code = stock_code
        self.results: List[SubagentResult] = []
        self.tasks: List[AnalysisTask] = []
        
    def generate_tasks(self) -> List[AnalysisTask]:
        """生成分析任务清单"""
        self.tasks = [
            AnalysisTask(
                type="technical_analysis",
                label=f"技术面分析-{self.stock_code}",
                task=self._get_technical_prompt(),
                stock_code=self.stock_code,
                priority=1
            ),
            AnalysisTask(
                type="sentiment_analysis",
                label=f"舆情面分析-{self.stock_code}",
                task=self._get_sentiment_prompt(),
                stock_code=self.stock_code,
                priority=1
            ),
            AnalysisTask(
                type="fundamental_analysis",
                label=f"基本面分析-{self.stock_code}",
                task=self._get_fundamental_prompt(),
                stock_code=self.stock_code,
                priority=1
            )
        ]
        return self.tasks
    
    def _get_technical_prompt(self) -> str:
        """技术面分析 prompt"""
        return f"""请对 {self.stock_code} 进行专业技术面分析，包括：

1. 价格趋势分析
   - 当前价格位置
   - 均线系统（20 日/60 日/200 日）
   - 趋势判断（上涨/下跌/震荡）

2. 技术指标
   - RSI(14) 数值和状态
   - MACD 状态（金叉/死叉）
   - 布林带位置
   - 成交量分析

3. 关键价位
   - 支撑位（至少 2 个）
   - 阻力位（至少 2 个）

4. 技术面评分（0-100 分）

请以 JSON 格式返回分析结果，包含以下字段：
{{
  "analysis_type": "technical_analysis",
  "stock_code": "{self.stock_code}",
  "timestamp": "ISO8601 时间戳",
  "score": 0-100,
  "conclusion": "一句话总结",
  "key_points": ["要点 1", "要点 2", ...],
  "data": {{
    "price": 当前价格，
    "ma20": 20 日均线，
    "ma60": 60 日均线，
    "ma200": 200 日均线，
    "rsi": RSI 值，
    "macd": MACD 状态，
    "volume_ratio": 量比，
    "support_levels": [支撑位 1, 支撑位 2],
    "resistance_levels": [阻力位 1, 阻力位 2]
  }}
}}
"""
    
    def _get_sentiment_prompt(self) -> str:
        """舆情面分析 prompt"""
        return f"""请对 {self.stock_code} 进行舆情面分析，包括：

1. 新闻情绪分析
   - 最近 7 天重要新闻
   - 新闻情感倾向（积极/消极/中性）
   - 重大事件影响

2. 社交媒体热度
   - 讨论热度变化
   - 主流观点倾向
   - 散户情绪

3. 机构观点
   - 投行评级变化
   - 目标价调整
   - 持仓变化

4. 舆情面评分（0-100 分）

请以 JSON 格式返回分析结果，包含以下字段：
{{
  "analysis_type": "sentiment_analysis",
  "stock_code": "{self.stock_code}",
  "timestamp": "ISO8601 时间戳",
  "score": 0-100,
  "conclusion": "一句话总结",
  "key_points": ["要点 1", "要点 2", ...],
  "data": {{
    "news_sentiment": "积极/消极/中性",
    "social_sentiment": "积极/消极/中性",
    "institutional_sentiment": "积极/消极/中性",
    "recent_news": [{{"title": "标题", "sentiment": "情感", "date": "日期"}}],
    "analyst_ratings": {{
      "buy": 买入数量，
      "hold": 持有数量，
      "sell": 卖出数量，
      "avg_target": 平均目标价
    }}
  }}
}}
"""
    
    def _get_fundamental_prompt(self) -> str:
        """基本面分析 prompt"""
        return f"""请对 {self.stock_code} 进行深度基本面分析，包括：

1. 估值水平
   - PE(TTM) 及历史分位
   - PEG 及合理性
   - PB 及行业对比
   - PS 及行业对比

2. 财务健康度
   - 营收增长率 (YoY)
   - 净利润增长率 (YoY)
   - 毛利率变化
   - ROE 水平
   - 负债率

3. 成长驱动力
   - 核心业务增长
   - 新业务进展
   - 市场空间
   - 竞争优势

4. 基本面评分（0-100 分）

请以 JSON 格式返回分析结果，包含以下字段：
{{
  "analysis_type": "fundamental_analysis",
  "stock_code": "{self.stock_code}",
  "timestamp": "ISO8601 时间戳",
  "score": 0-100,
  "conclusion": "一句话总结",
  "key_points": ["要点 1", "要点 2", ...],
  "data": {{
    "valuation": {{
      "pe_ttm": PE 值，
      "peg": PEG 值，
      "pb": PB 值，
      "ps": PS 值
    }},
    "financials": {{
      "revenue_growth": 营收增长率，
      "profit_growth": 利润增长率，
      "gross_margin": 毛利率，
      "roe": ROE,
      "debt_ratio": 负债率
    }},
    "growth_drivers": ["驱动力 1", "驱动力 2", ...]
  }}
}}
"""
    
    def parse_subagent_result(self, result_text: str, task_type: str) -> SubagentResult:
        """解析 subagent 返回结果"""
        try:
            # 尝试从文本中提取 JSON
            json_start = result_text.find('{')
            json_end = result_text.rfind('}') + 1
            
            if json_start == -1 or json_end == 0:
                raise ValueError("未找到 JSON 格式结果")
            
            json_str = result_text[json_start:json_end]
            data = json.loads(json_str)
            
            return SubagentResult(
                analysis_type=data.get("analysis_type", task_type),
                stock_code=data.get("stock_code", self.stock_code),
                timestamp=data.get("timestamp", datetime.now().isoformat()),
                score=data.get("score", 50),
                conclusion=data.get("conclusion", ""),
                key_points=data.get("key_points", []),
                data=data.get("data", {}),
                success=True
            )
            
        except Exception as e:
            logger.error(f"解析 subagent 结果失败：{e}")
            return SubagentResult(
                analysis_type=task_type,
                stock_code=self.stock_code,
                timestamp=datetime.now().isoformat(),
                score=50,
                conclusion="分析失败",
                key_points=[f"解析错误：{str(e)}"],
                data={},
                success=False,
                error=str(e)
            )
    
    def synthesize_results(self) -> Dict[str, Any]:
        """综合分析所有 subagent 结果"""
        # 获取各维度结果
        technical = next((r for r in self.results if r.analysis_type == "technical_analysis"), None)
        sentiment = next((r for r in self.results if r.analysis_type == "sentiment_analysis"), None)
        fundamental = next((r for r in self.results if r.analysis_type == "fundamental_analysis"), None)
        
        # 检查是否有失败的分析
        failed_analyses = [r for r in self.results if not r.success]
        if failed_analyses:
            logger.warning(f"以下分析失败：{[r.analysis_type for r in failed_analyses]}")
        
        # 计算综合评分
        scores = []
        weights = []
        
        if technical and technical.success:
            scores.append(technical.score)
            weights.append(0.35)
        if sentiment and sentiment.success:
            scores.append(sentiment.score)
            weights.append(0.25)
        if fundamental and fundamental.success:
            scores.append(fundamental.score)
            weights.append(0.40)
        
        if not scores:
            overall_score = 50
        else:
            overall_score = sum(s * w for s, w in zip(scores, weights)) / sum(weights)
        
        # 生成决策仪表盘
        dashboard = self._generate_dashboard(technical, sentiment, fundamental, overall_score)
        
        return {
            "stock_code": self.stock_code,
            "overall_score": round(overall_score, 1),
            "timestamp": datetime.now().isoformat(),
            "dashboard": dashboard,
            "subagent_results": {
                "technical": asdict(technical) if technical else None,
                "sentiment": asdict(sentiment) if sentiment else None,
                "fundamental": asdict(fundamental) if fundamental else None
            },
            "analysis_count": len([r for r in self.results if r.success]),
            "failed_count": len(failed_analyses)
        }
    
    def _generate_dashboard(
        self,
        technical: Optional[SubagentResult],
        sentiment: Optional[SubagentResult],
        fundamental: Optional[SubagentResult],
        overall_score: float
    ) -> Dict[str, Any]:
        """生成决策仪表盘"""
        
        # 核心结论
        core_conclusion = self._generate_core_conclusion(technical, sentiment, fundamental, overall_score)
        
        # 数据透视
        data_perspective = self._generate_data_perspective(technical)
        
        # 情报信息
        intelligence = self._generate_intelligence(sentiment, fundamental)
        
        # 作战计划
        battle_plan = self._generate_battle_plan(technical, overall_score)
        
        return {
            "core_conclusion": core_conclusion,
            "data_perspective": data_perspective,
            "intelligence": intelligence,
            "battle_plan": battle_plan
        }
    
    def _generate_core_conclusion(
        self,
        technical: Optional[SubagentResult],
        sentiment: Optional[SubagentResult],
        fundamental: Optional[SubagentResult],
        overall_score: float
    ) -> Dict[str, str]:
        """生成核心结论"""
        
        # 判断信号类型
        if overall_score >= 75:
            signal_type = "强烈买入"
        elif overall_score >= 65:
            signal_type = "买入"
        elif overall_score >= 55:
            signal_type = "持有"
        elif overall_score >= 45:
            signal_type = "减持"
        else:
            signal_type = "卖出"
        
        # 仓位建议
        if overall_score >= 75:
            position = "重仓 (70-80%)"
        elif overall_score >= 65:
            position = "中等仓位 (50-60%)"
        elif overall_score >= 55:
            position = "轻仓 (30-40%)"
        else:
            position = "观望"
        
        # 一句话总结
        conclusions = []
        if technical and technical.success:
            conclusions.append(technical.conclusion)
        if sentiment and sentiment.success:
            conclusions.append(sentiment.conclusion)
        if fundamental and fundamental.success:
            conclusions.append(fundamental.conclusion)
        
        one_sentence = "；".join(conclusions[:2]) if conclusions else "综合分析，建议谨慎操作"
        
        return {
            "one_sentence": one_sentence,
            "signal_type": signal_type,
            "position_suggestion": position
        }
    
    def _generate_data_perspective(self, technical: Optional[SubagentResult]) -> Dict[str, str]:
        """生成数据透视"""
        if not technical or not technical.success:
            return {
                "trend_status": "数据不足",
                "price_position": "未知",
                "volume_status": "未知",
                "chip_structure": "未知"
            }
        
        tech_data = technical.data
        price = tech_data.get("price", 0)
        ma20 = tech_data.get("ma20", 0)
        ma60 = tech_data.get("ma60", 0)
        
        # 价格位置判断
        if price > ma20:
            price_position = f"位于 20 日均线 (${ma20}) 上方"
        else:
            price_position = f"位于 20 日均线 (${ma20}) 下方"
        
        return {
            "trend_status": technical.conclusion,
            "price_position": price_position,
            "volume_status": tech_data.get("volume_status", "成交量正常"),
            "chip_structure": "机构持仓稳定"
        }
    
    def _generate_intelligence(
        self,
        sentiment: Optional[SubagentResult],
        fundamental: Optional[SubagentResult]
    ) -> Dict[str, Any]:
        """生成情报信息"""
        risk_alerts = []
        positive_catalysts = []
        news = []
        
        if sentiment and sentiment.success:
            # 风险警报
            if sentiment.score < 50:
                risk_alerts.append("舆情面偏消极，需警惕负面新闻")
            
            # 积极催化剂
            if sentiment.score >= 70:
                positive_catalysts.append("舆情面积极，市场情绪良好")
            
            # 新闻列表
            news_data = sentiment.data.get("recent_news", [])
            news = news_data[:5] if news_data else []
        
        if fundamental and fundamental.success:
            fund_data = fundamental.data
            
            # 财务风险
            financials = fund_data.get("financials", {})
            if financials.get("revenue_growth", 0) < 0:
                risk_alerts.append("营收负增长，需关注业务下滑")
            if financials.get("debt_ratio", 0) > 0.7:
                risk_alerts.append("负债率偏高，财务风险较大")
            
            # 成长驱动力
            growth_drivers = fund_data.get("growth_drivers", [])
            if growth_drivers:
                positive_catalysts.extend(growth_drivers[:3])
        
        return {
            "news": news,
            "risk_alerts": risk_alerts,
            "positive_catalysts": positive_catalysts
        }
    
    def _generate_battle_plan(
        self,
        technical: Optional[SubagentResult],
        overall_score: float
    ) -> Dict[str, Any]:
        """生成作战计划"""
        if not technical or not technical.success:
            return {
                "sniper_points": {
                    "buy_zone_1": "等待技术面分析",
                    "buy_zone_2": "等待技术面分析",
                    "stop_loss": "等待技术面分析",
                    "target_1": "等待技术面分析",
                    "target_2": "等待技术面分析"
                },
                "position_strategy": "等待完整分析",
                "risk_checklist": []
            }
        
        tech_data = technical.data
        price = tech_data.get("price", 0)
        ma60 = tech_data.get("ma60", price * 0.95)
        support_levels = tech_data.get("support_levels", [price * 0.95, price * 0.90])
        resistance_levels = tech_data.get("resistance_levels", [price * 1.05, price * 1.10])
        
        # 买卖点位
        sniper_points = {
            "buy_zone_1": f"${support_levels[0] if len(support_levels) > 0 else price * 0.95:.2f}",
            "buy_zone_2": f"${support_levels[1] if len(support_levels) > 1 else price * 0.90:.2f}",
            "stop_loss": f"${ma60 * 0.92:.2f}",
            "target_1": f"${resistance_levels[0] if len(resistance_levels) > 0 else price * 1.05:.2f}",
            "target_2": f"${resistance_levels[1] if len(resistance_levels) > 1 else price * 1.10:.2f}"
        }
        
        # 仓位策略
        if overall_score >= 75:
            position_strategy = "分批建仓：第一买点 30%，第二买点 30%，突破阻力位加仓 20%"
        elif overall_score >= 65:
            position_strategy = "逢低布局：第一买点 30%，第二买点 30%，总仓位不超过 60%"
        elif overall_score >= 55:
            position_strategy = "轻仓试探：第一买点 20%，严格止损，总仓位不超过 40%"
        else:
            position_strategy = "观望为主，等待更明确的买入信号"
        
        # 风险检查清单
        risk_checklist = [
            "20 日均线是否有效支撑",
            "成交量是否放大",
            "是否跌破关键支撑位",
            "是否有重大利空消息",
            "大盘环境是否稳定"
        ]
        
        return {
            "sniper_points": sniper_points,
            "position_strategy": position_strategy,
            "risk_checklist": risk_checklist
        }


# 测试函数
def test_orchestrator():
    """测试编排器"""
    orchestrator = MultiAgentOrchestrator("AAPL")
    
    # 生成任务
    tasks = orchestrator.generate_tasks()
    print(f"生成 {len(tasks)} 个分析任务:")
    for task in tasks:
        print(f"  - {task.label}")
    
    # 模拟 subagent 结果
    mock_results = [
        """{
  "analysis_type": "technical_analysis",
  "stock_code": "AAPL",
  "timestamp": "2026-03-24T22:45:00Z",
  "score": 65,
  "conclusion": "短期震荡，中期上涨趋势未变",
  "key_points": ["价格位于 20 日均线附近", "成交量萎缩", "RSI 中性"],
  "data": {
    "price": 172.50,
    "ma20": 171.20,
    "ma60": 168.80,
    "rsi": 58,
    "volume_ratio": 0.90,
    "support_levels": [168.80, 165.00],
    "resistance_levels": [175.40, 180.00]
  }
}""",
        """{
  "analysis_type": "sentiment_analysis",
  "stock_code": "AAPL",
  "timestamp": "2026-03-24T22:45:00Z",
  "score": 72,
  "conclusion": "舆情面积极，Vision Pro 预售超预期",
  "key_points": ["Vision Pro 预售突破 50 万台", "1100 亿美元回购计划", "中国销量担忧"],
  "data": {
    "news_sentiment": "积极",
    "recent_news": [
      {"title": "Vision Pro 预售突破 50 万台", "sentiment": "积极", "date": "2026-03-23"}
    ]
  }
}""",
        """{
  "analysis_type": "fundamental_analysis",
  "stock_code": "AAPL",
  "timestamp": "2026-03-24T22:45:00Z",
  "score": 85,
  "conclusion": "基本面强劲，Services 业务持续增长",
  "key_points": ["Services 业务 +15%", "毛利率 45.2%", "ROE 145%"],
  "data": {
    "valuation": {"pe_ttm": 28.5, "peg": 2.1, "pb": 45.2, "ps": 7.8},
    "financials": {
      "revenue_growth": 0.085,
      "profit_growth": 0.123,
      "gross_margin": 0.452,
      "roe": 1.45,
      "debt_ratio": 0.32
    },
    "growth_drivers": ["Services 业务高增长", "Vision Pro 新增长点", "回购支撑 EPS"]
  }
}"""
    ]
    
    # 解析结果
    for i, result_text in enumerate(mock_results):
        result = orchestrator.parse_subagent_result(result_text, tasks[i].type)
        orchestrator.results.append(result)
        print(f"\n解析结果 {i+1}:")
        print(f"  类型：{result.analysis_type}")
        print(f"  评分：{result.score}")
        print(f"  结论：{result.conclusion}")
    
    # 综合分析
    final_report = orchestrator.synthesize_results()
    
    print(f"\n=== 综合分析报告 ===")
    print(f"股票：{final_report['stock_code']}")
    print(f"综合评分：{final_report['overall_score']}")
    print(f"核心结论：{final_report['dashboard']['core_conclusion']['one_sentence']}")
    print(f"信号类型：{final_report['dashboard']['core_conclusion']['signal_type']}")
    print(f"仓位建议：{final_report['dashboard']['core_conclusion']['position_suggestion']}")
    
    return final_report


if __name__ == "__main__":
    test_orchestrator()
