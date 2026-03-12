#!/usr/bin/env python3
"""
生成多股对比 HTML 报告
使用数据源适配层，支持动态切换数据源
"""

import sys
import os
from datetime import datetime
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.data_provider import data_provider

def generate_comparison_report(stock_codes: list, output_file: str):
    """生成对比报告"""
    
    # 获取股票数据
    stocks = {}
    for code in stock_codes:
        data = data_provider.get_stock_data(code)
        if data:
            stocks[code] = data
            print(f'✅ {data["名称"]}（{code}）: {data["最新价"]:.2f} CNY, PE={data["市盈率"]}')
        else:
            print(f'❌ {code} 数据获取失败')
    
    if not stocks:
        print('❌ 没有获取到任何股票数据')
        return
    
    # 生成 HTML（这里简化，实际应该调用完整的 HTML 生成函数）
    html_content = f'''<!DOCTYPE html>
<html>
<head>
    <title>股票对比报告 - {datetime.now().strftime("%Y-%m-%d")}</title>
</head>
<body>
    <h1>股票对比报告</h1>
    <p>生成时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
    
    <h2>数据说明</h2>
    <div style="background: #f0f0f0; padding: 1rem; border-left: 4px solid #10b981;">
        <p><strong>数据来源：</strong>配置的数据源（当前：{data_provider.primary_source}）</p>
        <p><strong>PE 数据：</strong>{'✅ 准确（Tushare）' if data_provider.primary_source == 'tushare' else '⚠️ 数据源暂时不可用，显示 N/A'}</p>
        <p><strong>切换数据源：</strong>设置环境变量 STOCK_DATA_SOURCE=tushare 并配置 TUSHARE_TOKEN</p>
    </div>
    
    <h2>股票数据</h2>
    <table border="1" cellpadding="8">
        <thead>
            <tr>
                <th>指标</th>
                {''.join([f'<th>{stocks[code]["名称"]}（{code}）</th>' for code in stocks])}
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>最新价</td>
                {''.join([f'<td>{stocks[code]["最新价"]:.2f} CNY</td>' for code in stocks])}
            </tr>
            <tr>
                <td>涨跌幅</td>
                {''.join([f'<td>{stocks[code]["涨跌幅"]:+.2f}%</td>' for code in stocks])}
            </tr>
            <tr>
                <td>市盈率</td>
                {''.join([f'<td>{stocks[code]["市盈率"]}</td>' for code in stocks])}
            </tr>
            <tr>
                <td>市净率</td>
                {''.join([f'<td>{stocks[code]["市净率"]:.2f}</td>' for code in stocks])}
            </tr>
        </tbody>
    </table>
</body>
</html>
'''
    
    # 保存文件
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f'\n✅ HTML 报告已生成：{output_file}')

if __name__ == '__main__':
    # 示例：生成 3 只股票的对比报告
    stock_codes = ['603039', '600588', '002230']
    output_file = 'output/comparison-report.html'
    
    generate_comparison_report(stock_codes, output_file)
