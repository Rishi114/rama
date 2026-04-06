# RAMA AI v2.0 - Tools
# Advanced capabilities for AI agent

# Web Search Tools (based on Agent-Reach)
from .web_tools import WebSearchTool, CriticalThinkingTool, CodeAnalysisTool, KnowledgeGraphTool

# God Mode Tools (based on G0DM0D3 + code-review-graph)
from .god_mode import (
    GodModeTool,
    AutomationTool,
    MemoryTool,
    ToolManager
)

__all__ = [
    'WebSearchTool',
    'CriticalThinkingTool', 
    'CodeAnalysisTool',
    'KnowledgeGraphTool',
    'GodModeTool',
    'AutomationTool',
    'MemoryTool',
    'ToolManager',
]