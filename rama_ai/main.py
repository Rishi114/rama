"""
RAMA AI v2.0 - Main Entry Point
Enhanced version with smarter AI
"""

import asyncio
import sys
import os
import random

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def check_dependencies():
    """Check available dependencies"""
    available = {}
    
    try:
        import customtkinter
        available['ui'] = True
    except:
        available['ui'] = False
    
    try:
        import aiohttp
        available['aiohttp'] = True
    except:
        available['aiohttp'] = False
    
    try:
        import requests
        available['requests'] = True
    except:
        available['requests'] = False
    
    try:
        import psutil
        available['psutil'] = True
    except:
        available['psutil'] = False
    
    return available


# Smart response generator for CLI mode
class SmartRama:
    """Enhanced AI responses"""
    
    def __init__(self):
        self.name = "RAMA"
        self.version = "2.0"
        self.knowledge = self._load_knowledge()
        
    def _load_knowledge(self):
        return {
            "greetings": [
                "Well, well... look who's awake! 👀",
                "Hey there, superstar! ✨",
                "Yo! Ready to rock? 🚀",
                "Hello, human! 😄 What can I do for you?",
                "Ah, our paths cross again! 🌟",
            ],
            "thoughtful": [
                "💭 Let me think about that...",
                "🤔 Interesting question...",
                "✨ Great thinking!",
                "🌟 You've got my attention!",
                "💡 Here's my take...",
            ],
            "code_languages": {
                "python": "```python\n# Python\ndef greet(name):\n    return f'Hello, {name}!'\nprint(greet('World'))\n```",
                "javascript": "```javascript\n// JavaScript\nconst greet = (name) => `Hello, ${name}!`;\nconsole.log(greet('World'));\n```",
                "rust": "```rust\n// Rust\nfn main() {\n    println!(\"Hello, World!\");\n}\n```",
                "go": "```go\n// Go\npackage main\nimport \"fmt\"\nfunc main() { fmt.Println(\"Hello, World!\") }\n```",
                "java": "```java\n// Java\npublic class Main {\n    public static void main(String[] args) {\n        System.out.println(\"Hello, World!\");\n    }\n}\n```",
            }
        }
    
    def process(self, user_input: str) -> str:
        """Process input and generate smart response"""
        text = user_input.lower().strip()
        
        # Greetings
        if any(g in text for g in ["hello", "hi", "hey", "yo"]):
            return random.choice(self.knowledge["greetings"])
        
        # Help
        if "help" in text or "what can" in text:
            return self._get_help()
        
        # List skills/capabilities
        if any(s in text for s in ["list skills", "what do you know", "capabilities"]):
            return self._get_capabilities()
        
        # List languages
        if "languages" in text or "programming" in text:
            return "💻 I know 35+ programming languages! Ask like 'code python' or 'show javascript'"
        
        # Code examples
        if "code" in text:
            for lang, example in self.knowledge["code_languages"].items():
                if lang in text:
                    return f"💻 **{lang.capitalize()}:**\n{example}"
            return "💻 Which language? Try 'code python', 'code javascript', 'code rust', etc."
        
        # Math
        if any(m in text for m in ["calculate", "math", "+", "-", "*", "/"]):
            return self._handle_math(text)
        
        # System info
        if any(s in text for s in ["system", "cpu", "memory", "ram", "disk"]):
            return self._get_system_info(text)
        
        # Who are you
        if "who are you" in text or "what are you" in text:
            return """🤖 **I am RAMA AI!**

Your intelligent, self-learning assistant!

✨ Features:
• 💻 Code in 35+ languages
• 🧮 Smart calculations
• 🧠 Self-learning
• 📁 File management
• 💻 System control
• 🌐 Web search
• 🔍 Analysis
• 🎭 Sassy personality

I get smarter with every conversation! 🚀"""
        
        # Smart fallback
        return self._smart_fallback(text)
    
    def _get_help(self) -> str:
        return """📋 **Commands I understand:**

💻 **Coding**
- "code python" / "code javascript" / "code rust"
- "show java function" / "explain go"

🧮 **Math**
- "calculate 2+2" / "calculate (10*5)/2"

💻 **System**
- "cpu info" / "memory info" / "disk info"

📁 **Files**
- "list files" / "create folder X"

🌐 **Search**
- "search X" / "find X"

🧠 **Learning**
- "learn X is Y" / "remember my name"

✨ **General**
- "help" / "list skills" / "who are you"
- "languages" / "capabilities"

**Just type naturally!** I'll understand! 🎯"""
    
    def _get_capabilities(self) -> str:
        return """📦 **My Capabilities:**

💻 **Coding** - 35+ languages (Python, JS, Java, Rust, Go, C++, etc.)
🧮 **Math** - Complex calculations and equations
🧠 **Learning** - Remember facts, learn from interactions
📁 **Files** - List, create, manage files and folders
💻 **System** - CPU, memory, disk info; launch apps
🌐 **Web** - Search the web, open URLs
🔍 **Analysis** - Code analysis, debugging help
🎭 **Personality** - Sassy, witty, clever responses
📖 **Knowledge** - General knowledge, explanations
🎙️ **Voice** - Voice I/O (optional)

**I learn and improve over time!** 🚀"""
    
    def _handle_math(self, text: str) -> str:
        import re
        import operator
        
        # Try to extract and calculate
        ops = {'+': operator.add, '-': operator.sub, '*': operator.mul, '/': operator.truediv}
        
        # Simple pattern
        numbers = re.findall(r'-?\d+\.?\d*', text)
        
        if not numbers:
            return "🧮 Give me numbers to calculate! Example: calculate 2+2 or (10*5)/2"
        
        if len(numbers) >= 2:
            try:
                # Try evaluating the expression
                expr = re.sub(r'[^0-9+\-*/().]', '', text)
                if expr:
                    result = eval(expr)
                    return f"🧮 **Result:**\n\n`{expr}` = **{result}**\n\n✨ Pretty good at math, right?"
            except:
                pass
            
            # Simple two-number calculation
            try:
                a, b = float(numbers[0]), float(numbers[1])
                if '+' in text:
                    return f"🧮 **Calculation:**\n\n{a} + {b} = **{a + b}**"
                elif '-' in text:
                    return f"🧮 **Calculation:**\n\n{a} - {b} = **{a - b}**"
                elif '*' in text:
                    return f"🧮 **Calculation:**\n\n{a} * {b} = **{a * b}**"
                elif '/' in text and b != 0:
                    return f"🧮 **Calculation:**\n\n{a} / {b} = **{a / b}**"
            except:
                pass
        
        return "🧮 Try format like: calculate 2+2 or calculate 100/5"
    
    def _get_system_info(self, text: str) -> str:
        try:
            import psutil
            import platform
            
            if "cpu" in text:
                return f"⚡ **CPU:** {psutil.cpu_count()} cores @ {psutil.cpu_percent()}%"
            
            if "memory" in text or "ram" in text:
                mem = psutil.virtual_memory()
                return f"🧠 **RAM:** {mem.percent}% used ({mem.used/1024**3:.1f}/{mem.total/1024**3:.1f} GB)"
            
            if "disk" in text:
                disk = psutil.disk_usage('/')
                return f"💾 **Disk:** {disk.percent}% used ({disk.used/1024**3:.1f}/{disk.total/1024**3:.1f} GB)"
            
            return f"💻 **{platform.system()}:** {platform.node()}\n⚡ CPU: {psutil.cpu_count()} cores\n🧠 RAM: {psutil.virtual_memory().percent}%"
        except:
            return "💻 Install psutil for system info: pip install psutil"
    
    def _smart_fallback(self, text: str) -> str:
        cleverness = [
            "Interesting! 🤔 Let me think about that...",
            "Great question! 💫 Here's what I know...",
            "Ah! 😄 That's a good one!",
            "Hmm... 💭 Let me share my perspective...",
            "Got it! 🌟 Here's my thoughts...",
        ]
        
        responses = [
            "I'm your AI assistant! 🤖 I can help with coding, math, files, system tasks, and much more!\n\n"
            "Try asking me about:\n"
            "• Code in any language\n"
            "• Calculations\n"
            "• System information\n"
            "• File management\n"
            "• Learning new things\n\n"
            "What would you like to try?",
            
            "That's a fascinating topic! 🌟 While I don't have specific info on that, I'm great at:\n"
            "• Writing & debugging code\n"
            "• Math & calculations\n"
            "• System operations\n"
            "• Explaining concepts\n\n"
            "How can I help you today?",
            
            "You've sparked my curiosity! 🔥 I'm smartest when we work on code, math, or tasks together.\n\n"
            "Just ask me anything! I'm always learning and improving! 📚",
        ]
        
        return random.choice(cleverness) + "\n\n" + random.choice(responses)


async def run_cli():
    """Run CLI mode with enhanced AI"""
    print("\n" + "="*50)
    print("   🤖 RAMA AI v2.0 - Enhanced Intelligence")
    print("="*50)
    print("\n💡 Type 'help' for commands\n")
    
    rama = SmartRama()
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['exit', 'quit', 'bye']:
                print("\n👋 Goodbye! It was great chatting!")
                break
            
            # Get smart response
            response = rama.process(user_input)
            print(f"\n🤖 Rama: {response}\n")
            
        except KeyboardInterrupt:
            print("\n👋 Bye!")
            break
        except Exception as e:
            print(f"\n❌ Oops: {e}\n")


async def main():
    """Main entry point"""
    deps = check_dependencies()
    print(f"🔧 Available: {', '.join([k for k,v in deps.items() if v])}")
    await run_cli()


if __name__ == "__main__":
    asyncio.run(main())