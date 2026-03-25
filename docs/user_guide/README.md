# 用户指南

## 快速开始

### 1. 安装

参考 [安装指南](install.md)

### 2. 运行分析

```bash
# 分析单只股票
python -m scripts.generate_report AAPL

# 分析多只股票
python -m scripts.generate_report AAPL GOOG MSFT

# 生成 HTML 报告
python -m scripts.generate_report AAPL --format html

# 生成 Markdown 报告
python -m scripts.generate_report AAPL --format markdown
```

### 3. 查看报告

报告生成在 `output/reports/` 目录：

```
output/reports/
├── 2026-03-25/
│   ├── AAPL.html
│   ├── AAPL.md
│   └── ...
```

## 功能特性

### 16 模块分析

- 收入质量
- 盈利能力
- 现金流
- 前瞻指引
- 竞争格局
- 核心 KPI
- 产品与新业务
- 合作伙伴生态
- 高管团队
- 宏观政策
- 估值模型
- 筹码分布
- 长期监控变量
- 研发效率
- 会计质量
- ESG 筛查

### 6 大投资视角

- 质量复利（巴菲特/芒格）
- 想象力成长（Baillie Gifford/ARK）
- 基本面多空（Tiger Cubs）
- 深度价值（Klarman/Marks）
- 催化剂驱动（Tepper/Ackman）
- 宏观战术（Druckenmiller）

### 估值模型

- DCF（现金流折现）
- PEG（市盈率相对盈利增长比率）
- EV/EBITDA（企业价值倍数）
- 反向 DCF

## 配置

### 自定义 Agent

在 `config/agents.yaml` 中添加：

```yaml
agents:
  - name: my_custom_agent
    module: plugins.custom_agents.my_agent
    enabled: true
    priority: 10
```

### 自定义数据源

在 `config/data_sources.yaml` 中添加：

```yaml
data_sources:
  - name: my_data_source
    module: plugins.custom_data_sources.my_data_source
    enabled: true
```

## 常见问题

### Q: 如何添加新的数据源？

A: 创建 `plugins/custom_data_sources/my_data_source.py`，继承 `BaseDataSource` 类。

### Q: 如何自定义报告模板？

A: 创建 `plugins/custom_templates/my_template.py`，继承 `BaseTemplate` 类。

### Q: 如何修改分析模块？

A: 修改 `src/core/analysis/` 下的对应模块。

## 下一步

- [API 参考](../api_reference/README.md) - 查看 API 文档
- [开发者指南](../developer_guide/README.md) - 参与开发
