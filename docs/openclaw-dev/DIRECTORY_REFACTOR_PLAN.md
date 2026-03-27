# daily-stock-analysis-openclaw-skill 目录结构优化规划报告

**生成日期:** 2026-03-27  
**项目位置:** `/Users/webleon/.openclaw/workspace/skills/daily-stock-analysis-openclaw-skill/`  
**分析范围:** 根目录 216 个文件，66 个目录，约 752KB

---

## 1. 当前文件分类清单

### 1.1 保留文件 (Keep)

#### 核心功能文件
| 类别 | 文件/目录 | 说明 |
|------|----------|------|
| 主入口 | `main.py` | 主程序入口 |
| 服务层 | `analyzer_service.py` | 分析服务核心 |
| 配置 | `.env` | 环境变量（已在.gitignore） |
| 配置 | `litellm_config.example.yaml` | LiteLLM 配置示例 |
| 配置 | `pyproject.toml` | Python 项目配置 |
| 配置 | `requirements.txt` | 依赖列表 |
| 配置 | `setup.cfg` | 安装配置 |
| 脚本 | `run.sh` | 运行脚本 |
| 源码 | `src/` | 主要源代码目录 |
| 数据源 | `data_provider/` | 数据提供器模块 |
| 插件 | `plugins/` | 插件系统 |
| 模板 | `templates/` | 报告模板 |
| 测试 | `tests/` | 单元测试和集成测试 |

#### 必要文档
| 文件 | 说明 | 建议位置 |
|------|------|----------|
| `README.md` | 项目主文档 | 根目录 |
| `SKILL.md` | OpenClaw 技能定义 | 根目录 |
| `LICENSE` | 许可证 | 根目录 |
| `INSTALL.md` | 安装指南 | → docs/user_guide/ |
| `AGENTS.md` | Agent 配置 | → docs/developer_guide/ |
| `CLAUDE.md` | Claude 配置 | → docs/developer_guide/ |

#### 必要脚本
| 文件 | 说明 |
|------|------|
| `scripts/build-*.sh` | 构建脚本 |
| `scripts/ci_gate.sh` | CI 检查 |
| `scripts/validate_config.py` | 配置验证 |
| `scripts/sync_data_fetcher.py` | 数据同步 |

### 1.2 清理文件 (Clean)

#### 立即删除 - 缓存文件
| 目录/文件 | 数量 | 风险等级 |
|----------|------|----------|
| `__pycache__/` | ~50 个目录 | 🟢 低 |
| `.pytest_cache/` | 1 个目录 | 🟢 低 |
| `src/__pycache__/` | 14 个子目录 | 🟢 低 |
| `data_provider/__pycache__/` | 1 个子目录 | 🟢 低 |
| `patch/__pycache__/` | 1 个子目录 | 🟢 低 |
| `src/utils/__pycache__/` | 1 个子目录 | 🟢 低 |
| `tests/__pycache__/` | 66 个子目录 | 🟢 低 |
| `*.pyc` | ~189 个 | 🟢 低 |
| `.DS_Store` | ~10 个 | 🟢 低 |

#### 立即删除 - 临时文件
| 文件 | 说明 | 风险等级 |
|------|------|----------|
| `test_*.py` (根目录) | 临时测试脚本 | 🟢 低 |
| `verify_*.py` | 验证脚本 | 🟢 低 |

#### 清理 - 重复/过时文档
| 文件 | 说明 | 建议操作 |
|------|------|----------|
| `review.md` | 通用评审 | → 归档或合并 |
| `CLEANUP_REPORT.md` | 清理报告 | → docs/archive/ |
| `PROJECT_STRUCTURE.md` | 结构说明 | → docs/archive/ |

### 1.3 归档文件 (Archive)

