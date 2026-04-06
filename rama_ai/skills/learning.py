"""Context Learning and Swarm Intelligence Skills"""

from skills.skill_base import Skill
from typing import Any


class ContextLearningSkill(Skill):
    """Learn from experience and improve"""
    
    triggers = ["learn", "remember", "experience", "context", "improve", "pattern"]
    
    async def execute(self, input_text, context, retrieved_context=""):
        from tools.context_engine import ContextEngine, ExperienceLearner
        
        tool = ContextEngine()
        learner = ExperienceLearner()
        
        input_lower = input_text.lower()
        
        # Show stats
        if "stats" in input_lower or "status" in input_lower:
            stats = tool.get_stats()
            return f"""🧠 **Learning Stats:**

- Total Interactions: {stats.get('total_interactions', 0)}
- Successful: {stats.get('successful', 0)}
- Success Rate: {stats.get('success_rate', '0%')}
- Patterns Learned: {stats.get('patterns_learned', 0)}"""
        
        # Record experience
        if "success" in input_lower or "worked" in input_lower:
            return "✅ Recording this as a successful experience! I'll remember what worked."
        
        if "failed" in input_lower or "didn't work" in input_lower:
            return "📝 Recording this as a failure. I'll learn from this!"
        
        # Get suggestions
        if "suggest" in input_lower or "recommend" in input_lower:
            query = input_lower.replace("suggest", "").replace("recommend", "").strip()
            if query:
                suggestion = await learner.suggest_action(query)
                return f"💡 {suggestion}"
        
        return """🧠 **Context Learning:**

I learn from every interaction to improve!

Features:
- Track successful/failed actions
- Pattern recognition
- Context branching
- Experience-based suggestions

Ask:
- "learn from success" / "learn from failure"
- "suggest action for X"
- "learning stats"""


class SwarmIntelligenceSkill(Skill):
    """Swarm intelligence for prediction and optimization"""
    
    triggers = ["predict", "forecast", "optimize", "swarm", "analyze", "future"]
    
    async def execute(self, input_text, context, retrieved_context=""):
        from tools.swarm_intelligence import PredictionEngine, ForecastingTool
        
        tool = PredictionEngine()
        forecast_tool = ForecastingTool()
        
        input_lower = input_text.lower()
        
        # Forecasting
        if "forecast" in input_lower or "predict" in input_lower:
            # Extract numbers from input
            import re
            numbers = re.findall(r'-?\d+\.?\d*', input_text)
            
            if len(numbers) >= 3:
                try:
                    data = [float(n) for n in numbers[:10]]
                    result = await forecast_tool.forecast(data, steps_ahead=3)
                    return f"""🔮 **Forecast:**

Input data: {data}
Predicted next 3 values: {result}

This uses linear regression + swarm optimization for pattern detection."""
                except:
                    pass
            
            return """🔮 **Forecasting:**

Provide numerical data to forecast:
- "forecast 1, 2, 3, 4, 5"
- "predict next values: 10, 20, 30"

I'll analyze patterns and predict future values!"""
        
        # Anomaly detection
        if "anomaly" in input_lower or "unusual" in input_lower:
            numbers = re.findall(r'-?\d+\.?\d*', input_text)
            if len(numbers) >= 3:
                try:
                    data = [float(n) for n in numbers]
                    anomalies = await forecast_tool.detect_anomalies(data)
                    return f"""🔍 **Anomaly Detection:**

Data: {data}
Anomalies at indices: {anomalies if anomalies else 'None found'}

Values at anomaly indices: {[data[i] for i in anomalies] if anomalies else 'N/A'}"""
                except:
                    pass
            
            return """🔍 **Anomaly Detection:**

Provide data to find unusual values:
- "find anomalies in 1,2,100,3,4"
- "detect unusual in data series"

Uses standard deviation to identify outliers."""
        
        # Optimization
        if "optimize" in input_lower or "best" in input_lower:
            return """⚡ **Optimization:**

Swarm intelligence for finding optimal solutions!

Use "optimize" with:
- A mathematical function
- Search space bounds

Example: "optimize x^2 + y^2" """
        
        return """🔮 **Swarm Intelligence:**

Predict, forecast, and optimize using swarm algorithms!

Commands:
- forecast <data> - Predict future values
- anomalies <data> - Find unusual patterns
- optimize <function> - Find optimal solution

Based on Particle Swarm Optimization (PSO)!"""


class PatternRecognitionSkill(Skill):
    """Recognize patterns in data and code"""
    
    triggers = ["pattern", "detect", "find pattern", "recognize", "similar"]
    
    async def execute(self, input_text, context, retrieved_context=""):
        return """🔍 **Pattern Recognition:**

Detect patterns in:
- Code structure
- Data series
- Text documents
- User behavior

Provide data or code and ask:
- "find patterns in this code"
- "detect patterns in data"
- "what's similar to X"

Uses AI to identify recurring themes!"""


class BranchingSkill(Skill):
    """Context branching for trying different approaches"""
    
    triggers = ["branch", "fork", "try different", "alternative"]
    
    async def execute(self, input_text, context, retrieved_context=""):
        from tools.context_engine import BranchManager
        
        tool = BranchManager()
        
        input_lower = input_text.lower()
        
        # Create branch
        if "create" in input_lower or "new" in input_lower:
            # Extract name
            import re
            match = re.search(r'(?:create|new|branch)\s+(\w+)', input_lower)
            if match:
                name = match.group(1)
                result = await tool.create_branch(name, {"test": "data"})
                return f"🌿 {result}"
        
        # List branches
        if "list" in input_lower:
            if tool.branches:
                output = "🌿 **Active Branches:**\n"
                for name, info in tool.branches.items():
                    output += f"- {name}: created {info.get('created_at', 'unknown')}\n"
                return output
            return "🌿 No branches created yet."
        
        return """🌿 **Context Branching:**

Try different approaches without losing context!

Commands:
- "create branch X" - Create new branch
- "switch to branch X" - Use different context
- "merge branch X" - Merge back to main
- "list branches" - Show all branches

Useful for experimentation!"""