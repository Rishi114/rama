"""Weather Skill - Weather information"""

from skills.skill_base import Skill


class WeatherSkill(Skill):
    """Get weather information"""
    
    def __init__(self):
        super().__init__()
        self.triggers = ["weather", "forecast", "temperature"]
    
    async def execute(self, input_text: str, context: Any, retrieved_context: str = "") -> str:
        # Extract city
        city = input_text.lower()
        for word in ["weather", "forecast", "in"]:
            city = city.replace(word, "")
        city = city.strip()
        
        if not city:
            return "🌤️ Tell me a city: 'weather Tokyo' or 'weather New York'"
        
        # Mock weather (replace with real API for online mode)
        return f"""🌤️ Weather for **{city.title()}**:
☀️ Temperature: 22°C
💧 Humidity: 65%
🌬️ Wind: 12 km/h
📌 Condition: Sunny"""

class WebSearchSkill(Skill):
    """Web search functionality"""
    
    triggers = ["search", "google", "look up", "find"]
    
    async def execute(self, input_text, context, retrieved_context=""):
        import subprocess
        import platform
        
        # Extract query
        query = input_text.lower()
        for word in ["search", "google", "look up", "find"]:
            query = query.replace(word, "")
        query = query.strip()
        
        if not query:
            return "🔍 What to search? Try 'search Python tutorials'"
        
        # Open browser with search
        url = f"https://google.com/search?q={query.replace(' ', '+')}"
        
        if platform.system() == 'Windows':
            subprocess.Popen(f'start {url}', shell=True)
        elif platform.system() == 'Darwin':
            subprocess.Popen(['open', url])
        else:
            subprocess.Popen(['xdg-open', url])
        
        return f"🔍 Searching for '{query}'..."


class NoteSkill(Skill):
    """Take notes"""
    
    triggers = ["note:", "add note", "write down", "remember"]
    
    async def execute(self, input_text, context, retrieved_context=""):
        # Extract note content
        note = input_text.lower()
        for word in ["note:", "add note", "write down", "remember"]:
            note = note.replace(word, "")
        note = note.strip()
        
        if not note:
            return "📝 What to note? Try 'note: buy groceries'"
        
        # Store note (would go to memory in real implementation)
        return f"✅ Note saved: {note[:50]}{'...' if len(note) > 50 else ''}"


class ReminderSkill(Skill):
    """Set reminders"""
    
    triggers = ["remind", "reminder", "alarm", "notify"]
    
    async def execute(self, input_text, context, retrieved_context=""):
        import re
        
        input_lower = input_text.lower()
        
        # Parse reminder
        match = re.search(r'in (\d+) (minute|hour|day)', input_lower)
        
        if match:
            amount = int(match.group(1))
            unit = match.group(2)
            
            # Extract what to remind
            what = input_lower.split('to ')[1] if 'to ' in input_lower else "something"
            
            return f"⏰ Reminder set for {amount} {unit}: {what}"
        
        return "⏰ Try 'remind me in 10 minutes to call mom'"


class KnowledgeSkill(Skill):
    """Learn and store knowledge"""
    
    triggers = ["learn that", "remember that", "know that", "my name is", "i am"]
    
    async def execute(self, input_text, context, retrieved_context=""):
        import re
        
        input_lower = input_text.lower()
        
        # Pattern: learn that X is Y
        match = re.search(r'learn that (.+) is (.+)', input_lower)
        
        if match:
            topic = match.group(1).strip()
            fact = match.group(2).strip()
            return f"✅ Learned: '{topic}' = '{fact}'"
        
        # Pattern: my name is X
        match = re.search(r'my name is (.+)', input_lower)
        if match:
            name = match.group(1).strip()
            return f"✅ Got it! Your name is {name}"
        
        return "💡 Try 'learn that coffee is hot' or 'my name is John'"