#### 历史分析报告
| 文件 | 说明 |
|------|------|
| `ABCD_COMPARISON.md` | 方案对比分析 |
| `HYBRID_VS_SCHEME_B_COMPARISON.md` | 混合方案对比 |
| `HYBRID_SCENARIO_SUPPORT.md` | 混合场景支持 |
| `DATA_FETCHER_ANALYSIS.md` | 数据获取器分析 |
| `UPSTREAM_UPDATES_ANALYSIS.md` | 上游更新分析 |
| `V3.4_TO_V3.10_UPDATES.md` | 版本更新记录 |
| `MISSING_FEATURES_REPORT.md` | 缺失功能报告 |
| `REQUIREMENTS_REVIEW.md` | 需求评审 |
| `TEST_REPORT.md` | 测试报告 |

#### 计划文档
| 文件 | 说明 |
|------|------|
| `FINAL_IMPLEMENTATION_PLAN.md` | 最终实现计划 |
| `SCHEME_B_IMPLEMENTATION_PLAN.md` | 方案 B 实现计划 |
| `FINAL_CLEANUP_PLAN.md` | 最终清理计划 |
| `HOT_RELOAD_EXPLAINED.md` | 热重载说明 |

#### 建议归档位置
所有归档文件应移至：`docs/archive/2026-Q1-development/`

---

## 2. 优化后的目录结构设计

### 2.1 设计原则

1. **单一职责**: 每个目录有明确的用途
2. **层次清晰**: 不超过 4 层嵌套
3. **易于导航**: 按功能而非技术分层
4. **可扩展**: 预留扩展空间
5. **符合 Python 惯例**: 遵循 PEP 8 和项目结构最佳实践

### 2.2 优化后结构

