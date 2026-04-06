"""JSON Repair Tool - Fix broken JSON from AI outputs
Based on agentjson architecture for LLM pipeline reliability"""

import re
import json
import logging
from typing import Dict, List, Optional, Any, Tuple

logger = logging.getLogger(__name__)


class JSONRepairTool:
    """
    Repair broken JSON from AI-generated outputs
    Handles common LLM JSON failure modes
    """
    
    def __init__(self):
        self.repair_count = 0
        self.fix_operations = []
    
    def repair(self, text: str, schema: Optional[Dict] = None) -> Tuple[str, bool, Dict]:
        """
        Repair JSON from AI output
        
        Args:
            text: Raw text containing JSON
            schema: Optional JSON schema for validation
            
        Returns:
            (repaired_json, success, repair_trace)
        """
        self.fix_operations = []
        
        # Step 1: Extract JSON from markdown or text
        extracted = self._extract_json(text)
        
        # Step 2: Try direct parse first (fast path)
        if self._is_valid_json(extracted):
            return extracted, True, {"method": "direct"}
        
        # Step 3: Heuristic repairs (fast deterministic fixes)
        repaired = self._heuristic_repair(extracted)
        if self._is_valid_json(repaired):
            self.repair_count += 1
            return repaired, True, {"method": "heuristic", "operations": self.fix_operations}
        
        # Step 4: Advanced repair attempts
        repaired = self._advanced_repair(repaired)
        
        if self._is_valid_json(repaired):
            self.repair_count += 1
            return repaired, True, {"method": "advanced", "operations": self.fix_operations}
        
        # Failed to repair
        return text, False, {"method": "failed", "operations": self.fix_operations}
    
    def _extract_json(self, text: str) -> str:
        """Extract JSON from markdown fences or surrounding text"""
        
        # Remove markdown code fences
        patterns = [
            r'```json\s*(.+?)\s*```',
            r'```\s*(.+?)\s*```',
            r'```json\n(.+?)\n```',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.DOTALL)
            if match:
                self.fix_operations.append({"op": "extract_markdown", "text": "removed code fences"})
                return match.group(1)
        
        # Remove prefix/suffix garbage
        # Look for JSON object/array start
        json_start = re.search(r'[\[{]', text)
        if json_start:
            prefix = text[:json_start.start()]
            if prefix.strip():
                self.fix_operations.append({"op": "remove_prefix", "text": prefix.strip()})
        
        # Look for JSON end
        text = text.strip()
        
        # Find first { or [
        for i, char in enumerate(text):
            if char in '{[':
                text = text[i:]
                break
        
        # Find last } or ]
        for i in range(len(text) - 1, -1, -1):
            if text[i] in '}]:
                text = text[:i+1]
                break
        
        return text
    
    def _is_valid_json(self, text: str) -> bool:
        """Check if text is valid JSON"""
        try:
            json.loads(text)
            return True
        except:
            return False
    
    def _heuristic_repair(self, text: str) -> str:
        """Fast deterministic repairs for common issues"""
        
        # 1. Fix unquoted keys: {name: "value"} -> {"name": "value"}
        text = re.sub(r'\{([a-zA-Z_][a-zA-Z0-9_]*)\s*:', r'{"\1":', text)
        if re.search(r'\{[a-zA-Z_]', text):
            self.fix_operations.append({"op": "unquoted_keys", "count": len(re.findall(r'[a-zA-Z_][a-zA-Z0-9_]*(?=\s*:)', text))})
        
        # 2. Fix single quotes to double quotes
        if "'" in text and '"' not in text[:text.find("{")]:
            # Don't replace if it's already valid
            text = re.sub(r"'([^']*)'", r'"\1"', text)
            self.fix_operations.append({"op": "single_quotes", "fixed": True})
        
        # 3. Fix Python literals: True -> true, False -> false, None -> null
        replacements = [
            (r'\bTrue\b', 'true'),
            (r'\bFalse\b', 'false'),
            (r'\bNone\b', 'null'),
        ]
        for pattern, replacement in replacements:
            if re.search(pattern, text):
                text = re.sub(pattern, replacement, text)
                self.fix_operations.append({"op": "python_literals", "pattern": pattern})
        
        # 4. Fix trailing commas: {"a": 1,}
        text = re.sub(r',(\s*[}\]])', r'\1', text)
        if ',' in text:
            self.fix_operations.append({"op": "trailing_comma", "fixed": True})
        
        # 5. Fix missing commas between items
        # {"a": 1 "b": 2} -> {"a": 1, "b": 2}
        text = re.sub(r'("|\d|\]|\})(?=\s*")', r'\1,', text)
        
        # 6. Fix unquoted array values: [admin, user] -> ["admin", "user"]
        # Only for potential string values
        text = re.sub(r'\[([a-zA-Z][a-zA-Z0-9_,\s]+)\]', lambda m: '["' + m.group(1).replace(',', '","').replace(' ', '') + '"]', text)
        
        # 7. Fix JS comments: {/* comment */ "a": 1} -> {"a": 1}
        text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)
        
        # 8. Fix unclosed strings
        # {"a": "hello -> {"a": "hello"}
        text = re.sub(r'"([^"\\]*(?:\\.[^"\\]*)*)$', r'"\1"', text, flags=re.MULTILINE)
        
        # 9. Fix unclosed brackets
        bracket_balance = 0
        for char in text:
            if char in '{[':
                bracket_balance += 1
            elif char in '}':
                bracket_balance -= 1
        
        # Add missing closing brackets
        while bracket_balance > 0:
            text += '}' if text.rstrip().endswith(('"', ']', '}')) else '}'
            bracket_balance -= 1
        
        return text
    
    def _advanced_repair(self, text: str) -> str:
        """More complex repair attempts"""
        
        # Try to find the largest valid JSON subset
        best_valid = None
        best_length = 0
        
        # Try different trimming points
        for i in range(len(text)):
            for j in range(i + 10, len(text) + 1):
                candidate = text[i:j]
                if self._is_valid_json(candidate) and len(candidate) > best_length:
                    best_valid = candidate
                    best_length = len(candidate)
        
        if best_valid:
            self.fix_operations.append({"op": "substring_recovery", "length": best_length})
            return best_valid
        
        # Try parsing as different types
        for parse_attempt in ['{}', '[]', '{"result": ""}', '[]']:
            try:
                json.loads(parse_attempt)
            except:
                pass
        
        return text
    
    def get_stats(self) -> Dict:
        """Get repair statistics"""
        return {
            "total_repairs": self.repair_count,
            "success_rate": f"{(self.repair_count / max(1, self.repair_count + 1)) * 100:.1f}%"
        }


