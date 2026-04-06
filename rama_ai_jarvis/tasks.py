"""
RAMA Task Executor
Execute real system commands and tasks
Following the tutorial's task execution modules
"""

import os
import subprocess
import webbrowser
import platform
import psutil
from datetime import datetime
import random


class TaskExecutor:
    """
    Execute tasks based on commands
    Similar to tutorial's task functions
    """
    
    def __init__(self):
        self.platform = platform.system()
        
        # App mappings
        self.app_map = {
            'notepad': 'notepad.exe',
            'calculator': 'calc.exe',
            'chrome': 'chrome',
            'explorer': 'explorer.exe',
            'cmd': 'cmd.exe',
            'powershell': 'powershell.exe',
            'spotify': 'spotify',
            'discord': 'discord',
            'telegram': 'telegram',
            'vscode': 'code',
            'word': 'winword',
            'excel': 'excel',
        }
        
        # Responses for personality
        self.responses = {
            'greeting': [
                "Hey bhai! 🔥 Kya karna hai?",
                "Yo! ✨ Tell me what to do!",
                "At your service! 😎 What do you need?",
            ],
            'goodbye': [
                "Alvida bhai! 👋 Phir milenge!",
                "Bye! ✨ Take care!",
                "See you soon! 🔥",
            ],
            'help': """
📋 **Available Commands:**

**🖥️ Open Apps:**
- "open notepad" / "open calculator"
- "open chrome" / "open spotify"
- "open explorer"

**🔍 Search:**
- "search google for [query]"
- "search youtube for [query]"
- "wikipedia [topic]"

**⏰ Time/Date:**
- "what time is it"
- "what is the date"
- "what day is it"

**💻 System:**
- "system info" / "screenshot"
- "shutdown" / "restart"

**Other:**
- "weather" / "who are you" / "help"
            """,
            'who_are_you': """
🤖 **I am RAMA!**

Your personal AI assistant like Jarvis!

I can:
• Open apps and programs
• Search the web
• Tell time and date
• Get system info
• Take screenshots
• And much more!

Just say "Hey Rama" and tell me what to do! 😎
            """,
        }
        
        print("⚙️ Task Executor initialized")
    
    def execute(self, command_string):
        """
        Execute a command
        Args:
            command_string: Format "task:action:params"
        """
        if not command_string:
            return None
        
        # Parse command
        if not command_string.startswith("task:"):
            # AI response, not a task
            return None
        
        parts = command_string.split(":")
        action = parts[1] if len(parts) > 1 else ""
        param = parts[2] if len(parts) > 2 else ""
        
        # Execute based on action
        if action == "open_app":
            return self._open_app(param)
        
        if action == "open_website":
            return self._open_website(param)
        
        if action == "search":
            source = param
            query = parts[3] if len(parts) > 3 else ""
            return self._search(source, query)
        
        if action == "wikipedia":
            return self._wikipedia(param)
        
        if action == "time":
            return self._get_time()
        
        if action == "date":
            return self._get_date()
        
        if action == "day":
            return self._get_day()
        
        if action == "system_info":
            return self._get_system_info()
        
        if action == "screenshot":
            return self._take_screenshot()
        
        if action == "shutdown":
            return self._shutdown()
        
        if action == "restart":
            return self._restart()
        
        if action == "weather":
            return self._get_weather()
        
        if action == "help":
            return self._get_help()
        
        if action == "who_are_you":
            return self._who_are_you()
        
        if action == "exit":
            return self._goodbye()
        
        return None
    
    def _open_app(self, app_name):
        """Open an application"""
        app = self.app_map.get(app_name.lower(), app_name)
        
        try:
            if self.platform == "Windows":
                subprocess.Popen(app, shell=True)
            else:
                subprocess.Popen(["open", "-a", app])
            
            return f"✅ Opened {app_name.title()}! 🔥"
        except Exception as e:
            return f"❌ Couldn't open {app_name}: {str(e)}"
    
    def _open_website(self, site):
        """Open a website"""
        urls = {
            'youtube': 'https://youtube.com',
            'google': 'https://google.com',
            'github': 'https://github.com',
            'wikipedia': 'https://wikipedia.org',
        }
        
        url = urls.get(site.lower(), f"https://{site}")
        
        try:
            webbrowser.open(url)
            return f"✅ Opened {site.title()}! 🌐"
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def _search(self, source, query):
        """Search the web"""
        if not query:
            return "Kya search karna hai bhai?"
        
        if source == "google":
            url = f"https://google.com/search?q={query}"
        elif source == "youtube":
            url = f"https://youtube.com/results?search_query={query}"
        else:
            url = f"https://google.com/search?q={query}"
        
        try:
            webbrowser.open(url)
            return f"🔍 Searching {source} for: {query}... 🌐"
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def _wikipedia(self, topic):
        """Search Wikipedia"""
        if not topic:
            return "Kis topic ki information chahiye?"
        
        url = f"https://en.wikipedia.org/wiki/{topic.replace(' ', '_')}"
        
        try:
            webbrowser.open(url)
            return f"📖 Opening Wikipedia for: {topic}..."
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def _get_time(self):
        """Get current time"""
        now = datetime.now()
        time_str = now.strftime("%I:%M %p")
        return f"⏰ Time: {time_str}"
    
    def _get_date(self):
        """Get current date"""
        now = datetime.now()
        date_str = now.strftime("%B %d, %Y")
        return f"📅 Date: {date_str}"
    
    def _get_day(self):
        """Get current day"""
        now = datetime.now()
        day = now.strftime("%A")
        return f"📆 Today is: {day}"
    
    def _get_system_info(self):
        """Get system information"""
        try:
            cpu = psutil.cpu_percent()
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            return f"""💻 **System Info:**
CPU: {cpu}%
RAM: {memory.percent}%
Disk: {disk.percent}%"""
        except:
            return "❌ Couldn't get system info"
    
    def _take_screenshot(self):
        """Take screenshot"""
        try:
            if self.platform == "Windows":
                import mss
                with mss.mss() as sct:
                    sct.shot()
                return "📸 Screenshot saved! 🔥"
            else:
                return "📸 Screenshot only on Windows"
        except:
            return "📸 Screenshot feature"
    
    def _shutdown(self):
        """Shutdown PC"""
        try:
            if self.platform == "Windows":
                os.system("shutdown /s /t 60")
                return "🔴 Shutting down in 60 seconds..."
            return "🔧 Only on Windows"
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def _restart(self):
        """Restart PC"""
        try:
            if self.platform == "Windows":
                os.system("shutdown /r /t 60")
                return "🔄 Restarting in 60 seconds..."
            return "🔧 Only on Windows"
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def _get_weather(self):
        """Get weather (placeholder)"""
        return "🌤️ Weather feature coming soon! Location batao bhai!"
    
    def _get_help(self):
        """Get help"""
        return self.responses['help']
    
    def _who_are_you(self):
        """Who are you response"""
        return random.choice([
            "Main RAMA hoon - tera personal AI assistant! 😎",
            "I am RAMA - your Jarvis-style assistant! 🔥",
            "Your personal AI helper here! ✨",
        ])
    
    def _goodbye(self):
        """Goodbye response"""
        return random.choice(self.responses['goodbye'])
    
    def get_greeting(self, user_name="bhai"):
        """Get greeting based on time"""
        hour = datetime.now().hour
        
        if hour < 12:
            time_greet = "Good morning"
        elif hour < 17:
            time_greet = "Good afternoon"
        else:
            time_greet = "Good evening"
        
        greetings = [
            f"Hey {user_name}! {time_greet}! 🔥",
            f"Yo {user_name}! {time_greet}! ✨",
            f"{user_name}! {time_greet}! 😎",
        ]
        
        return random.choice(greetings)


# Test
if __name__ == "__main__":
    executor = TaskExecutor()
    
    # Test tasks
    test_tasks = [
        "task:open_app:notepad",
        "task:search:google:python",
        "task:time",
        "task:system_info",
    ]
    
    print("🧪 Testing Task Executor...\n")
    
    for task in test_tasks:
        result = executor.execute(task)
        print(f"Task: {task}")
        print(f"Result: {result}\n")