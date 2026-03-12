# -*- coding: utf-8 -*-
"""
Ask command - analyze a stock using a specific Agent strategy.

Usage:
    /ask 600519                        -> Analyze with default strategy
    /ask 600519 用缠论分析              -> Parse strategy from message
    /ask 600519 chan_theory             -> Specify strategy id directly
"""

import re
import logging
from typing import List, Optional

from bot.commands.base import BotCommand
from bot.models import BotMessage, BotResponse
from data_provider.base import canonical_stock_code
from src.config import get_config

logger = logging.getLogger(__name__)

# Strategy name to id mapping (CN name -> strategy id)
STRATEGY_NAME_MAP = {
    "缠论": "chan_theory",
    "缠论分析": "chan_theory",
    "波浪": "wave_theory",
    "波浪理论": "wave_theory",
    "艾略特": "wave_theory",
    "箱体": "box_oscillation",
    "箱体震荡": "box_oscillation",
    "情绪": "emotion_cycle",
    "情绪周期": "emotion_cycle",
    "趋势": "bull_trend",
    "多头趋势": "bull_trend",
    "均线金叉": "ma_golden_cross",
    "金叉": "ma_golden_cross",
    "缩量回踩": "shrink_pullback",
    "回踩": "shrink_pullback",
    "放量突破": "volume_breakout",
    "突破": "volume_breakout",
    "地量见底": "bottom_volume",
    "龙头": "dragon_head",
    "龙头战法": "dragon_head",
    "一阳穿三阴": "one_yang_three_yin",
}


class AskCommand(BotCommand):
    """
    Ask command handler - invoke Agent with a specific strategy to analyze a stock.

    Usage:
        /ask 600519                    -> Analyze with default strategy (bull_trend)
        /ask 600519 用缠论分析          -> Automatically selects chan_theory strategy
        /ask 600519 chan_theory         -> Directly specify strategy id
        /ask hk00700 波浪理论看看       -> HK stock with wave_theory
    """

    @property
    def name(self) -> str:
        return "ask"

    @property
    def aliases(self) -> List[str]:
        return ["问股"]

    @property
    def description(self) -> str:
        return "使用 Agent 策略分析股票"

    @property
    def usage(self) -> str:
        return "/ask <股票代码> [策略名称]"

    def validate_args(self, args: List[str]) -> Optional[str]:
        """Validate arguments."""
        if not args:
            return "请输入股票代码。用法：/ask <股票代码> [策略名称]\n示例：/ask 600519 用缠论分析"

        code = args[0].upper()
        is_a_stock = re.match(r"^\d{6}$", code)
        is_hk_stock = re.match(r"^HK\d{5}$", code)
        is_us_stock = re.match(r"^[A-Z]{1,5}(\.[A-Z]{1,2})?$", code)

        if not (is_a_stock or is_hk_stock or is_us_stock):
            return f"无效的股票代码：{code}（A 股 6 位数字 / 港股 HK+5 位数字 / 美股 1-5 个字母）"

        return None

    def _parse_strategy(self, args: List[str]) -> str:
        """Parse strategy from arguments, returning strategy id."""
        if len(args) < 2:
            return "bull_trend"  # Default strategy

        # Join remaining args as the strategy text
        strategy_text = " ".join(args[1:]).strip()

        # Try direct strategy id match first
        try:
            from src.core.market_strategy import get_strategy
            strategy = get_strategy(strategy_text)
            if strategy:
                return strategy
        except:
            pass

        # Try Chinese name mapping
        for name, strategy_id in STRATEGY_NAME_MAP.items():
            if name in strategy_text:
                logger.info(f"[AskCommand] Matched strategy '{name}' -> '{strategy_id}'")
                return strategy_id

        # Default to bull_trend if no match
        logger.warning(f"[AskCommand] No strategy matched from '{strategy_text}', using default")
        return "bull_trend"

    def execute(self, message: BotMessage, args: List[str]) -> BotResponse:
        """Execute the ask command."""
        from src.analyzer import GeminiAnalyzer
        from src.search_service import SearchService
        from data_provider.manager import DataFetcherManager
        
        # Parse arguments
        code = args[0].upper()
        strategy_id = self._parse_strategy(args)
        
        logger.info(f"[AskCommand] Analyzing {code} with strategy {strategy_id}")
        
        try:
            # Get stock data
            data_manager = DataFetcherManager()
            stock_data = data_manager.get_stock_data(code)
            
            if not stock_data:
                return BotResponse.error_response(f"无法获取股票 {code} 的数据")
            
            # Initialize analyzer
            analyzer = GeminiAnalyzer()
            search_service = SearchService()
            
            # Get strategy blueprint
            from src.core.market_strategy import get_strategy
            strategy = get_strategy(strategy_id)
            
            # Generate analysis
            logger.info(f"[AskCommand] Generating analysis with LLM...")
            analysis = analyzer.analyze_stock_with_strategy(
                stock_data=stock_data,
                strategy_id=strategy_id,
                search_service=search_service
            )
            
            if analysis:
                return BotResponse.markdown_response(analysis)
            else:
                return BotResponse.error_response("分析失败，请稍后重试")
                
        except Exception as e:
            logger.error(f"[AskCommand] Error: {e}")
            return BotResponse.error_response(f"分析出错：{str(e)}")
