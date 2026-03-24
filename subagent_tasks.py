#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Subagent 任务模板
用于在 OpenClaw 中启动专业分析 subagent
"""

from datetime import datetime
from typing import Dict, Any


def create_technical_analysis_task(stock_code: str) -> Dict[str, Any]:
    """创建技术面分析 subagent 任务"""
    return {
        "label": f"技术面分析-{stock_code}",
        "task": f"""请对 {stock_code} 进行专业技术面分析。

## 分析要求

1. **价格趋势分析**
   - 当前价格位置
   - 均线系统（20 日/60 日/200 日）
   - 趋势判断（上涨/下跌/震荡）

2. **技术指标**
   - RSI(14) 数值和状态
   - MACD 状态（金叉/死叉）
   - 布林带位置
   - 成交量分析

3. **关键价位**
   - 支撑位（至少 2 个）
   - 阻力位（至少 2 个）

4. **技术面评分**（0-100 分）

## 输出格式

请严格按照以下 JSON 格式返回（只返回 JSON，不要其他内容）：

```json
{{
  "analysis_type": "technical_analysis",
  "stock_code": "{stock_code}",
  "timestamp": "{datetime.now().isoformat()}",
  "score": 65,
  "conclusion": "短期震荡，中期上涨趋势未变",
  "key_points": [
    "价格位于 20 日均线附近",
    "成交量萎缩，观望情绪浓厚",
    "RSI 中性，MACD 金叉"
  ],
  "data": {{
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
  }}
}}
```

## 注意事项

- 只返回 JSON，不要 Markdown 格式
- 所有数值必须是实际数字，不要字符串
- 评分必须基于客观指标，不要主观臆断
- 结论要简洁明了，一句话总结
"""
    }


def create_sentiment_analysis_task(stock_code: str) -> Dict[str, Any]:
    """创建舆情面分析 subagent 任务"""
    return {
        "label": f"舆情面分析-{stock_code}",
        "task": f"""请对 {stock_code} 进行舆情面分析。

## 分析要求

1. **新闻情绪分析**
   - 最近 7 天重要新闻
   - 新闻情感倾向（积极/消极/中性）
   - 重大事件影响

2. **社交媒体热度**
   - 讨论热度变化
   - 主流观点倾向
   - 散户情绪

3. **机构观点**
   - 投行评级变化
   - 目标价调整
   - 持仓变化

4. **舆情面评分**（0-100 分）

## 输出格式

请严格按照以下 JSON 格式返回（只返回 JSON，不要其他内容）：

```json
{{
  "analysis_type": "sentiment_analysis",
  "stock_code": "{stock_code}",
  "timestamp": "{datetime.now().isoformat()}",
  "score": 72,
  "conclusion": "舆情面积极，Vision Pro 预售超预期",
  "key_points": [
    "Vision Pro 预售突破 50 万台",
    "1100 亿美元回购计划支撑股价",
    "中国销量担忧仍存"
  ],
  "data": {{
    "news_sentiment": "积极",
    "social_sentiment": "中性",
    "institutional_sentiment": "积极",
    "recent_news": [
      {{
        "title": "Apple Vision Pro 预售突破 50 万台",
        "sentiment": "积极",
        "date": "2026-03-23",
        "source": "Bloomberg"
      }},
      {{
        "title": "苹果宣布 1100 亿美元回购计划",
        "sentiment": "积极",
        "date": "2026-03-22",
        "source": "Reuters"
      }}
    ],
    "analyst_ratings": {{
      "buy": 25,
      "hold": 8,
      "sell": 2,
      "avg_target": 195.50
    }}
  }}
}}
```

## 注意事项

- 只返回 JSON，不要 Markdown 格式
- 新闻列表最多 5 条，按时间倒序
- 评级数据必须是实际数字
- 结论要简洁明了，一句话总结
"""
    }


def create_fundamental_analysis_task(stock_code: str) -> Dict[str, Any]:
    """创建基本面分析 subagent 任务"""
    return {
        "label": f"基本面分析-{stock_code}",
        "task": f"""请对 {stock_code} 进行深度基本面分析。

## 分析要求

1. **估值水平**
   - PE(TTM) 及历史分位
   - PEG 及合理性
   - PB 及行业对比
   - PS 及行业对比

2. **财务健康度**
   - 营收增长率 (YoY)
   - 净利润增长率 (YoY)
   - 毛利率变化
   - ROE 水平
   - 负债率

3. **成长驱动力**
   - 核心业务增长
   - 新业务进展
   - 市场空间
   - 竞争优势

4. **基本面评分**（0-100 分）

## 输出格式

请严格按照以下 JSON 格式返回（只返回 JSON，不要其他内容）：

```json
{{
  "analysis_type": "fundamental_analysis",
  "stock_code": "{stock_code}",
  "timestamp": "{datetime.now().isoformat()}",
  "score": 85,
  "conclusion": "基本面强劲，Services 业务持续增长",
  "key_points": [
    "Services 业务同比增长 15%，毛利率 72%",
    "Vision Pro 预售超预期，新增长点确立",
    "1100 亿美元回购计划，每股 EPS 增厚约 5%"
  ],
  "data": {{
    "valuation": {{
      "pe_ttm": 28.5,
      "peg": 2.1,
      "pb": 45.2,
      "ps": 7.8,
      "industry_avg_pe": 25.2
    }},
    "financials": {{
      "revenue_growth": 0.085,
      "profit_growth": 0.123,
      "gross_margin": 0.452,
      "net_margin": 0.268,
      "roe": 1.45,
      "debt_ratio": 0.32
    }},
    "growth_drivers": [
      "Services 业务高增长，成为新引擎",
      "Vision Pro 开启空间计算新时代",
      "iPhone 16 AI 功能升级迎来换机潮",
      "回购计划支撑 EPS 增长"
    ]
  }}
}}
```

## 注意事项

- 只返回 JSON，不要 Markdown 格式
- 所有财务数据必须是实际数字（小数形式，如 0.085 表示 8.5%）
- 估值数据要与行业对比
- 结论要简洁明了，一句话总结
"""
    }


def get_all_tasks(stock_code: str) -> list:
    """获取所有 subagent 任务"""
    return [
        create_technical_analysis_task(stock_code),
        create_sentiment_analysis_task(stock_code),
        create_fundamental_analysis_task(stock_code)
    ]


# 测试
if __name__ == "__main__":
    import json
    
    tasks = get_all_tasks("AAPL")
    
    print(f"生成 {len(tasks)} 个 subagent 任务:\n")
    
    for i, task in enumerate(tasks, 1):
        print(f"{i}. {task['label']}")
        print(f"   任务长度：{len(task['task'])} 字符")
        print()
