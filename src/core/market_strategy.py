# -*- coding: utf-8 -*-
"""Market strategy blueprints for CN/US daily market recap and stock analysis."""

from dataclasses import dataclass
from typing import List, Optional


@dataclass(frozen=True)
class StrategyDimension:
    """Single strategy dimension used by market recap prompts."""

    name: str
    objective: str
    checkpoints: List[str]


@dataclass(frozen=True)
class MarketStrategyBlueprint:
    """Region specific market strategy blueprint."""

    region: str
    strategy_id: str
    title: str
    positioning: str
    principles: List[str]
    dimensions: List[StrategyDimension]
    action_framework: List[str]
    prompt_template: str

    def to_prompt_block(self) -> str:
        """Render blueprint as prompt instructions."""
        principles_text = "\n".join([f"- {item}" for item in self.principles])
        action_text = "\n".join([f"- {item}" for item in self.action_framework])

        dims = []
        for dim in self.dimensions:
            checkpoints = "\n".join([f"  - {cp}" for cp in dim.checkpoints])
            dims.append(f"- {dim.name}: {dim.objective}\n{checkpoints}")
        dimensions_text = "\n".join(dims)

        return (
            f"## Strategy Blueprint: {self.title}\n"
            f"{self.positioning}\n\n"
            f"### Strategy Principles\n{principles_text}\n\n"
            f"### Analysis Dimensions\n{dimensions_text}\n\n"
            f"### Action Framework\n{action_text}"
        )

    def to_markdown_block(self) -> str:
        """Render blueprint as markdown section for template fallback report."""
        dims = "\n".join([f"- **{dim.name}**: {dim.objective}" for dim in self.dimensions])
        section_title = "### 六、策略框架" if self.region == "cn" else "### VI. Strategy Framework"
        return f"{section_title}\n{dims}\n"


# ==================== A 股策略 ====================

BULL_TREND_STRATEGY = MarketStrategyBlueprint(
    region="cn",
    strategy_id="bull_trend",
    title="A 股市场多头趋势策略",
    positioning="聚焦指数趋势、资金博弈与板块轮动，形成次日交易计划。",
    principles=[
        "先看指数方向，再看量能结构，最后看板块持续性。",
        "结论必须映射到仓位、节奏与风险控制动作。",
        "判断使用当日数据与近 3 日新闻，不臆测未验证信息。",
    ],
    dimensions=[
        StrategyDimension(
            name="趋势结构",
            objective="判断市场处于上升、震荡还是防守阶段。",
            checkpoints=["上证/深证/创业板是否同向", "放量上涨或缩量下跌是否成立", "关键支撑阻力是否被突破"],
        ),
        StrategyDimension(
            name="资金情绪",
            objective="识别短线风险偏好与情绪温度。",
            checkpoints=["涨跌家数与涨跌停结构", "成交额是否扩张", "高位股是否出现分歧"],
        ),
        StrategyDimension(
            name="主线板块",
            objective="提炼可交易主线与规避方向。",
            checkpoints=["领涨板块是否具备事件催化", "板块内部是否有龙头带动", "领跌板块是否扩散"],
        ),
    ],
    action_framework=[
        "进攻：指数共振上行 + 成交额放大 + 主线强化。",
        "均衡：指数分化或缩量震荡，控制仓位并等待确认。",
        "防守：指数转弱 + 领跌扩散，优先风控与减仓。",
    ],
    prompt_template="""你是一位专业的 A 股趋势分析师，请根据以下数据生成趋势分析报告。

【分析要求】
- 判断当前市场趋势（上升/震荡/下跌）
- 分析成交量与价格的关系
- 识别主线板块和资金流向
- 给出具体的操作建议

【输出格式】
## 趋势判断
（明确判断市场处于什么阶段）

## 量能分析
（分析成交额、量比等指标）

## 板块分析
（分析领涨领跌板块）

## 操作建议
（给出具体的仓位和操作指引）
"""
)