```
daily-stock-analysis-openclaw-skill/
├── 📁 .git/                          # Git 仓库
├── 📁 .github/                       # GitHub 配置（新建）
│   └── workflows/                    # CI/CD 工作流
├── 📁 docs/                          # 文档
│   ├── 📁 user_guide/                # 用户指南
│   │   ├── README.md                 # 用户入门
│   │   ├── install.md                # 安装指南
│   │   └── bot-commands.md           # 机器人命令
│   ├── 📁 developer_guide/           # 开发指南
│   │   ├── README.md                 # 开发入门
│   │   ├── architecture.md           # 架构说明
│   │   ├── api-reference.md          # API 参考
│   │   └── contributing.md           # 贡献指南
│   ├── 📁 openclaw/                  # OpenClaw 集成文档
│   │   ├── SKILL.md                  # 技能定义（可保留根目录）
│   │   ├── integration-guide.md      # 集成指南
│   │   └── multi-agent-guide.md      # 多 Agent 指南
│   ├── 📁 deployment/                # 部署文档
│   │   ├── docker.md                 # Docker 部署
│   │   ├── zeabur.md                 # Zeabur 部署
│   │   └── desktop.md                # 桌面版打包
│   ├── 📁 archive/                   # 归档文档
│   │   └── 2026-Q1-development/      # 2026 Q1 开发文档
│   │       ├── analysis-reports/     # 分析报告
│   │       └── plans/                # 历史计划
│   ├── CHANGELOG.md                  # 变更日志
│   ├── FAQ.md                        # 常见问题
│   └── README_EN.md                  # 英文文档
├── 📁 src/                           # 源代码
│   ├── 📁 agent/                     # Agent 相关
│   │   ├── executor.py
│   │   ├── models.py
│   │   ├── pipeline.py
│   │   └── registry.py
│   ├── 📁 agents/                    # 多 Agent 系统
│   │   ├── technical_agent.py
│   │   ├── sentiment_agent.py
│   │   └── fundamental_agent.py
│   ├── 📁 core/                      # 核心业务逻辑
│   │   ├── analyzer.py
│   │   ├── market_analyzer.py
│   │   └── stock_analyzer.py
│   ├── 📁 data/                      # 数据处理
│   │   ├── fetcher.py
│   │   ├── cache.py
│   │   └── validator.py
│   ├── 📁 notification_sender/       # 通知发送
│   │   └── sender.py
│   ├── 📁 openclaw/                  # OpenClaw 集成
│   │   └── integration.py
│   ├── 📁 plugins/                   # 插件系统
│   │   └── loader.py
│   ├── 📁 repositories/              # 数据仓库
│   │   └── base.py
│   ├── 📁 schemas/                   # 数据模型
│   │   ├── analysis.py
│   │   └── config.py
│   ├── 📁 services/                  # 服务层
│   │   ├── backtest.py
│   │   ├── search.py
│   │   └── storage.py
│   ├── 📁 utils/                     # 工具函数
│   │   ├── formatters.py
│   │   ├── logging_config.py
│   │   └── helpers.py
│   ├── auth.py                       # 认证模块
│   ├── config.py                     # 配置管理
│   ├── enums.py                      # 枚举定义
│   ├── multi_agent_orchestrator.py   # 多 Agent 协调器
│   └── scheduler.py                  # 调度器
├── 📁 data_provider/                 # 数据提供器（保持独立）
│   ├── base.py                       # 基类
│   ├── akshare_fetcher.py
│   ├── tushare_fetcher.py
│   ├── yfinance_fetcher.py
│   ├── efinance_fetcher.py
│   ├── baostock_fetcher.py
│   ├── pytdx_fetcher.py
│   ├── longbridge_fetcher.py
│   ├── tickflow_fetcher.py
│   ├── eastmoney_fetcher.py
│   ├── eastmoney_spider.py
│   ├── fundamental_adapter.py
│   ├── hybrid_fetcher.py
│   ├── realtime_types.py
│   ├── us_index_mapping.py
│   └── akshare_test.py
├── 📁 tests/                         # 测试
│   ├── 📁 unit/                      # 单元测试
│   ├── 📁 integration/               # 集成测试
│   ├── 📁 e2e/                       # 端到端测试
│   ├── 📁 fixtures/                  # 测试夹具
│   ├── 📁 data/                      # 测试数据
│   ├── 📁 openclaw/                  # OpenClaw 测试
│   ├── 📁 report/                    # 报告测试
│   ├── conftest.py                   # pytest 配置
│   └── litellm_stub.py               # LiteLLM 模拟
├── 📁 scripts/                       # 脚本工具
│   ├── 📁 build/                     # 构建脚本
│   │   ├── build-backend-macos.sh
│   │   ├── build-desktop-macos.sh
│   │   ├── build-all-macos.sh
│   │   ├── build-backend.ps1
│   │   ├── build-desktop.ps1
│   │   └── build-all.ps1
│   ├── 📁 ci/                        # CI 脚本
│   │   └── ci_gate.sh
│   ├── 📁 tools/                     # 工具脚本
│   │   ├── validate_config.py
│   │   ├── sync_data_fetcher.py
│   │   ├── check_ai_assets.py
│   │   ├── send_to_telegram.py
│   │   └── demo_multi_agent_prompt.py
│   └── 📁 generators/                # 生成器脚本
│       ├── generate_market_review_html.py
│       ├── generate_enhanced_review.py
│       └── generate_comparison_html.py
├── 📁 templates/                     # 模板文件
│   ├── 📁 reports/                   # 报告模板
│   ├── 📁 notifications/             # 通知模板
│   └── 📁 emails/                    # 邮件模板
├── 📁 output/                        # 输出目录（.gitignore）
│   ├── 📁 cache/                     # 缓存
│   ├── 📁 logs/                      # 日志
│   └── 📁 reports/                   # 生成的报告
├── 📁 plugins/                       # 插件目录
│   ├── 📁 custom_agents/             # 自定义 Agent
│   ├── 📁 custom_data_sources/       # 自定义数据源
│   ├── 📁 custom_modules/            # 自定义模块
│   ├── 📁 custom_notifications/      # 自定义通知
│   └── 📁 custom_templates/          # 自定义模板
├── 📁 sources/                       # 源代码归档（可选清理）
│   └── 📁 dsa_vi/                    # 原始项目来源
├── 📁 patch/                         # 补丁目录
│   └── (补丁文件)
├── .env                              # 环境变量（.gitignore）
├── .env.example                      # 环境变量示例（新建）
├── .gitignore                        # Git 忽略规则
├── .python-version                   # Python 版本（新建）
├── litellm_config.example.yaml       # LiteLLM 配置示例
├── pyproject.toml                    # Python 项目配置
├── requirements.txt                  # 依赖列表
├── requirements-dev.txt              # 开发依赖（新建）
├── setup.cfg                         # 安装配置
├── run.sh                            # 运行脚本
├── main.py                           # 主入口
├── analyzer_service.py               # 分析服务（→ src/services/）
├── market_review_cli.py              # 市场复盘 CLI（→ src/cli/）
├── cleanup_and_optimize.py           # 清理脚本（→ scripts/tools/）
└── subagent_tasks.py                 # Subagent 任务定义（→ src/agents/）
```

