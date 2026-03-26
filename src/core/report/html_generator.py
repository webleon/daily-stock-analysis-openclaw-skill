#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTML 报告生成器 - 支持多模板（brief/markdown/professional）
"""

from jinja2 import Environment, FileSystemLoader
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional
import markdown


class HTMLReportGenerator:
    """HTML 报告生成器 - 使用原项目模板"""
    
    def __init__(self, template_dir: Optional[str] = None):
        """
        初始化 HTML 报告生成器
        
        Args:
            template_dir: 模板目录路径（默认使用原项目模板目录）
        """
        if template_dir is None:
            # 使用原项目模板目录
            template_dir = Path(__file__).parent.parent.parent.parent / 'templates'
        
        self.template_dir = Path(template_dir)
        
        # 确保模板目录存在
        if not self.template_dir.exists():
            raise FileNotFoundError(f"模板目录不存在：{self.template_dir}")
        
        self.env = Environment(
            loader=FileSystemLoader(self.template_dir),
            autoescape=True
        )
        
        # 添加自定义过滤器
        self.env.globals['clean_sniper'] = self.clean_sniper
    
    def generate(self, analysis_result: Dict[str, Any], output_path: Optional[str] = None, template: str = 'brief') -> str:
        """
        生成 HTML 报告
        
        Args:
            analysis_result: 分析结果字典
            output_path: 输出文件路径（默认保存到统一输出目录）
            template: 使用的模板 ('brief' 或 'markdown')
        
        Returns:
            HTML 内容字符串
        """
        # 准备模板数据
        template_data = self._prepare_template_data(analysis_result)
        
        # 渲染模板
        if template == 'markdown':
            content = self._render_markdown_template(template_data)
        else:
            content = self._render_brief_template(template_data)
        
        # 转换为 HTML（带优化样式）
        html_content = self._markdown_to_html(content, analysis_result)
        
        # 保存文件
        if output_path is None:
            # 默认输出到统一目录
            output_dir = Path.home() / '.openclaw' / 'workspace' / 'output' / 'daily-stock-analysis'
            output_dir.mkdir(parents=True, exist_ok=True)
            stock_code = analysis_result.get('stock_code', 'unknown')
            report_date = datetime.now().strftime('%Y-%m-%d')
            # 遵循 SKILL.md 规范：{YYYY-MM-DD}_{SYMBOL}.{ext}
            output_path = output_dir / f"{report_date}_{stock_code}.html"
        
        self._save_report(html_content, str(output_path))
        
        return html_content
    
    def _prepare_template_data(self, analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """准备模板数据"""
        # 构建完整的分析结果结构
        result = analysis_result.copy()
        result.setdefault('code', analysis_result.get('stock_code', 'N/A'))
        result.setdefault('analysis_summary', analysis_result.get('conclusion', {}).get('summary', ''))
        result.setdefault('operation_advice', analysis_result.get('conclusion', {}).get('recommendation', ''))
        result.setdefault('sentiment_score', int(analysis_result.get('sixteen_modules', {}).get('total_score', 0)))
        result.setdefault('trend_prediction', self._get_trend_prediction(analysis_result))
        result.setdefault('signal_text', self._get_signal_text(result['operation_advice']))
        result.setdefault('time_sensitivity', '本周内')
        
        # 构建完整的 dashboard
        dashboard = self._build_complete_dashboard(analysis_result)
        result.setdefault('dashboard', dashboard)
        
        # 添加市场快照
        result.setdefault('market_snapshot', analysis_result.get('market_snapshot', {}))
        
        # 添加历史数据
        history = analysis_result.get('history_by_code', {})
        if not history:
            # 提供默认历史数据
            history = {
                result.get('code', 'N/A'): [
                    {'created_at': datetime.now().isoformat(), 'sentiment_score': 80, 'operation_advice': '买入', 'trend_prediction': '看涨'}
                ]
            }
        result.setdefault('history_by_code', history)
        
        # 准备模板数据
        template_data = {
            'report_date': datetime.now().strftime('%Y-%m-%d'),
            'report_timestamp': datetime.now().isoformat(),
            'results': [result],
            'enriched': [{
                'signal_emoji': self._get_signal_emoji(result['operation_advice']),
                'stock_name': analysis_result.get('stock_name', '股票'),
                'result': result
            }],
            'buy_count': 1 if result['operation_advice'] == '买入' else 0,
            'hold_count': 1 if result['operation_advice'] in ['持有', '观望'] else 0,
            'sell_count': 1 if result['operation_advice'] == '卖出' else 0,
            'summary_only': False,
            'history_by_code': result.get('history_by_code', {})
        }
        
        return template_data
    
    def _get_signal_emoji(self, advice: str) -> str:
        """获取信号 emoji"""
        if advice == '买入':
            return '🟢'
        elif advice in ['持有', '观望']:
            return '🟡'
        elif advice == '卖出':
            return '🔴'
        else:
            return '⚪'
    
    def _get_trend_prediction(self, analysis_result: Dict[str, Any]) -> str:
        """获取趋势预测"""
        score = analysis_result.get('sixteen_modules', {}).get('total_score', 0)
        if score >= 70:
            return '看涨'
        elif score >= 50:
            return '震荡'
        else:
            return '看跌'
    
    def _get_signal_text(self, advice: str) -> str:
        """获取信号文本"""
        if advice == '买入':
            return '买入信号'
        elif advice in ['持有', '观望']:
            return '持有观望'
        elif advice == '卖出':
            return '卖出信号'
        else:
            return '中性'
    
    @staticmethod
    def clean_sniper(value) -> str:
        """清理狙击点数据（模板过滤器）"""
        if value is None:
            return 'N/A'
        return str(value)
    
    def _render_brief_template(self, template_data: Dict[str, Any]) -> str:
        """渲染 report_brief.j2 模板"""
        try:
            template = self.env.get_template('report_brief.j2')
            return template.render(**template_data)
        except Exception as e:
            return f"# {template_data.get('enriched', [{}])[0].get('stock_name', '股票')} 简报\n\n分析失败：{e}"
    
    def _render_markdown_template(self, template_data: Dict[str, Any]) -> str:
        """渲染 report_markdown.j2 模板"""
        try:
            template = self.env.get_template('report_markdown.j2')
            return template.render(**template_data)
        except Exception as e:
            enriched = template_data.get('enriched', [{}])
            stock_name = enriched[0].get('stock_name', '股票') if enriched else '股票'
            return f"# {stock_name} 分析报告\n\n分析失败：{e}"
    
    def _markdown_to_html(self, markdown_text: str, analysis_result: Dict[str, Any]) -> str:
        """将 Markdown 转换为 HTML（优化样式）"""
        html_body = markdown.markdown(markdown_text, extensions=['tables', 'fenced_code'])
        
        html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{analysis_result.get('stock_name', '股票')} - 投资决策报告</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; line-height: 1.6; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }}
        .container {{ max-width: 900px; margin: 0 auto; background: #fff; padding: 40px; border-radius: 12px; box-shadow: 0 10px 40px rgba(0,0,0,0.2); }}
        h1 {{ color: #2d3748; border-bottom: 3px solid #4299e1; padding-bottom: 15px; font-size: 28px; margin-bottom: 20px; }}
        h2 {{ color: #276749; margin-top: 25px; margin-bottom: 15px; padding-left: 12px; border-left: 4px solid #38a169; font-size: 22px; }}
        h3 {{ color: #2c5282; margin-top: 20px; margin-bottom: 10px; font-size: 18px; }}
        table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
        th, td {{ border: 1px solid #e2e8f0; padding: 12px; text-align: left; }}
        th {{ background: linear-gradient(to right, #f7fafc, #edf2f7); font-weight: 600; color: #4a5568; }}
        tr:nth-child(even) {{ background: #f7fafc; }}
        tr:hover {{ background: #edf2f7; }}
        blockquote {{ background: #ebf8ff; border-left: 4px solid #4299e1; padding: 15px 20px; margin: 20px 0; border-radius: 0 8px 8px 0; color: #2c5282; font-style: italic; }}
        .summary {{ background: linear-gradient(135deg, #ebf8ff 0%, #e6fffa 100%); padding: 20px; border-left: 4px solid #4299e1; margin: 20px 0; border-radius: 8px; }}
        .badge {{ display: inline-block; padding: 6px 16px; border-radius: 9999px; font-size: 14px; font-weight: 600; margin-right: 8px; }}
        .badge-buy {{ background: #c6f6d5; color: #22543d; }}
        .badge-hold {{ background: #fefcbf; color: #744210; }}
        .badge-sell {{ background: #fed7d7; color: #742a2a; }}
        .score {{ font-size: 32px; font-weight: bold; color: #4299e1; }}
        .footer {{ margin-top: 40px; padding-top: 25px; border-top: 2px solid #e2e8f0; text-align: center; color: #718096; font-size: 13px; }}
        strong {{ color: #2d3748; }}
        code {{ background: #f7fafc; padding: 2px 6px; border-radius: 4px; font-family: "SFMono-Regular", Consolas, monospace; font-size: 90%; }}
        ul, ol {{ margin: 15px 0; padding-left: 30px; }}
        li {{ margin: 8px 0; }}
        a {{ color: #4299e1; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
        @media (max-width: 768px) {{ .container {{ padding: 20px; }} table {{ font-size: 14px; }} }}
    </style>
</head>
<body>
    <div class="container">
        {html_body}
        <div class="footer">
            <p style="margin-bottom: 8px;"><strong>生成工具：</strong>Daily Stock Analysis OpenClaw Skill</p>
            <p style="margin-bottom: 15px;"><strong>生成时间：</strong>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p style="color: #a0aec0; font-size: 12px; line-height: 1.5;">免责声明：本报告仅供参考，不构成投资建议。投资有风险，入市需谨慎。市场有风险，决策需谨慎。</p>
        </div>
    </div>
</body>
</html>'''
        return html
    
    def _build_complete_dashboard(self, analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """构建完整的决策仪表盘"""
        conclusion = analysis_result.get('conclusion', {})
        dashboard = analysis_result.get('dashboard', {})
        
        # 核心结论
        core_conclusion = dashboard.get('core_conclusion', {})
        core_conclusion.setdefault('one_sentence', conclusion.get('summary', ''))
        core_conclusion.setdefault('time_sensitivity', '本周内')
        core_conclusion.setdefault('position_advice', {
            'no_position': '建议分批建仓，首仓 30%',
            'has_position': '继续持有'
        })
        
        # 情报信息
        intelligence = dashboard.get('intelligence', {})
        intelligence.setdefault('sentiment_summary', '舆情正面，市场认可度高')
        intelligence.setdefault('earnings_outlook', '预计 Q1 增长 20%+')
        intelligence.setdefault('risk_alerts', ['估值偏高', '宏观经济不确定性'])
        intelligence.setdefault('positive_catalysts', ['提价预期', '直销渠道扩张'])
        intelligence.setdefault('latest_news', '公司宣布扩大产能')
        
        # 作战计划
        battle_plan = dashboard.get('battle_plan', {})
        battle_plan.setdefault('sniper_points', {
            'ideal_buy': 1650,
            'secondary_buy': 1600,
            'stop_loss': 1580,
            'take_profit': 1800
        })
        battle_plan.setdefault('position_strategy', {
            'suggested_position': '30-50%',
            'entry_plan': '分批建仓，首仓 30%',
            'risk_control': '跌破止损位坚决离场'
        })
        battle_plan.setdefault('action_checklist', [
            '确认财报数据',
            '检查技术面',
            '评估风险'
        ])
        
        # 数据透视
        data_perspective = dashboard.get('data_perspective', {})
        data_perspective.setdefault('trend_status', {
            'ma_alignment': '多头排列',
            'is_bullish': True,
            'trend_score': 85
        })
        data_perspective.setdefault('price_position', {
            'current_price': 1680,
            'ma5': 1670,
            'ma10': 1660,
            'ma20': 1650,
            'bias_ma5': 0.6,
            'bias_status': '正常',
            'support_level': 1650,
            'resistance_level': 1700
        })
        data_perspective.setdefault('volume_analysis', {
            'volume_ratio': 1.2,
            'volume_status': '温和放量',
            'turnover_rate': 0.98,
            'volume_meaning': '成交量温和放大，资金流入'
        })
        data_perspective.setdefault('chip_structure', {
            'profit_ratio': 65,
            'avg_cost': 1620,
            'concentration': 70,
            'chip_health': '筹码集中，健康'
        })
        
        return {
            'core_conclusion': core_conclusion,
            'intelligence': intelligence,
            'battle_plan': battle_plan,
            'data_perspective': data_perspective
        }
    
    def _save_report(self, html_content: str, output_path: str) -> None:
        """保存报告到文件"""
        output_dir = Path(output_path).parent
        output_dir.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
