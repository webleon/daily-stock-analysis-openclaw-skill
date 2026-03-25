"""
Agent 基类
所有 Agent 必须继承此类
"""


class BaseAgent:
    """Agent 基类"""
    
    name = "base_agent"
    version = "1.0.0"
    description = "基础 Agent"
    priority = 0
    
    def __init__(self, config=None):
        self.config = config or {}
    
    def analyze(self, context):
        """
        分析逻辑（子类实现）
        
        Args:
            context: 分析上下文
        
        Returns:
            分析结果
        """
        raise NotImplementedError("子类必须实现 analyze 方法")
    
    def validate(self):
        """
        验证配置
        
        Returns:
            bool: 配置是否有效
        """
        return True
    
    def get_info(self):
        """获取 Agent 信息"""
        return {
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "priority": self.priority
        }
