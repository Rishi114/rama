"""Advanced Tools Skill - Access to Web Search, Code Analysis, God Mode
Integrates Agent-Reach, code-review-graph, and GodMode capabilities"""

import asyncio
from skills.skill_base import Skill
from typing import Any


class ToolsSkill(Skill):
    """
    Advanced tools skill - web search, code analysis, system operations
    """
    
    def __init__(self):
        super().__init__()
        self.triggers = [
            "search", "find", "look up", "analyze", "critical",
            "code analysis", "system info", "processes", "workflow",
            "remember", "recall", "graph", "knowledge"
        ]
        self.tools = None
    
    async def execute(self, input_text: str, context: Any, retrieved_context: str = "") -> str:
        # Initialize tools if needed
        if self.tools is None:
            from tools.god_mode import ToolManager
            self.tools = ToolManager()
        
        input_lower = input_text.lower()
        
        # Web search
        if any(w in input_lower for w in ["search", "find", "look up"]):
            query = input_lower.replace("search", "").replace("find", "").replace("look up", "").strip()
            if query:
                result = await self.tools.web_search.search(query)
                return result
        
        # Critical thinking
        if "analyze" in input_lower or "critical" in input_lower:
            analysis_type = "full"
            if "logic" in input_lower:
                analysis_type = "logic"
            elif "bias" in input_lower:
                analysis_type = "bias"
            elif "evidence" in input_lower:
                analysis_type = "evidence"
            
            text = input_lower.replace("analyze", "").replace("critical", "").strip()
            if text:
                result = await self.tools.critical_thinking.analyze(text, analysis_type)
                return result
        
        # Code analysis
        if "code" in input_lower and ("analyze" in input_lower or "analysis" in input_lower):
            # Would extract code from context
            return "💻 For code analysis, provide the code or use 'analyze code <language>'"
        
        # System info
        if "system" in input_lower and "info" in input_lower:
            result = await self.tools.god_mode.get_system_info()
            return result
        
        # Process list
        if "process" in input_lower or "tasks" in input_lower:
            result = await self.tools.god_mode.list_processes()
            return result
        
        # Memory operations
        if "remember" in input_lower:
            content = input_lower.replace("remember", "").strip()
            if content:
                result = await self.tools.memory.store(content)
                return result
        
        if "recall" in input_lower or "memory" in input_lower:
            query = input_lower.replace("recall", "").replace("memory", "").strip()
            if query:
                result = await self.tools.memory.search(query)
                return result
        
        # List tools
        return self.tools.list_tools()


class WebSearchSkill(Skill):
    """Web and social platform search"""
    
    triggers = ["search web", "search twitter", "search reddit", "search github", "search youtube"]
    
    async def execute(self, input_text, context, retrieved_context=""):
        from tools.god_mode import ToolManager
        
        tools = ToolManager()
        
        platform = "all"
        if "twitter" in input_text.lower():
            platform = "twitter"
        elif "reddit" in input_text.lower():
            platform = "reddit"
        elif "github" in input_text.lower():
            platform = "github"
        elif "youtube" in input_text.lower():
            platform = "youtube"
        
        query = input_text.lower()
        for word in ["search", "web", "twitter", "reddit", "github", "youtube"]:
            query = query.replace(word, "")
        query = query.strip()
        
        if not query:
            return "🔍 What to search? Try 'search python tutorials'"
        
        result = await tools.web_search.search(query, platform)
        return result


class CriticalThinkingSkill(Skill):
    """Critical thinking and analysis"""
    
    triggers = ["analyze", "critical thinking", "evaluate", "assess", "review"]
    
    async def execute(self, input_text, context, retrieved_context=""):
        from tools.god_mode import ToolManager
        
        tools = ToolManager()
        
        # Determine analysis type
        analysis_type = "full"
        if "logic" in input_text.lower():
            analysis_type = "logic"
        elif "bias" in input_text.lower():
            analysis_type = "bias"
        elif "evidence" in input_text.lower():
            analysis_type = "evidence"
        
        # Extract text to analyze
        # In practice, would use the context/retrieved_context
        return await tools.critical_thinking.analyze(input_text, analysis_type)


class CodeAnalysisSkill(Skill):
    """Code understanding and analysis"""
    
    triggers = ["analyze code", "code analysis", "review code", "understand code", "explain code"]
    
    async def execute(self, input_text, context, retrieved_context=""):
        from tools.god_mode import ToolManager
        
        tools = ToolManager()
        
        # Detect language
        language = "auto"
        for lang in ["python", "javascript", "java", "rust", "go", "c++", "c", "ruby", "php"]:
            if lang in input_text.lower():
                language = lang
                break
        
        return await tools.code_analysis.analyze_code("{}".format(input_text), language)


class SystemInfoSkill(Skill):
    """System information and control - God Mode"""
    
    triggers = ["system info", "processes", "tasks", "cpu", "memory", "disk", "system status"]
    
    async def execute(self, input_text, context, retrieved_context=""):
        from tools.god_mode import ToolManager
        
        tools = ToolManager()
        
        if "process" in input_text.lower() or "task" in input_text.lower():
            return await tools.god_mode.list_processes()
        
        if "cpu" in input_text.lower() or "memory" in input_text.lower():
            return await tools.god_mode.get_system_info()
        
        return await tools.god_mode.get_system_info()


class AutomationSkill(Skill):
    """Workflow automation"""
    
    triggers = ["workflow", "automation", "automate", "routine", "create automation"]
    
    async def execute(self, input_text, context, retrieved_context=""):
        from tools.god_mode import ToolManager
        
        tools = ToolManager()
        
        input_lower = input_text.lower()
        
        # List workflows
        if "list" in input_lower or "show" in input_lower:
            return tools.automation.list_workflows()
        
        # Run workflow
        if "run" in input_lower:
            # Extract workflow name
            name = input_lower.replace("run", "").replace("workflow", "").strip()
            if name:
                return await tools.automation.run_workflow(name)
        
        return """🔄 **Automation System:**

- workflow run <name> - Run a workflow
- workflow list - Show all workflows
- create workflow - Create new workflow (not implemented yet)

Create workflows by defining steps in the automation system."""


class MemorySkill(Skill):
    """Persistent memory with search"""
    
    triggers = ["remember", "recall", "memory", "store", "forget"]
    
    async def execute(self, input_text, context, retrieved_context=""):
        from tools.god_mode import ToolManager
        
        tools = ToolManager()
        
        input_lower = input_text.lower()
        
        # Remember / Store
        if "remember" in input_lower or "store" in input_lower:
            content = input_lower.replace("remember", "").replace("store", "").strip()
            if content:
                return await tools.memory.store(content)
        
        # Recall / Search
        if "recall" in input_lower or "search" in input_lower:
            query = input_lower.replace("recall", "").replace("memory", "").replace("search", "").strip()
            if query:
                return await tools.memory.search(query)
        
        # List all
        return tools.memory.list_memories()