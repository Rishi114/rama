"""Memory System - Short-term and Long-term Memory
Inspired by Claude Code's memory architecture"""

import asyncio
import logging
from typing import List, Optional, Dict, Any
from datetime import datetime
from pathlib import Path
import json
import sqlite3

logger = logging.getLogger(__name__)


class MemorySystem:
    """
    Complete memory system with short-term and long-term storage
    """
    
    def __init__(self, db_path: str = "data/memory.db"):
        self.db_path = db_path
        self.short_term = ShortTermMemory()
        self.long_term = LongTermMemory(db_path)
    
    async def initialize(self):
        """Initialize memory system"""
        logger.info("🧠 Initializing Memory System...")
        await self.long_term.initialize()
        logger.info("✅ Memory System initialized!")
    
    async def store_interaction(self, user_input: str, assistant_response: str):
        """Store a conversation interaction"""
        # Short-term
        self.short_term.add_message("user", user_input)
        self.short_term.add_message("assistant", assistant_response)
        
        # Long-term
        await self.long_term.store_interaction(user_input, assistant_response)
    
    async def retrieve(self, query: str, top_k: int = 5) -> List[str]:
        """Retrieve relevant memories"""
        return await self.long_term.retrieve(query, top_k)
    
    def get_short_term_context(self) -> str:
        """Get current conversation context"""
        return self.short_term.get_context()
    
    async def get_stats(self) -> Dict[str, Any]:
        """Get memory statistics"""
        return await self.long_term.get_stats()


class ShortTermMemory:
    """
    Short-term memory for current conversation session
    """
    
    def __init__(self, max_messages: int = 20):
        self.max_messages = max_messages
        self.messages: List[Dict[str, str]] = []
    
    def add_message(self, role: str, content: str):
        """Add message to short-term memory"""
        self.messages.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
        
        # Trim if too long
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages:]
    
    def get_context(self) -> str:
        """Get formatted context string"""
        return "\n".join(
            f"{m['role'].upper()}: {m['content']}" 
            for m in self.messages
        )
    
    def clear(self):
        """Clear short-term memory"""
        self.messages.clear()
    
    def get_messages(self) -> List[Dict[str, str]]:
        """Get all messages"""
        return self.messages.copy()


class LongTermMemory:
    """
    Long-term memory with SQLite storage
    Supports vector search and fact extraction
    """
    
    def __init__(self, db_path: str = "data/memory.db"):
        self.db_path = db_path
        self.conn = None
    
    async def initialize(self):
        """Initialize SQLite database"""
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
        
        # Create index for search
        self.conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_facts_topic ON facts(topic)
        """)
        
        self.conn.commit()
        logger.info("✅ Long-term memory initialized")
    
    async def store_interaction(self, user_input: str, assistant_response: str):
        """Store conversation interaction"""
        timestamp = datetime.now().isoformat()
        
        self.conn.execute(
            "INSERT INTO interactions (user_input, assistant_response, timestamp) VALUES (?, ?, ?)",
            (user_input, assistant_response, timestamp)
        )
        
        # Extract facts (simple pattern matching)
        await self._extract_facts(user_input, assistant_response)
        
        self.conn.commit()
    
    async def _extract_facts(self, user_input: str, response: str):
        """Extract facts from conversation"""
        import re
        
        # Patterns for fact extraction
        patterns = [
            r"learn that (.+) is (.+)",
            r"remember (.+) is (.+)",
            r"my (.+) is (.+)",
            r"(.+) likes (.+)",
        ]
        
        for pattern in patterns:
            match = re.search(pattern, user_input.lower())
            if match:
                topic = match.group(1).strip()
                fact = match.group(2).strip()
                
                self.conn.execute(
                    "INSERT OR REPLACE INTO facts (topic, fact, timestamp) VALUES (?, ?, ?)",
                    (topic, fact, datetime.now().isoformat())
                )
    
    async def retrieve(self, query: str, top_k: int = 5) -> List[str]:
        """Retrieve relevant memories"""
        results = []
        
        # Search in facts
        cursor = self.conn.execute(
            "SELECT topic, fact FROM facts WHERE topic LIKE ? OR fact LIKE ? LIMIT ?",
            (f"%{query}%", f"%{query}%", top_k)
        )
        
        for row in cursor:
            results.append(f"{row['topic']}: {row['fact']}")
        
        # Search in knowledge
        cursor = self.conn.execute(
            "SELECT key, value FROM knowledge WHERE key LIKE ? OR value LIKE ? LIMIT ?",
            (f"%{query}%", f"%{query}%", top_k)
        )
        
        for row in cursor:
            results.append(f"{row['key']}: {row['value']}")
        
        return results
    
    async def store_knowledge(self, key: str, value: str):
        """Store a knowledge fact"""
        self.conn.execute(
            "INSERT OR REPLACE INTO knowledge (key, value, timestamp) VALUES (?, ?, ?)",
            (key, value, datetime.now().isoformat())
        )
        self.conn.commit()
    
    async def get_knowledge(self, key: str) -> Optional[str]:
        """Get knowledge by key"""
        cursor = self.conn.execute(
            "SELECT value FROM knowledge WHERE key = ?",
            (key,)
        )
        row = cursor.fetchone()
        return row['value'] if row else None
    
    async def get_stats(self) -> Dict[str, Any]:
        """Get memory statistics"""
        interactions = self.conn.execute(
            "SELECT COUNT(*) FROM interactions"
        ).fetchone()[0]
        
        facts = self.conn.execute(
            "SELECT COUNT(*) FROM facts"
        ).fetchone()[0]
        
        knowledge = self.conn.execute(
            "SELECT COUNT(*) FROM knowledge"
        ).fetchone()[0]
        
        return {
            "interactions": interactions,
            "facts": facts,
            "knowledge": knowledge
        }
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()


class VectorMemory:
    """
    Vector-based memory using FAISS for semantic search
    (Optional enhancement for future)
    """
    
    def __init__(self, dimension: int = 384):
        self.dimension = dimension
        self.index = None
        self.texts = []
    
    def initialize(self):
        """Initialize FAISS index"""
        try:
            import faiss
            self.index = faiss.IndexFlatL2(self.dimension)
            logger.info("✅ Vector memory initialized")
        except Exception as e:
            logger.warning(f"Vector memory init failed: {e}")
    
    def add_text(self, text: str, embedding: List[float]):
        """Add text with embedding"""
        if self.index is None:
            return
        
        import numpy as np
        
        # Normalize embedding
        vec = np.array([embedding]).astype('float32')
        faiss.normalize_L2(vec)
        
        self.index.add(vec)
        self.texts.append(text)
    
    def search(self, query_embedding: List[float], top_k: int = 5) -> List[str]:
        """Search similar texts"""
        if self.index is None:
            return []
        
        import numpy as np
        
        vec = np.array([query_embedding]).astype('float32')
        faiss.normalize_L2(vec)
        
        distances, indices = self.index.search(vec, top_k)
        
        return [self.texts[i] for i in indices[0] if i < len(self.texts)]