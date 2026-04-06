"""Memory System - Short-term and Long-term Memory
Simplified version - works without sqlite"""

import asyncio
import os
from typing import Dict, Any
from datetime import datetime
from pathlib import Path


class ShortTermMemory:
    """Short-term memory for current conversation"""
    
    def __init__(self, max_messages: int = 20):
        self.max_messages = max_messages
        self.messages = []
    
    def add_message(self, role: str, content: str):
        self.messages.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages:]
    
    def get_context(self) -> str:
        return "\n".join(f"{m['role']}: {m['content']}" for m in self.messages[-10:])
    
    def clear(self):
        self.messages.clear()


class LongTermMemory:
    """Long-term memory - simplified version"""
    
    def __init__(self, db_path: str = "data/memory.db"):
        self.db_path = db_path
        self.data = {}
        self._load()
    
    def _load(self):
        """Load from file if exists"""
        try:
            path = Path(self.db_path.replace(".db", ".json"))
            if path.exists():
                import json
                self.data = json.loads(path.read_text())
        except:
            self.data = {}
    
    def _save(self):
        """Save to file"""
        try:
            path = Path(self.db_path.replace(".db", ".json"))
            path.parent.mkdir(parents=True, exist_ok=True)
            import json
            path.write_text(json.dumps(self.data))
        except:
            pass
    
    async def initialize(self):
        """Initialize"""
        pass
    
    async def store_interaction(self, user_input: str, assistant_response: str):
        """Store conversation"""
        self.data[datetime.now().isoformat()] = {
            "user": user_input[:100],
            "assistant": assistant_response[:100]
        }
        # Keep only last 100
        if len(self.data) > 100:
            keys = list(self.data.keys())[:-100]
            for k in keys:
                del self.data[k]
        self._save()
    
    async def retrieve(self, query: str, top_k: int = 5) -> list:
        """Simple keyword search"""
        results = []
        for key, val in self.data.items():
            if query.lower() in val.get("user", "").lower():
                results.append(val.get("assistant", ""))
        return results[:top_k]
    
    async def get_stats(self) -> Dict:
        return {"interactions": len(self.data)}


class MemorySystem:
    """Complete memory system"""
    
    def __init__(self, db_path: str = "data/memory.db"):
        self.short_term = ShortTermMemory()
        self.long_term = LongTermMemory(db_path)
    
    async def initialize(self):
        """Initialize"""
        await self.long_term.initialize()
    
    async def store_interaction(self, user_input: str, assistant_response: str):
        """Store interaction"""
        self.short_term.add_message("user", user_input)
        self.short_term.add_message("assistant", assistant_response)
        await self.long_term.store_interaction(user_input, assistant_response)
    
    async def retrieve(self, query: str, top_k: int = 5) -> list:
        """Retrieve"""
        return await self.long_term.retrieve(query, top_k)
    
    def get_short_term_context(self) -> str:
        return self.short_term.get_context()
    
    async def get_stats(self) -> Dict:
        stats = await self.long_term.get_stats()
        return {"interactions": stats["interactions"]}