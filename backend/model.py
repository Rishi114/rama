"""
RAMA AI - Model (Brain)
The "brain" for decision-making
Combines all modules for intelligent responses
"""

import re
import asyncio
from datetime import datetime


class RAMAModel:
    """
    RAMA's brain - central decision making
    Coordinates all modules and produces responses
    """
    
    def __init__(self, config=None):
        self.config = config or {}
        
        # Initialize modules (imported lazily)
        self.automation = None
        self.chat_bot = None
        self.tts = None
        self.stt = None
        
        # Settings
        self.wake_word = self.config.get('wake_word', 'hey rama')
        self.user_name = self.config.get('user_name', 'bhai')
        
        # State
        self.is_listening = False
        self.history = []
    
    def initialize(self):
        """Initialize all modules"""
        try:
            from automation import Automation
            from chat_bot import ChatBot
            from text_to_speech import TextToSpeech
            from speech_to_text import SpeechToText
            
            self.automation = Automation(self.config)
            self.chat_bot = ChatBot({
                'user_name': self.user_name,
                'language': self.config.get('language', 'en')
            })
            self.tts = TextToSpeech(self.config)
            self.stt = SpeechToText(self.config)
            
            print("✅ RAMA Brain initialized!")
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
            return "Kya bol raha hai bhai?"
        
        text = user_input.strip()
        text_lower = text.lower()
        
        # Record in history
        self.history.append({
            'role': 'user',
            'content': text,
            'timestamp': datetime.now().isoformat()
        })
        
        # Determine what to do based on input
        response = self._decide(text_lower)
        
        # Record response
        self.history.append({
            'role': 'assistant',
            'content': response,
            'timestamp': datetime.now().isoformat()
        })
        
        return response
    
    def _decide(self, text):
        """
        Decide what action to take
        Core decision logic
        """
        
        # ============================================
        # AUTOMATION COMMANDS
        # ============================================
        
        # Open apps
        if text.startswith('open '):
            app = text.replace('open ', '').strip()
            return self.automation.open_app(app)
        
        # Close apps
        if text.startswith('close '):
            app = text.replace('close ', '').strip()
            return self.automation.close_app(app)
        
        # Search web
        if 'search' in text:
            query = text.replace('search', '').replace('google', '').strip()
            return self.automation.search_web(query)
        
        # Open website
        if text.startswith('open '):
            site = text.replace('open ', '').strip()
            return self.automation.open_website(site)
        
        # Files
        if any(w in text for w in ['list files', 'show files', 'files']):
            return self.automation.list_files()
        
        # Create folder
        if 'create folder' in text or 'new folder' in text:
            name = text.replace('create folder', '').replace('new folder', '').strip()
            return self.automation.create_folder(name)
        
        # System info
        if 'system info' in text or 'pc info' in text:
            return self._get_system_info()
        
        # Screenshot
        if 'screenshot' in text or 'capture' in text:
            return self.automation.take_screenshot()
        
        # Settings
        if 'settings' in text:
            return self.automation.open_settings()
        
        # Shutdown
        if 'shutdown' in text or 'shut down' in text:
            return self.automation.shutdown()
        
        # Restart
        if 'restart' in text or 'reboot' in text:
            return self.automation.restart()
        
        # ============================================
        # CHAT COMMANDS
        # ============================================
        
        return self.chat_bot.chat(text)
    
    def _get_system_info(self):
        """Get system information"""
        try:
            import platform
            import psutil
            
            cpu = psutil.cpu_percent()
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            return f"""💻 **System Info:**

**OS:** {platform.system()} {platform.release()}
**Node:** {platform.node()}

**CPU:** {cpu}%
**RAM:** {memory.percent}% ({memory.used/1024**3:.1f}/{memory.total/1024**3:.1f} GB)
**Disk:** {disk.percent}%"""
        except:
            return "❌ Couldn't get system info"
    
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
        """Get greeting"""
        return self.chat_bot.greet()


# Test
if __name__ == "__main__":
    model = RAMAModel({'user_name': 'bhai'})
    model.initialize()
    
    # Test
    print(model.process("hello"))
    print(model.process("open notepad"))
    print(model.process("system info"))