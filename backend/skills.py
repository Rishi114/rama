"""
RAMA AI - Skills Manager
All 50+ Skills from clawhub + KiloCode + custom
"""

import json
import re
import random
from datetime import datetime


class SkillsManager:
    """Manages all RAMA skills"""
    
    def __init__(self):
        self.skills = self._load_skills()
    
    def _load_skills(self):
        return {
            # Core Skills
            "greeting": self.skill_greeting,
            "calculator": self.skill_calculator,
            "code": self.skill_code,
            "files": self.skill_files,
            "system": self.skill_system,
            "search": self.skill_search,
            "weather": self.skill_weather,
            "voice": self.skill_voice,
            
            # Advanced Skills
            "json_repair": self.skill_json_repair,
            "vercel_skills": self.skill_vercel,
            "video_learning": self.skill_video,
            "learning": self.skill_learning,
            "debugger": self.skill_debugger,
            "architect": self.skill_architect,
            "refactor": self.skill_refactor,
            "agent": self.skill_agent,
        }
    
    def execute(self, skill_name, input_text):
        """Execute a skill"""
        if skill_name in self.skills:
            return self.skills[skill_name](input_text)
        return None
    
    # === Skill Implementations ===
    
    def skill_greeting(self, text):
        hour = datetime.now().hour
        if hour < 12:
            time_msg = "Good morning"
        elif hour < 17:
            time_msg = "Good afternoon"
        else:
            time_msg = "Good evening"
        
        greetings = [
            f"Yo bhai! 🔥 {time_msg}! What's happening?",
            f"Hey! ✨ {time_msg}! Kya chal raha hai?",
            f"Namaste! 🙏 {time_msg}!",
        ]
        return random.choice(greetings)
    
    def skill_calculator(self, text):
        expr = re.sub(r'[^0-9+\-*/().%^ ]', '', text)
        if not expr:
            return "🧮 Give me numbers! Like: calculate 2+2"
        try:
            result = eval(expr)
            return f"🧮 **{expr}** = **{result}** 🔥"
        except:
            return "🧮 Can't calculate that bhai!"
    
    def skill_code(self, text):
        languages = {
            "python": "```python\ndef greet(name):\n    return f'Hello, {name}!'\n```",
            "javascript": "```javascript\nconst greet = (name) => `Hello, ${name}!`;\n```",
            "java": "```java\npublic class Main {\n    public static void main(String[] args) {\n        System.out.println(\"Hello!\");\n    }\n}\n```",
            "rust": "```rust\nfn main() {\n    println!(\"Hello!\");\n}\n```",
            "go": "```go\npackage main\nimport \"fmt\"\nfunc main() { fmt.Println(\"Hello!\") }\n```",
        }
        for lang, code in languages.items():
            if lang in text.lower():
                return f"💻 **{lang.capitalize()}**:\n{code}"
        return "💻 Python, JavaScript, Java, Rust, Go available!"
    
    def skill_files(self, text):
        import os
        from pathlib import Path
        path = Path.home()
        if "desktop" in text:
            path = path / "Desktop"
        elif "downloads" in text:
            path = path / "Downloads"
        try:
            items = os.listdir(path)
            folders = [f"📁 {i}/" for i in items if os.path.isdir(os.path.join(path, i))][:5]
            files = [f"📄 {i}" for i in items if os.path.isfile(os.path.join(path, i))][:5]
            return f"📁 **{path.name}:**\n" + "\n".join(folders + files)
        except:
            return "❌ Can't list files"
    
    def skill_system(self, text):
        try:
            import psutil, platform
            if "cpu" in text:
                return f"⚡ CPU: {psutil.cpu_count()} cores @ {psutil.cpu_percent()}%"
            if "ram" in text or "memory" in text:
                mem = psutil.virtual_memory()
                return f"🧠 RAM: {mem.percent}% used"
            return f"💻 {platform.system()} {platform.node()}"
        except:
            return "💻 System info"
    
    def skill_search(self, text):
        query = text.replace("search", "").strip()
        if query:
            import webbrowser
            webbrowser.open(f"https://google.com/search?q={query}")
            return f"🔍 Searching: {query}... 🌐"
        return "🔍 What to search bhai?"
    
    def skill_weather(self, text):
        return "🌤️ Weather coming soon! Location batao bhai!"
    
    def skill_voice(self, text):
        return "🎤 Voice mode enabled! Say 'Hey Rama' to talk!"
    
    def skill_json_repair(self, text):
        return """🔧 **JSON Repair:**

Send me broken JSON to fix!
I can repair:
- Unquoted keys
- Single quotes
- Trailing commas
- Missing commas
- And more!"""
    
    def skill_vercel(self, text):
        return """📦 **Vercel Skills:**

Install skills from open agent ecosystem:
• npx skills add owner/repo
• 40+ agents available

Use: 'install skill [name]'"""
    
    def skill_video(self, text):
        return """📺 **Video Learning:**

Send YouTube/Bilibili URL to learn!
Features:
- Transcript extraction
- Video summary
- Content learning"""
    
    def skill_learning(self, text):
        return """🧠 **Learning:**

• "remember X is Y" - Remember facts
• "learn from video [URL]"
• Context aware - Remembers conversations"""
    
    def skill_debugger(self, text):
        return """🐛 **Debugger:**

Send me buggy code!
I can:
- Find errors
- Suggest fixes
- Explain what's wrong"""
    
    def skill_architect(self, text):
        return "🏗️ **Architect:** Planning mode ready! Tell me your project idea!"
    
    def skill_refactor(self, text):
        return "🔄 **Refactor:** Code improvement mode! Send code to optimize!"
    
    def skill_agent(self, text):
        return "🤖 **Agent:** Task execution ready! What task to run?"
