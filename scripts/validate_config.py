#!/usr/bin/env python3
"""
配置验证脚本
验证所有配置文件是否正确
"""

import yaml
import sys
from pathlib import Path


def validate_config(config_file):
    """验证单个配置文件"""
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        print(f"✅ {config_file} 验证通过")
        return True
    
    except Exception as e:
        print(f"❌ {config_file} 验证失败：{e}")
        return False


def main():
    """主函数"""
    config_dir = Path(__file__).parent.parent / 'config'
    
    if not config_dir.exists():
        print(f"❌ 配置目录不存在：{config_dir}")
        sys.exit(1)
    
    all_valid = True
    
    for config_file in config_dir.glob('*.yaml'):
        if not validate_config(config_file):
            all_valid = False
    
    if all_valid:
        print("\n✅ 所有配置文件验证通过")
        sys.exit(0)
    else:
        print("\n❌ 部分配置文件验证失败")
        sys.exit(1)


if __name__ == '__main__':
    main()
