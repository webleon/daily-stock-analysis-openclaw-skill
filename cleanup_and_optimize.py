#!/usr/bin/env python3
"""
清理和优化项目结构脚本
"""

import os
import shutil
from pathlib import Path

BASE_DIR = Path(__file__).parent

def remove_dir(path):
    """删除目录"""
    if path.exists():
        shutil.rmtree(path)
        print(f"✅ 删除目录：{path}")
        return True
    return False

def remove_file(path):
    """删除文件"""
    if path.exists():
        path.unlink()
        print(f"✅ 删除文件：{path}")
        return True
    return False

def remove_pycache():
    """删除所有 __pycache__ 目录"""
    count = 0
    for pycache in BASE_DIR.rglob('__pycache__'):
        remove_dir(pycache)
        count += 1
    print(f"✅ 共删除 {count} 个 __pycache__ 目录")
    return count

def cleanup_old_files():
    """清理旧文件和不需要的文件"""
    removed = []
    
    # 根目录旧文件
    old_files = [
        'server.py',
        'webui.py',
        'webui_frontend.py',
        'md2img.py',
        'feishu_doc.py',
        '.DS_Store',
    ]
    
    for f in old_files:
        if remove_file(BASE_DIR / f):
            removed.append(f)
    
    # src 目录旧文件
    src_old_files = [
        'src/__init__.py',  # 空的
        'src/analyzer.py',  # 旧的分析器
        'src/auth.py',
        'src/config.py',  # 太大，可能重复
        'src/data_provider.py',  # 重复
        'src/enums.py',
        'src/logging_config.py',
        'src/market_analyzer.py',
        'src/market_analyzer_update.py',
        'src/multi_agent_orchestrator.py',  # 重复
        'src/notification.py',
        'src/report_language.py',
        'src/run_multi_agent.py',
        'src/scheduler.py',
        'src/stock_analyzer.py',
        'src/storage.py',
    ]
    
    for f in src_old_files:
        if remove_file(BASE_DIR / f):
            removed.append(f)
    
    # 重复的目录
    duplicate_dirs = [
        'src/agent',  # 与 agents 重复
        'src/agents',  # 保留 core
        'src/data',  # 与 data_provider 重复
        'src/data_provider',
        'src/openclaw',
        'src/plugins',
        'src/repositories',
        'src/services',
        'src/utils',
    ]
    
    for d in duplicate_dirs:
        if remove_dir(BASE_DIR / d):
            removed.append(d)
    
    # 其他不需要的目录
    other_dirs = [
        'apps',
        'bot',
        'api',
        'strategies',
        'patch',
        'config',
        'reports',
    ]
    
    for d in other_dirs:
        if remove_dir(BASE_DIR / d):
            removed.append(d)
    
    print(f"✅ 共删除 {len(removed)} 个旧文件/目录")
    return removed

def optimize_structure():
    """优化目录结构"""
    
    # 确保核心目录存在
    core_dirs = [
        'core/data',
        'core/analysis',
        'core/report',
        'templates',
        'tests',
        'docs',
        'scripts',
    ]
    
    for d in core_dirs:
        (BASE_DIR / d).mkdir(parents=True, exist_ok=True)
    
    print("✅ 目录结构优化完成")

def main():
    print("=" * 60)
    print("🧹 开始清理和优化项目结构")
    print("=" * 60)
    print()
    
    # 1. 删除 __pycache__
    print("1️⃣ 清理 __pycache__")
    remove_pycache()
    print()
    
    # 2. 删除旧文件
    print("2️⃣ 删除旧文件")
    cleanup_old_files()
    print()
    
    # 3. 优化结构
    print("3️⃣ 优化目录结构")
    optimize_structure()
    print()
    
    print("=" * 60)
    print("✅ 清理和优化完成！")
    print("=" * 60)

if __name__ == '__main__':
    main()
