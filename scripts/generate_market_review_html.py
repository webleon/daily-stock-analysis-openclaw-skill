#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===================================
大盘复盘 HTML 报告生成器
===================================

基于原项目的 market_review.py 实现，生成 HTML 格式的复盘报告
"""

import logging
import sys
from datetime import datetime
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.market_review import run_market_review
from src.notification import NotificationService
from src.analyzer import GeminiAnalyzer
from src.search_service import SearchService

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def convert_markdown_to_html(markdown_text: str) -> str:
    """
    将 Markdown 格式的复盘报告转换为 HTML
    
    Args:
        markdown_text: Markdown 格式的复盘报告
        
    Returns:
        HTML 格式的复盘报告
    """
    import re
    
    html = markdown_text
    
    # 处理标题
    html = re.sub(r'^## (.*$)', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^### (.*$)', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    
    # 处理表格
    # 简单的表格转换（假设表格格式标准）
    table_pattern = r'\|(.+?)\|\n\|([-:\s\|]+)\|\n((?:\|.+\|\n)+)'
    def replace_table(match):
        headers = match.group(1).strip().split('|')
        rows = match.group(3).strip().split('\n')
        
        html_table = '<table>\n<thead>\n<tr>'
        for h in headers:
            html_table += f'<th>{h.strip()}</th>'
        html_table += '</tr>\n</thead>\n<tbody>\n'
        
        for row in rows:
            cells = row.strip().split('|')
            html_table += '<tr>'
            for cell in cells:
                html_table += f'<td>{cell.strip()}</td>'
            html_table += '</tr>\n'
        
        html_table += '</tbody>\n</table>'
        return html_table
    
    html = re.sub(table_pattern, replace_table, html, flags=re.MULTILINE)
    
    # 处理引用块
    html = re.sub(r'^> (.*$)', r'<blockquote>\1</blockquote>', html, flags=re.MULTILINE)
    
    # 处理列表
    html = re.sub(r'^- (.*$)', r'<li>\1</li>', html, flags=re.MULTILINE)
    html = re.sub(r'^\d+\. (.*$)', r'<li>\1</li>', html, flags=re.MULTILINE)
    
    # 处理粗体和斜体
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)
    
    # 处理换行
    html = html.replace('\n\n', '</p><p>')
    html = html.replace('\n', '<br>')
    
    return html


def generate_html_report(markdown_report: str, date_str: str) -> str:
    """
    生成完整的 HTML 报告
    
    Args:
        markdown_report: Markdown 格式的复盘报告
        date_str: 日期字符串
        
    Returns:
        完整的 HTML 文档
    """
    html_content = convert_markdown_to_html(markdown_report)
    
    html_doc = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>A 股大盘复盘 - {date_str}</title>
  <style>
    :root {{
      --bg: #0a0a0f;
      --surface: #15151f;
      --surface-light: #1e1e2d;
      --accent: #10b981;
      --danger: #ef4444;
      --warning: #f59e0b;
      --text-primary: #ffffff;
      --text-secondary: #a0a0b0;
      --border: #2d2d3a;
    }}
    
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    
    body {{
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
      background: var(--bg);
      color: var(--text-primary);
      line-height: 1.8;
      padding: 2rem;
    }}
    
    .container {{ max-width: 900px; margin: 0 auto; }}
    
    header {{
      text-align: center;
      padding: 3rem 0;
      border-bottom: 3px solid var(--accent);
      margin-bottom: 3rem;
    }}
    
    h1 {{
      font-size: 2.5rem;
      font-weight: 700;
      margin-bottom: 1rem;
      color: var(--accent);
    }}
    
    .subtitle {{ font-size: 1.2rem; color: var(--text-secondary); }}
    
    .section {{
      background: var(--surface);
      border-radius: 12px;
      padding: 2rem;
      margin-bottom: 2rem;
      border-left: 4px solid var(--accent);
    }}
    
    h2 {{
      font-size: 1.8rem;
      margin: 1.5rem 0 1rem;
      color: var(--accent);
      border-bottom: 1px solid var(--border);
      padding-bottom: 0.5rem;
    }}
    
    h3 {{
      font-size: 1.4rem;
      margin: 1.5rem 0 1rem;
      color: var(--text-primary);
    }}
    
    p {{ margin: 1rem 0; }}
    
    ul, ol {{ margin: 1rem 0; padding-left: 2rem; }}
    li {{ margin: 0.5rem 0; }}
    
    blockquote {{
      background: var(--surface-light);
      padding: 1.5rem;
      border-radius: 8px;
      margin: 1.5rem 0;
      border-left: 4px solid var(--accent);
    }}
    
    table {{
      width: 100%;
      border-collapse: collapse;
      margin: 1.5rem 0;
      background: var(--surface-light);
      border-radius: 8px;
      overflow: hidden;
    }}
    
    th, td {{
      padding: 1rem;
      text-align: left;
      border-bottom: 1px solid var(--border);
    }}
    
    th {{
      background: rgba(16, 185, 129, 0.1);
      color: var(--accent);
      font-weight: 600;
    }}
    
    tr:last-child td {{ border-bottom: none; }}
    
    .highlight {{
      background: var(--surface-light);
      padding: 1.5rem;
      border-radius: 8px;
      margin: 1.5rem 0;
      border-left: 4px solid var(--accent);
    }}
    
    .footer {{
      text-align: center;
      padding: 2rem 0;
      color: var(--text-secondary);
      border-top: 1px solid var(--border);
      margin-top: 3rem;
    }}
    
    /* 表格中的 emoji 对齐 */
    td {{ white-space: nowrap; }}
    
    /* 列表样式 */
    ul li::before {{
      content: "•";
      color: var(--accent);
      font-weight: bold;
      display: inline-block;
      width: 1em;
      margin-left: -1em;
    }}
  </style>
</head>
<body>
  <div class="container">
    <header>
      <h1>🎯 A 股大盘复盘</h1>
      <p class="subtitle">{date_str}</p>
    </header>

    <div class="content">
      {html_content}
    </div>

    <footer class="footer">
      <p>生成时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
      <p>数据来源：AkShare, 新闻搜索</p>
      <p style="margin-top: 1rem; font-size: 0.9rem;">⚠️ 免责声明：本报告仅供参考，不构成投资建议。股市有风险，投资需谨慎。</p>
    </footer>
  </div>
</body>
</html>
'''
    
    return html_doc


def main():
    """主函数"""
    print('=' * 60)
    print('📊 A 股大盘复盘 HTML 报告生成器')
    print('=' * 60)
    print()
    
    date_str = datetime.now().strftime('%Y-%m-%d')
    print(f'📅 生成日期：{date_str}')
    print()
    
    # 创建服务
    print('🔧 初始化服务...')
    notifier = NotificationService()
    search_service = SearchService()
    analyzer = GeminiAnalyzer()
    
    # 执行大盘复盘
    print('📈 执行大盘复盘分析...')
    review_report = run_market_review(
        notifier=notifier,
        analyzer=analyzer,
        search_service=search_service,
        send_notification=False,  # 不发送通知，只生成报告
        merge_notification=False,
        override_region='cn'
    )
    
    if not review_report:
        print('❌ 复盘报告生成失败')
        return
    
    print(f'✅ 复盘报告生成成功，{len(review_report)} 字符')
    print()
    
    # 保存 Markdown 报告
    output_dir = Path(__file__).parent.parent / 'output'
    output_dir.mkdir(exist_ok=True)
    
    date_code = datetime.now().strftime('%Y%m%d')
    md_filename = output_dir / f'market-review-{date_code}.md'
    
    with open(md_filename, 'w', encoding='utf-8') as f:
        f.write(review_report)
    
    print(f'✅ Markdown 报告已保存：{md_filename}')
    print()
    
    # 生成 HTML 报告
    print('📄 生成 HTML 报告...')
    html_content = generate_html_report(review_report, date_str)
    
    html_filename = output_dir / f'market-review-{date_code}.html'
    
    with open(html_filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f'✅ HTML 报告已保存：{html_filename}')
    print(f'📁 文件路径：{html_filename.absolute()}')
    print()
    
    # 打开 HTML 文件
    print('🌐 打开 HTML 报告...')
    import subprocess
    subprocess.run(['open', str(html_filename.absolute())])
    
    print()
    print('=' * 60)
    print('✅ 报告生成完成！')
    print('=' * 60)


if __name__ == '__main__':
    main()