### 2.3 关键变更说明

| 变更类型 | 原位置 | 新位置 | 说明 |
|---------|--------|--------|------|
| 移动 | `analyzer_service.py` | `src/services/analyzer_service.py` | 服务层归位 |
| 移动 | `market_review_cli.py` | `src/cli/market_review.py` | CLI 工具归位 |
| 移动 | `subagent_tasks.py` | `src/agents/subagent_tasks.py` | Agent 任务归位 |
| 移动 | `cleanup_and_optimize.py` | `scripts/tools/cleanup.py` | 工具脚本归位 |
| 新建 | - | `.github/workflows/` | CI/CD 配置 |
| 新建 | - | `docs/archive/2026-Q1-development/` | 归档目录 |
| 新建 | - | `scripts/build/` | 构建脚本目录 |
| 新建 | - | `scripts/ci/` | CI 脚本目录 |
| 新建 | - | `scripts/tools/` | 工具脚本目录 |
| 新建 | - | `scripts/generators/` | 生成器脚本目录 |
| 新建 | - | `.env.example` | 环境变量示例 |
| 新建 | - | `.python-version` | Python 版本指定 |
| 新建 | - | `requirements-dev.txt` | 开发依赖 |

---

## 3. 清理操作清单（按风险等级）

### 3.1 低风险操作（可立即执行）

#### 缓存文件清理
```bash
# Python 缓存
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -type f -name "*.pyc" -delete 2>/dev/null

# pytest 缓存
rm -rf .pytest_cache/

# 系统文件
find . -name ".DS_Store" -delete 2>/dev/null
find . -name "Thumbs.db" -delete 2>/dev/null
```

**影响:** 无  
**可恢复:** 自动重新生成  
**预计释放:** ~50-100MB

#### 临时文件清理
```bash
# 根目录临时测试脚本
rm -f test_*.py 2>/dev/null
rm -f verify_*.py 2>/dev/null
```

**影响:** 无（已纳入 tests/ 的测试不受影响）  
**可恢复:** Git 恢复

### 3.2 中风险操作（需确认）

#### 文档归档
```bash
# 创建归档目录
mkdir -p docs/archive/2026-Q1-development/analysis-reports
mkdir -p docs/archive/2026-Q1-development/plans

# 移动分析报告
mv ABCD_COMPARISON.md docs/archive/2026-Q1-development/analysis-reports/
mv HYBRID_VS_SCHEME_B_COMPARISON.md docs/archive/2026-Q1-development/analysis-reports/
mv HYBRID_SCENARIO_SUPPORT.md docs/archive/2026-Q1-development/analysis-reports/
mv DATA_FETCHER_ANALYSIS.md docs/archive/2026-Q1-development/analysis-reports/
mv UPSTREAM_UPDATES_ANALYSIS.md docs/archive/2026-Q1-development/analysis-reports/
mv V3.4_TO_V3.10_UPDATES.md docs/archive/2026-Q1-development/analysis-reports/
mv MISSING_FEATURES_REPORT.md docs/archive/2026-Q1-development/analysis-reports/
mv REQUIREMENTS_REVIEW.md docs/archive/2026-Q1-development/analysis-reports/
mv TEST_REPORT.md docs/archive/2026-Q1-development/analysis-reports/
mv review.md docs/archive/2026-Q1-development/analysis-reports/

# 移动计划文档
mv FINAL_IMPLEMENTATION_PLAN.md docs/archive/2026-Q1-development/plans/
mv SCHEME_B_IMPLEMENTATION_PLAN.md docs/archive/2026-Q1-development/plans/
mv FINAL_CLEANUP_PLAN.md docs/archive/2026-Q1-development/plans/
mv HOT_RELOAD_EXPLAINED.md docs/archive/2026-Q1-development/plans/
mv CLEANUP_REPORT.md docs/archive/2026-Q1-development/plans/
mv PROJECT_STRUCTURE.md docs/archive/2026-Q1-development/plans/
```

