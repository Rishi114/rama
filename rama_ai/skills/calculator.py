"""Calculator Skill - Math operations"""

import re
from skills.skill_base import Skill


class CalculatorSkill(Skill):
    """Basic calculator functionality"""
    
    def __init__(self):
        super().__init__()
        self.triggers = ["calculate", "compute", "math", "+", "-", "*", "/", "what is"]
    
    async def execute(self, input_text: str, context: Any, retrieved_context: str = "") -> str:
        # Extract mathematical expression
        expr = input_text.lower()
        for word in ["calculate", "compute", "what is", "what's"]:
            expr = expr.replace(word, "")
        
        # Clean expression
        expr = re.sub(r'[^\d+\-*/().]', '', expr).strip()
        
        if not expr:
            return "🔢 Tell me what to calculate, like 'calculate 2+2' or '15% of 200'"
        
        try:
            allowed_chars = set('0123456789+-*/(). ')
            if all(c in allowed_chars for c in expr):
                result = eval(expr)
                if isinstance(result, float):
                    result = round(result, 6)
                return f"🔢 **{expr}** = **{result}**"
            return "🔢 Invalid expression"
        except Exception as e:
            return f"🔢 Can't calculate: {str(e)}"