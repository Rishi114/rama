"""
RAMA AI - Chat Bot Module
Manages general AI conversational queries
"""

import random
from datetime import datetime


class ChatBot:
    """
    Conversational AI for RAMA
    Handles general chat and responses
    """
    
    def __init__(self, config=None):
        self.config = config or {}
        self.user_name = self.config.get('user_name', 'bhai')
        self.language = self.config.get('language', 'en')
        
        # Load knowledge
        self._load_knowledge()
    
    def _load_knowledge(self):
        """Load conversation knowledge"""
        
        # Greetings
        self.greetings = {
            'en': [
                "Yo {name}! 🔥 What's happening?",
                "Hey {name}! ✨ Kya chal raha hai?",
                "Namaste {name}! 🙏",
                "Yo yo {name}! 😎 Good to see you!",
            ],
            'hi': [
                "Yo {name}! 🔥 Kya haal chaal?",
                "Arrey {name}! ✨ Kya kar rahe ho?",
                "Namaste {name}! 🙏 Kaisa hai?",
            ]
        }
        
        # Responses
        self.responses = {
            'good': [
                "Abe kya baat hai! 😏",
                "Obviously! ✨",
                "Zabardast! 🔥",
                "Choicest! 💯",
            ],
            'thanks': [
                "Koi nahi {name}! ✨",
                "Mere liye pleasure! 😎",
                "No problem! 💫",
            ],
            'help': """📋 **Commands:**

**🖥️ Apps:**
- "open notepad" / "open chrome"

**🔍 Search:**
- "search [query]"

**⏰ Time:**
- "what time"

**💻 System:**
- "system info"

**🗣️ Just talk to me!**""",
            'who_are_you': """🤖 **I am RAMA!**

Your personal AI assistant like Jarvis!

I can:
• Open apps and programs
• Search the web
• Tell time and date
• Get system info
• Take screenshots
• Chat with you
• And much more!

Just say "Hey Rama" and tell me what to do! 😎"""
        }
    
    def greet(self):
        """Get greeting based on time and language"""
        hour = datetime.now().hour
        
        if hour < 12:
            time_msg = "Good morning"
        elif hour < 17:
            time_msg = "Good afternoon"
        else:
            time_msg = "Good evening"
        
        lang_greetings = self.greetings.get(self.language, self.greetings['en'])
        greeting = random.choice(lang_greetings)
        
        return f"{greeting.format(name=self.user_name)} {time_msg}!"
    
    def chat(self, message):
        """
        Process chat message and return response
        """
        if not message:
            return "Kya bol raha hai bhai?"
        
        text = message.lower().strip()
        
        # Greetings
        if any(w in text for w in ['hello', 'hi', 'hey', 'namaste']):
            return self.greet()
        
        # Thanks
        if any(w in text for w in ['thanks', 'thank', 'dhanyawad', 'shukriya']):
            return random.choice(self.responses['thanks']).format(name=self.user_name)
        
        # Help
        if any(w in text for w in ['help', 'commands', 'kya kar sakta']):
            return self.responses['help']
        
        # Who are you
        if any(w in text for w in ['who are you', 'what are you', 'tu kaun hai']):
            return self.responses['who_are_you']
        
        # Time
        if 'time' in text:
            from datetime import datetime
            now = datetime.now()
            return f"⏰ Time: {now.strftime('%I:%M %p')}"
        
        # Date
        if 'date' in text or 'day' in text:
            from datetime import datetime
            now = datetime.now()
            return f"📅 {now.strftime('%A, %B %d, %Y')}"
        
        # Exit
        if any(w in text for w in ['bye', 'exit', 'quit', 'chal']):
            return "Alvida bhai! Phir milenge! 👋"
        
        # Default - smart response
        return self._smart_response(text)
    
    def _smart_response(self, text):
        """Generate smart response"""
        
        sassy = [
            "Hmm... 😏 Interesting!",
            "Arrey bhai! ✨",
            "Boht interesting! 🔥",
            "Socho toh sahi! 💭",
        ]
        
        responses = [
            "Main RAMA hoon - tera AI assistant! 😎\n\nKya karna hai bhai?",
            "Kya pooch raha hai bhai? 😏\n\nTry: 'open notepad' or 'search python'",
            "Abhi thoda confuse hua! 😅\n\nBolo kya chahiye? 🔥"
        ]
        
        return random.choice(sassy) + "\n\n" + random.choice(responses)


if __name__ == "__main__":
    bot = ChatBot({'user_name': 'bhai', 'language': 'en'})
    print(bot.greet())
    print(bot.chat("hello"))
    print(bot.chat("help"))