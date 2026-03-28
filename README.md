# 📈 股票智能分析系统 - OpenClaw Skill

[![GitHub stars](https://img.shields.io/github/stars/ZhuLinsen/daily_stock_analysis?style=social)](https://github.com/ZhuLinsen/daily_stock_analysis/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-Ready-2088FF?logo=github-actions&logoColor=white)](https://github.com/features/actions)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker&logoColor=white)](https://hub.docker.com/)

基于 OpenClaw 的股票分析技能，支持 A 股/港股/美股数据分析。

AI-powered stock analysis skill for OpenClaw, supporting A-share/HK-share/US-stock analysis.

> **致敬原项目**: 本项目基于 [ZhuLinsen/daily_stock_analysis](https://github.com/ZhuLinsen/daily_stock_analysis) 优化，专注于 OpenClaw 集成和路径规范化。

---

## ✨ 功能特性 / Features

### 核心分析功能

| 功能 | 说明 | 状态 |
|------|------|------|
| **多市场支持** | A 股/港股/美股及美股指数 | ✅ 原项目 |
| **16 模块技术分析** | 均线/筹码/量能/技术指标等 | ✅ 原项目 |
| **6 大投资视角** | 巴菲特/芒格/达利奥等视角 | ✅ 原项目 |
| **AI 决策仪表盘** | 一句话结论 + 精确买卖点位 | ✅ 原项目 |
| **多渠道推送** | 微信/飞书/Telegram/Discord 等 | ✅ 原项目 |
| **GitHub Actions** | 定时自动执行，无需服务器 | ✅ 原项目 |

### 本项目新增/优化功能

| 功能 | 说明 | 状态 |
|------|------|------|
| **统一输出路径** | 所有输出强制到 `~/.openclaw/workspace/output/` | ✅ **新增** |
| **路径安全检查** | 自动检测并纠正违规文件位置 | ✅ **新增** |
| **统一配置模块** | `core/config.py` 集中管理路径 | ✅ **新增** |
| **文档精简** | 从 17 个文档合并到 3 个核心文档 | ✅ **优化** |
| **项目清理** | 删除 48MB 临时文件和缓存 | ✅ **优化** |
| **OpenClaw 集成** | 深度集成 OpenClaw 技能系统 | ✅ **优化** |

---

## 🚀 快速开始 / Quick Start

### 方式 1: GitHub Actions (推荐)

```bash
# 1. Fork 仓库
# 2. 配置 Secrets (AIHUBMIX_KEY, STOCK_LIST, 通知渠道)
# 3. 启用 Actions
# 4. 每个工作日 18:00 自动执行
```

**最少配置**:
- AI 模型 API Key (AIHUBMIX_KEY 或 GEMINI_API_KEY)
- 通知渠道 (至少一个 Webhook)
- 股票列表 (STOCK_LIST)

### 方式 2: 本地运行

```bash
# 1. 克隆项目
git clone https://github.com/ZhuLinsen/daily_stock_analysis.git
cd daily_stock_analysis

# 2. 安装依赖
pip3 install -r requirements.txt

# 3. 配置环境变量
cp .env.example .env
# 编辑 .env，配置 API Key

# 4. 运行分析
python3 main.py 600519
```

---

## 📚 文档 / Documentation

| 文档 | 说明 |
|------|------|
| **[完整指南](docs/GUIDE.md)** | 部署、配置、FAQ、多 Agent |
| **[更新日志](docs/CHANGELOG.md)** | 版本历史 |
| **[清理报告](docs/CLEANUP_REPORT.md)** | 项目优化记录 |
| **[路径规范](docs/OUTPUT_PATHS.md)** | 输出路径规范 |

---

## 📁 项目结构 / Project Structure

```
daily_stock_analysis/
├── src/                    # 核心代码
├── data_provider/          # 数据源 (15 个数据源适配器)
├── tests/                  # 测试用例
├── templates/              # 报告模板
├── scripts/                # 脚本工具
├── core/                   # 配置模块 (路径配置)
├── docs/                   # 文档目录
│   ├── GUIDE.md            # 完整指南
│   ├── CHANGELOG.md        # 更新日志
│   ├── CLEANUP_REPORT.md   # 清理报告
│   └── README.md           # 文档索引
├── .env.example            # 环境变量示例
├── requirements.txt        # Python 依赖
└── README.md               # 项目说明 (本文件)
```

---

## 🔧 环境要求 / Requirements

- **Python**: 3.9+
- **依赖**: 见 `requirements.txt`
- **可选**: Docker, GitHub Actions

---

## 📊 输出说明 / Output

**输出目录**: `~/.openclaw/workspace/output/daily-stock-analysis/`

**命名规范**: `{YYYY-MM-DD}_{SYMBOL}[_{HHMMSS}].html`

**示例**:
- `2026-03-26_600519.html` - 当天第一份
- `2026-03-26_600519_143022.html` - 同一天第二份

---

## 🤝 贡献 / Contributing

欢迎提交 Issue 和 Pull Request！

详细指南见：[docs/GUIDE.md#-贡献指南](docs/GUIDE.md#-贡献指南--contributing)

### 贡献方式
- 🐛 报告 Bug
- 💡 功能建议
- 🔧 提交代码
- 📖 文档改进

---

## 📄 许可证 / License

MIT License

---

## 🙏 致谢 / Acknowledgments

本项目基于以下优秀项目：

- **[ZhuLinsen/daily_stock_analysis](https://github.com/ZhuLinsen/daily_stock_analysis)** - A 股自选股智能分析系统
- **[OpenClaw](https://github.com/openclaw/openclaw)** - 开源 AI 自动化平台

感谢原作者们的杰出贡献！

---

## 📧 联系方式 / Contact

- **Issues**: https://github.com/ZhuLinsen/daily_stock_analysis/issues
- **Discussions**: https://github.com/ZhuLinsen/daily_stock_analysis/discussions
- **原项目**: https://github.com/ZhuLinsen/daily_stock_analysis

---

**最后更新**: 2026-03-28
