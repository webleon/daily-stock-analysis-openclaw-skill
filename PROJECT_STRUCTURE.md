# 项目目录结构（优化版）

**版本**: 1.0  
**创建日期**: 2026-03-25  
**设计原则**: 根目录简洁、功能模块化、便于维护

---

## 📁 优化后的目录结构

```
daily-stock-analysis-openclaw-skill/
│
├── 📄 根目录文件（仅保留必需文件）
│   ├── README.md                    # 项目说明
│   ├── LICENSE                      # 许可证
│   ├── pyproject.toml               # Python 项目配置
│   ├── requirements.txt             # 依赖列表
│   └── .gitignore                   # Git 忽略规则
│
├── 📂 src/                          # 源代码（核心代码）
│   ├── openclaw/                    # OpenClaw 适配层
│   │   ├── __init__.py
│   │   ├── adapter.py               # API 适配器
│   │   ├── version_detector.py      # 版本检测
│   │   └── tool_registry.py         # tool 注册
│   │
│   ├── agents/                      # 多 Agent 编排引擎
│   │   ├── __init__.py
│   │   ├── base.py                  # Agent 基类
│   │   ├── analysis_agent.py        # 分析 Agent
│   │   ├── scheduler_agent.py       # 调度 Agent
│   │   ├── report_agent.py          # 报告 Agent
│   │   ├── registry.py              # 注册中心
│   │   └── isolation.py             # 进程隔离
│   │
│   ├── plugins/                     # 插件基类
│   │   ├── __init__.py
│   │   ├── base.py                  # 插件基类
│   │   ├── data_source.py           # 数据源插件
│   │   ├── template.py              # 模板插件
│   │   ├── module.py                # 模块插件
│   │   └── notification.py          # 通知插件
│   │
│   └── core/                        # 原项目核心库（只读）
│       ├── data/                    # 数据获取
│       ├── analysis/                # 分析引擎
│       ├── report/                  # 报告生成
│       └── utils/                   # 工具函数
│
├── 📂 config/                       # 配置文件
│   ├── agents.yaml                  # Agent 配置
│   ├── data_sources.yaml            # 数据源配置
│   ├── templates.yaml               # 模板配置
│   ├── modules.yaml                 # 模块配置
│   └── notifications.yaml           # 通知配置
│
├── 📂 plugins/                      # 自定义插件（用户扩展）
│   ├── custom_agents/               # 自定义 Agent
│   ├── custom_data_sources/         # 自定义数据源
│   ├── custom_templates/            # 自定义模板
│   ├── custom_modules/              # 自定义模块
│   └── custom_notifications/        # 自定义通知
│
├── 📂 tests/                        # 测试代码
│   ├── unit/                        # 单元测试
│   ├── integration/                 # 集成测试
│   ├── e2e/                         # E2E 测试
│   └── fixtures/                    # 测试数据
│
├── 📂 docs/                         # 文档
│   ├── README.md                    # 文档索引
│   ├── user_guide/                  # 用户指南
│   ├── developer_guide/             # 开发者指南
│   ├── api_reference/               # API 参考
│   └── upgrade_guide/               # 升级指南
│
├── 📂 scripts/                      # 工具脚本
│   ├── setup_env.sh                 # 环境搭建
│   ├── validate_config.py           # 配置验证
│   ├── generate_report.py           # 报告生成
│   └── upgrade_check.py             # 升级检查
│
├── 📂 output/                       # 输出目录
│   ├── reports/                     # 分析报告
│   ├── logs/                        # 日志文件
│   └── cache/                       # 缓存文件
│
└── 📂 tools/                        # 工具模块
    ├── cli.py                       # 命令行工具
    ├── config_loader.py             # 配置加载器
    └── logger.py                    # 日志工具
```

---

## 📊 根目录文件对比

### 优化前（约 15 个文件）

```
根目录/
├── README.md
├── LICENSE
├── pyproject.toml
├── requirements.txt
├── .gitignore
├── SKILL.md
├── AGENTS.md
├── INSTALL.md
├── USER_GUIDE.md
├── DEVELOPER_GUIDE.md
├── API_REFERENCE.md
├── UPGRADE_GUIDE.md
├── ABCD_COMPARISON.md
├── SCHEME_B_IMPLEMENTATION_PLAN.md
├── SCHEME_B_REVIEW_REPORT.md
├── HYBRID_VS_SCHEME_B_COMPARISON.md
├── HYBRID_SCENARIO_SUPPORT.md
└── HOT_RELOAD_EXPLAINED.md
```

