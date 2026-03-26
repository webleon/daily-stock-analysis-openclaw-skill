# 报告模板实现工作量评估报告

**评估日期**: 2026-03-25  
**评估人**: 研究分析师 🔬  
**项目**: Daily Stock Analysis OpenClaw Skill

---

## 1. 原项目模板分析

### 1.1 模板文件概览

| 模板文件 | 用途 | 行数 | 复杂度 |
|----------|------|------|--------|
| `templates/report_markdown.j2` | 完整 Markdown 报告 | ~150 行 | 高 |
| `templates/report_wechat.j2` | 微信格式精简报告 | ~60 行 | 中 |
| `templates/report_brief.j2` | 极简简报 | ~15 行 | 低 |
| `templates/_macros.j2` | 共享宏定义 | ~30 行 | 中 |

---

### 1.2 report_markdown.j2 详细分析

**用途**: 生成完整的 Markdown 格式分析报告

**需要的数据结构**:

```python
{
    # 顶层变量
    'report_date': str,              # 报告日期
    'report_timestamp': str,         # 报告时间戳
    'results': List[AnalysisResult], # 分析结果列表
    'enriched': List[Dict],          # 增强数据（含信号 emoji、信号文本等）
    'buy_count': int,                # 买入信号数量
    'hold_count': int,               # 观望信号数量
    'sell_count': int,               # 卖出信号数量
    'summary_only': bool,            # 是否仅摘要
    
    # 每个结果需要
    'result': {
        'code': str,                 # 股票代码
        'analysis_summary': str,     # 分析摘要
        'operation_advice': str,     # 操作建议
        'sentiment_score': int,      # 情感评分
        'trend_prediction': str,     # 趋势预测
        'buy_reason': str,           # 买入理由
        'risk_warning': str,         # 风险提示
        
        # dashboard 块（核心）
        'dashboard': {
            'intelligence': {        # 情报块
                'sentiment_summary': str,
                'earnings_outlook': str,
                'risk_alerts': List[str],
                'positive_catalysts': List[str],
                'latest_news': str
            },
            'core_conclusion': {     # 核心结论
                'one_sentence': str,
                'time_sensitivity': str,
                'position_advice': {
                    'no_position': str,
                    'has_position': str
                }
            },
            'battle_plan': {         # 作战计划
                'sniper_points': {
                    'ideal_buy': float,
                    'secondary_buy': float,
                    'stop_loss': float,
                    'take_profit': float
                },
                'position_strategy': {
                    'suggested_position': str,
                    'entry_plan': str,
                    'risk_control': str
                },
                'action_checklist': List[str]
            },
            'data_perspective': {    # 数据透视
                'trend_status': {
                    'ma_alignment': str,
                    'is_bullish': bool,
                    'trend_score': int
                },
                'price_position': {
                    'current_price': float,
                    'ma5': float,
                    'ma10': float,
                    'ma20': float,
                    'bias_ma5': float,
                    'bias_status': str,
                    'support_level': float,
                    'resistance_level': float
                },
                'volume_analysis': {
                    'volume_ratio': float,
                    'volume_status': str,
                    'turnover_rate': float,
                    'volume_meaning': str
                },
                'chip_structure': {
                    'profit_ratio': float,
                    'avg_cost': float,
                    'concentration': float,
                    'chip_health': str
                }
            }
        },
        'market_snapshot': {         # 当日行情
            'close': float,
            'prev_close': float,
            'open': float,
            'high': float,
            'low': float,
            'pct_chg': float,
            'change_amount': float,
            'amplitude': float,
            'volume': float,
            'amount': float,
            'price': float,
            'volume_ratio': float,
            'turnover_rate': float,
            'source': str
        }
    },
    'history_by_code': Dict          # 历史信号对比
}
```

**复杂度分析**:
- **数据字段**: 约 60+ 个字段
- **嵌套层级**: 4-5 层
- **条件渲染**: 10+ 个条件块
- **循环**: 2 个主要循环（摘要 + 详情）
- **宏调用**: 1 个 (`market_snapshot`)
- **自定义过滤器**: 3 个 (`failed_checks`, `clean_sniper`, `localize_*`)

---

### 1.3 report_wechat.j2 详细分析

**用途**: 微信格式的精简报告（适合移动端阅读）

**数据结构**: 与 `report_markdown.j2` 相同，但渲染更简洁

**特点**:
- 文本截断（标题 80 字符、风险 50 字符等）
- 精简布局（适合微信消息长度）
- 保留核心信息（情报、狙击点、检查清单）

