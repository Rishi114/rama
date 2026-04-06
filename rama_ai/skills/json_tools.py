"""JSON Repair and Pipeline Skills - Based on agentjson"""

from skills.skill_base import Skill
from typing import Any


class JSONRepairSkill(Skill):
    """Repair broken JSON from AI outputs"""
    
    triggers = ["fix json", "repair json", "json error", "invalid json", "json parse"]
    
    async def execute(self, input_text, context, retrieved_context=""):
        from tools.json_tools import JSONRepairTool
        
        tool = JSONRepairTool()
        
        # Extract JSON from input
        # In practice, would extract from conversation context
        text_to_fix = input_text.lower().replace("fix json", "").replace("repair json", "").strip()
        
        if not text_to_fix:
            return """🔧 **JSON Repair:**

Provide broken JSON to fix, like:
- "fix json {name: 'value'}"
- "repair json {'key': True}"

I can fix:
- Unquoted keys
- Single quotes
- Python literals (True/False/None)
- Trailing commas
- Missing commas
- Markdown code fences"""
        
        repaired, success, trace = tool.repair(text_to_fix)
        
        return f"""🔧 **JSON Repair Result:**

**Method:** {trace.get('method', 'unknown')}
**Success:** {'✅ Yes' if success else '❌ No'}

**Operations:** {len(trace.get('operations', []))}
{chr(10).join([f"- {op.get('op', 'unknown')}" for op in trace.get('operations', [])]) if trace.get('operations') else '- None needed'}

**Repaired JSON:**
```json
{repaired[:500]}"""
    
    def can_handle(self, input_text):
        return "json" in input_text.lower()


class PipelineSkill(Skill):
    """Complete JSON pipeline for AI outputs"""
    
    triggers = ["pipeline", "process json", "extract json", "parse json"]
    
    async def execute(self, input_text, context, retrieved_context=""):
        from tools.json_tools import JSONPipelineTool
        
        tool = JSONPipelineTool()
        
        input_lower = input_text.lower()
        
        if "stats" in input_lower or "status" in input_lower:
            stats = tool.get_stats()
            return f"""📊 **JSON Pipeline Stats:**

- Total Repairs: {stats.get('total_repairs', 0)}
- Success Rate: {stats.get('success_rate', '0%')}"""
        
        return """📊 **JSON Pipeline:**

Process AI outputs through:
1. Extract JSON from text/markdown
2. Fast-path parse attempt
3. Heuristic repairs
4. Advanced repairs
5. Return strict JSON

Use 'process json <text>' to process through pipeline."""


class ToolCallSkill(Skill):
    """Parse and execute tool calls from AI outputs"""
    
    triggers = ["tool call", "function call", "execute tool", "run function"]
    
    async def execute(self, input_text, context, retrieved_context=""):
        from tools.json_tools import ToolCallParser
        
        parser = ToolCallParser()
        
        return """🔧 **Tool Call Parser:**

Parse tool/function calls from AI outputs:

Format expected:
```json
{"tool": "name", "args": {...}}
```

Or array:
```json
[{"tool": "name", "args": {...}}, ...]
```

Use 'parse tool calls <text>' to extract."""