**影响:** 文档访问路径变更  
**可恢复:** Git 恢复  
**建议:** 在 docs/archive/README.md 中添加索引

#### 代码文件重组
```bash
# 移动服务层文件
mv analyzer_service.py src/services/

# 移动 CLI 工具
mv market_review_cli.py src/cli/market_review.py

# 移动 Agent 任务定义
mv subagent_tasks.py src/agents/

# 移动清理脚本
mv cleanup_and_optimize.py scripts/tools/cleanup.py
```

**影响:** 导入路径需要更新  
**可恢复:** Git 恢复  
**注意:** 需要更新相关 import 语句

### 3.3 高风险操作（需谨慎）

#### sources/ 目录处理
```bash
# sources/ 包含原始项目文件，建议：
# 选项 A: 保留但添加 .gitignore
echo "sources/*" >> .gitignore
echo "!sources/README.md" >> .gitignore

# 选项 B: 归档后删除
mv sources/ docs/archive/original-source/
```

**影响:** 可能影响代码对比和参考  
**建议:** 选项 A（保留但忽略）

#### 根目录脚本清理
```bash
# 以下文件已迁移到 scripts/，可考虑删除或保留作为快捷方式
# 保留建议：run.sh（常用入口）
# 可删除：已迁移的脚本文件
```

**影响:** 可能破坏现有工作流程  
**建议:** 保留常用脚本，删除已迁移的脚本

---

## 4. 实施步骤

### 阶段 1: 准备工作（5 分钟）

```bash
# 1. 创建新分支
git checkout -b refactor/directory-structure

# 2. 确保当前状态干净
git status
git add -A
git commit -m "chore: snapshot before directory restructuring"

# 3. 创建回滚标签
git tag backup/pre-refactor-2026-03-27
```

### 阶段 2: 低风险清理（10 分钟）

```bash
# 1. 清理缓存
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
rm -rf .pytest_cache/
find . -name ".DS_Store" -delete 2>/dev/null

# 2. 清理临时文件
rm -f test_*.py verify_*.py 2>/dev/null

# 3. 提交清理
git add -A
git commit -m "chore: clean cache and temporary files"
```

### 阶段 3: 目录结构调整（30 分钟）