**复杂度分析**:
- **数据字段**: 约 40+ 个字段
- **嵌套层级**: 3-4 层
- **条件渲染**: 8+ 个条件块
- **命名空间**: 使用 Jinja2 `namespace` 构建动态内容

---

### 1.4 report_brief.j2 详细分析

**用途**: 极简简报（适合快速浏览）

**数据结构**: 最小化，仅需：
- `report_date`, `report_timestamp`
- `results`, `enriched`
- `buy_count`, `hold_count`, `sell_count`
- 每个结果：`stock_name`, `code`, `operation_advice`, `sentiment_score`, `analysis_summary`

**复杂度分析**:
- **数据字段**: 约 10 个字段
- **嵌套层级**: 2 层
- **条件渲染**: 1 个循环
- **适合**: 快速预览、推送通知

---

### 1.5 _macros.j2 详细分析

**用途**: 共享宏定义

**包含宏**:
- `market_snapshot(result)`: 渲染当日行情表格

**需要的数据**:
```python
{
    'market_snapshot': {
        'close', 'prev_close', 'open', 'high', 'low',
        'pct_chg', 'change_amount', 'amplitude',
        'volume', 'amount', 'price',
        'volume_ratio', 'turnover_rate', 'source'
    }
}
```

---

## 2. 工作量评估

### 2.1 需要补充的数据字段

| 数据块 | 字段数量 | 当前状态 | 需要实现 |
|--------|----------|----------|----------|
| `dashboard.intelligence` | 5 | ❌ 缺失 | 舆情摘要、业绩预期、风险警报、利好催化、最新动态 |
| `dashboard.core_conclusion` | 4 | ❌ 缺失 | 一句话决策、时效性、持仓建议（空仓/持仓） |
| `dashboard.battle_plan` | 8 | ❌ 缺失 | 狙击点位、仓位策略、检查清单 |
| `dashboard.data_perspective` | 15 | ❌ 缺失 | 均线、价格、量能、筹码分析 |
| `market_snapshot` | 14 | ❌ 缺失 | 当日行情数据 |
| `history_by_code` | 1 | ❌ 缺失 | 历史信号对比 |

**总计**: 约 47 个字段需要补充

---

### 2.2 需要修改的代码

| 模块 | 文件 | 修改内容 | 复杂度 |
|------|------|----------|--------|
| **报告生成器** | `src/core/report/html_generator.py` | 完整重写，支持 Jinja2 模板加载 | 高 |
| **数据结构** | `src/schemas/report_schema.py` | 已有，需验证完整性 | 低 |
| **渲染服务** | `src/services/report_renderer.py` | 已有，需集成到核心 | 中 |
| **分析引擎** | `src/core/__init__.py` | 补充 dashboard 数据构建 | 高 |
| **数据获取** | `src/core/data/*.py` | 补充 market_snapshot 数据 | 中 |
| **模板集成** | `templates/*.j2` | 已有，需测试 | 低 |

---

### 2.3 工作量评估表

| 任务 | 预计工时 (小时) | 技术难度 | 优先级 |
|------|-----------------|----------|--------|
| **1. 数据结构补充** | 4-6 | 中 | 🔴 高 |
| - dashboard.intelligence | 1-2 | 低 | 🔴 |
| - dashboard.core_conclusion | 1 | 低 | 🔴 |
| - dashboard.battle_plan | 1-2 | 中 | 🟡 |
| - dashboard.data_perspective | 1-2 | 中 | 🟡 |
| **2. 市场数据集成** | 2-3 | 中 | 🟡 中 |
| - market_snapshot 数据获取 | 2-3 | 中 | 🟡 |
| **3. 报告生成器重写** | 3-4 | 高 | 🔴 高 |
| - Jinja2 模板加载 | 1 | 中 | 🔴 |
| - 模板数据准备 | 1-2 | 中 | 🔴 |
| - 多格式支持 (MD/WeChat/Brief) | 1-2 | 高 | 🟡 |
| **4. 集成测试** | 2-3 | 中 | 🔴 高 |
| - 单元测试 | 1 | 低 | 🟡 |
| - 集成测试 | 1-2 | 中 | 🔴 |
| - 模板渲染测试 | 1 | 低 | 🟡 |
| **5. 文档更新** | 1-2 | 低 | 🟢 低 |
| - API 文档 | 1 | 低 | 🟢 |
| - 使用示例 | 1 | 低 | 🟢 |

**总计工时**: **12-18 小时**

**技术难度**: **中-高**

---

## 3. 简化方案对比

### 方案 A: 最小改动（保持当前简化模板）

