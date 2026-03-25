"""
6 大投资视角分析引擎
基于巴菲特、芒格等投资大师的理念
"""

from typing import Dict, Any


class SixPerspectivesAnalyzer:
    """6 大投资视角分析器"""
    
    def __init__(self):
        self.perspectives = {
            'quality_compounder': self._analyze_quality_compounder,
            'imaginative_growth': self._analyze_imaginative_growth,
            'fundamental_long_short': self._analyze_fundamental_long_short,
            'deep_value': self._analyze_deep_value,
            'catalyst_driven': self._analyze_catalyst_driven,
            'macro_tactical': self._analyze_macro_tactical,
        }
    
    def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行 6 大投资视角分析
        
        Args:
            data: 股票数据
        
        Returns:
            6 大视角分析结果
        """
        results = {}
        
        for perspective_name, analyzer_func in self.perspectives.items():
            try:
                results[perspective_name] = analyzer_func(data)
            except Exception as e:
                results[perspective_name] = {
                    "score": 0,
                    "analysis": f"分析失败：{str(e)}",
                    "status": "error"
                }
        
        # 计算综合评分
        total_score = sum(r.get('score', 0) for r in results.values())
        avg_score = total_score / len(results) if results else 0
        
        return {
            "perspectives": results,
            "total_score": round(avg_score, 1),
            "status": "success"
        }
    
    def _analyze_quality_compounder(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """1. 质量复利视角（巴菲特/芒格）"""
        # 分析 ROE 可持续性、护城河、管理层质量
        roe = data.get('roe', 0)
        moat = data.get('economic_moat', 'none')
        management = data.get('management', {})
        
        score = 50
        analysis = []
        
        # ROE 分析
        if roe > 0.2:
            score += 25
            analysis.append("ROE 优秀 (>20%)，符合巴菲特标准")
        elif roe > 0.15:
            score += 15
            analysis.append("ROE 良好 (15-20%)")
        
        # 护城河分析
        if moat == 'wide':
            score += 25
            analysis.append("护城河宽阔，芒格偏好")
        elif moat == 'narrow':
            score += 15
            analysis.append("护城河狭窄")
        
        # 管理层分析
        if management.get('track_record') == 'excellent':
            score += 20
            analysis.append("管理层记录优秀")
        
        return {
            "score": min(100, max(0, score)),
            "analysis": "。".join(analysis) if analysis else "质量复利视角分析待完善",
            "representatives": "巴菲特/芒格",
            "status": "success",
            "metrics": {
                "roe": roe,
                "moat": moat,
                "management": management.get('track_record', 'unknown')
            },
            "recommendation": "买入" if score >= 70 else "观望" if score >= 50 else "卖出"
        }
    
    def _analyze_imaginative_growth(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """2. 想象力成长视角（Baillie Gifford/ARK）"""
        # 分析长期成长潜力、颠覆性创新
        revenue_growth = data.get('revenue_growth', 0)
        tam = data.get('tam', 0)  # 总可寻址市场
        innovation = data.get('innovation', 'low')
        
        score = 50
        analysis = []
        
        # 增长分析
        if revenue_growth > 0.3:
            score += 30
            analysis.append("高速增长 (>30%)，符合 Baillie Gifford 标准")
        elif revenue_growth > 0.2:
            score += 20
            analysis.append("较快增长 (20-30%)")
        
        # 市场空间分析
        if tam > 1000:  # 1000 亿美元
            score += 25
            analysis.append("市场空间巨大 (>1000 亿美元)")
        elif tam > 100:
            score += 15
            analysis.append("市场空间较大 (100-1000 亿美元)")
        
        # 创新分析
        if innovation == 'disruptive':
            score += 25
            analysis.append("颠覆性创新，ARK 偏好")
        elif innovation == 'incremental':
            score += 10
            analysis.append("渐进式创新")
        
        return {
            "score": min(100, max(0, score)),
            "analysis": "。".join(analysis) if analysis else "想象力成长视角分析待完善",
            "representatives": "Baillie Gifford/ARK",
            "status": "success",
            "metrics": {
                "revenue_growth": revenue_growth,
                "tam": tam,
                "innovation": innovation
            },
            "recommendation": "买入" if score >= 70 else "观望" if score >= 50 else "卖出"
        }
    
    def _analyze_fundamental_long_short(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """3. 基本面多空视角（Tiger Cubs）"""
        # 分析多空因素、风险收益比
        bullish_factors = data.get('bullish_factors', [])
        bearish_factors = data.get('bearish_factors', [])
        
        score = 50
        analysis = []
        
        # 多头因素分析
        if len(bullish_factors) >= 5:
            score += 25
            analysis.append(f"多头因素{len(bullish_factors)}项，强劲")
        elif len(bullish_factors) >= 3:
            score += 15
            analysis.append(f"多头因素{len(bullish_factors)}项，中等")
        
        # 空头因素分析
        if len(bearish_factors) >= 5:
            score -= 25
            analysis.append(f"空头因素{len(bearish_factors)}项，风险高")
        elif len(bearish_factors) >= 3:
            score -= 15
            analysis.append(f"空头因素{len(bearish_factors)}项，风险中等")
        
        return {
            "score": min(100, max(0, score)),
            "analysis": "。".join(analysis) if analysis else "基本面多空视角分析待完善",
            "representatives": "Tiger Cubs",
            "status": "success",
            "metrics": {
                "bullish_factors": len(bullish_factors),
                "bearish_factors": len(bearish_factors)
            },
            "recommendation": "做多" if score >= 60 else "中性" if score >= 40 else "做空"
        }
    
    def _analyze_deep_value(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """4. 深度价值视角（Klarman/Marks）"""
        # 分析安全边际、内在价值
        pe = data.get('pe', 0)
        pb = data.get('pb', 0)
        margin_of_safety = data.get('margin_of_safety', 0)
        
        score = 50
        analysis = []
        
        # 估值分析
        if 0 < pe < 15:
            score += 25
            analysis.append("PE 低 (<15)，Klarman 偏好")
        elif 15 <= pe < 25:
            score += 10
            analysis.append("PE 适中 (15-25)")
        
        if 0 < pb < 2:
            score += 25
            analysis.append("PB 低 (<2)，深度价值")
        elif 2 <= pb < 4:
            score += 10
            analysis.append("PB 适中 (2-4)")
        
        # 安全边际分析
        if margin_of_safety > 0.3:
            score += 25
            analysis.append("安全边际高 (>30%)，Marks 偏好")
        elif margin_of_safety > 0.15:
            score += 15
            analysis.append("安全边际中等 (15-30%)")
        
        return {
            "score": min(100, max(0, score)),
            "analysis": "。".join(analysis) if analysis else "深度价值视角分析待完善",
            "representatives": "Klarman/Marks",
            "status": "success",
            "metrics": {
                "pe": pe,
                "pb": pb,
                "margin_of_safety": margin_of_safety
            },
            "recommendation": "买入" if score >= 70 else "观望" if score >= 50 else "卖出"
        }
    
    def _analyze_catalyst_driven(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """5. 催化剂驱动视角（Tepper/Ackman）"""
        # 分析短期催化剂、事件驱动
        catalysts = data.get('catalysts', [])
        event_driven = data.get('event_driven', False)
        
        score = 50
        analysis = []
        
        # 催化剂分析
        if len(catalysts) >= 3:
            score += 30
            analysis.append(f"催化剂{len(catalysts)}项，Tepper 偏好")
        elif len(catalysts) >= 2:
            score += 20
            analysis.append(f"催化剂{len(catalysts)}项，中等")
        
        # 事件驱动分析
        if event_driven:
            score += 20
            analysis.append("事件驱动机会，Ackman 策略")
        
        return {
            "score": min(100, max(0, score)),
            "analysis": "。".join(analysis) if analysis else "催化剂驱动视角分析待完善",
            "representatives": "Tepper/Ackman",
            "status": "success",
            "metrics": {
                "catalysts": len(catalysts),
                "event_driven": event_driven
            },
            "recommendation": "买入" if score >= 70 else "观望" if score >= 50 else "卖出"
        }
    
    def _analyze_macro_tactical(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """6. 宏观战术视角（Druckenmiller）"""
        # 分析宏观环境、流动性、市场情绪
        macro = data.get('macro', 'neutral')
        liquidity = data.get('liquidity', 'neutral')
        sentiment = data.get('sentiment', 'neutral')
        
        score = 50
        analysis = []
        
        # 宏观分析
        if macro == 'positive':
            score += 20
            analysis.append("宏观环境积极")
        elif macro == 'negative':
            score -= 20
            analysis.append("宏观环境消极")
        
        # 流动性分析
        if liquidity == 'loose':
            score += 20
            analysis.append("流动性宽松，Druckenmiller 偏好")
        elif liquidity == 'tight':
            score -= 20
            analysis.append("流动性紧缩")
        
        # 情绪分析
        if sentiment == 'extreme_fear':
            score += 25
            analysis.append("极度恐惧，逆向买入机会")
        elif sentiment == 'extreme_greed':
            score -= 25
            analysis.append("极度贪婪，警惕回调")
        
        return {
            "score": min(100, max(0, score)),
            "analysis": "。".join(analysis) if analysis else "宏观战术视角分析待完善",
            "representatives": "Druckenmiller",
            "status": "success",
            "metrics": {
                "macro": macro,
                "liquidity": liquidity,
                "sentiment": sentiment
            },
            "recommendation": "买入" if score >= 70 else "观望" if score >= 50 else "卖出"
        }
