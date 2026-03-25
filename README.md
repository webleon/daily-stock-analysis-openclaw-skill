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

## 目录结构

```
├── src/                       # 源代码
├── config/                    # 配置文件
├── plugins/                   # 自定义插件
├── tests/                     # 测试代码
├── docs/                      # 文档
├── scripts/                   # 工具脚本
└── output/                    # 输出目录
```

## 许可证

MIT License
