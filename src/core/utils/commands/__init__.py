# -*- coding: utf-8 -*-
"""
===================================
命令处理器模块
===================================

包含所有机器人命令的实现。
"""

from src.core.utils.commands.base import BotCommand
from src.core.utils.commands.help import HelpCommand
from src.core.utils.commands.status import StatusCommand
from src.core.utils.commands.analyze import AnalyzeCommand
from src.core.utils.commands.market import MarketCommand
from src.core.utils.commands.batch import BatchCommand
from src.core.utils.commands.ask import AskCommand
from src.core.utils.commands.chat import ChatCommand

# 所有可用命令（用于自动注册）
ALL_COMMANDS = [
    HelpCommand,
    StatusCommand,
    AnalyzeCommand,
    MarketCommand,
    BatchCommand,
    AskCommand,
    ChatCommand,
]

__all__ = [
    'BotCommand',
    'HelpCommand',
    'StatusCommand',
    'AnalyzeCommand',
    'MarketCommand',
    'BatchCommand',
    'AskCommand',
    'ChatCommand',
    'MarketCommand',
    'BatchCommand',
    'ALL_COMMANDS',
]
