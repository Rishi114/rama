# RAMA AI v2.0 - Tools
# Advanced capabilities for AI agent

# Web Search Tools (based on Agent-Reach)
from .web_tools import WebSearchTool, CriticalThinkingTool, CodeAnalysisTool, KnowledgeGraphTool

# God Mode Tools (based on G0DM0D3 + code-review-graph)
from .god_mode import (
    GodModeTool,
    AutomationTool,
    MemoryTool,
    ToolManager,
)

# JSON Repair Tools (based on agentjson)
from .json_tools import JSONRepairTool, JSONPipelineTool, ToolCallParser

# Video Learning Tools
from .video_tools import VideoLearningTool, TranscriptExtractor, VideoAnalysisTool

# Context Engine (based on agentic-context-engine)
from .context_engine import (
    ContextEngine,
    ContextPipeline,
    DeduplicationTool,
    BranchManager,
    ExperienceLearner
)

# Swarm Intelligence (based on MiroFish)
from .swarm_intelligence import (
    SwarmIntelligence,
    ForecastingTool,
    OptimizationTool,
    PredictionEngine
)

# Self-Learning Engine (NEW - Continuous Improvement)
from .self_learning import (
    SelfLearningEngine,
    EmotionLearningSystem,
    SelfRepairSystem,
    UniversalCodeKnowledge
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
    'JSONRepairTool',
    'JSONPipelineTool',
    'ToolCallParser',
    'VideoLearningTool',
    'TranscriptExtractor',
    'VideoAnalysisTool',
    'ContextEngine',
    'ContextPipeline',
    'DeduplicationTool',
    'BranchManager',
    'ExperienceLearner',
    'SwarmIntelligence',
    'ForecastingTool',
    'OptimizationTool',
    'PredictionEngine',
    'SelfLearningEngine',
    'EmotionLearningSystem',
    'SelfRepairSystem',
    'UniversalCodeKnowledge',
]