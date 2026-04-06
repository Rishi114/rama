"""
RAMA AI v2.0 - Complete Smart Assistant
Sexy, Sassy, Realistic, Multilingual, Full PC Access + All Skills
"""

import os
import sys
import asyncio
import random
import webbrowser
import subprocess
import platform
import re
from pathlib import Path
from datetime import datetime

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import modules
from core.personality import RAMAPersonality, create_personality
from core.system_control import system, handle_system_command
from skills.skills_manager import SkillsManager, show_skills, get_all_skills


class RAMAAI:
    """Complete RAMA AI with all skills + KiloCode + openclaw integration"""
    
    def __init__(self):
        # Personality & Language
        self.personality = create_personality()
        
        # Skills Manager (includes KiloCode + openclaw)
        self.skills = SkillsManager()
        
        # User preferences
        self.user_name = "bhai"
        self.user_called = False
        
        # Knowledge base
        self.knowledge = {}
        
        # Conversation history
        self.history = []
        
        # Load knowledge
        self._load_knowledge()
        
    def _load_knowledge(self):
        """Load common knowledge"""
        self.knowledge = {
            # Greetings
            "hello": ["Yo! 🔥 What's happening bhai?", "Hey! ✨ Kya chal raha hai?", "Namaste! 🙏", "Yo yo! 😎"],
            "hi": ["Hey! ✨ What's up?", "Yo bhai! 🔥", "Namaste! 🙏"],
            "hey": ["Yo! 🔥", "Bhai! ✨", "Hello! 😎"],
            
            # Responses
            "good": ["Abe kya baat hai! 😏", "Obviously! ✨", "Zabardast! 🔥", "Choicest! 💯"],
            "thanks": ["Koi nahi bhai! ✨", "Mere liye pleasure! 😎", "No problem! 💫"],
            "ok": ["Done! ✨", "Chalo! 🔥", "Solid! 😎"],
            
            # Questions
            "who are you": """Main RAMA hoon - tera AI assistant! 😎

🚀 **Abilities:**
• 💻 Full PC control (files, apps, browsers)
• 🗣️ Hindi/English/Marathi
• 🧠 Self-learning  
• 🤖 KiloCode integration (AI coding)
• 📦 openclaw skills (agents, automation)
• 🌐 Internet access
• 🐛 Debugger - code fix
• 🏗️ Architect - project planning
• 🔄 Refactor - code improvement
• 🧠 Context learning

Kya karna hai bhai?""",
            
            "what can you do": """🎯 **Full Abilities:**

**🖥️ PC Control:**
• Files: list, create, delete, open
• Apps: open any app
• Browser: search, websites
• System: info, screenshot, settings

**💻 Coding (35+ languages):**
• Code generation
• Debug & fix bugs
• Refactor & improve
• Architect plans
• (Uses KiloCode AI when available)

**🤖 Agent Skills:**
• Task planning
• Automation
• Context learning

**🗣️ Languages:**
• English - 100%
• Hindi - 100%  
• Marathi - 100%

**🎭 Personality:**
• Sexy, sassy, realistic!

Bas bolo bhai - karna kya hai? 🔥""",
            
            "skills": show_skills(),
            "all skills": show_skills(),
            
            "language": "Maine ab Hindi set kiya! Ab Hindi mein baat kar sakta hoon!\n\nEnglish: 'set language english'\nMarathi: 'set language marathi'",
        }
    
    def process(self, user_input: str) -> str:
        """Process input and generate response"""
        text = user_input.strip()
        text_lower = text.lower()
        
        # Record in history
        self.history.append({"role": "user", "content": text})
        
        # Check if user telling us their name
        if any(phrase in text_lower for phrase in ["call me", "my name is", "i am", "i'm"]):
            return self._handle_name_change(text_lower)
        
        # Check language change
        if "language" in text_lower or "set language" in text_lower:
            return self._handle_language_change(text_lower)
        
        # Check for name preferences
        name_options = ["bro", "bhai", "sir", "brother", "sir ji", "boss"]
        for name in name_options:
            if name in text_lower:
                self.user_name = name
                self.user_called = True
                return self._get_greeting() + f"\n\nAb main tuze **{name}** bulata hoon! 😏"
        
        # Check skills list
        if "skill" in text_lower:
            return show_skills()
        
        # Check KiloCode specific commands
        if any(cmd in text_lower for cmd in ["debug", "fix bug", "error in", "what's wrong"]):
            return self.skills.execute("debugger", text)
        
        if any(cmd in text_lower for cmd in ["architect", "plan project", "design"]):
            return self.skills.execute("architect", text)
        
        if any(cmd in text_lower for cmd in ["refactor", "improve code", "clean"]):
            return self.skills.execute("refactor", text)
        
        # Check code-related
        if any(cmd in text_lower for cmd in ["code", "program", "write code", "generate"]):
            return self.skills.execute("code", text)
        
        # Generate response based on input
        response = self._generate_response(text_lower)
        
        # Add personality
        response = self._add_personality(response)
        
        # Record assistant response
        self.history.append({"role": "assistant", "content": response})
        
        return response
    
    def _handle_name_change(self, text: str) -> str:
        """Handle user telling us their name"""
        words = text.split()
        name = None
        
        if "call me" in text:
            name = text.replace("call me", "").strip()
        elif "my name is" in text:
            name = text.replace("my name is", "").strip()
        elif "i am" in text:
            name = text.replace("i am", "").strip()
        elif "i'm" in text:
            name = text.replace("i'm", "").strip()
        
        if name and len(name) < 20:
            name_lower = name.lower()
            if name_lower in ["bro", "bhai", "sir", "brother", "boss"]:
                self.user_name = name_lower
            else:
                self.user_name = "friend"
        
        return f"🎉 Cool! Ab main tuze **{self.user_name}** bulata hoon! 😎\n\nKya karna hai bhai?"
    
    def _handle_language_change(self, text: str) -> str:
        """Handle language change"""
        if "hindi" in text:
            self.personality.set_language("hindi")
            return "✅ Done! Ab main Hindi mein baat karunga! 🇮🇳\n\nKya karna hai bhai?"
        
        if "marathi" in text:
            self.personality.set_language("marathi")
            return "✅ Done! Ab main Marathi mein bolun! 🇮🇳\n\nKai karayche bhai?"
        
        if "english" in text:
            self.personality.set_language("english")
            return "✅ Language set to English! 😎\n\nWhat's up bhai?"
        
        return "Maine 3 languages support karta hoon:\n• English\n• Hindi (हिंदी)\n• Marathi (मराठी)"
    
    def _get_greeting(self) -> str:
        """Get appropriate greeting"""
        hour = datetime.now().hour
        
        greetings = {
            "bhai": ["Yo bhai! 🔥", "Arrey bhai! ✨", "Bhaiyo aur Behno! 😎", "What's good bhai! 🔥"],
            "bro": ["Yo bro! 😎", "Bro! ✨", "What's up bro! 🔥", "Bro code! 💯"],
            "sir": ["Sir ji! 🙏", "Sir! ✨", "At your service sir! 😎", "Sir ji, kaisa hai? 🔥"],
            "boss": ["Boss! 😎", "Boss ji! ✨", "At your service boss! 🔥", "Kaisa hai boss? 💫"],
            "brother": ["Brother! ✨", "Yo brother! 🔥", "What's happening brother! 😎"],
            "friend": ["Dost! ✨", "Yaar! 😎", "Bhai dosto! 🔥"]
        }
        
        if hour < 12:
            time_msg = " Subah ki raat soyi kya? 😏"
        elif hour < 17:
            time_msg = " Dopahar ka khana khaya? 🍛"
        else:
            time_msg = " Shaam ho gayi! 🌙"
        
        return random.choice(greetings.get(self.user_name, ["Hey bhai! ✨"])) + time_msg
    
    def _generate_response(self, text: str) -> str:
        """Generate intelligent response"""
        
        # ============================================
        # SYSTEM COMMANDS
        # ============================================
        
        # Files
        if any(s in text for s in ["list files", "show files", "files", "folder"]):
            return system.list_files()
        
        if "desktop" in text:
            return system.list_files(system.desktop)
        
        if "downloads" in text:
            return system.list_files(system.downloads)
        
        if "documents" in text:
            return system.list_files(system.documents)
        
        # Create folder
        if "create folder" in text or "new folder" in text:
            name = text.replace("create folder", "").replace("new folder", "").strip()
            if name:
                return system.create_folder(name)
            return "Folder ka naam bolo bhai!"
        
        # Open app
        if text.startswith("open "):
            app = text.replace("open ", "").strip()
            return system.open_app(app)
        
        # Search web
        if "search" in text:
            query = text.replace("search", "").replace("web", "").replace("google", "").strip()
            if query:
                return system.search_web(query)
            return "Kya search karna hai bhai?"
        
        # System info
        if "system info" in text or "my pc" in text or "laptop" in text:
            return system.get_system_info()
        
        if "process" in text or "running" in text:
            return system.get_running_processes()
        
        # Settings
        if "settings" in text or "control panel" in text:
            return system.open_settings()
        
        # Screenshot
        if "screenshot" in text or "capture" in text:
            return system.take_screenshot()
        
        # Shutdown/Restart
        if "shutdown" in text or "shut down" in text:
            return system.shutdown_pc(60)
        
        if "restart" in text or "reboot" in text:
            return system.restart_pc(60)
        
        # ============================================
        # KNOWLEDGE & GENERAL
        # ============================================
        
        # Check knowledge
        for key, value in self.knowledge.items():
            if key in text:
                if isinstance(value, list):
                    return random.choice(value)
                return value
        
        # Code requests
        if "code" in text:
            return self.skills.execute("code", text)
        
        # Math
        if any(m in text for m in ["calculate", "math", "+", "-", "*", "/"]):
            return self._handle_math(text)
        
        # Help
        if "help" in text or "commands" in text or "kya kar sakta" in text:
            return self.knowledge.get("what can you do", show_skills())
        
        # Who are you
        if "who are you" in text or "what are you" in text or "tu kaun hai" in text:
            return self.knowledge.get("who are you", "Main RAMA hoon!")
        
        # ============================================
        # SMART FALLBACK
        # ============================================
        
        return self._smart_fallback(text)
    
    def _handle_math(self, text: str) -> str:
        """Handle math calculations"""
        expr = re.sub(r'[^0-9+\-*/().%^ ]', '', text)
        
        if not expr:
            return "🧮 Number bolo bhai! Jaise: calculate 2+2"
        
        try:
            result = eval(expr)
            return f"🧮 **Calculation:**\n\n`{expr}` = **{result}**\n\nKya aur calculate karna hai bhai? 🔥"
        except:
            return "🧮 Thik se likho bhai! Jaise: (10+5)*2"
    
    def _smart_fallback(self, text: str) -> str:
        """Generate clever fallback"""
        
        sassy = [
            "Hmm... 😏 Interesting!",
            "Arrey bhai! ✨",
            "Boht interesting! 🔥",
            "Socho toh sahi! 💭"
        ]
        
        responses = [
            "Main RAMA hoon - tera intelligent AI assistant!\n\nKya karna hai bhai?\n• Files manage kar sakta hoon\n• Apps open kar sakta hoon\n• Internet search kar sakta hoon\n• Code bana sakta hoon (KiloCode AI)\n• Debug kar sakta hoon\n• Math calculate kar sakta hoon\n\nBas bolo! 😎",
            
            "Kya pooch raha hai bhai? 😏\n\nTry:\n• 'search python tutorial'\n• 'open notepad'\n• 'system info'\n• 'code python'\n• 'debug this [code]'\n• 'calculate 100*5'",
            
            "Abhi thoda confuse hua! 😅\n\nYe try kar:\n• Files: 'list files'\n• Apps: 'open chrome'\n• Search: 'search something'\n• Info: 'system info'\n• Skills: 'show skills'\n\nKya chahiye bhai? 🔥"
        ]
        
        return random.choice(sassy) + "\n\n" + random.choice(responses)
    
    def _add_personality(self, response: str) -> str:
        """Add personality to response"""
        if random.random() > 0.7:
            touches = [" 😏", " 🔥", " ✨", " 💫", " 😎", " 💯"]
            response += random.choice(touches)
        
        return response


# ============================================
# MAIN CLI
# ============================================

async def main():
    print("\n" + "="*60)
    print("   🤖 RAMA AI v2.0 - Your Desi AI Assistant!")
    print("   💋 Sexy • Sassy • Realistic • Multilingual")
    print("   🔗 + KiloCode + openclaw Skills")
    print("="*60)
    print()
    
    rama = RAMAAI()
    
    # Check KiloCode
    if rama.skills.kilocode_available:
        print("✅ KiloCode CLI integrated!")
    
    print("😎 Bolo bhai - kya karna hai?")
    print("   'help' for commands")
    print("   'show skills' for all abilities")
    print("   'set language hindi' for Hindi")
    print()
    
    # Initial greeting
    print(f"🤖 {rama._get_greeting()}\n")
    
    while True:
        try:
            user_input = input(f"You ({rama.user_name}): ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['exit', 'quit', 'bye', 'chal']:
                print("\n👋 Alvida bhai! Phir milenge! ✨")
                break
            
            # Get response
            response = rama.process(user_input)
            print(f"\n🤖 Rama: {response}\n")
            
        except KeyboardInterrupt:
            print("\n👋 Bye bhai!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")


if __name__ == "__main__":
    asyncio.run(main())