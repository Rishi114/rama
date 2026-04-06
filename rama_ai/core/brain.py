"""RAMA AI v2.0 - Core Brain Module
Simplified version - graceful fallback on import errors"""

import asyncio
from typing import Optional, Dict, Any
from datetime import datetime


class Brain:
    """Main AI Brain - simplified version"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.context = ContextManager()
        self.skill_manager = None
        self.ollama_client = None
        self.memory = None
        
    async def initialize(self):
        """Initialize brain components with graceful fallbacks"""
        print("🧠 Initializing RAMA Brain...")
        
        # Initialize skill manager
        try:
            from core.brain import SkillManager as OriginalSkillManager
            self.skill_manager = OriginalSkillManager()
            await self.skill_manager.load_skills()
            print(f"✅ Loaded {len(self.skill_manager.skills)} skills")
        except Exception as e:
            print(f"⚠️ Skill manager: {e}")
            self.skill_manager = SimpleSkillManager()
        
        # Try to initialize Ollama client
        try:
            from core.ollama_client import OllamaClient
            self.ollama_client = OllamaClient(
                model=self.config.get("llm_model", "llama3.2:1b")
            )
            print("✅ Ollama client ready")
        except Exception as e:
            print(f"⚠️ Ollama: {e}")
        
        print("✅ Brain initialized!")
    
    async def process(self, user_input: str, context: Optional[Dict] = None) -> str:
        """Process user input"""
        self.context.add_message("user", user_input)
        
        # Try skill first
        if self.skill_manager:
            skill = self.skill_manager.find_best_skill(user_input)
            if skill:
                try:
                    response = await skill.execute(user_input, self.context, "")
                    self.context.add_message("assistant", response)
                    return response
                except Exception as e:
                    print(f"Skill error: {e}")
        
        # Default response
        return "I'm RAMA! Say 'help' for commands or 'list skills' to see what I can do!"


class SimpleSkillManager:
    """Fallback skill manager"""
    
    def __init__(self):
        self.skills = {}
    
    def find_best_skill(self, input_text: str):
        return None


class ContextManager:
    """Simple context manager"""
    
    def __init__(self):
        self.messages = []
    
    def add_message(self, role: str, content: str):
        self.messages.append({"role": role, "content": content, "timestamp": datetime.now().isoformat()})
        if len(self.messages) > 20:
            self.messages = self.messages[-20:]


# Keep original SkillManager for full functionality
class SkillManager:
    """Manages all skills - full version"""
    
    def __init__(self):
        self.skills: Dict[str, Any] = {}
    
    async def load_skills(self):
        """Load all available skills"""
        # Import and load all skills
        skill_classes = []
        
        try:
            from skills.greeting import GreetingSkill
            skill_classes.append(GreetingSkill)
        except: pass
        
        try:
            from skills.calculator import CalculatorSkill
            skill_classes.append(CalculatorSkill)
        except: pass
        
        try:
            from skills.system import AppLauncherSkill, FileManagerSkill, SystemInfoSkill
            skill_classes.extend([AppLauncherSkill, FileManagerSkill, SystemInfoSkill])
        except: pass
        
        try:
            from skills.utilities import WeatherSkill, WebSearchSkill, NoteSkill
            skill_classes.extend([WeatherSkill, WebSearchSkill, NoteSkill])
        except: pass
        
        try:
            from skills.coding import CodingSkill, AutomationSkill
            skill_classes.extend([CodingSkill, AutomationSkill])
        except: pass
        
        try:
            from skills.self_learning import SelfLearningSkill, UniversalCodeSkill
            skill_classes.extend([SelfLearningSkill, UniversalCodeSkill])
        except: pass
        
        try:
            from skills.debugging import DebuggingSkill
            skill_classes.append(DebuggingSkill)
        except: pass
        
        # Instantiate all skills
        for skill_class in skill_classes:
            try:
                skill = skill_class()
                self.skills[skill.name] = skill
            except Exception as e:
                print(f"Failed to load {skill_class}: {e}")
        
        print(f"✅ Loaded {len(self.skills)} skills")
    
    def find_best_skill(self, input_text: str):
        """Find best matching skill"""
        input_lower = input_text.lower()
        best_skill = None
        best_score = 0
        
        for name, skill in self.skills.items():
            score = 0
            if hasattr(skill, 'triggers'):
                for trigger in skill.triggers:
                    if trigger.lower() in input_lower:
                        score += 10
            
            if hasattr(skill, 'can_handle'):
                try:
                    if skill.can_handle(input_text):
                        score += 5
                except: pass
            
            if score > best_score:
                best_score = score
                best_skill = skill
        
        return best_skill if best_score > 0 else None


# For backwards compatibility - import original modules
def __getattr__(name):
    """Lazy load modules"""
    if name == "LongTermMemory":
        try:
            from memory.long_term import LongTermMemory
            return LongTermMemory
        except:
            return type("LongTermMemory", (), {"__init__": lambda self, *args, **kwargs: None, "initialize": lambda self: None})
    elif name == "RAGEngine":
        try:
            from core.rag_engine import RAGEngine
            return RAGEngine
        except:
            return type("RAGEngine", (), {"__init__": lambda self, *args, **kwargs: None, "initialize": lambda self: None, "retrieve": lambda self, *args, **kwargs: []})
    elif name == "OllamaClient":
        try:
            from core.ollama_client import OllamaClient
            return OllamaClient
        except:
            return type("OllamaClient", (), {"__init__": lambda self, *args, **kwargs: None, "is_connected": False, "generate": lambda self, *args, **kwargs: ""})
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")