```bash
# 1. 创建新目录结构
mkdir -p docs/user_guide
mkdir -p docs/developer_guide
mkdir -p docs/openclaw
mkdir -p docs/deployment
mkdir -p docs/archive/2026-Q1-development/{analysis-reports,plans}
mkdir -p src/cli
mkdir -p scripts/{build,ci,tools,generators}
mkdir -p templates/{reports,notifications,emails}
mkdir -p .github/workflows

# 2. 移动文档
mv INSTALL.md docs/user_guide/
mv AGENTS.md docs/developer_guide/
mv CLAUDE.md docs/developer_guide/
mv CONTRIBUTING.md docs/developer_guide/

# 3. 移动归档文档（中风险操作）
mv ABCD_COMPARISON.md docs/archive/2026-Q1-development/analysis-reports/
mv HYBRID_VS_SCHEME_B_COMPARISON.md docs/archive/2026-Q1-development/analysis-reports/
mv HYBRID_SCENARIO_SUPPORT.md docs/archive/2026-Q1-development/analysis-reports/
mv DATA_FETCHER_ANALYSIS.md docs/archive/2026-Q1-development/analysis-reports/
mv UPSTREAM_UPDATES_ANALYSIS.md docs/archive/2026-Q1-development/analysis-reports/
mv V3.4_TO_V3.10_UPDATES.md docs/archive/2026-Q1-development/analysis-reports/
mv MISSING_FEATURES_REPORT.md docs/archive/2026-Q1-development/analysis-reports/
mv REQUIREMENTS_REVIEW.md docs/archive/2026-Q1-development/analysis-reports/
mv TEST_REPORT.md docs/archive/2026-Q1-development/analysis-reports/
mv review.md docs/archive/2026-Q1-development/analysis-reports/

mv FINAL_IMPLEMENTATION_PLAN.md docs/archive/2026-Q1-development/plans/
mv SCHEME_B_IMPLEMENTATION_PLAN.md docs/archive/2026-Q1-development/plans/
mv FINAL_CLEANUP_PLAN.md docs/archive/2026-Q1-development/plans/
mv HOT_RELOAD_EXPLAINED.md docs/archive/2026-Q1-development/plans/
mv CLEANUP_REPORT.md docs/archive/2026-Q1-development/plans/
mv PROJECT_STRUCTURE.md docs/archive/2026-Q1-development/plans/

# 4. 移动代码文件
mv analyzer_service.py src/services/
mv market_review_cli.py src/cli/market_review.py
mv subagent_tasks.py src/agents/
mv cleanup_and_optimize.py scripts/tools/cleanup.py

# 5. 重组 scripts 目录
mv scripts/build-*.sh scripts/build/ 2>/dev/null
mv scripts/build-*.ps1 scripts/build/ 2>/dev/null
mv scripts/ci_gate.sh scripts/ci/
mv scripts/validate_config.py scripts/tools/
mv scripts/sync_data_fetcher.py scripts/tools/
mv scripts/check_ai_assets.py scripts/tools/
mv scripts/send_to_telegram.py scripts/tools/
mv scripts/demo_multi_agent_prompt.py scripts/tools/
mv scripts/generate_*.py scripts/generators/

# 6. 提交结构变更
git add -A
git commit -m "refactor: restructure directory layout"
```

### 阶段 4: 更新导入和引用（20 分钟）

```bash
# 1. 更新 Python 导入
# 使用 sed 或 IDE 批量替换
# 示例：更新 analyzer_service 导入
grep -r "from analyzer_service" --include="*.py" . | cut -d: -f1 | sort -u
# 手动或使用脚本更新每个文件

# 2. 更新文档引用
grep -r "analyzer_service.py" docs/ --include="*.md"
# 更新文档中的路径引用

# 3. 提交更新
git add -A
git commit -m "refactor: update imports and references"
```

### 阶段 5: 创建新文件（10 分钟）

```bash
# 1. 创建环境变量示例
cp .env .env.example
# 编辑 .env.example，移除敏感信息

# 2. 创建 Python 版本文件
python --version | awk '{print $2}' > .python-version

# 3. 创建开发依赖
cat > requirements-dev.txt << 'EOF'
pytest>=7.0
pytest-cov>=4.0
pylint>=2.0
black>=23.0
mypy>=1.0
EOF

# 4. 创建归档索引
cat > docs/archive/README.md << 'EOF'
# 文档归档

本目录包含历史文档，按时间周期组织。

## 归档列表

- [2026-Q1-development](2026-Q1-development/) - 2026 年第一季度开发文档
  - [analysis-reports/](2026-Q1-development/analysis-reports/) - 分析报告
  - [plans/](2026-Q1-development/plans/) - 历史计划文档

## 访问指南

归档文档仅供参考，请以最新文档为准。
EOF

# 5. 提交新文件
git add -A
git commit -m "docs: add example files and archive index"
```

### 阶段 6: 验证和测试（15 分钟）

```bash
# 1. 运行测试确保功能正常
python -m pytest tests/ -v

# 2. 验证导入
python -c "from src.services.analyzer_service import analyze_stock"
python -c "from src.agents.subagent_tasks import create_technical_analysis_task"

# 3. 运行主程序
python main.py --help

# 4. 提交验证结果
git add -A
git commit -m "test: verify functionality after refactoring"
```

### 阶段 7: 最终清理和合并（5 分钟）

