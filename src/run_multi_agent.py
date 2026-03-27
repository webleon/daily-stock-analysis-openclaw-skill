#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多 Agent 编排主入口
在 OpenClaw 主会话中调用此模块启动多 Agent 分析
"""

import sys
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List

# 添加模块路径
sys.path.insert(0, str(Path(__file__).parent))

from multi_agent_orchestrator import MultiAgentOrchestrator, SubagentResult
try:
    from .agents.subagent_tasks import get_all_tasks
except ImportError:
    get_all_tasks = None

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def run_multi_agent_analysis(stock_code: str) -> Dict[str, Any]:
    """
    执行多 Agent 编排分析
    
    Args:
        stock_code: 股票代码
    
    Returns:
        综合分析报告字典
    """
    logger.info(f"开始多 Agent 分析：{stock_code}")
    
    # 1. 创建编排器
    orchestrator = MultiAgentOrchestrator(stock_code)
    
    # 2. 生成任务清单
    tasks = orchestrator.generate_tasks()
    logger.info(f"生成 {len(tasks)} 个分析任务")
    
    # 3. 在真实 OpenClaw 环境中，这里会启动 subagents
    # 目前使用模拟数据演示流程
    logger.info("启动 subagents...（模拟模式）")
    
    # 模拟 subagent 执行
    mock_results = _execute_mock_subagents(stock_code)
    
    # 4. 解析 subagent 结果
    for i, (result_text, task) in enumerate(zip(mock_results, tasks)):
        result = orchestrator.parse_subagent_result(result_text, task.type)
        orchestrator.results.append(result)
        logger.info(f"解析结果 {i+1}: {result.analysis_type} - 评分 {result.score}")
    
    # 5. 综合分析
    logger.info("综合分析中...")
    final_report = orchestrator.synthesize_results()
    
    logger.info(f"分析完成！综合评分：{final_report['overall_score']}")
    
    return final_report


def _execute_mock_subagents(stock_code: str) -> List[str]:
    """
    模拟 subagent 执行（演示用）
    
    在真实 OpenClaw 环境中，这里会通过 sessions_spawn 启动真实的 subagents
    """
    
    # 模拟技术面分析结果
    technical_result = json.dumps({
        "analysis_type": "technical_analysis",
        "stock_code": stock_code,
        "timestamp": datetime.now().isoformat(),
        "score": 65,
        "conclusion": "短期震荡，中期上涨趋势未变",
        "key_points": [
            "价格位于 20 日均线附近",
            "成交量萎缩，观望情绪浓厚",
            "RSI 中性，MACD 金叉"
        ],
        "data": {
            "price": 172.50,
            "ma20": 171.20,
            "ma60": 168.80,
            "ma200": 175.40,
            "rsi": 58,
            "macd": "金叉",
            "volume_ratio": 0.90,
            "volume_status": "成交量萎缩",
            "support_levels": [168.80, 165.00],
            "resistance_levels": [175.40, 180.00]
        }
    }, ensure_ascii=False)
    
    # 模拟舆情面分析结果
    sentiment_result = json.dumps({
        "analysis_type": "sentiment_analysis",
        "stock_code": stock_code,
        "timestamp": datetime.now().isoformat(),
        "score": 72,
        "conclusion": "舆情面积极，Vision Pro 预售超预期",
        "key_points": [
            "Vision Pro 预售突破 50 万台",
            "1100 亿美元回购计划支撑股价",
            "中国销量担忧仍存"
        ],
        "data": {
            "news_sentiment": "积极",
            "social_sentiment": "中性",
            "institutional_sentiment": "积极",
            "recent_news": [
                {
                    "title": "Apple Vision Pro 预售突破 50 万台",
                    "sentiment": "积极",
                    "date": "2026-03-23",
                    "source": "Bloomberg"
                },
                {
                    "title": "苹果宣布 1100 亿美元回购计划",
                    "sentiment": "积极",
                    "date": "2026-03-22",
                    "source": "Reuters"
                }
            ],
            "analyst_ratings": {
                "buy": 25,
                "hold": 8,
                "sell": 2,
                "avg_target": 195.50
            }
        }
    }, ensure_ascii=False)
    
    # 模拟基本面分析结果
    fundamental_result = json.dumps({
        "analysis_type": "fundamental_analysis",
        "stock_code": stock_code,
        "timestamp": datetime.now().isoformat(),
        "score": 85,
        "conclusion": "基本面强劲，Services 业务持续增长",
        "key_points": [
            "Services 业务同比增长 15%，毛利率 72%",
            "Vision Pro 预售超预期，新增长点确立",
            "1100 亿美元回购计划，每股 EPS 增厚约 5%"
        ],
        "data": {
            "valuation": {
                "pe_ttm": 28.5,
                "peg": 2.1,
                "pb": 45.2,
                "ps": 7.8,
                "industry_avg_pe": 25.2
            },
            "financials": {
                "revenue_growth": 0.085,
                "profit_growth": 0.123,
                "gross_margin": 0.452,
                "net_margin": 0.268,
                "roe": 1.45,
                "debt_ratio": 0.32
            },
            "growth_drivers": [
                "Services 业务高增长，成为新引擎",
                "Vision Pro 开启空间计算新时代",
                "iPhone 16 AI 功能升级迎来换机潮",
                "回购计划支撑 EPS 增长"
            ]
        }
    }, ensure_ascii=False)
    
    return [technical_result, sentiment_result, fundamental_result]


def format_report_for_output(report: Dict[str, Any]) -> str:
    """
    格式化报告为输出文本
    
    Args:
        report: 综合分析报告
    
    Returns:
        格式化的文本报告
    """
    dashboard = report["dashboard"]
    core = dashboard["core_conclusion"]
    
    output_lines = [
        f"# {report['stock_code']} 多 Agent 分析报告",
        f"",
        f"**分析时间**: {report['timestamp']}",
        f"**子 Agent 数量**: {report['analysis_count']}/{report['analysis_count'] + report['failed_count']}",
        f"",
        f"## 🎯 核心结论",
        f"",
        f"**一句话总结**: {core['one_sentence']}",
        f"",
        f"| 指标 | 数值 |",
        f"|------|------|",
        f"| **综合评分** | {report['overall_score']}/100 |",
        f"| **信号类型** | {core['signal_type']} |",
        f"| **仓位建议** | {core['position_suggestion']} |",
        f"",
        f"## 📊 决策仪表盘",
        f"",
        f"### 数据透视",
        f"- 趋势状态：{dashboard['data_perspective']['trend_status']}",
        f"- 价格位置：{dashboard['data_perspective']['price_position']}",
        f"- 成交量：{dashboard['data_perspective']['volume_status']}",
        f"- 筹码结构：{dashboard['data_perspective']['chip_structure']}",
        f"",
        f"### 情报信息",
    ]
    
    # 风险警报
    if dashboard["intelligence"]["risk_alerts"]:
        output_lines.append("")
        output_lines.append("**⚠️ 风险提示**:")
        for risk in dashboard["intelligence"]["risk_alerts"]:
            output_lines.append(f"- {risk}")
    
    # 积极催化剂
    if dashboard["intelligence"]["positive_catalysts"]:
        output_lines.append("")
        output_lines.append("**✅ 积极因素**:")
        for catalyst in dashboard["intelligence"]["positive_catalysts"]:
            output_lines.append(f"- {catalyst}")
    
    # 作战计划
    battle_plan = dashboard["battle_plan"]
    output_lines.append("")
    output_lines.append("## 💰 作战计划")
    output_lines.append("")
    output_lines.append("### 买卖点位")
    output_lines.append("")
    output_lines.append(f"- **第一买点**: {battle_plan['sniper_points']['buy_zone_1']}")
    output_lines.append(f"- **第二买点**: {battle_plan['sniper_points']['buy_zone_2']}")
    output_lines.append(f"- **止损点**: {battle_plan['sniper_points']['stop_loss']}")
    output_lines.append(f"- **第一目标**: {battle_plan['sniper_points']['target_1']}")
    output_lines.append(f"- **第二目标**: {battle_plan['sniper_points']['target_2']}")
    output_lines.append("")
    output_lines.append(f"### 仓位策略")
    output_lines.append(f"{battle_plan['position_strategy']}")
    output_lines.append("")
    output_lines.append("### 风险检查清单")
    output_lines.append("")
    for item in battle_plan["risk_checklist"]:
        output_lines.append(f"- [ ] {item}")
    
    return "\n".join(output_lines)


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法：python run_multi_agent.py <股票代码>")
        print("示例：python run_multi_agent.py AAPL")
        sys.exit(1)
    
    stock_code = sys.argv[1].upper()
    
    # 执行多 Agent 分析
    report = run_multi_agent_analysis(stock_code)
    
    # 格式化输出
    formatted_report = format_report_for_output(report)
    print(formatted_report)
    
    # 保存报告
    output_dir = Path.home() / ".openclaw" / "workspace" / "output" / "daily-stock-analysis"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    output_file = output_dir / f"{timestamp}_{stock_code}_multi_agent.md"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(formatted_report)
    
    print(f"\n✅ 报告已保存至：{output_file}")


if __name__ == "__main__":
    main()
