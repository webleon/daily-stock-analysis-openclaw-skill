# 未移植功能对比报告

**对比日期**: 2026-03-26  
**原项目**: sources/ (原 daily_stock_analysis)  
**当前项目**: src/ + core/ + data_provider/

---

## ⚠️ 严重问题：核心目录被误删

### 问题描述

清理脚本**错误删除了 core/ 目录下的所有核心文件**：

```
core/
├── analysis/      # ❌ 空目录 (原有 sixteen_modules.py, six_perspectives.py)
├── data/          # ❌ 空目录 (原有所有 fetcher 文件)
└── report/        # ❌ 空目录 (原有 html_generator.py)
```

### 原因分析

清理脚本中的以下操作删除了 core/ 目录：
```bash
✅ 删除目录：/Users/webleon/.openclaw/workspace/skills/daily-stock-analysis-openclaw-skill/src/core
```

---

## 📋 原项目核心功能

### sources/dsa_vi/ 目录结构

```
sources/dsa_vi/
├── app/                    # 主应用
│   ├── __init__.py
│   ├── main.py            # 应用入口
│   ├── api/               # API 接口
│   ├── models/            # 数据模型
│   ├── services/          # 业务服务
│   └── utils/             # 工具函数
├── core/                   # 核心模块
│   ├── analysis/          # 分析模块
│   ├── data/              # 数据获取
│   ├── report/            # 报告生成
│   └── utils/             # 核心工具
├── agents/                 # Agent 系统
├── skills/                 # 技能系统
└── tools/                  # 工具系统
```

---

## 🔍 功能对比

### 1. 核心分析模块

| 功能 | 原项目 | 当前项目 | 状态 |
|------|--------|----------|------|
| **16 模块分析** | ✅ sixteen_modules.py | ❌ 已删除 | ❌ 缺失 |
| **6 大视角** | ✅ six_perspectives.py | ❌ 已删除 | ❌ 缺失 |
| **分析管道** | ✅ pipeline.py | ❌ 已删除 | ❌ 缺失 |
| **回测引擎** | ✅ backtest_engine.py | ❌ 已删除 | ❌ 缺失 |
| **市场策略** | ✅ market_strategy.py | ❌ 已删除 | ❌ 缺失 |
| **市场概况** | ✅ market_profile.py | ❌ 已删除 | ❌ 缺失 |
| **交易日历** | ✅ trading_calendar.py | ❌ 已删除 | ❌ 缺失 |

### 2. 数据获取模块

| 功能 | 原项目 | 当前项目 | 状态 |
|------|--------|----------|------|
| **数据基类** | ✅ base.py (92KB) | ✅ data_provider/base.py | ✅ 保留 |
| **AKShare** | ✅ akshare_fetcher.py | ✅ data_provider/akshare_fetcher.py | ✅ 保留 |
| **Tushare** | ✅ tushare_fetcher.py | ✅ data_provider/tushare_fetcher.py | ✅ 保留 |
| **YFinance** | ✅ yfinance_fetcher.py | ✅ src/core/data/yfinance_fetcher.py | ✅ 保留 |
| **其他数据源** | ✅ 多个 fetcher | ✅ data_provider/ 中 | ✅ 保留 |

### 3. 报告生成模块

