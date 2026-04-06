"""Context Engine - Learning from Experience
Based on agentic-context-engine for agent memory and learning"""

import asyncio
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
import json
from pathlib import Path

logger = logging.getLogger(__name__)


class ContextEngine:
    """
    Context engine for AI agents - learns from experience
    Based on agentic-context-engine architecture
    """
    
    def __init__(self, storage_path: str = "data/context"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        # Context management
        self.current_context = {}
        self.context_history = []
        self.max_history = 100
        
        # Learning components
        self.patterns = {}
        self.learned_actions = {}
        self.success_metrics = {}
        
    async def add_to_context(self, key: str, value: Any):
        """Add information to current context"""
        self.current_context[key] = {
            "value": value,
            "timestamp": datetime.now().isoformat()
        }
        
        # Save to history
        self.context_history.append({
            "key": key,
            "value": str(value)[:100],  # Truncate for storage
            "timestamp": datetime.now().isoformat()
        })
        
        if len(self.context_history) > self.max_history:
            self.context_history = self.context_history[-self.max_history:]
    
    async def get_context(self, key: str = None) -> Any:
        """Get context by key or all current context"""
        if key:
            return self.current_context.get(key, {}).get("value")
        return self.current_context
    
    async def learn_from_interaction(self, action: str, result: str, success: bool):
        """Learn from an interaction - record what worked/didn't work"""
        
        # Store action-result pattern
        if action not in self.learned_actions:
            self.learned_actions[action] = {"success": 0, "failure": 0}
        
        if success:
            self.learned_actions[action]["success"] += 1
        else:
            self.learned_actions[action]["failure"] += 1
        
        # Save to storage
        self._save_learning()
        
        logger.info(f"🧠 Learned: {action} -> {'success' if success else 'failure'}")
    
    def _save_learning(self):
        """Save learned patterns to disk"""
        learning_file = self.storage_path / "learning.json"
        data = {
            "learned_actions": self.learned_actions,
            "patterns": self.patterns,
            "context_history": self.context_history[-20:]
        }
        learning_file.write_text(json.dumps(data, indent=2))
    
    def _load_learning(self):
        """Load learned patterns from disk"""
        learning_file = self.storage_path / "learning.json"
        if learning_file.exists():
            try:
                data = json.loads(learning_file.read_text())
                self.learned_actions = data.get("learned_actions", {})
                self.patterns = data.get("patterns", {})
            except:
                pass
    
    async def get_successful_actions(self, context: str) -> List[str]:
        """Get list of actions that worked in similar context"""
        self._load_learning()
        
        # Find relevant patterns
        similar = []
        for action, stats in self.learned_actions.items():
            total = stats.get("success", 0) + stats.get("failure", 0)
            success_rate = stats.get("success", 0) / max(1, total)
            
            if success_rate > 0.7:  # Only return actions with 70%+ success
                similar.append((action, success_rate))
        
        # Sort by success rate
        similar.sort(key=lambda x: x[1], reverse=True)
        
        return [action for action, _ in similar[:5]]
    
    def get_stats(self) -> Dict:
        """Get learning statistics"""
        total_actions = sum(
            s.get("success", 0) + s.get("failure", 0) 
            for s in self.learned_actions.values()
        )
        successful = sum(s.get("success", 0) for s in self.learned_actions.values())
        
        return {
            "total_interactions": total_actions,
            "successful": successful,
            "success_rate": f"{(successful / max(1, total_actions)) * 100:.1f}%",
            "patterns_learned": len(self.learned_actions)
        }


class ContextPipeline:
    """
    Pipeline for context processing
    Based on agentic-context-engine pipeline architecture
    """
    
    def __init__(self):
        self.steps = []
        self.current_step = 0
    
    def add_step(self, name: str, processor):
        """Add a processing step to pipeline"""
        self.steps.append({"name": name, "processor": processor})
    
    async def execute(self, input_data: Any) -> Any:
        """Execute pipeline on input"""
        data = input_data
        
        for step in self.steps:
            logger.info(f"➡️ Pipeline step: {step['name']}")
            data = await step["processor"](data)
        
        return data


class DeduplicationTool:
    """
    Deduplicate similar contexts and learnings
    """
    
    def __init__(self):
        self.seen = set()
    
    def is_duplicate(self, content: str) -> bool:
        """Check if content is duplicate"""
        # Simple hash-based deduplication
        content_hash = str(content).lower().strip()[:50]
        
        if content_hash in self.seen:
            return True
        
        self.seen.add(content_hash)
        return False
    
    def clear(self):
        """Clear deduplication cache"""
        self.seen.clear()


class BranchManager:
    """
    Context branching - try different approaches
    Based on agentic-context-engine branching
    """
    
    def __init__(self):
        self.branches = {}
        self.active_branch = "main"
    
    async def create_branch(self, name: str, context: Dict) -> str:
        """Create a new context branch"""
        self.branches[name] = {
            "context": context.copy(),
            "created_at": datetime.now().isoformat()
        }
        logger.info(f"🌿 Created branch: {name}")
        return name
    
    async def switch_branch(self, name: str) -> Dict:
        """Switch to a different branch"""
        if name in self.branches:
            self.active_branch = name
            return self.branches[name]["context"]
        return {}
    
    async def merge_branch(self, source: str, target: str = "main") -> str:
        """Merge branch back to main"""
        if source in self.branches:
            # Simple merge - update target with source values
            for key, value in self.branches[source]["context"].items():
                self.branches[target]["context"][key] = value
            
            del self.branches[source]
            logger.info(f"🔀 Merged {source} into {target}")
            return f"Merged {source} into {target}"
        
        return f"Branch {source} not found"


class ExperienceLearner:
    """
    Learn from experience - pattern recognition and improvement
    """
    
    def __init__(self):
        self.experiences = []
        self.improvements = []
    
    async def record_experience(self, situation: str, action: str, outcome: str):
        """Record an experience"""
        experience = {
            "situation": situation,
            "action": action,
            "outcome": outcome,
            "timestamp": datetime.now().isoformat()
        }
        self.experiences.append(experience)
        
        # Analyze for improvements
        if outcome in ["success", "good", "worked"]:
            self.improvements.append({
                "from_situation": situation,
                "action": action,
                "success_count": 1
            })
    
    async def suggest_action(self, situation: str) -> str:
        """Suggest action based on past experiences"""
        # Find similar situations
        similar = [e for e in self.experiences if situation.lower() in e["situation"].lower()]
        
        if not similar:
            return "No similar experiences found. I'll try a general approach."
        
        # Find most successful action
        actions = {}
        for exp in similar:
            action = exp["action"]
            if action not in actions:
                actions[action] = {"success": 0, "total": 0}
            
            actions[action]["total"] += 1
            if exp["outcome"] in ["success", "good", "worked"]:
                actions[action]["success"] += 1
        
        # Find best action
        best_action = max(actions.items(), key=lambda x: x[1]["success"] / max(1, x[1]["total"]))
        
        return f"Based on past experiences, try: {best_action[0]}"