MA_GOLDEN_CROSS_STRATEGY = MarketStrategyBlueprint(
    region="cn",
    strategy_id="ma_golden_cross",
    title="均线金叉策略",
    positioning="通过均线系统金叉死叉判断买卖点，适合趋势跟踪。",
    principles=[
        "金叉买入，死叉卖出。",
        "结合成交量确认信号有效性。",
        "设置明确的止损位。",
    ],
    dimensions=[
        StrategyDimension(
            name="均线形态",
            objective="判断 MA5/MA10/MA20 的排列状态。",
            checkpoints=["MA5 是否上穿 MA10", "MA10 是否上穿 MA20", "均线是否多头排列"],
        ),
        StrategyDimension(
            name="成交量确认",
            objective="验证金叉信号的有效性。",
            checkpoints=["金叉日是否放量", "成交量是否持续放大", "量价是否配合"],
        ),
        StrategyDimension(
            name="风险控制",
            objective="设置止损和止盈位。",
            checkpoints=["止损位设置", "止盈位设置", "仓位管理"],
        ),
    ],
    action_framework=[
        "买入：MA5 上穿 MA10 + 放量确认。",
        "持有：均线多头排列 + 量价配合。",
        "卖出：MA5 下穿 MA10 或跌破止损位。",
    ],
    prompt_template="""你是一位专业的均线分析师，请根据以下数据生成均线金叉分析报告。

【分析要求】
- 分析 MA5/MA10/MA20 的排列状态
- 判断是否形成金叉或死叉
- 结合成交量验证信号
- 给出具体的买卖点建议

【输出格式】
## 均线形态
（描述当前均线排列状态）

## 金叉/死叉判断
（明确是否形成金叉或死叉）

## 成交量验证
（分析成交量是否确认信号）

## 操作建议
（给出具体的买入/卖出/持有建议）
"""
)

VOLUME_BREAKOUT_STRATEGY = MarketStrategyBlueprint(
    region="cn",
    strategy_id="volume_breakout",
    title="放量突破策略",
    positioning="通过成交量放大和价格突破判断突破有效性，捕捉主升浪。",
    principles=[
        "放量突破关键阻力位是买入信号。",
        "缩量回调是加仓机会。",
        "跌破支撑位止损。",
    ],
    dimensions=[
        StrategyDimension(
            name="突破形态",
            objective="判断是否形成有效突破。",
            checkpoints=["是否突破关键阻力位", "突破是否伴随放量", "突破幅度是否超过 3%"],
        ),
        StrategyDimension(
            name="成交量分析",
            objective="验证突破的量能支持。",
            checkpoints=["量比是否大于 2", "成交额是否创近期新高", "资金流入是否持续"],
        ),
        StrategyDimension(
            name="持续性判断",
            objective="判断突破的持续性。",
            checkpoints=["板块是否配合", "市场情绪是否支持", "是否有消息面催化"],
        ),
    ],
    action_framework=[
        "买入：放量突破关键阻力位 + 板块配合。",
        "加仓：缩量回调至支撑位。",
        "止损：跌破突破起点或支撑位。",
    ],
    prompt_template="""你是一位专业的突破分析师，请根据以下数据生成放量突破分析报告。

【分析要求】
- 判断是否形成有效突破
- 分析成交量是否确认突破
- 评估突破的持续性
- 给出具体的操作建议

【输出格式】
## 突破形态
（描述突破的关键价位和形态）

## 量能分析
（分析成交量是否支持突破）

## 持续性评估
（评估突破的可持续性）

## 操作建议
（给出具体的买入/加仓/止损建议）
"""
)

SHRINK_PULLBACK_STRATEGY = MarketStrategyBlueprint(
    region="cn",
    strategy_id="shrink_pullback",
    title="缩量回踩策略",
    positioning="通过缩量回踩支撑位判断低吸机会，适合波段操作。",
    principles=[
        "上升趋势中的缩量回踩是低吸机会。",
        "回踩不破支撑位是关键。",
        "再次放量上涨是加仓信号。",
    ],
    dimensions=[
        StrategyDimension(
            name="趋势判断",
            objective="判断是否处于上升趋势。",
            checkpoints=["均线是否多头排列", "前期是否有明显上涨", "上涨是否伴随放量"],
        ),
        StrategyDimension(
            name="回踩分析",
            objective="分析回踩的幅度和量能。",
            checkpoints=["回踩幅度是否合理（不超过前期涨幅的 50%）", "回踩是否缩量", "是否触及支撑位"],
        ),
        StrategyDimension(
            name="买入时机",
            objective="判断最佳买入时机。",
            checkpoints=["是否在支撑位企稳", "是否出现缩量止跌信号", "是否准备再次放量"],
        ),
    ],
    action_framework=[
        "低吸：上升趋势中的缩量回踩支撑位。",
        "加仓：再次放量上涨确认。",
        "止损：跌破支撑位止损。",
    ],
    prompt_template="""你是一位专业的波段分析师，请根据以下数据生成缩量回踩分析报告。

【分析要求】
- 判断当前趋势状态
- 分析回踩的幅度和量能
- 判断是否形成低吸机会
- 给出具体的操作建议

【输出格式】
## 趋势判断
（描述当前趋势状态）

## 回踩分析
（分析回踩的幅度和量能特征）

## 低吸机会
（判断是否形成低吸机会）

## 操作建议
（给出具体的低吸/加仓/止损建议）
"""
)