| 功能 | 原项目 | 当前项目 | 状态 |
|------|--------|----------|------|
| **HTML 生成器** | ✅ html_generator.py | ✅ src/core/report/html_generator.py | ✅ 保留 |
| **报告模板** | ✅ templates/*.j2 | ✅ templates/*.j2 | ✅ 保留 |
| **格式化** | ✅ formatters.py | ✅ src/formatters.py | ✅ 保留 |

### 4. Agent 和工具系统

| 功能 | 原项目 | 当前项目 | 状态 |
|------|--------|----------|------|
| **Agent 系统** | ✅ agents/ | ❌ 已删除 | ❌ 缺失 |
| **技能系统** | ✅ skills/ | ❌ 已删除 | ❌ 缺失 |
| **工具系统** | ✅ tools/ | ❌ 已删除 | ❌ 缺失 |
| **命令系统** | ✅ utils/commands/ | ❌ 已删除 | ❌ 缺失 |
| **平台集成** | ✅ utils/platforms/ | ❌ 已删除 | ❌ 缺失 |

### 5. 通知系统

| 功能 | 原项目 | 当前项目 | 状态 |
|------|--------|----------|------|
| **通知基类** | ✅ notification.py | ❌ 已删除 | ❌ 缺失 |
| **通知发送器** | ✅ notification_sender/ | ✅ notification_sender/ | ✅ 保留 |
| **搜索服务** | ✅ search_service.py | ✅ src/search_service.py | ✅ 保留 |

### 6. UI 和 API

| 功能 | 原项目 | 当前项目 | 状态 |
|------|--------|----------|------|
| **FastAPI 服务** | ✅ fastapi_server.py | ❌ 已删除 | ❌ 缺失 |
| **Web UI** | ✅ webui.py | ❌ 已删除 | ❌ 缺失 |
| **Server** | ✅ server.py | ❌ 已删除 | ❌ 缺失 |

---

## 📊 缺失功能统计

### 核心功能缺失

| 类别 | 缺失文件数 | 影响 |
|------|-----------|------|
| **分析模块** | 7 个文件 | 🔴 严重 |
| **Agent 系统** | 整个目录 | 🔴 严重 |
| **技能系统** | 整个目录 | 🔴 严重 |
| **工具系统** | 整个目录 | 🔴 严重 |
| **命令系统** | 整个目录 | 🟡 中等 |
| **平台集成** | 整个目录 | 🟡 中等 |
| **UI/API** | 3 个文件 | 🟢 轻微 |

### 保留功能

| 类别 | 保留情况 |
|------|----------|
| **数据获取** | ✅ 100% 保留 (data_provider/) |
| **报告生成** | ✅ 100% 保留 (templates/, html_generator.py) |
| **通知发送** | ✅ 100% 保留 (notification_sender/) |
| **搜索服务** | ✅ 100% 保留 (search_service.py) |
| **格式化** | ✅ 100% 保留 (formatters.py) |

---

## 🔧 恢复建议

### 高优先级（必须恢复）

1. **核心分析模块**
   ```bash
   # 从 sources/ 复制回 core/
   cp -r sources/dsa_vi/core/analysis/ core/
   cp -r sources/dsa_vi/core/data/ core/
   cp -r sources/dsa_vi/core/report/ core/
   cp sources/dsa_vi/core/pipeline.py core/
   cp sources/dsa_vi/core/backtest_engine.py core/
   cp sources/dsa_vi/core/market_strategy.py core/
   cp sources/dsa_vi/core/market_profile.py core/
   cp sources/dsa_vi/core/trading_calendar.py core/
   ```

2. **Agent 和技能系统**
   ```bash
   # 这些是 OpenClaw Skill 的核心
   cp -r sources/dsa_vi/agents/ src/
   cp -r sources/dsa_vi/skills/ src/
   cp -r sources/dsa_vi/tools/ src/
   ```

### 中优先级（建议恢复）

3. **命令和平台系统**
   ```bash
   cp -r sources/dsa_vi/core/utils/commands/ src/core/utils/
   cp -r sources/dsa_vi/core/utils/platforms/ src/core/utils/
   ```

### 低优先级（可选恢复）

4. **UI 和 API** (如果不使用 Web UI，可不恢复)
   - fastapi_server.py
   - webui.py
   - server.py

---

## 📝 当前项目状态

### 保留的核心文件

```
src/
├── core/
│   ├── data/              # ✅ 数据获取 (保留)
│   └── report/            # ✅ 报告生成 (保留)
├── data_provider/         # ✅ 数据提供器 (保留)
├── notification_sender/   # ✅ 通知发送器 (保留)
├── schemas/               # ✅ 数据模式 (保留)
├── formatters.py          # ✅ 格式化 (保留)
└── search_service.py      # ✅ 搜索服务 (保留)
```

### 缺失的核心文件

```
❌ core/analysis/          # 16 模块分析、6 大视角
❌ core/pipeline.py        # 分析管道
❌ core/backtest_engine.py # 回测引擎
❌ core/market_strategy.py # 市场策略
❌ core/market_profile.py  # 市场概况
❌ core/trading_calendar.py# 交易日历
❌ agents/                 # Agent 系统
❌ skills/                 # 技能系统
❌ tools/                  # 工具系统
```

---

## ⚠️ 影响评估

### 当前可用功能

- ✅ 数据获取（所有数据源）
- ✅ 报告生成（HTML/Markdown/微信）
- ✅ 通知发送（所有平台）
- ✅ 搜索服务
- ✅ 格式化

### 当前不可用功能

- ❌ 16 模块技术分析
- ❌ 6 大投资视角分析
- ❌ 分析管道执行
- ❌ 回测功能
- ❌ 市场策略
- ❌ Agent 系统
- ❌ 技能系统
- ❌ 工具系统

---

## 🎯 紧急程度

| 功能 | 紧急程度 | 说明 |
|------|----------|------|
| **16 模块分析** | 🔴 紧急 | 核心分析功能 |
| **6 大视角** | 🔴 紧急 | 核心分析功能 |
| **分析管道** | 🔴 紧急 | 执行核心 |
| **Agent 系统** | 🟡 重要 | OpenClaw 集成 |
| **回测引擎** | 🟡 重要 | 回测功能 |
| **工具系统** | 🟢 可选 | 辅助功能 |

---

## 📋 恢复步骤

### 步骤 1: 恢复核心分析模块

```bash
cd /Users/webleon/.openclaw/workspace/skills/daily-stock-analysis-openclaw-skill

# 恢复分析模块
cp -r sources/dsa_vi/core/analysis/* core/analysis/
cp sources/dsa_vi/core/pipeline.py core/
cp sources/dsa_vi/core/backtest_engine.py core/
cp sources/dsa_vi/core/market_strategy.py core/
cp sources/dsa_vi/core/market_profile.py core/
cp sources/dsa_vi/core/trading_calendar.py core/
```

### 步骤 2: 恢复 Agent 和技能系统

```bash
# 恢复 Agent 系统
cp -r sources/dsa_vi/agents/ src/
cp -r sources/dsa_vi/skills/ src/
cp -r sources/dsa_vi/tools/ src/
```

### 步骤 3: 验证恢复

```bash
# 检查文件
ls -la core/analysis/
ls -la src/agents/
ls -la src/skills/

# 测试导入
python3 -c "from core.analysis import sixteen_modules; print('✅ 分析模块恢复')"
python3 -c "from src.agents import factory; print('✅ Agent 系统恢复')"
```

---

## 📊 恢复后状态

### 预期完整功能

- ✅ 16 模块技术分析
- ✅ 6 大投资视角
- ✅ 分析管道执行
- ✅ 数据获取（所有数据源）
- ✅ 报告生成（HTML/Markdown/微信）
- ✅ 通知发送（所有平台）
- ✅ Agent 系统
- ✅ 技能系统
- ✅ 工具系统
- ⚠️ 回测引擎（可选）
- ⚠️ Web UI（可选）

---

**报告生成时间**: 2026-03-26  
**紧急程度**: 🔴 高（核心分析功能缺失）