### 优化后（仅 5 个文件）

```
根目录/
├── README.md                    # 项目说明
├── LICENSE                      # 许可证
├── pyproject.toml               # Python 项目配置
├── requirements.txt             # 依赖列表
└── .gitignore                   # Git 忽略规则
```

**减少**: 15 → 5 个文件（-67%）

---

## 📂 文件归类说明

### 移至 docs/

| 原位置 | 新位置 | 说明 |
|--------|--------|------|
| `INSTALL.md` | `docs/user_guide/install.md` | 安装指南 |
| `USER_GUIDE.md` | `docs/user_guide/README.md` | 用户指南 |
| `DEVELOPER_GUIDE.md` | `docs/developer_guide/README.md` | 开发者指南 |
| `API_REFERENCE.md` | `docs/api_reference/README.md` | API 参考 |
| `UPGRADE_GUIDE.md` | `docs/upgrade_guide/README.md` | 升级指南 |
| `ABCD_COMPARISON.md` | `docs/analysis/abcd_comparison.md` | 方案对比 |
| `SCHEME_B_IMPLEMENTATION_PLAN.md` | `docs/analysis/scheme_b_plan.md` | 方案 B 计划 |
| `SCHEME_B_REVIEW_REPORT.md` | `docs/analysis/scheme_b_review.md` | 方案 B 评审 |
| `HYBRID_VS_SCHEME_B_COMPARISON.md` | `docs/analysis/hybrid_vs_b.md` | 混合方案对比 |
| `HYBRID_SCENARIO_SUPPORT.md` | `docs/analysis/hybrid_support.md` | 支持能力分析 |
| `HOT_RELOAD_EXPLAINED.md` | `docs/technical/hot_reload.md` | 热加载技术 |
| `FINAL_IMPLEMENTATION_PLAN.md` | `docs/plans/implementation.md` | 实施方案 |
| `PROJECT_STRUCTURE.md` | `docs/plans/structure.md` | 目录结构 |

### 移至 config/

| 原位置 | 新位置 | 说明 |
|--------|--------|------|
| `config/agents.yaml` | `config/agents.yaml` | Agent 配置（保持不变） |
| `config/data_sources.yaml` | `config/data_sources.yaml` | 数据源配置 |
| `config/templates.yaml` | `config/templates.yaml` | 模板配置 |

### 移至 scripts/

| 原位置 | 新位置 | 说明 |
|--------|--------|------|
| `validate_config.py` | `scripts/validate_config.py` | 配置验证 |
| `generate_report.py` | `scripts/generate_report.py` | 报告生成 |

---

## 📄 根目录文件说明

### README.md

```markdown
# Daily Stock Analysis OpenClaw Skill

A 股、港股、美股智能分析系统，基于 OpenClaw 多 Agent 编排。

## 快速开始

```bash
# 安装依赖
pip install -r requirements.txt

# 运行分析
python -m scripts.generate_report AAPL
```

## 文档

- [安装指南](docs/user_guide/install.md)
- [用户指南](docs/user_guide/README.md)
- [开发者指南](docs/developer_guide/README.md)
- [API 参考](docs/api_reference/README.md)

## 功能特性

- ✅ 16 模块分析
- ✅ 6 大投资视角
- ✅ 多 Agent 编排
- ✅ 自定义扩展
```

### pyproject.toml

```toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "daily-stock-analysis-openclaw-skill"
version = "1.0.0"
description = "Daily Stock Analysis OpenClaw Skill"
readme = "README.md"
requires-python = ">=3.9"
dependencies = [
    "openclaw>=1.0.0",
    "akshare>=1.0.0",
    "tushare>=1.0.0",
    "yfinance>=0.2.0",
    "pyyaml>=6.0",
    "jinja2>=3.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-cov>=4.0",
    "pylint>=2.0",
    "black>=23.0",
]

[tool.setuptools.packages.find]
where = ["src"]
```

### .gitignore