```bash
# 1. 运行代码格式化
black src/ scripts/ tests/
isort src/ scripts/ tests/

# 2. 最终提交
git add -A
git commit -m "style: format code after refactoring"

# 3. 推送到远程
git push origin refactor/directory-structure

# 4. 创建 Pull Request
# 在 GitHub/GitLab 上创建 PR，等待审查
```

---

## 5. 回滚方案

### 5.1 快速回滚（Git 标签）

```bash
# 如果重构过程中出现问题，立即回滚：
git checkout main
git branch -D refactor/directory-structure
git tag -d backup/pre-refactor-2026-03-27

# 从标签恢复
git checkout backup/pre-refactor-2026-03-27
git checkout -b recovery-branch
```

### 5.2 部分回滚

```bash
# 如果只有部分变更需要回滚：
git checkout backup/pre-refactor-2026-03-27 -- <file-or-directory>

# 示例：只回滚代码文件移动
git checkout backup/pre-refactor-2026-03-27 -- src/
git checkout backup/pre-refactor-2026-03-27 -- *.py
```

### 5.3 手动回滚步骤

```bash
# 1. 移回代码文件
mv src/services/analyzer_service.py .
mv src/cli/market_review.py .
mv src/agents/subagent_tasks.py .
mv scripts/tools/cleanup.py .

# 2. 移回文档
mv docs/archive/2026-Q1-development/analysis-reports/*.md .
mv docs/archive/2026-Q1-development/plans/*.md .

# 3. 清理新目录
rm -rf docs/archive/
rm -rf scripts/build/
rm -rf scripts/ci/
rm -rf scripts/tools/
rm -rf scripts/generators/

# 4. 恢复缓存（可选）
python -m pytest --cache-clear
```

### 5.4 回滚检查清单

- [ ] 所有代码文件回到原位置
- [ ] 所有文档回到原位置
- [ ] 导入语句已更新回原路径
- [ ] 测试通过
- [ ] 主程序可正常运行
- [ ] Git 状态干净

---

## 6. 风险评估总结

| 风险等级 | 操作类型 | 影响范围 | 可恢复性 | 建议 |
|---------|---------|---------|---------|------|
| 🟢 低 | 清理缓存 | 无 | 自动生成 | 立即执行 |
| 🟢 低 | 清理临时文件 | 无 | Git 恢复 | 立即执行 |
| 🟡 中 | 文档归档 | 文档访问路径 | Git 恢复 | 创建索引 |
| 🟡 中 | 代码文件移动 | 导入路径 | Git 恢复 + 更新导入 | 批量更新 |
| 🟠 高 | sources/ 处理 | 代码参考 | Git 恢复 | 保留但忽略 |
| 🟠 高 | 根目录脚本 | 工作流程 | Git 恢复 | 保留常用 |

---

## 7. 后续优化建议

### 7.1 短期（1-2 周）

1. **添加 CI/CD 配置**: 在 `.github/workflows/` 中添加自动化测试
2. **完善文档索引**: 为 docs/ 目录创建完整的导航结构
3. **更新 README**: 反映新的目录结构

### 7.2 中期（1 个月）

1. **代码模块化**: 进一步拆分大文件（如 config.py 97KB）
2. **类型注解**: 为所有函数添加类型提示
3. **测试覆盖**: 提高单元测试覆盖率至 80%+

### 7.3 长期（3 个月）

1. **API 文档**: 使用 Sphinx 生成 API 文档
2. **性能优化**: 分析并优化瓶颈
3. **插件系统**: 完善插件架构，支持第三方扩展

---

## 8. 总结

本次目录结构优化规划旨在：

1. **清理冗余**: 移除缓存和临时文件，释放空间
2. **归档历史**: 将开发文档移至归档目录，保持根目录简洁
3. **重组结构**: 按功能组织代码和脚本，提高可维护性
4. **降低风险**: 提供完整的回滚方案，确保可恢复

**预计总耗时:** 95 分钟  
**风险等级:** 中（有完整回滚方案）  
**建议执行:** 在独立分支中进行，验证后合并

---

*报告生成完成。请审阅后决定是否执行。*