CHAN_THEORY_STRATEGY = MarketStrategyBlueprint(
    region="cn",
    strategy_id="chan_theory",
    title="缠论分析策略",
    positioning="通过缠论的笔、段、中枢判断买卖点，适合精确捕捉转折点。",
    principles=[
        "笔、段、中枢是缠论的核心。",
        "背驰是转折的信号。",
        "三类买卖点是操作的核心。",
    ],
    dimensions=[
        StrategyDimension(
            name="笔段分析",
            objective="识别当前的笔和段。",
            checkpoints=["当前是上升笔还是下降笔", "是否形成线段", "线段的方向"],
        ),
        StrategyDimension(
            name="中枢分析",
            objective="判断中枢的位置和状态。",
            checkpoints=["中枢的位置", "中枢的震荡区间", "是否形成中枢延伸或扩张"],
        ),
        StrategyDimension(
            name="背驰判断",
            objective="判断是否形成背驰。",
            checkpoints=["是否形成盘整背驰", "是否形成趋势背驰", "背驰的力度"],
        ),
    ],
    action_framework=[
        "一类买点：趋势背驰后的反转。",
        "二类买点：回踩不破前低。",
        "三类买点：突破中枢后回踩。",
    ],
    prompt_template="""你是一位专业的缠论分析师，请根据以下数据生成缠论分析报告。

【分析要求】
- 识别当前的笔、段、中枢
- 判断是否形成背驰
- 识别买卖点类型
- 给出具体的操作建议

【输出格式】
## 笔段分析
（描述当前的笔和段状态）

## 中枢分析
（描述中枢的位置和状态）

## 背驰判断
（判断是否形成背驰及类型）

## 操作建议
（给出具体的买卖点和操作建议）
"""
)

WAVE_THEORY_STRATEGY = MarketStrategyBlueprint(
    region="cn",
    strategy_id="wave_theory",
    title="波浪理论策略",
    positioning="通过艾略特波浪理论判断市场周期位置，捕捉主升浪。",
    principles=[
        "5 浪上升，3 浪下跌是基本形态。",
        "第 3 浪通常是最强的。",
        "数浪需要灵活，不要僵化。",
    ],
    dimensions=[
        StrategyDimension(
            name="浪型判断",
            objective="判断当前处于什么浪型。",
            checkpoints=["是上升浪还是调整浪", "如果是上升浪，是第几浪", "如果是调整浪，是 ABC 中的哪一浪"],
        ),
        StrategyDimension(
            name="浪型验证",
            objective="验证浪型判断的正确性。",
            checkpoints=["成交量是否支持", "时间周期是否合理", "幅度是否符合黄金分割"],
        ),
        StrategyDimension(
            name="目标位预测",
            objective="预测下一浪的目标位。",
            checkpoints=["使用黄金分割预测目标位", "参考前期高低点", "考虑成交量配合"],
        ),
    ],
    action_framework=[
        "买入：确认第 3 浪启动。",
        "持有：第 3 浪和第 5 浪持有。",
        "卖出：第 5 浪结束或 ABC 调整开始。",
    ],
    prompt_template="""你是一位专业的波浪理论分析师，请根据以下数据生成波浪理论分析报告。

【分析要求】
- 判断当前处于什么浪型
- 验证浪型判断的正确性
- 预测下一浪的目标位
- 给出具体的操作建议

【输出格式】
## 浪型判断
（描述当前浪型位置）

## 浪型验证
（验证浪型判断的依据）

## 目标位预测
（预测下一浪的目标位）

## 操作建议
（给出具体的买入/持有/卖出建议）
"""
)

