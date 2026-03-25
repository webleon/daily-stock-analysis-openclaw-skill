#!/usr/bin/env python3
"""
数据获取模块同步脚本
从原项目同步最新代码到当前项目

使用方法:
    python scripts/sync_data_fetcher.py

功能:
1. 从原项目复制最新的 data_provider 代码
2. 自动调整导入路径
3. 保留本地自定义模块
4. 清理临时文件和缓存
"""

import os
import shutil
import subprocess
from pathlib import Path


def get_project_root():
    """获取项目根目录"""
    return Path(__file__).parent.parent


def get_original_project_path():
    """获取原项目路径（假设在同一父目录下）"""
    # 假设目录结构：
    # parent/
    #   daily-stock-analysis-openclaw-skill/  (当前项目)
    #   daily_stock_analysis/                 (原项目)
    root = get_project_root()
    original = root.parent / "daily_stock_analysis"
    
    if original.exists():
        return original
    
    # 尝试其他可能的位置
    alternatives = [
        root.parent / "daily-stock-analysis",
        root / "daily_stock_analysis",
        Path.home() / "daily_stock_analysis",
    ]
    
    for alt in alternatives:
        if alt.exists():
            return alt
    
    print("❌ 未找到原项目目录")
    print("请设置 ORIGINAL_PROJECT_PATH 环境变量或调整目录结构")
    return None


def sync_data_provider():
    """同步 data_provider 模块"""
    root = get_project_root()
    original = get_original_project_path()
    
    if not original:
        return False
    
    src = original / "data_provider"
    dst = root / "src" / "core" / "data"
    
    if not src.exists():
        print(f"❌ 原项目数据源目录不存在：{src}")
        return False
    
    print(f"📥 从 {src} 同步到 {dst}")
    
    # 创建目标目录
    dst.mkdir(parents=True, exist_ok=True)
    
    # 复制所有 Python 文件
    copied_files = []
    for file in src.glob("*.py"):
        if file.name.startswith("__"):
            continue
        
        dst_file = dst / file.name
        shutil.copy2(file, dst_file)
        copied_files.append(file.name)
        print(f"  ✅ {file.name}")
    
    print(f"✅ 复制完成：{len(copied_files)} 个文件")
    
    # 调整导入路径
    fix_imports(dst)
    
    # 创建 stock_mapping.py（如果不存在）
    create_stock_mapping(dst)
    
    # 更新 __init__.py
    update_init_py(dst)
    
    # 清理缓存
    cleanup_cache(dst)
    
    return True


def fix_imports(dst: Path):
    """修复导入路径"""
    print("🔧 修复导入路径...")
    
    for file in dst.glob("*.py"):
        if file.name == "__init__.py":
            continue
        
        content = file.read_text(encoding='utf-8')
        
        # 替换导入路径
        content = content.replace("from src.data.", "from .")
        content = content.replace("from src.config", "from ...config")
        
        # 写回文件
        file.write_text(content, encoding='utf-8')
    
    print("  ✅ 导入路径修复完成")


def create_stock_mapping(dst: Path):
    """创建 stock_mapping.py（简化版本）"""
    stock_mapping = dst / "stock_mapping.py"
    
    if stock_mapping.exists():
        print("  ℹ️  stock_mapping.py 已存在，跳过")
        return
    
    content = '''"""
股票代码映射和名称验证
简化版本，仅包含基本功能
"""

# A 股指数代码映射
STOCK_NAME_MAP = {
    '000001': '上证指数',
    '399001': '深证成指',
    '399006': '创业板指',
    '000016': '上证 50',
    '000300': '沪深 300',
    '000688': '科创 50',
}


def is_meaningful_stock_name(name: str) -> bool:
    """
    检查股票名称是否有意义
    
    Args:
        name: 股票名称
    
    Returns:
        bool: 是否有意义
    """
    if not name:
        return False
    
    # 排除无意义的名称
    meaningless = ['未知', 'N/A', 'None', '']
    return name not in meaningless
'''
    
    stock_mapping.write_text(content, encoding='utf-8')
    print("  ✅ stock_mapping.py 创建完成")


def update_init_py(dst: Path):
    """更新 __init__.py"""
    content = '''"""
数据获取模块
支持 AkShare、Tushare、Yahoo Finance 等多数据源
带故障切换、重试、速率限制等高级功能
"""

# 基础类
from .base import (
    BaseFetcher,
    DataFetcherManager,
    DataFetchError,
    RateLimitError,
)

# 具体数据源
from .akshare_fetcher import AkshareFetcher
from .tushare_fetcher import TushareFetcher
from .efinance_fetcher import EfinanceFetcher
from .yfinance_fetcher import YFinanceFetcher

__all__ = [
    'BaseFetcher',
    'DataFetcherManager',
    'DataFetchError',
    'RateLimitError',
    'AkshareFetcher',
    'TushareFetcher',
    'EfinanceFetcher',
    'YFinanceFetcher',
]
'''
    
    init_py = dst / "__init__.py"
    init_py.write_text(content, encoding='utf-8')
    print("  ✅ __init__.py 更新完成")


def cleanup_cache(dst: Path):
    """清理缓存"""
    print("🧹 清理缓存...")
    
    cache_dir = dst / "__pycache__"
    if cache_dir.exists():
        shutil.rmtree(cache_dir)
        print("  ✅ __pycache__ 清理完成")
    
    # 清理临时文件
    for file in dst.glob(".*!*.py"):
        file.unlink()
        print(f"  ✅ 清理临时文件：{file.name}")


def test_import():
    """测试导入"""
    print("🧪 测试导入...")
    
    try:
        import sys
        sys.path.insert(0, str(get_project_root()))
        
        from src.core.data import DataFetcherManager
        manager = DataFetcherManager()
        
        print(f"  ✅ DataFetcherManager 初始化成功")
        print(f"  ✅ 数据源数量：{len(manager._fetchers)}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ 导入失败：{e}")
        return False


def main():
    """主函数"""
    print("=" * 60)
    print("数据获取模块同步脚本")
    print("=" * 60)
    print()
    
    # 同步代码
    if not sync_data_provider():
        print("\n❌ 同步失败")
        return 1
    
    print()
    
    # 测试导入
    if not test_import():
        print("\n⚠️  导入测试失败，请检查错误信息")
        return 1
    
    print()
    print("=" * 60)
    print("✅ 同步完成！")
    print("=" * 60)
    
    return 0


if __name__ == "__main__":
    exit(main())
