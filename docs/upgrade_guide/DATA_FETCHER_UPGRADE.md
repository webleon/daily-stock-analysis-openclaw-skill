# 数据获取模块升级指南

**最后更新**: 2026-03-25  
**适用版本**: v1.0+  
**状态**: ✅ 可用

---

## 📋 升级方式

### 方式 1：自动同步脚本（推荐）

```bash
cd /Users/webleon/.openclaw/workspace/skills/daily-stock-analysis-openclaw-skill

# 运行同步脚本
python scripts/sync_data_fetcher.py
```

**前提条件**:
- 原项目目录存在（默认位置：`../daily_stock_analysis`）
- 或设置环境变量：`ORIGINAL_PROJECT_PATH=/path/to/daily_stock_analysis`

**目录结构要求**:
```
parent/
├── daily-stock-analysis-openclaw-skill/  (当前项目)
│   └── scripts/
│       └── sync_data_fetcher.py
└── daily_stock_analysis/                 (原项目)
    └── data_provider/
```

---

### 方式 2：手动同步

#### 步骤 1：复制原项目代码

```bash
# 进入当前项目
cd /Users/webleon/.openclaw/workspace/skills/daily-stock-analysis-openclaw-skill

# 复制原项目代码
cp -r /path/to/daily_stock_analysis/data_provider/* src/core/data/
```

#### 步骤 2：调整导入路径

```bash
# 修复导入路径
cd src/core/data/

# 替换所有 src.data 为相对导入
find . -name "*.py" -exec sed -i '' 's/from src\.data\./from ./g' {} \;

# 替换 config 导入
find . -name "*.py" -exec sed -i '' 's/from src\.config/from ...config/g' {} \;
```

#### 步骤 3：创建 stock_mapping.py

如果原项目没有此文件，需要创建：

```python
"""
股票代码映射和名称验证
简化版本，仅包含基本功能
"""

STOCK_NAME_MAP = {
    '000001': '上证指数',
    '399001': '深证成指',
    '399006': '创业板指',
    '000016': '上证 50',
    '000300': '沪深 300',
    '000688': '科创 50',
}


def is_meaningful_stock_name(name: str) -> bool:
    if not name:
        return False
    meaningless = ['未知', 'N/A', 'None', '']
    return name not in meaningless
```

#### 步骤 4：更新 __init__.py

```python
"""
数据获取模块
支持 AkShare、Tushare、Yahoo Finance 等多数据源
带故障切换、重试、速率限制等高级功能
"""

from .base import (
    BaseFetcher,
    DataFetcherManager,
    DataFetchError,
    RateLimitError,
)

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
```

#### 步骤 5：清理缓存

```bash
# 清理 Python 缓存
find . -type d -name "__pycache__" -exec rm -rf {} \;

# 清理临时文件
rm -f .!*.py
```

#### 步骤 6：测试验证

```bash
cd /Users/webleon/.openclaw/workspace/skills/daily-stock-analysis-openclaw-skill

python3 -c "
from src.core.data import DataFetcherManager
manager = DataFetcherManager()
print(f'✅ 数据源数量：{len(manager._fetchers)}')
for fetcher in manager._fetchers:
    print(f'   - {fetcher.name} (Priority {fetcher.priority})')
"
```

---

## 📊 升级检查清单

### 升级前

- [ ] 备份当前代码
- [ ] 确认原项目路径
- [ ] 记录当前数据源数量

### 升级中

- [ ] 复制所有 Python 文件
- [ ] 修复导入路径
- [ ] 创建 stock_mapping.py
- [ ] 更新 __init__.py
- [ ] 清理缓存

### 升级后

- [ ] 测试导入
- [ ] 测试数据源初始化
- [ ] 测试数据获取功能
- [ ] 更新版本文档

---

## 🔧 常见问题

### Q1: 找不到原项目目录

**解决方案**:

```bash
# 设置环境变量
export ORIGINAL_PROJECT_PATH=/path/to/daily_stock_analysis

# 或调整目录结构
ln -s /path/to/daily_stock_analysis ../daily_stock_analysis
```

### Q2: 导入错误

**症状**: `ModuleNotFoundError: No module named 'src.core.data.stock_mapping'`

**解决方案**:

```bash
# 检查 stock_mapping.py 是否存在
ls src/core/data/stock_mapping.py

# 如果不存在，创建简化版本
cat > src/core/data/stock_mapping.py << 'EOF'
STOCK_NAME_MAP = {
    '000001': '上证指数',
    '399001': '深证成指',
}

def is_meaningful_stock_name(name: str) -> bool:
    return bool(name and name not in ['未知', 'N/A', 'None', ''])
EOF
```

### Q3: 类名大小写错误

**症状**: `NameError: name 'YfinanceFetcher' is not defined`

**解决方案**:

```bash
# 修复类名大小写
sed -i '' 's/YfinanceFetcher/YFinanceFetcher/g' src/core/data/base.py
```

### Q4: 循环依赖

**症状**: `ImportError: cannot import name 'BaseFetcher'`

**解决方案**:

```bash
# 简化 __init__.py，只导出必要内容
cat > src/core/data/__init__.py << 'EOF'
from .base import DataFetcherManager

__all__ = ['DataFetcherManager']
EOF
```

---

## 📈 升级频率建议

| 升级类型 | 频率 | 说明 |
|----------|------|------|
| **Bug 修复** | 按需 | 发现严重 Bug 时立即升级 |
| **小版本** | 每月 | 包含新功能和小改进 |
| **大版本** | 每季度 | 包含重大架构变更 |

---

## 📝 升级日志

### v1.0 (2026-03-25)

- ✅ 初始迁移
- ✅ 8 个数据源
- ✅ 自动故障切换
- ✅ 指数退避重试
- ✅ 速率限制
- ✅ 线程安全缓存

---

## 🎯 下一步行动

升级完成后：

1. 测试数据获取功能
2. 更新版本文档
3. 提交代码到 Git

---

**文档位置**: `docs/upgrade_guide/DATA_FETCHER_UPGRADE.md`  
**维护者**: 研究分析师 🔬  
**最后审查**: 2026-03-25