BOX_OSCILLATION_STRATEGY = MarketStrategyBlueprint(
    region="cn",
    strategy_id="box_oscillation",
    title="箱体震荡策略",
    positioning="通过箱体上下沿判断买卖点，适合震荡市操作。",
    principles=[
        "箱体下沿买入，上沿卖出。",
        "突破箱体后追涨杀跌。",
        "箱体震荡中高抛低吸。",
    ],
    dimensions=[
        StrategyDimension(
            name="箱体识别",
            objective="识别箱体的上下沿。",
            checkpoints=["箱体上沿的价格", "箱体下沿的价格", "箱体的时间跨度"],
        ),
        StrategyDimension(
            name="位置判断",
            objective="判断当前价格在箱体中的位置。",
            checkpoints=["是否接近箱体下沿", "是否接近箱体上沿", "是否在箱体中部"],
        ),
        StrategyDimension(
            name="突破判断",
            objective="判断是否形成突破。",
            checkpoints=["是否放量突破上沿", "是否缩量跌破下沿", "突破后是否有回踩确认"],
        ),
    ],
    action_framework=[
        "低吸：接近箱体下沿 + 缩量企稳。",
        "高抛：接近箱体上沿 + 放量受阻。",
        "突破：放量突破箱体后追涨。",
    ],
    prompt_template="""你是一位专业的震荡分析师，请根据以下数据生成箱体震荡分析报告。

【分析要求】
- 识别箱体的上下沿
- 判断当前价格在箱体中的位置
- 判断是否形成突破
- 给出具体的操作建议

【输出格式】
## 箱体识别
（描述箱体的上下沿和范围）

## 位置判断
（判断当前价格在箱体中的位置）

## 突破判断
（判断是否形成突破及方向）

## 操作建议
（给出具体的低吸/高抛/突破操作建议）
"""
)

EMOTION_CYCLE_STRATEGY = MarketStrategyBlueprint(
    region="cn",
    strategy_id="emotion_cycle",
    title="情绪周期策略",
    positioning="通过市场情绪周期判断买卖点，适合短线操作。",
    principles=[
        "情绪周期分为冰点、回暖、高潮、退潮。",
        "冰点买入，高潮卖出。",
        "龙头股是情绪的风向标。",
    ],
    dimensions=[
        StrategyDimension(
            name="情绪判断",
            objective="判断当前情绪周期位置。",
            checkpoints=["涨停家数", "连板高度", "跌停家数", "炸板率"],
        ),
        StrategyDimension(
            name="龙头分析",
            objective="分析龙头股的状态。",
            checkpoints=["龙头股是否连板", "龙头股是否放量", "龙头股是否见顶"],
        ),
        StrategyDimension(
            name="周期判断",
            objective="判断情绪周期的阶段。",
            checkpoints=["是冰点期还是高潮期", "是回暖期还是退潮期", "周期转换的信号"],
        ),
    ],
    action_framework=[
        "买入：情绪冰点 + 龙头股企稳。",
        "持有：情绪回暖 + 龙头股连板。",
        "卖出：情绪高潮 + 龙头股见顶。",
    ],
    prompt_template="""你是一位专业的情绪分析师，请根据以下数据生成情绪周期分析报告。

【分析要求】
- 判断当前情绪周期位置
- 分析龙头股的状态
- 判断周期转换的信号
- 给出具体的操作建议

【输出格式】
## 情绪判断
（描述当前情绪状态和周期位置）

## 龙头分析
（分析龙头股的状态和信号）

## 周期判断
（判断周期阶段和转换信号）

## 操作建议
（给出具体的买入/持有/卖出建议）
"""
)

BOTTOM_VOLUME_STRATEGY = MarketStrategyBlueprint(
    region="cn",
    strategy_id="bottom_volume",
    title="地量见底策略",
    positioning="通过地量判断底部，适合左侧交易。",
    principles=[
        "地量见地价，天量见天价。",
        "地量后需要等待确认信号。",
        "左侧交易需要严格控制仓位。",
    ],
    dimensions=[
        StrategyDimension(
            name="地量判断",
            objective="判断是否形成地量。",
            checkpoints=["成交量是否创近期新低", "量比是否小于 0.5", "是否持续缩量"],
        ),
        StrategyDimension(
            name="底部特征",
            objective="判断是否形成底部。",
            checkpoints=["是否止跌企稳", "是否形成双底或底背离", "是否有资金流入"],
        ),
        StrategyDimension(
            name="确认信号",
            objective="等待底部确认信号。",
            checkpoints=["是否放量上涨", "是否突破短期均线", "是否有板块配合"],
        ),
    ],
    action_framework=[
        "观察：地量出现后等待确认。",
        "试仓：出现确认信号后小仓位试仓。",
        "加仓：放量上涨确认后加仓。",
    ],
    prompt_template="""你是一位专业的底部分析师，请根据以下数据生成地量见底分析报告。

【分析要求】
- 判断是否形成地量
- 分析底部特征
- 等待确认信号
- 给出具体的操作建议

【输出格式】
## 地量判断
（描述成交量是否形成地量）

## 底部特征
（分析是否形成底部及特征）

## 确认信号
（描述需要的确认信号）

## 操作建议
（给出具体的观察/试仓/加仓建议）
"""
)

