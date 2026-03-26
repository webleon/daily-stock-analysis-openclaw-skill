# Daily Stock Analysis - OpenClaw Skill

基于 OpenClaw 的股票分析技能，支持 A 股/港股/美股数据分析。

## 功能特性

- ✅ 多市场支持（A 股/港股/美股）
- ✅ 16 模块技术分析
- ✅ 6 大投资视角
- ✅ HTML/Markdown/微信报告
- ✅ 多 Agent 编排
- ✅ 自动命名规范

## 环境要求

- Python 3.9+
- 已安装核心依赖

## 安装

### 1. 安装依赖（使用主机环境）

```bash
pip3 install -r requirements.txt
```

### 2. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env，配置必要的 API Key
```

### 3. 验证安装

```bash
./run.sh --check
```

## 使用方法

### 分析单只股票

```bash
./run.sh 600519
```

### 分析多只股票

```bash
./run.sh 600519,000858,00700
```

### 市场复盘

```bash
./run.sh --market-review
```

### 深度分析（多 Agent）

```bash
# 在 OpenClaw 中
深度分析 AAPL
```

## 输出目录

报告保存在：`~/.openclaw/workspace/output/daily-stock-analysis/`

命名规范：`{YYYY-MM-DD}_{SYMBOL}[_{HHMMSS}].html`

示例：
- `2026-03-26_600519.html` - 当天第一份
- `2026-03-26_600519_143022.html` - 当天第二份

## 项目结构

```
├── core/                    # 核心模块
│   ├── data/               # 数据获取
│   ├── analysis/           # 分析模块
│   └── report/             # 报告生成
├── data_provider/          # 数据提供器
├── templates/              # Jinja2 模板
├── scripts/                # 工具脚本
├── tests/                  # 测试文件
├── output/                 # 输出目录
└── docs/                   # 文档
```

## 依赖说明

### 核心依赖

- `akshare` - A 股数据
- `yfinance` - 美股/港股数据
- `tushare` - 备用数据源
- `pyyaml` - 配置文件
- `jinja2` - 模板引擎
- `openclaw` - OpenClaw SDK

### 测试依赖

- `pytest` - 测试框架
- `pytest-cov` - 测试覆盖

## 配置说明

### 环境变量 (.env)

```bash
# 数据源 API Key
TUSHARE_TOKEN=your_token
AKSHARE_QPS=1

# OpenClaw 配置
OPENCLAW_MODEL=modelstudio/qwen3.5-plus
```

## 常见问题

### Q: 数据不可用？

A: 检查 API Key 配置和网络连接。

### Q: 报告生成失败？

A: 检查模板文件是否完整。

### Q: 如何切换模型？

A: 修改 `.env` 中的 `OPENCLAW_MODEL`。

## 文档

- [安装指南](INSTALL.md)
- [功能说明](README_FEATURES.md)
- [清理报告](CLEANUP_REPORT.md)

## 许可证

MIT License

## 更新日志

详见 [review.md](review.md)