```gitignore
# Python
__pycache__/
*.py[cod]
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# 虚拟环境
venv/
env/
ENV/

# IDE
.idea/
.vscode/
*.swp
*.swo
*~

# 测试
.pytest_cache/
.coverage
htmlcov/
.tox/

# 输出
output/
logs/
*.log

# 环境
.env
.env.*
*.env

# 临时文件
*.tmp
*.bak
*.orig
```

---

## 📂 docs/ 目录结构

```
docs/
├── README.md                    # 文档索引
│
├── user_guide/                  # 用户指南
│   ├── README.md
│   ├── install.md               # 安装指南
│   ├── quickstart.md            # 快速开始
│   ├── configuration.md         # 配置说明
│   └── faq.md                   # 常见问题
│
├── developer_guide/             # 开发者指南
│   ├── README.md
│   ├── architecture.md          # 架构设计
│   ├── development.md           # 开发流程
│   ├── testing.md               # 测试指南
│   └── contributing.md          # 贡献指南
│
├── api_reference/               # API 参考
│   ├── README.md
│   ├── openclaw_adapter.md      # OpenClaw 适配层
│   ├── agents.md                # Agent API
│   ├── plugins.md               # 插件 API
│   └── config.md                # 配置 API
│
├── upgrade_guide/               # 升级指南
│   ├── README.md
│   ├── origin_project.md        # 原项目升级
│   └── openclaw.md              # OpenClaw 升级
│
└── analysis/                    # 分析报告
    ├── abcd_comparison.md       # 四方案对比
    ├── scheme_b_plan.md         # 方案 B 计划
    ├── scheme_b_review.md       # 方案 B 评审
    ├── hybrid_vs_b.md           # 混合方案对比
    ├── hybrid_support.md        # 支持能力分析
    └── ...
```

---

## 📂 config/ 目录结构

```
config/
├── agents.yaml                  # Agent 配置
├── data_sources.yaml            # 数据源配置
├── templates.yaml               # 模板配置
├── modules.yaml                 # 模块配置
├── notifications.yaml           # 通知配置
└── openclaw.yaml                # OpenClaw 配置
```

### agents.yaml 示例

```yaml
agents:
  - name: analysis_agent
    module: agents.analysis_agent
    enabled: true
    priority: 10
    config:
      model: qwen3.5-plus
      max_tokens: 4096
  
  - name: scheduler_agent
    module: agents.scheduler_agent
    enabled: true
    priority: 5
    config:
      max_workers: 3
      timeout: 300
  
  - name: report_agent
    module: agents.report_agent
    enabled: true
    priority: 3
    config:
      output_formats: ["html", "markdown"]
      languages: ["zh", "en"]
```

---

## 📂 plugins/ 目录结构

```
plugins/
├── custom_agents/               # 自定义 Agent
│   └── my_agent.py
├── custom_data_sources/         # 自定义数据源
│   └── my_data_source.py
├── custom_templates/            # 自定义模板
│   └── my_template.py
├── custom_modules/              # 自定义模块
│   └── my_module.py
└── custom_notifications/        # 自定义通知
    └── my_notification.py
```

### 自定义 Agent 示例

```python
# plugins/custom_agents/my_agent.py
from agents.base import BaseAgent

class MyCustomAgent(BaseAgent):
    name = "my_custom_agent"
    version = "1.0.0"
    description = "我的自定义 Agent"
    
    def analyze(self, context):
        # 自定义分析逻辑
        result = {...}
        return result
```

---

## 📂 tests/ 目录结构

```
tests/
├── unit/                        # 单元测试
│   ├── test_agents/
│   │   ├── test_base.py
│   │   ├── test_analysis.py
│   │   └── ...
│   ├── test_plugins/
│   │   ├── test_base.py
│   │   └── ...
│   └── test_openclaw/
│       ├── test_adapter.py
│       └── ...
│
├── integration/                 # 集成测试
│   ├── test_workflow.py
│   └── ...
│
├── e2e/                         # E2E 测试
│   ├── test_full_analysis.py
│   └── ...
│
└── fixtures/                    # 测试数据
    ├── sample_stock_data.json
    └── ...
```

---

## 📂 scripts/ 目录结构

```
scripts/
├── setup_env.sh                 # 环境搭建
├── validate_config.py           # 配置验证
├── generate_report.py           # 报告生成
├── upgrade_check.py             # 升级检查
└── run_tests.sh                 # 运行测试
```

