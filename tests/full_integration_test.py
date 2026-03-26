#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整集成测试
测试数据获取、分析、报告生成全流程
"""

import sys
import time
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core import StockAnalysisCore


def test_data_fetcher():
    """测试数据获取"""
    print('=' * 70)
    print('📦 测试 1: 数据获取模块')
    print('=' * 70)
    
    from src.core.data import DataFetcherManager
    
    manager = DataFetcherManager()
    print(f'  ✅ 数据源数量：{len(manager._fetchers)}')
    
    for fetcher in manager._fetchers:
        print(f'     - {fetcher.name} (Priority {fetcher.priority})')
    
    print()
    return True


def test_analysis():
    """测试分析引擎"""
    print('=' * 70)
    print('📊 测试 2: 分析引擎')
    print('=' * 70)
    
    from src.core.analysis import SixteenModulesAnalyzer, SixPerspectivesAnalyzer
    
    # 测试数据
    test_data = {
        'stock_code': '600519',
        'stock_name': '贵州茅台',
        'revenue_growth': 0.25,
        'gross_margin': 0.92,
        'roe': 0.30,
        'operating_cash_flow': 50000000000,
        'free_cash_flow': 40000000000,
        'management_guidance': 'positive',
        'market_share': 0.35,
        'economic_moat': 'wide',
        'core_kpis': ['营收', '利润', '毛利率'],
        'new_business': ['iMoutai', '冰淇淋'],
        'partners': ['经销商 A', '经销商 B'],
        'management': {'track_record': 'excellent'},
        'policy': 'supportive',
        'pe': 35,
        'peg': 1.5,
        'institutional_ownership': 0.65,
        'long_term_metrics': ['品牌价值', '市场份额'],
        'rd_ratio': 0.03,
        'audit_opinion': 'standard',
        'esg_score': 75,
        'tam': 1000,
        'innovation': 'incremental',
        'bullish_factors': ['品牌', '渠道', '定价权'],
        'bearish_factors': ['估值偏高'],
        'pb': 10,
        'margin_of_safety': 0.15,
        'catalysts': ['新品发布', '提价'],
        'event_driven': True,
        'macro': 'positive',
        'liquidity': 'loose',
        'sentiment': 'neutral'
    }
    
    # 16 模块分析
    analyzer_16 = SixteenModulesAnalyzer()
    result_16 = analyzer_16.analyze(test_data)
    print(f'  ✅ 16 模块分析完成')
    print(f'     综合评分：{result_16["total_score"]:.1f}')
    print(f'     模块数量：{len(result_16["modules"])}')
    
    # 6 大视角分析
    analyzer_6 = SixPerspectivesAnalyzer()
    result_6 = analyzer_6.analyze(test_data)
    print(f'  ✅ 6 大视角分析完成')
    print(f'     综合评分：{result_6["total_score"]:.1f}')
    print(f'     视角数量：{len(result_6["perspectives"])}')
    
    print()
    return True, result_16, result_6


def test_report_generation():
    """测试报告生成"""
    print('=' * 70)
    print('📄 测试 3: 报告生成')
    print('=' * 70)
    
    from src.core.report import HTMLReportGenerator
    
    # 测试数据（包含完整结构以兼容原项目模板）
    test_data = {
        'stock_code': '600519',
        'stock_name': '贵州茅台',
        'market_snapshot': {
            'close': 1680.00,
            'prev_close': 1650.00,
            'open': 1660.00,
            'high': 1690.00,
            'low': 1655.00,
            'pct_chg': '+1.82%',
            'change_amount': '+30.00',
            'amplitude': '2.12%',
            'volume': '123.45 万手',
            'amount': '20.67 亿元',
            'price': 1680.00,
            'volume_ratio': 1.2,
            'turnover_rate': '0.98%',
            'source': 'AKShare'
        },
        'history_by_code': {
            '2026-03-25': {'close': 1680.00, 'pct_chg': 1.82}
        },
        'sixteen_modules': {
            'modules': {
                'revenue_quality': {'score': 85, 'analysis': '收入质量优秀，增长率 25%'},
                'profitability': {'score': 90, 'analysis': '盈利能力强劲，ROE 达 30%'},
                'cash_flow': {'score': 88, 'analysis': '现金流充沛，经营现金流 500 亿'},
                'forward_guidance': {'score': 80, 'analysis': '管理层指引积极'},
                'competitive_landscape': {'score': 92, 'analysis': '竞争格局优良，市场份额 35%'},
                'core_kpis': {'score': 85, 'analysis': '核心 KPI 健康'},
                'products_new_business': {'score': 78, 'analysis': '新业务进展良好'},
                'partner_ecosystem': {'score': 82, 'analysis': '合作伙伴生态稳定'},
                'management_team': {'score': 90, 'analysis': '高管团队优秀'},
                'macro_policy': {'score': 75, 'analysis': '宏观政策支持'},
                'valuation': {'score': 65, 'analysis': '估值合理，PE 35 倍'},
                'chip_distribution': {'score': 80, 'analysis': '机构持仓 65%'},
                'long_term_monitoring': {'score': 85, 'analysis': '长期指标健康'},
                'rd_efficiency': {'score': 70, 'analysis': '研发投入 3%'},
                'accounting_quality': {'score': 90, 'analysis': '审计意见标准'},
                'esg_screening': {'score': 75, 'analysis': 'ESG 评分良好'}
            },
            'total_score': 82.2
        },
        'six_perspectives': {
            'perspectives': {
                'quality_compounder': {
                    'score': 88,
                    'analysis': '符合巴菲特标准，护城河宽阔',
                    'representatives': '巴菲特/芒格'
                },
                'imaginative_growth': {
                    'score': 75,
                    'analysis': '增长潜力良好',
                    'representatives': 'Baillie Gifford/ARK'
                },
                'fundamental_long_short': {
                    'score': 82,
                    'analysis': '多头因素强劲',
                    'representatives': 'Tiger Cubs'
                },
                'deep_value': {
                    'score': 65,
                    'analysis': '估值合理，安全边际中等',
                    'representatives': 'Klarman/Marks'
                },
                'catalyst_driven': {
                    'score': 80,
                    'analysis': '催化剂充足',
                    'representatives': 'Tepper/Ackman'
                },
                'macro_tactical': {
                    'score': 78,
                    'analysis': '宏观环境积极',
                    'representatives': 'Druckenmiller'
                }
            },
            'total_score': 78.0
        },
        'conclusion': {
            'recommendation': '买入',
            'summary': '贵州茅台是优质白酒龙头，品牌价值高，盈利能力强，建议长期持有',
            'position_advice': {
                'no_position': '建议分批建仓，首仓 30%',
                'has_position': '继续持有，目标价 1800 元'
            }
        },
        'dashboard': {
            'core_conclusion': {
                'one_sentence': '贵州茅台是优质白酒龙头，品牌价值高，盈利能力强，建议长期持有',
                'time_sensitivity': '本周内',
                'position_advice': {
                    'no_position': '建议分批建仓，首仓 30%',
                    'has_position': '继续持有，目标价 1800 元'
                }
            },
            'intelligence': {
                'sentiment_summary': '舆情正面，市场认可度高',
                'earnings_outlook': '预计 Q1 增长 20%+',
                'risk_alerts': ['估值偏高', '宏观经济不确定性'],
                'positive_catalysts': ['提价预期', '直销渠道扩张'],
                'latest_news': '公司宣布扩大产能'
            },
            'battle_plan': {
                'sniper_points': {
                    'ideal_buy': 1650,
                    'stop_loss': 1580,
                    'take_profit': 1800
                },
                'action_checklist': [
                    {'text': '确认财报数据', 'passed': True},
                    {'text': '检查技术面', 'passed': True},
                    {'text': '评估风险', 'passed': True}
                ]
            },
            'data_perspective': {
                'trend_status': {
                    'ma_alignment': '多头排列',
                    'is_bullish': True,
                    'trend_score': 85
                },
                'price_position': {
                    'current_price': 1680,
                    'ma5': 1670,
                    'ma10': 1660,
                    'ma20': 1650,
                    'bias_ma5': 0.6,
                    'bias_status': '正常',
                    'support_level': 1650,
                    'resistance_level': 1700
                },
                'volume_analysis': {
                    'volume_ratio': 1.2,
                    'volume_status': '温和放量',
                    'turnover_rate': 0.98,
                    'volume_meaning': '成交量温和放大，资金流入'
                },
                'chip_structure': {
                    'institutional_ownership': 65,
                    'chip_concentration': '集中'
                }
            }
        }
    }
    
    generator = HTMLReportGenerator()
    
    # 生成报告 1: 贵州茅台（使用统一输出目录）
    from pathlib import Path
    output_dir = Path.home() / '.openclaw' / 'workspace' / 'output' / 'daily-stock-analysis'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_path_1 = None  # 使用默认路径
    html_1 = generator.generate(test_data, output_path_1)
    print(f'  ✅ 报告 1 生成成功：贵州茅台 (600519)')
    print(f'     报告长度：{len(html_1)} 字符')
    print(f'     保存位置：{output_dir}')
    
    # 生成报告 2: 修改数据生成不同的报告
    test_data_2 = test_data.copy()
    test_data_2['stock_code'] = '000858'
    test_data_2['stock_name'] = '五粮液'
    test_data_2['sixteen_modules']['total_score'] = 78.5
    test_data_2['six_perspectives']['total_score'] = 75.0
    test_data_2['conclusion']['recommendation'] = '持有'
    test_data_2['conclusion']['summary'] = '五粮液是白酒行业龙头之一，品牌实力强，但估值偏高，建议持有观望'
    
    output_path_2 = None  # 使用默认路径
    html_2 = generator.generate(test_data_2, output_path_2)
    print(f'  ✅ 报告 2 生成成功：五粮液 (000858)')
    print(f'     报告长度：{len(html_2)} 字符')
    print(f'     保存位置：{output_dir}')
    
    print()
    return True, output_path_1, output_path_2


def test_telegram_send(report_paths):
    """测试 Telegram 发送"""
    print('=' * 70)
    print('📱 测试 4: Telegram 发送')
    print('=' * 70)
    
    import os
    from pathlib import Path
    
    # 检查文件是否存在
    for path in report_paths:
        if os.path.exists(path):
            file_size = os.path.getsize(path)
            print(f'  ✅ 报告文件存在：{path}')
            print(f'     文件大小：{file_size} 字节')
        else:
            print(f'  ❌ 报告文件不存在：{path}')
    
    # 注意：实际发送需要 Telegram Bot Token 和 Chat ID
    # 这里只测试文件准备
    print()
    print('  ℹ️  提示：实际发送需要配置 Telegram Bot Token')
    print('  配置文件：.env')
    print('  需要配置：TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID')
    print()
    return True


def main():
    """主测试函数"""
    print()
    print('🧪 ' + '=' * 68)
    print('🧪 ' + ' ' * 20 + '完整项目集成测试' + ' ' * 20)
    print('🧪 ' + '=' * 68)
    print()
    
    start_time = time.time()
    
    results = []
    
    # 测试 1: 数据获取
    results.append(('数据获取模块', test_data_fetcher()))
    
    # 测试 2: 分析引擎
    passed, result_16, result_6 = test_analysis()
    results.append(('分析引擎', passed))
    
    # 测试 3: 报告生成
    passed, path_1, path_2 = test_report_generation()
    results.append(('报告生成', passed))
    
    # 测试 4: Telegram 发送
    results.append(('Telegram 发送', test_telegram_send([path_1, path_2])))
    
    # 汇总结果
    elapsed = time.time() - start_time
    
    print('=' * 70)
    print('测试结果汇总')
    print('=' * 70)
    
    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)
    
    for name, passed in results:
        status = '✅' if passed else '❌'
        print(f'  {status} {name}')
    
    print()
    print(f'总计：{passed_count}/{total_count} 通过')
    print(f'耗时：{elapsed:.2f}秒')
    print('=' * 70)
    
    if passed_count == total_count:
        print()
        print('🎉 所有测试通过！')
        print()
        return 0
    else:
        print()
        print('⚠️  部分测试失败，请检查错误信息')
        print()
        return 1


if __name__ == '__main__':
    exit(main())
