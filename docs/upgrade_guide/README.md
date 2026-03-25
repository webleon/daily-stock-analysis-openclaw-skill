# 升级指南

本目录包含所有升级相关文档。

---

## 📋 文档列表

### 1. [数据获取模块升级](DATA_FETCHER_UPGRADE.md)

**适用场景**: 从原项目同步最新的数据获取代码

**升级方式**:
- **自动同步**（推荐）: `python scripts/sync_data_fetcher.py`
- **手动同步**: 详见文档

**升级频率**: 
- Bug 修复：按需
- 小版本：每月
- 大版本：每季度

---

### 2. [升级检查清单](../../scripts/UPGRADE_CHECKLIST.md)

**使用方法**: 每次升级时填写此清单，确保不遗漏任何步骤

**包含内容**:
- 升级前准备
- 升级执行步骤
- 测试验证
- 升级后处理

---

## 🔄 标准升级流程

### 数据获取模块升级

```bash
# 1. 备份当前代码
git checkout -b upgrade-data-fetcher-YYYYMMDD

# 2. 运行同步脚本
python scripts/sync_data_fetcher.py

# 3. 测试验证
python3 -c "from src.core.data import DataFetcherManager; print('✅ 成功')"

# 4. 提交代码
git add src/core/data/
git commit -m "chore: sync data fetcher from original project"

# 5. 填写检查清单
# 打开 scripts/UPGRADE_CHECKLIST.md 并填写
```

---

## 📝 升级日志模板

```markdown
### v1.0 (YYYY-MM-DD)

- ✅ 同步原项目最新代码
- ✅ 修复导入路径
- ✅ 测试通过
- 📝 已知问题：________
```

---

## 🎯 相关文档

- [开发者指南](../developer_guide/README.md)
- [API 参考](../api_reference/README.md)
- [项目结构](../PROJECT_STRUCTURE.md)

---

**文档维护**: 研究分析师 🔬  
**最后更新**: 2026-03-25