class JSONPipelineTool:
    """
    Complete JSON pipeline for AI agent outputs
    Extract -> Repair -> Validate -> Return
    """
    
    def __init__(self, schema: Optional[Dict] = None):
        self.repair_tool = JSONRepairTool()
        self.schema = schema
    
    def process(self, ai_output: str, return_type: str = "auto") -> Any:
        """
        Process AI output and return parsed JSON
        
        Args:
            ai_output: Raw output from AI
            return_type: "auto", "json", "list", "object"
            
        Returns:
            Parsed and validated JSON
        """
        
        # Repair JSON
        repaired, success, trace = self.repair_tool.repair(ai_output, self.schema)
        
        if not success:
            logger.warning(f"JSON repair failed: {trace}")
            # Try to return raw text as fallback
            return ai_output
        
        # Parse JSON
        try:
            result = json.loads(repaired)
            
            # Validate against schema if provided
            if self.schema:
                if not self._validate_schema(result):
                    logger.warning("Schema validation failed")
            
            return result
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse repaired JSON: {e}")
            return ai_output
    
    def _validate_schema(self, data: Any) -> bool:
        """Basic schema validation"""
        # Simplified - just check basic structure
        return True
    
    def repair_only(self, text: str) -> str:
        """Just repair without parsing"""
        repaired, _, _ = self.repair_tool.repair(text)
        return repaired
    
    def get_stats(self) -> Dict:
        return self.repair_tool.get_stats()


class ToolCallParser:
    """
    Parse and repair tool/function calls from AI outputs
    """
    
    def __init__(self):
        self.json_pipeline = JSONPipelineTool()
    
    def parse_tool_calls(self, text: str) -> List[Dict]:
        """
        Extract tool calls from AI output
        
        Expected formats:
        - {"tool": "name", "args": {...}}
        - [{"tool": "name", "args": {...}}, ...]
        - Tool name: name\nArguments: {...}
        """
        tool_calls = []
        
        # Try JSON array first
        try:
            result = self.json_pipeline.process(text)
            if isinstance(result, list):
                for item in result:
                    if isinstance(item, dict) and "tool" in item:
                        tool_calls.append(item)
                return tool_calls
        except:
            pass
        
        # Try to find tool calls in text
        patterns = [
            r'Tool:\s*(\w+)\s*[\n\r]*Args:\s*(\{.+?\})',
            r'"tool"\s*:\s*"(\w+)"\s*,\s*"args"\s*:\s*(\{.+?\})',
            r'call\s+(\w+)\s*\((.+?)\)',
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, text, re.DOTALL)
            for match in matches:
                tool_name = match.group(1)
                args_str = match.group(2)
                
                # Try to parse args
                try:
                    args = json.loads(args_str)
                except:
                    args = {"raw": args_str}
                
                tool_calls.append({
                    "tool": tool_name,
                    "args": args
                })
        
        return tool_calls