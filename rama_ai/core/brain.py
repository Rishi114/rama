"""RAMA AI v2.0 - Core Brain Module
AI processing, context management, and skill orchestration"""

import asyncio
from typing import Optional, List, Dict, Any
from datetime import datetime
import json
import logging

logger = logging.getLogger(__name__)


class Brain:
    """
    Main AI Brain - orchestrates all AI processing
    Inspired by Claude Code's multi-agent architecture
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.context = ContextManager()
        self.rag_engine = None  # RAGEngine()
        self.skill_manager = SkillManager()
        self.ollama_client = None  # OllamaClient()
        self.memory = None  # MemorySystem()
        
    async def initialize(self):
        """Initialize all brain components"""
        logger.info("🧠 Initializing RAMA Brain...")
        
        # Initialize memory
        from memory.long_term import LongTermMemory
        self.memory = LongTermMemory()
        
        # Initialize RAG
        from core.rag_engine import RAGEngine
        self.rag_engine = RAGEngine()
        
        # Initialize Ollama
        from core.ollama_client import OllamaClient
        self.ollama_client = OllamaClient(
            model=self.config.get("llm_model", "llama3.2:1b"),
            host=self.config.get("ollama_host", "http://localhost:11434")
        )
        
        # Initialize skills
        await self.skill_manager.load_skills()
        
        logger.info("✅ Brain initialized!")
    
    async def process(self, user_input: str, context: Optional[Dict] = None) -> str:
        """
        Process user input and generate response
        Main entry point for AI processing
        """
        logger.info(f"🧠 Processing: {user_input[:50]}...")
        
        # Add to short-term memory
        self.context.add_message("user", user_input)
        
        # Retrieve relevant context from long-term memory
        retrieved_context = await self._retrieve_context(user_input)
        
        # Check for skill match
        skill = self.skill_manager.find_best_skill(user_input)
        if skill:
            response = await skill.execute(user_input, self.context, retrieved_context)
            await self._learn(user_input, response)
            return response
        
        # Use LLM for general responses
        if self.ollama_client.is_connected:
            prompt = self._build_prompt(user_input, retrieved_context)
            response = await self.ollama_client.generate(prompt)
            await self._learn(user_input, response)
            return response
        
        # Fallback response
        return "I'm ready! Try asking me to do something, or say 'help' to see what I can do."
    
    async def _retrieve_context(self, query: str) -> str:
        """Retrieve relevant context from memory"""
        try:
            if self.rag_engine:
                results = await self.rag_engine.retrieve(query, top_k=3)
                return "\n".join(results)
        except Exception as e:
            logger.warning(f"Context retrieval failed: {e}")
        return ""
    
    async def _learn(self, user_input: str, response: str):
        """Learn from interaction"""
        try:
            if self.memory:
                await self.memory.store_interaction(user_input, response)
        except Exception as e:
            logger.warning(f"Learning failed: {e}")
    
    def _build_prompt(self, user_input: str, context: str) -> str:
        """Build prompt with context"""
        system_prompt = """You are RAMA, a helpful AI assistant with a sassy personality.
Be helpful, witty, and concise. Use context if provided."""
        
        prompt = f"{system_prompt}\n\n"
        if context:
            prompt += f"Context:\n{context}\n\n"
        prompt += f"User: {user_input}\n\nRama:"
        
        return prompt
    
    async def stop(self):
        """Cleanup resources"""
        logger.info("🧠 Brain stopping...")
        if self.ollama_client:
            await self.ollama_client.close()


class ContextManager:
    """
    Manages short-term conversation context
    """
    
    def __init__(self, max_messages: int = 20):
        self.max_messages = max_messages
        self.messages: List[Dict[str, str]] = []
        self.metadata: Dict[str, Any] = {}
    
    def add_message(self, role: str, content: str):
        """Add message to context"""
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
            f"{m['role']}: {m['content']}" 
            for m in self.messages[-10:]
        )
    
    def clear(self):
        """Clear context"""
        self.messages.clear()


class SkillManager:
    """
    Manages skills/plugins - inspired by Vercel Skills architecture
    """
    
    def __init__(self):
        self.skills: Dict[str, Any] = {}
    
    async def load_skills(self):
        """Load all available skills"""
        from skills.greeting import GreetingSkill
        from skills.calculator import CalculatorSkill
        from skills.system import AppLauncherSkill, FileManagerSkill, SystemInfoSkill
        from skills.utilities import WeatherSkill, WebSearchSkill, NoteSkill, ReminderSkill, KnowledgeSkill
        from skills.coding import CodingSkill, AutomationSkill, LocalAISkill
        from skills.advanced_tools import (
            ToolsSkill, WebSearchSkill as AdvancedWebSearchSkill,
            CriticalThinkingSkill, CodeAnalysisSkill, SystemInfoSkill as GodModeSystemInfo,
            AutomationSkill as AdvancedAutomation, MemorySkill
        )
        
        skills = [
            # Core skills
            GreetingSkill(),
            CalculatorSkill(),
            AppLauncherSkill(),
            FileManagerSkill(),
            SystemInfoSkill(),
            WeatherSkill(),
            WebSearchSkill(),
            NoteSkill(),
            ReminderSkill(),
            KnowledgeSkill(),
            CodingSkill(),
            AutomationSkill(),
            LocalAISkill(),
            # Advanced tools
            ToolsSkill(),
            AdvancedWebSearchSkill(),
            CriticalThinkingSkill(),
            CodeAnalysisSkill(),
            GodModeSystemInfo(),
            AdvancedAutomation(),
            MemorySkill(),
        ]
        
        for skill in skills:
            self.skills[skill.name] = skill
        
        logger.info(f"✅ Loaded {len(self.skills)} skills")
    
    def find_best_skill(self, input_text: str) -> Optional[Any]:
        """Find best matching skill"""
        input_lower = input_text.lower()
        
        best_skill = None
        best_score = 0
        
        for name, skill in self.skills.items():
            score = 0
            
            # Check triggers
            for trigger in skill.triggers:
                if trigger.lower() in input_lower:
                    score += 10
            
            # Check can_handle
            if hasattr(skill, 'can_handle') and skill.can_handle(input_text):
                score += 5
            
            if score > best_score:
                best_score = score
                best_skill = skill
        
        return best_skill if best_score > 0 else None
    
    def register_skill(self, skill):
        """Dynamically register a new skill"""
        self.skills[skill.name] = skill
        logger.info(f"✅ Registered skill: {skill.name}")
    
    def list_skills(self) -> List[str]:
        """List all available skills"""
        return list(self.skills.keys())