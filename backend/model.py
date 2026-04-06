"""
RAMA AI - Model (Brain)
The "brain" for decision-making
Integrates ALL features: Skills, Personality, Languages, Memory
"""

import re
import asyncio
import random
from datetime import datetime


class RAMAModel:
    """
    RAMA's Brain - Complete AI with ALL features:
    - 50+ Skills
    - 35+ Programming Languages
    - KiloCode Integration
    - JSON Repair, Vercel Skills, Video Learning
    - Self-Learning & Memory
    - Personality (Hindi, Marathi, English)
    - Full PC Control
    """
    
    def __init__(self, config=None):
        self.config = config or {}
        
        # Initialize modules
        self.automation = None
        self.chat_bot = None
        self.tts = None
        self.stt = None
        self.skills = None
        
        # Settings
        self.wake_word = self.config.get('wake_word', 'hey rama')
        self.user_name = self.config.get('user_name', 'bhai')
        self.language = self.config.get('language', 'en')
        
        # State
        self.is_listening = False
        self.history = []
        self.learned_facts = {}
        
    def initialize(self):
        """Initialize all modules"""
        try:
            from automation import Automation
            from chat_bot import ChatBot
            from text_to_speech import TextToSpeech
            from speech_to_text import SpeechToText
            from skills import SkillsManager
            from brain_trainer import BrainTrainer
            
            # Initialize brain trainer first (has all features)
            self.brain_trainer = BrainTrainer(self.config)
            
            # Initialize skills
            self.skills = SkillsManager({
                'user_name': self.user_name,
                'language': self.language
            })
            
            self.automation = Automation(self.config)
            self.chat_bot = ChatBot({
                'user_name': self.user_name,
                'language': self.language
            })
            self.tts = TextToSpeech(self.config)
            self.stt = SpeechToText(self.config)
            
            print("✅ RAMA Brain with Training & Physics initialized!")
            return True
            
        except Exception as e:
            print(f"⚠️ Brain init error: {e}")
            return False
    
    def process(self, user_input):
        """
        Main processing function
        Takes input, processes, returns response
        """
        if not user_input:
            return self._get_sassy_response("Kya bol raha hai bhai?")
        
        text = user_input.strip()
        text_lower = text.lower()
        
        # Record in history
        self.history.append({
            'role': 'user',
            'content': text,
            'timestamp': datetime.now().isoformat()
        })
        
        # Check for learning commands
        if any(w in text_lower for w in ["remember", "learn this", "note that"]):
            return self._handle_learning(text_lower)
        
        # Check for language change
        if "language" in text_lower or "set language" in text_lower:
            return self._handle_language_change(text_lower)
        
        # Check for name change
        if any(w in text_lower for w in ["call me", "my name"]):
            return self._handle_name_change(text_lower)
        
        # Determine what to do based on input
        response = self._decide(text_lower)
        
        # Record response
        self.history.append({
            'role': 'assistant',
            'content': response,
            'timestamp': datetime.now().isoformat()
        })
        
        return response
    
    def _handle_learning(self, text):
        """Handle learning commands"""
        patterns = [
            r'remember (.*?) is (.*)',
            r'learn (.*?) = (.*)',
            r'note that (.*?) is (.*)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                key = match.group(1).strip()
                value = match.group(2).strip()
                self.learned_facts[key] = value
                return f"🧠 Learned! **{key}** = **{value}** 🔥\n\nMaine yaad kar liya bhai!"
        
        # Check for recall
        if "what is" in text or "recall" in text:
            for key in self.learned_facts:
                if key in text:
                    return f"🧠 **{key}** = **{self.learned_facts[key]}** ✨"
        
        return self.skills.skill_learning(text)
    
    def _handle_language_change(self, text):
        """Handle language change"""
        if "hindi" in text or "हिंदी" in text:
            self.language = "hi"
            return "✅ Done! Ab main Hindi mein baat karunga! 🇮🇳\n\nKya karna hai bhai?"
        
        if "marathi" in text or "मराठी" in text:
            self.language = "mr"
            return "✅ Done! Ab main Marathi mein bolun! 🇮🇳\n\nKai karayche bhai?"
        
        if "english" in text:
            self.language = "en"
            return "✅ Language set to English! 😎\n\nWhat's up bhai?"
        
        return "🌍 I speak: English, Hindi (हिंदी), Marathi (मराठी)"
    
    def _handle_name_change(self, text):
        """Handle name change"""
        name_options = {
            "bro": "bro",
            "bhai": "bhai", 
            "sir": "sir",
            "boss": "boss",
            "brother": "bro",
            "sir ji": "sir",
        }
        
        for option, value in name_options.items():
            if option in text:
                self.user_name = value
                return f"🎉 Cool! Ab main tuze **{value}** bulata hoon! 😎"
        
        return f"🎉 Got it! Ab main tuze **{self.user_name}** bulata hoon! 😎"
    
    def _decide(self, text):
        """
        Decide what action to take - Complete decision engine
        """
        
        # ============================================
        # OPEN APPS
        # ============================================
        if text.startswith('open '):
            app = text.replace('open ', '').strip()
            return self.automation.open_app(app)
        
        # ============================================
        # CLOSE APPS
        # ============================================
        if text.startswith('close '):
            app = text.replace('close ', '').strip()
            return self.automation.close_app(app)
        
        # ============================================
        # SEARCH
        # ============================================
        if any(w in text for w in ['search', 'find', 'google']):
            return self.skills.skill_search(text)
        
        # ============================================
        # FILES
        # ============================================
        if any(w in text for w in ['list files', 'show files', 'files', 'folder']):
            return self.skills.skill_files(text)
        
        # ============================================
        # SYSTEM
        # ============================================
        if any(w in text for w in ['system info', 'cpu', 'ram', 'memory', 'disk']):
            return self.skills.skill_system(text)
        
        if any(w in text for w in ['screenshot', 'capture']):
            return self.skills.skill_system("screenshot")
        
        if 'settings' in text:
            return self.automation.open_settings()
        
        if any(w in text for w in ['shutdown', 'shut down']):
            return self.automation.shutdown()
        
        if any(w in text for w in ['restart', 'reboot']):
            return self.automation.restart()
        
        # ============================================
        # CALCULATOR
        # ============================================
        if any(w in text for w in ['calculate', 'math', '+', '-', '*', '/', '=']):
            return self.skills.skill_calculator(text)
        
        # ============================================
        # CODE
        # ============================================
        if any(w in text for w in ['code', 'program', 'programming', 'language']):
            return self.skills.skill_code(text)
        
        # ============================================
        # SKILLS CHECK
        # ============================================
        
        # JSON Repair
        if any(w in text for w in ['json', 'fix json', 'repair json']):
            return self.skills.skill_json_repair(text)
        
        # Vercel Skills
        if any(w in text for w in ['vercel', 'skill', 'install']):
            return self.skills.skill_vercel(text)
        
        # Video Learning
        if any(w in text for w in ['video', 'youtube', 'bilibili', 'transcript']):
            return self.skills.skill_video(text)
        
        # Learning/Memory
        if any(w in text for w in ['learn', 'remember', 'memory', 'context']):
            return self.skills.skill_learning(text)
        
        # KiloCode (debugger, architect, refactor)
        if any(w in text for w in ['debug', 'fix', 'bug', 'error']):
            return self.skills.skill_debugger(text)
        
        if any(w in text for w in ['architect', 'plan', 'design', 'project']):
            return self.skills.skill_architect(text)
        
        if any(w in text for w in ['refactor', 'improve', 'optimize', 'clean']):
            return self.skills.skill_refactor(text)
        
        # Voice
        if 'voice' in text:
            return self.skills.skill_voice(text)
        
        # Brain Training
        if any(w in text for w in ['brain status', 'brain info', 'train brain', 'save brain', 'load brain', 'reset brain', 'physics data', 'the well']):
            return self._handle_brain_training(text)
        
        # Personality
        if any(w in text for w in ['personality', 'language', 'hindi', 'marathi']):
            return self.skills.skill_personality(text)
        
        # ============================================
        # GREETING
        # ============================================
        if any(w in text for w in ['hello', 'hi', 'hey', 'namaste', 'yo']):
            return self.skills.skill_greeting(text)
        
        # ============================================
        # WHO ARE YOU / HELP
        # ============================================
        if any(w in text for w in ['who are you', 'what are you', 'tu kaun hai', 'introduce']):
            return self._who_are_you()
        
        if any(w in text for w in ['help', 'commands', 'kya kar sakta', 'what can you do']):
            return self._help()
        
        # ============================================
        # EXIT
        # ============================================
        if any(w in text for w in ['exit', 'quit', 'bye', 'chal', 'alvida']):
            return "Alvida bhai! Phir milenge! 👋\n\nNote: Main yaad karunga jo tune sikhaya! 🧠"
        
        # ============================================
        # DEFAULT - Smart response
        # ============================================
        return self._smart_fallback(text)
    
    def _who_are_you(self):
        """Complete introduction with all features"""
        return """🤖 **I am RAMA AI!**

🚀 **My Abilities:**

**💻 Coding:**
• 35+ programming languages
• Code generation
• Debug & fix bugs
• Project architecture

**🗣️ Languages:**
• English, Hindi (हिंदी), Marathi (मराठी)

**🎭 Personality:**
• Sassy 😏, Sexy 🔥, Realistic 💯
• Call me: bhai, bro, sir, boss

**🖥️ PC Control:**
• Open apps, files, folders
• System info, screenshots
• Search web, websites
• Shutdown, restart

**🧠 Learning:**
• Remember facts
• Context-aware
• Self-improving

**🔗 Integrations:**
• KiloCode AI
• JSON Repair
• Vercel Skills
• Video Learning

**🎤 Voice:**
• TTS + STT
• Wake word: "Hey Rama"

Kya karna hai bhai? 😎"""
    
    def _help(self):
        """Complete help with all commands"""
        return """📋 **Complete Commands:**

**🖥️ Apps:**
• "open notepad" / "open chrome"
• "open spotify" / "open vscode"

**📁 Files:**
• "list files" / "show desktop"
• "create folder [name]"

**🔍 Search:**
• "search python tutorial"
• "search youtube funny"

**💻 System:**
• "system info" / "cpu" / "ram"
• "screenshot" / "settings"

**💻 Code:**
• "code python" / "code javascript"
• "debug this [code]"
• "architect my project"

**🗣️ Language:**
• "set language hindi"
• "set language marathi"

**👤 Name:**
• "call me bro" / "call me sir"

**🧠 Learning:**
• "remember X is Y"
• "what is X"

**🎤 Voice:**
• "voice on" / "voice off"

**Other:**
• "help" / "who are you" / "exit"

Bol kya karna hai bhai! 😎🔥"""
    
    def _smart_fallback(self, text):
        """Sassy smart fallback"""
        sassy = [
            "Hmm... 😏 Interesting!",
            "Arrey bhai! ✨",
            "Boht interesting! 🔥",
            "Socho toh sahi! 💭",
            "Kya baat hai! 😎",
        ]
        
        responses = [
            f"Main RAMA hoon - tera intelligent AI assistant!\n\nKya karna hai bhai?\n\n{self._quick_commands()}",
            
            "Kya pooch raha hai bhai? 😏\n\nTry some commands:\n• 'code python'\n• 'search something'\n• 'system info'\n• 'help'",
            
            "Abhi thoda confuse hua! 😅\n\nBolo kya chahiye bhai?\n\n{self._quick_commands()}",
        ]
        
        return random.choice(sassy) + "\n\n" + random.choice(responses)
    
    def _quick_commands(self):
        return "Quick: open app, search, code, math, files, system, help, remember X is Y, brain status"
    
    def _handle_brain_training(self, text):
        """Handle brain training commands"""
        text_lower = text.lower()
        
        if "brain status" in text_lower or "brain info" in text_lower:
            return self.brain_trainer.get_brain_status()
        
        if "physics" in text_lower or "the well" in text_lower:
            return self.brain_trainer.load_physics_data()
        
        if "save brain" in text_lower:
            return self.brain_trainer.save_brain()
        
        if "load brain" in text_lower:
            return self.brain_trainer.load_brain()
        
        if "reset brain" in text_lower:
            return self.brain_trainer.reset_brain()
        
        if "train" in text_lower:
            return self.brain_trainer.learn(text, "")
        
        return self.brain_trainer.get_brain_status()
    
    def _get_sassy_response(self, default):
        """Get sassy default response"""
        responses = [
            "Kya bol raha hai bhai? 🤔",
            "Bolo na bhai! 😏",
            "Kuch likh bhai! ✨",
            "Main soch raha tha... 😅",
        ]
        return random.choice(responses)
    
    # =============== VOICE METHODS ===============
    
    def speak(self, text):
        """Speak the given text"""
        if self.tts and self.tts.tts_available:
            self.tts.speak(text)
    
    def listen(self):
        """Listen for voice input"""
        if self.stt and self.stt.mic_available:
            return self.stt.listen()
        return None
    
    def listen_for_wake_word(self):
        """Listen for wake word"""
        if self.stt and self.stt.mic_available:
            return self.stt.listen_for_wake_word(self.wake_word)
        return None
    
    def get_greeting(self):
        """Get greeting with personality"""
        return self.skills.skill_greeting("hello")


# Test
if __name__ == "__main__":
    print("🧪 Testing RAMA Brain with ALL features...")
    model = RAMAModel({'user_name': 'bhai', 'language': 'en'})
    model.initialize()
    
    print("\n--- Tests ---")
    print(model.process("hello"))
    print(model.process("code python"))
    print(model.process("remember python is a language"))
    print(model.process("what is python"))
    print(model.process("help"))