DRAGON_HEAD_STRATEGY = MarketStrategyBlueprint(
    region="cn",
    strategy_id="dragon_head",
    title="龙头战法策略",
    positioning="通过识别和参与龙头股，获取超额收益。",
    principles=[
        "只做龙头，不做跟风。",
        "龙头首阴是买入机会。",
        "龙头见顶坚决卖出。",
    ],
    dimensions=[
        StrategyDimension(
            name="龙头识别",
            objective="识别当前市场的龙头股。",
            checkpoints=["连板高度最高", "成交量最大", "板块影响力最强"],
        ),
        StrategyDimension(
            name="龙头状态",
            objective="判断龙头股的状态。",
            checkpoints=["是否继续连板", "是否放量", "是否见顶信号"],
        ),
        StrategyDimension(
            name="参与时机",
            objective="判断参与龙头的时机。",
            checkpoints=["首阴是否是买入机会", "是否回踩重要均线", "是否二次冲高"],
        ),
    ],
    action_framework=[
        "买入：龙头首阴或回踩均线。",
        "持有：龙头继续连板持有。",
        "卖出：龙头见顶信号出现。",
    ],
    prompt_template="""你是一位专业的龙头分析师，请根据以下数据生成龙头战法分析报告。

【分析要求】
- 识别当前市场的龙头股
- 判断龙头股的状态
- 判断参与时机
- 给出具体的操作建议

【输出格式】
## 龙头识别
（描述当前市场的龙头股）

## 龙头状态
（分析龙头股的状态和信号）

## 参与时机
（判断参与龙头的时机）

## 操作建议
（给出具体的买入/持有/卖出建议）
"""
)

ONE_YANG_THREE_YIN_STRATEGY = MarketStrategyBlueprint(
    region="cn",
    strategy_id="one_yang_three_yin",
    title="一阳穿三阴策略",
    positioning="通过一阳穿三阴形态判断反转信号，适合捕捉底部反转。",
    principles=[
        "一阳穿三阴是强烈的反转信号。",
        "需要成交量配合确认。",
        "后续需要继续放量确认。",
    ],
    dimensions=[
        StrategyDimension(
            name="形态识别",
            objective="识别一阳穿三阴形态。",
            checkpoints=["前面是否连续三根阴线", "阳线是否实体饱满", "阳线是否覆盖三根阴线"],
        ),
        StrategyDimension(
            name="量能分析",
            objective="分析成交量是否确认。",
            checkpoints=["阳线是否放量", "量比是否大于 2", "资金是否流入"],
        ),
        StrategyDimension(
            name="后续确认",
            objective="判断是否需要后续确认。",
            checkpoints=["次日是否继续放量", "是否突破短期均线", "是否有板块配合"],
        ),
    ],
    action_framework=[
        "买入：一阳穿三阴 + 放量确认。",
        "加仓：次日继续放量上涨。",
        "止损：跌破阳线实体底部。",
    ],
    prompt_template="""你是一位专业的 K 线形态分析师，请根据以下数据生成一阳穿三阴分析报告。

【分析要求】
- 识别一阳穿三阴形态
- 分析成交量是否确认
- 判断是否需要后续确认
- 给出具体的操作建议

【输出格式】
## 形态识别
（描述一阳穿三阴形态）

## 量能分析
（分析成交量是否确认形态）

## 后续确认
（判断是否需要后续确认信号）

## 操作建议
（给出具体的买入/加仓/止损建议）
"""
)

# Strategy registry
STRATEGY_REGISTRY = {
    "bull_trend": BULL_TREND_STRATEGY,
    "ma_golden_cross": MA_GOLDEN_CROSS_STRATEGY,
    "volume_breakout": VOLUME_BREAKOUT_STRATEGY,
    "shrink_pullback": SHRINK_PULLBACK_STRATEGY,
    "chan_theory": CHAN_THEORY_STRATEGY,
    "wave_theory": WAVE_THEORY_STRATEGY,
    "box_oscillation": BOX_OSCILLATION_STRATEGY,
    "emotion_cycle": EMOTION_CYCLE_STRATEGY,
    "bottom_volume": BOTTOM_VOLUME_STRATEGY,
    "dragon_head": DRAGON_HEAD_STRATEGY,
    "one_yang_three_yin": ONE_YANG_THREE_YIN_STRATEGY,
}


def get_strategy(strategy_id: str) -> MarketStrategyBlueprint:
    """Get strategy blueprint by ID."""
    return STRATEGY_REGISTRY.get(strategy_id, BULL_TREND_STRATEGY)


def list_strategies() -> List[dict]:
    """List all available strategies."""
    return [
        {
            "id": strategy.strategy_id,
            "title": strategy.title,
            "positioning": strategy.positioning,
        }
        for strategy in STRATEGY_REGISTRY.values()
    ]
