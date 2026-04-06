"""Skill Base - Base class for all skills
Inspired by Vercel Skills architecture"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)


class Skill(ABC):
    """
    Base class for all skills
    Skills are modular, reusable components that handle specific tasks
    """
    
    def __init__(self):
        self.name = self.__class__.__name__.replace('Skill', '')
        self.description = self.__doc__ or "A custom skill"
        self.triggers: List[str] = []
        self.version = "1.0.0"
    
    @abstractmethod
    async def execute(self, input_text: str, context: Any, retrieved_context: str = "") -> str:
        """
        Execute the skill
        Args:
            input_text: User input
            context: Conversation context
            retrieved_context: Retrieved memory/context
        Returns:
            Response string
        """
        pass
    
    def can_handle(self, input_text: str) -> bool:
        """Check if this skill can handle the input"""
        input_lower = input_text.lower()
        
        for trigger in self.triggers:
            if trigger.lower() in input_lower:
                return True
        
        return False
    
    def get_info(self) -> Dict[str, Any]:
        """Get skill information"""
        return {
            "name": self.name,
            "description": self.description,
            "triggers": self.triggers,
            "version": self.version
        }
    
    async def learn(self, input_text: str, response: str):
        """Learn from interaction (optional)"""
        pass


class SkillRegistry:
    """
    Registry for managing skills
    Inspired by Vercel Skills plugin system
    """
    
    def __init__(self):
        self.skills: Dict[str, Skill] = {}
    
    def register(self, skill: Skill):
        """Register a skill"""
        self.skills[skill.name] = skill
        logger.info(f"✅ Registered skill: {skill.name}")
    
    def unregister(self, name: str):
        """Unregister a skill"""
        if name in self.skills:
            del self.skills[name]
            logger.info(f"🗑️ Unregistered skill: {name}")
    
    def get(self, name: str) -> Optional[Skill]:
        """Get a skill by name"""
        return self.skills.get(name)
    
    def list_skills(self) -> List[str]:
        """List all registered skills"""
        return list(self.skills.keys())
    
    def find_best(self, input_text: str) -> Optional[Skill]:
        """Find the best matching skill"""
        best_skill = None
        best_score = 0
        
        for name, skill in self.skills.items():
            score = self._calculate_score(skill, input_text)
            
            if score > best_score:
                best_score = score
                best_skill = skill
        
        return best_skill if best_score > 5 else None
    
    def _calculate_score(self, skill: Skill, input_text: str) -> int:
        """Calculate match score for a skill"""
        score = 0
        
        for trigger in skill.triggers:
            if trigger.lower() in input_text.lower():
                score += 10
        
        if skill.can_handle(input_text):
            score += 5
        
        return score