**实现内容**:
- 保持当前内联 HTML 模板
- 仅补充核心字段（operation_advice, sentiment_score, analysis_summary）
- 不实现 dashboard 复杂结构

**工作量**: 2-4 小时

**优点**:
- ✅ 快速上线
- ✅ 代码简单，易维护
- ✅ 依赖少（无需 Jinja2 复杂配置）

**缺点**:
- ❌ 报告信息量少
- ❌ 无法使用原项目模板
- ❌ 缺少专业分析（狙击点、数据透视等）

**推荐度**: ⭐⭐ (2/5)

**适用场景**: 快速验证、MVP 版本

---

### 方案 B: 中等简化（部分使用原模板）

**实现内容**:
- 使用 `report_brief.j2` 模板（最简单）
- 补充必要字段（enriched 数据结构）
- 实现基础 dashboard（intelligence + core_conclusion）
- 暂不实现 battle_plan 和 data_perspective

**工作量**: 6-8 小时

**优点**:
- ✅ 使用原项目模板
- ✅ 报告结构清晰
- ✅ 工作量可控
- ✅ 后续可扩展

**缺点**:
- ❌ 缺少高级功能（狙击点、数据透视）
- ❌ 仍需补充部分数据

**推荐度**: ⭐⭐⭐⭐ (4/5)

**适用场景**: 平衡功能与工作量，推荐方案

---

### 方案 C: 完整实现（完全使用原模板）

**实现内容**:
- 完整支持所有 3 个模板（markdown/wechat/brief）
- 实现完整 dashboard 数据结构
- 集成 market_snapshot 数据
- 支持历史信号对比
- 完整的多语言支持

**工作量**: 12-18 小时

**优点**:
- ✅ 功能完整
- ✅ 与原项目一致
- ✅ 专业报告质量
- ✅ 多格式输出

**缺点**:
- ❌ 工作量大
- ❌ 数据结构复杂
- ❌ 需要更多数据源集成

**推荐度**: ⭐⭐⭐ (3/5)

**适用场景**: 追求完整功能，长期维护

---

## 4. 推荐方案及理由

### 推荐方案：**方案 B（中等简化）**

**理由**:

1. **性价比最高**
   - 6-8 小时工作量 vs 12-18 小时（方案 C）
   - 实现 70% 核心功能 vs 100% 功能
   - 快速上线，后续可迭代

2. **使用原项目模板**
   - `report_brief.j2` 模板简单但结构完整
   - 保持与原项目一致性
   - 便于后续升级到完整模板

3. **核心功能完整**
   - 信号判断（买入/观望/卖出）
   - 情感评分
   - 核心结论
   - 基础情报（舆情、业绩、风险）

4. **可扩展性强**
   - dashboard 结构已建立
   - 后续可逐步添加 battle_plan、data_perspective
   - 模板可无缝切换到 `report_markdown.j2`

---

### 实施建议

**第一阶段（2-3 小时）**:
- [ ] 修改 `HTMLReportGenerator` 使用 Jinja2 加载 `report_brief.j2`
- [ ] 构建基础 `enriched` 数据结构
- [ ] 测试模板渲染

**第二阶段（2-3 小时）**:
- [ ] 实现 `dashboard.intelligence` 数据填充
- [ ] 实现 `dashboard.core_conclusion` 数据填充
- [ ] 测试报告生成

**第三阶段（2 小时）**:
- [ ] 集成测试（完整流程）
- [ ] 修复问题
- [ ] 文档更新

---

### 后续升级路径

```
方案 B (当前)
    ↓ +2-3 小时
添加 battle_plan (狙击点、仓位策略)
    ↓ +2-3 小时
添加 data_perspective (数据透视)
    ↓ +2-3 小时
切换到 report_markdown.j2 (完整模板)
    ↓ +2-3 小时
添加 market_snapshot (当日行情)
    ↓
方案 C (完整实现)
```

---

## 5. 总结

| 方案 | 工作量 | 功能完整度 | 推荐度 |
|------|--------|------------|--------|
| 方案 A (最小改动) | 2-4 小时 | 30% | ⭐⭐ |
| **方案 B (中等简化)** | **6-8 小时** | **70%** | **⭐⭐⭐⭐** |
| 方案 C (完整实现) | 12-18 小时 | 100% | ⭐⭐⭐ |

**最终建议**: 采用 **方案 B（中等简化）**，在保证核心功能的前提下控制工作量，后续可根据需求逐步升级。

---

**报告位置**: `docs/TEMPLATE_EVALUATION_REPORT.md`  
**维护者**: 研究分析师 🔬  
**最后更新**: 2026-03-25
