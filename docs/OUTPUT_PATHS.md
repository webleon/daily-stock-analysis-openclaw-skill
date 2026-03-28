# 📁 输出路径规范

**生效日期**: 2026-03-28  
**状态**: ✅ 强制执行

---

## 🎯 核心原则

**所有输出必须到**: `/Users/webleon/.openclaw/workspace/output/`

**禁止行为**:
- ❌ 在项目根目录创建备份文件
- ❌ 在源码目录创建数据文件
- ❌ 使用相对路径
- ❌ 硬编码路径字符串

---

## 📂 标准目录结构

```
/Users/webleon/.openclaw/workspace/
├── skills/daily-stock-analysis-openclaw-skill/  # 项目根目录
│   ├── core/                                    # 核心模块
│   ├── src/                                     # 业务代码
│   ├── data_provider/                           # 数据源
│   ├── tests/                                   # 测试文件
│   └── templates/                               # 模板
│
└── output/                                      # ⭐ 统一输出目录
    ├── daily-stock-analysis/                    # 分析报告
    ├── backups/                                 # 备份文件
    ├── cache/                                   # 缓存数据
    ├── accuracy/                                # 准确率数据
    └── logs/                                    # 日志文件
```

---

## 🔧 使用方式

```python
# ✅ 正确：使用统一配置
from core.config import OUTPUT_ROOT, get_cache_db

cache_db = get_cache_db()  # → output/cache/analysis.db
report_path = OUTPUT_ROOT / "reports" / "test.html"

# ❌ 错误：硬编码路径
db_path = Path("cache.db")
backup_path = Path("backup.tar.gz")
```

---

## 📋 检查脚本

```bash
# 运行路径检查
./scripts/check_output_paths.sh

# 输出示例:
# ✅ 根目录干净
# ✅ 源码目录干净
# ✅ 备份文件位置正确
```

---

**违规处理**: 发现违规文件将自动移动到正确位置
