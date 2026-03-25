"""
OpenClaw API 适配器
支持版本检测和 API 兼容
"""

import importlib


class OpenClawAdapter:
    """OpenClaw API 适配器"""
    
    def __init__(self):
        self.api_version = self._detect_api_version()
    
    def _detect_api_version(self):
        """检测 OpenClaw API 版本"""
        try:
            import openclaw
            version = getattr(openclaw, '__version__', '1.0')
            if version >= "2.0":
                return "2.0"
            elif version >= "1.5":
                return "1.5"
            else:
                return "1.0"
        except:
            return "1.0"
    
    def spawn_subagent(self, task, **kwargs):
        """自动适配不同版本的 sessions_spawn"""
        if self.api_version >= "2.0":
            return self._spawn_v2(task, **kwargs)
        elif self.api_version >= "1.5":
            return self._spawn_v1_5(task, **kwargs)
        else:
            return self._spawn_v1(task, **kwargs)
    
    def _spawn_v1(self, task, **kwargs):
        """v1.0 API"""
        from openclaw import sessions_spawn
        return sessions_spawn(task=task, **kwargs)
    
    def _spawn_v1_5(self, task, **kwargs):
        """v1.5 API"""
        from openclaw import sessions_spawn
        return sessions_spawn(task=task, mode="run", **kwargs)
    
    def _spawn_v2(self, task, **kwargs):
        """v2.0 API"""
        from openclaw import sessions_spawn
        return sessions_spawn(task=task, mode="run", runtime="subagent", **kwargs)
    
    def register_tool(self, tool_name, tool_func):
        """注册 tool"""
        # v2.0+ 支持动态 tool 注册
        if self.api_version >= "2.0":
            import openclaw
            if hasattr(openclaw, 'register_tool'):
                openclaw.register_tool(tool_name, tool_func)