### setup_env.sh 示例

```bash
#!/bin/bash
# 环境搭建脚本

set -e

echo "🚀 开始环境搭建..."

# 创建虚拟环境
python -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 验证配置
python -m scripts.validate_config

echo "✅ 环境搭建完成！"
```

---

## 📂 output/ 目录结构

```
output/
├── reports/                     # 分析报告
│   ├── 2026-03-25/
│   │   ├── AAPL.html
│   │   ├── AAPL.md
│   │   └── ...
│   └── ...
├── logs/                        # 日志文件
│   ├── 2026-03-25.log
│   └── ...
└── cache/                       # 缓存文件
    ├── stock_data/
    ├── news/
    └── ...
```

---

## 🎯 目录结构优势

### 优势对比

| 维度 | 优化前 | 优化后 | 改善 |
|------|-------|--------|------|
| **根目录文件数** | 15 个 | 5 个 | -67% |
| **代码集中度** | 分散 | 集中于 src/ | 更清晰 |
| **文档组织** | 根目录散乱 | docs/ 分类 | 更易查找 |
| **配置管理** | 分散 | config/ 统一 | 更易维护 |
| **插件扩展** | 不明确 | plugins/ 清晰 | 更易扩展 |
| **测试组织** | 简单 | tests/ 分层 | 更专业 |

### 导航便利性

| 查找内容 | 优化前 | 优化后 | 改善 |
|----------|-------|--------|------|
| **安装指南** | 根目录 | docs/user_guide/install.md | ✅ 分类清晰 |
| **API 参考** | 根目录 | docs/api_reference/README.md | ✅ 分类清晰 |
| **Agent 配置** | config/ | config/agents.yaml | ✅ 保持不变 |
| **自定义 Agent** | 不明确 | plugins/custom_agents/ | ✅ 更清晰 |
| **测试代码** | tests/ | tests/（分层） | ✅ 更专业 |

---

## 📋 迁移计划

### 步骤 1：创建新目录

```bash
# 创建目录结构
mkdir -p src/openclaw src/agents src/plugins src/core
mkdir -p config
mkdir -p plugins/custom_agents plugins/custom_data_sources
mkdir -p tests/unit tests/integration tests/e2e tests/fixtures
mkdir -p docs/user_guide docs/developer_guide docs/api_reference docs/upgrade_guide
mkdir -p scripts
mkdir -p output/reports output/logs output/cache
```

### 步骤 2：移动文件

```bash
# 移动源代码
mv openclaw/ src/
mv agents/ src/
mv plugins_base.py src/plugins/base.py

# 移动文档
mv INSTALL.md docs/user_guide/install.md
mv USER_GUIDE.md docs/user_guide/README.md
mv DEVELOPER_GUIDE.md docs/developer_guide/README.md
mv API_REFERENCE.md docs/api_reference/README.md
mv UPGRADE_GUIDE.md docs/upgrade_guide/README.md
mv *.md docs/analysis/  # 分析报告

# 移动脚本
mv validate_config.py scripts/
mv generate_report.py scripts/
```

### 步骤 3：更新引用

```bash
# 更新 import 路径
# 从 import openclaw.adapter 改为 from src.openclaw import adapter

# 更新文档引用
# 从 README.md 改为 docs/user_guide/README.md
```

### 步骤 4：验证

```bash
# 运行测试
python -m pytest tests/

# 验证配置
python -m scripts.validate_config

# 生成报告
python -m scripts.generate_report AAPL
```

---

## 🎯 最终效果

### 根目录（简洁）

```
daily-stock-analysis-openclaw-skill/
├── README.md
├── LICENSE
├── pyproject.toml
├── requirements.txt
└── .gitignore
```

### 完整结构（清晰）

```
daily-stock-analysis-openclaw-skill/
├── 📄 根目录（5 个文件）
├── 📂 src/（源代码）
├── 📂 config/（配置文件）
├── 📂 plugins/（自定义插件）
├── 📂 tests/（测试代码）
├── 📂 docs/（文档）
├── 📂 scripts/（工具脚本）
└── 📂 output/（输出目录）
```

---

**创建日期**: 2026-03-25  
**最后更新**: 2026-03-25  
**维护者**: WebLeOn
