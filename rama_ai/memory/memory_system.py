"""Memory System - Short-term and Long-term Memory
Supports both SQLite (full) and JSON (lightweight)"""

import asyncio
import os
from typing import List, Dict, Any
from datetime import datetime
from pathlib import Path
import json
import logging

logger = logging.getLogger(__name__)


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
    
    def get_messages(self) -> List[Dict]:
        return self.messages.copy()
    
    def clear(self):
        self.messages.clear()


class LongTermMemory:
    """
    Long-term memory with dual storage support
    - SQLite (full features, recommended)
    - JSON (lightweight, no dependencies)
    """
    
    def __init__(self, db_path: str = "data/memory.db", storage: str = "auto"):
        self.db_path = db_path
        self.storage = storage
        self.use_sqlite = False
        
        # Check what storage to use
        if storage == "auto":
            # Try SQLite first, fall back to JSON
            self.use_sqlite = self._check_sqlite()
        elif storage == "sqlite":
            self.use_sqlite = True
        else:
            self.use_sqlite = False
        
        # Initialize storage
        if self.use_sqlite:
            self._init_sqlite()
        else:
            self._init_json()
    
    def _check_sqlite(self) -> bool:
        """Check if SQLite is available"""
        try:
            import sqlite3
            return True
        except ImportError:
            logger.warning("SQLite not available, using JSON")
            return False
    
    def _init_sqlite(self):
        """Initialize SQLite database"""
        try:
            import sqlite3
            
            Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
            
            # Create tables
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS interactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_input TEXT NOT NULL,
                    assistant_response TEXT NOT NULL,
                    timestamp TEXT NOT NULL
                )
            """)
            
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS facts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    topic TEXT NOT NULL,
                    fact TEXT NOT NULL,
                    confidence REAL DEFAULT 1.0,
                    timestamp TEXT NOT NULL
                )
            """)
            
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS knowledge (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    key TEXT NOT NULL UNIQUE,
                    value TEXT NOT NULL,
                    timestamp TEXT NOT NULL
                )
            """)
            
            self.conn.commit()
            logger.info("✅ SQLite memory initialized")
        except Exception as e:
            logger.warning(f"SQLite init failed: {e}, using JSON")
            self.use_sqlite = False
            self._init_json()
    
    def _init_json(self):
        """Initialize JSON storage"""
        self.json_path = Path(self.db_path.replace(".db", ".json"))
        self.json_path.parent.mkdir(parents=True, exist_ok=True)
        
        self.data = {
            "interactions": [],
            "facts": {},
            "knowledge": {}
        }
        self._load_json()
        logger.info("✅ JSON memory initialized")
    
    def _load_json(self):
        """Load from JSON file"""
        try:
            if self.json_path.exists():
                self.data = json.loads(self.json_path.read_text())
        except:
            self.data = {"interactions": [], "facts": {}, "knowledge": {}}
    
    def _save_json(self):
        """Save to JSON file"""
        try:
            self.json_path.write_text(json.dumps(self.data, indent=2))
        except:
            pass
    
    async def initialize(self):
        """Initialize - no-op, done in __init__"""
        pass
    
    async def store_interaction(self, user_input: str, assistant_response: str):
        """Store conversation interaction"""
        timestamp = datetime.now().isoformat()
        
        if self.use_sqlite:
            self.conn.execute(
                "INSERT INTO interactions (user_input, assistant_response, timestamp) VALUES (?, ?, ?)",
                (user_input, assistant_response, timestamp)
            )
            self.conn.commit()
        else:
            self.data["interactions"].append({
                "user": user_input[:200],
                "assistant": assistant_response[:200],
                "timestamp": timestamp
            })
            # Keep last 1000
            if len(self.data["interactions"]) > 1000:
                self.data["interactions"] = self.data["interactions"][-1000:]
            self._save_json()
    
    async def store_knowledge(self, key: str, value: str):
        """Store knowledge fact"""
        timestamp = datetime.now().isoformat()
        
        if self.use_sqlite:
            self.conn.execute(
                "INSERT OR REPLACE INTO knowledge (key, value, timestamp) VALUES (?, ?, ?)",
                (key, value, timestamp)
            )
            self.conn.commit()
        else:
            self.data["knowledge"][key] = {"value": value, "timestamp": timestamp}
            self._save_json()
    
    async def get_knowledge(self, key: str) -> str:
        """Get knowledge by key"""
        if self.use_sqlite:
            cursor = self.conn.execute("SELECT value FROM knowledge WHERE key = ?", (key,))
            row = cursor.fetchone()
            return row['value'] if row else None
        else:
            return self.data["knowledge"].get(key, {}).get("value")
    
    async def retrieve(self, query: str, top_k: int = 5) -> List[str]:
        """Retrieve relevant memories"""
        results = []
        
        if self.use_sqlite:
            cursor = self.conn.execute(
                "SELECT user_input, assistant_response FROM interactions WHERE user_input LIKE ? LIMIT ?",
                (f"%{query}%", top_k)
            )
            for row in cursor:
                results.append(row['assistant_response'])
        else:
            for item in self.data["interactions"][-100:]:
                if query.lower() in item.get("user", "").lower():
                    results.append(item.get("assistant", ""))
        
        return results[:top_k]
    
    async def get_stats(self) -> Dict[str, Any]:
        """Get memory statistics"""
        if self.use_sqlite:
            interactions = self.conn.execute("SELECT COUNT(*) FROM interactions").fetchone()[0]
            facts = self.conn.execute("SELECT COUNT(*) FROM facts").fetchone()[0]
            knowledge = self.conn.execute("SELECT COUNT(*) FROM knowledge").fetchone()[0]
        else:
            interactions = len(self.data.get("interactions", []))
            facts = len(self.data.get("facts", {}))
            knowledge = len(self.data.get("knowledge", {}))
        
        return {
            "storage": "sqlite" if self.use_sqlite else "json",
            "interactions": interactions,
            "facts": facts,
            "knowledge": knowledge
        }
    
    def close(self):
        """Close connection"""
        if self.use_sqlite and hasattr(self, 'conn'):
            self.conn.close()


class MemorySystem:
    """Complete memory system"""
    
    def __init__(self, db_path: str = "data/memory.db", storage: str = "auto"):
        self.short_term = ShortTermMemory()
        self.long_term = LongTermMemory(db_path, storage)
    
    async def initialize(self):
        """Initialize"""
        await self.long_term.initialize()
    
    async def store_interaction(self, user_input: str, assistant_response: str):
        """Store interaction in both memories"""
        self.short_term.add_message("user", user_input)
        self.short_term.add_message("assistant", assistant_response)
        await self.long_term.store_interaction(user_input, assistant_response)
    
    async def retrieve(self, query: str, top_k: int = 5) -> List[str]:
        """Retrieve from long-term memory"""
        return await self.long_term.retrieve(query, top_k)
    
    def get_short_term_context(self) -> str:
        """Get current conversation context"""
        return self.short_term.get_context()
    
    async def get_stats(self) -> Dict[str, Any]:
        """Get memory statistics"""
        stats = await self.long_term.get_stats()
        stats["short_term_messages"] = len(self.short_term.messages)
        return stats