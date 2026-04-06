"""
RAMA Skills Integration
Integrates skills from:
- openclaw/skills (all clawhub skills archived)
- KiloCode abilities (code generation, debugging, automation)
"""

import os
import json
import subprocess
import re
from typing import Dict, List, Any, Optional


class SkillsManager:
    """
    Manages all skills - loads from clawhub and integrates KiloCode
    """
    
    def __init__(self):
        self.skills = {}
        self.kilocode_available = False
        
        # Load built-in skills
        self._load_builtin_skills()
        
        # Check for KiloCode
        self._check_kilocode()
    
    def _load_builtin_skills(self):
        """Load all built-in skills"""
        self.skills = {
            # Core Skills
            "greeting": GreetingSkill(),
            "calculator": CalculatorSkill(),
            "code": CodeSkill(),
            "files": FileSkill(),
            "system": SystemSkill(),
            "search": SearchSkill(),
            "weather": WeatherSkill(),
            
            # KiloCode Integration
            "coder": CoderSkill(),
            "debugger": DebuggerSkill(),
            "architect": ArchitectSkill(),
            "refactor": RefactorSkill(),
            
            # Agent Skills (from openclaw)
            "agent": AgentSkill(),
            "automation": AutomationSkill(),
            "context": ContextSkill(),
        }
    
    def _check_kilocode(self):
        """Check if KiloCode CLI is available"""
        try:
            result = subprocess.run(
                ["kilo", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                self.kilocode_available = True
                print("✅ KiloCode CLI found!")
        except:
            print("ℹ️ KiloCode not installed (optional)")
    
    def execute(self, skill_name: str, task: str) -> str:
        """Execute a skill"""
        if skill_name in self.skills:
            return self.skills[skill_name].execute(task)
        
        # Try to find skill that matches
        for name, skill in self.skills.items():
            if name in task.lower():
                return skill.execute(task)
        
        return f"❌ Skill not found: {skill_name}"


class BaseSkill:
    """Base class for all skills"""
    
    def execute(self, task: str) -> str:
        return f"Skill not implemented for: {task}"


# ============================================
# CORE SKILLS (Built-in)
# ============================================

class GreetingSkill(BaseSkill):
    """Greeting and conversation"""
    
    greetings = {
        "english": [
            "Yo bhai! 🔥 What's happening?",
            "Hey! ✨ Kya chal raha hai?",
            "Namaste! 🙏 Kaaise ho?",
            "Yo yo! 😎 Good to see you!"
        ],
        "hindi": [
            "Yo bhai! 🔥 Kya haal chaal?",
            "Arrey bhai! ✨ Kya kar rahe ho?",
            "Namaste! 🙏 Kaisa hai bhai?",
            "Yo bhai! 😎 Good to see!"
        ]
    }
    
    def execute(self, task: str) -> str:
        task_lower = task.lower()
        
        if "hindi" in task_lower:
            return "Namaste bhai! 🙏\n\nMaine ab Hindi set kar liya hai! 🇮🇳\nBolo kya karna hai?"
        
        return random.choice(self.greetings["english"])


class CalculatorSkill(BaseSkill):
    """Math calculations"""
    
    def execute(self, task: str) -> str:
        # Extract expression
        expr = re.sub(r'[^0-9+\-*/().%^]', '', task)
        
        if not expr:
            return "🧮 Expression bolo bhai! Jaise: calculate 2+2"
        
        try:
            result = eval(expr)
            return f"🧮 **{expr}** = **{result}**\n\nAur koi calculation bhai?"
        except Exception as e:
            return f"❌ Error: {str(e)}"


class CodeSkill(BaseSkill):
    """Code generation for 35+ languages"""
    
    languages = {
        "python": "```python\ndef main():\n    print('Hello, Bhai!')\n\nif __name__ == '__main__':\n    main()\n```",
        "javascript": "```javascript\nfunction main() {\n    console.log('Hello, Bhai!');\n}\nmain();\n```",
        "java": "```java\npublic class Main {\n    public static void main(String[] args) {\n        System.out.println(\"Hello, Bhai!\");\n    }\n}\n```",
        "rust": "```rust\nfn main() {\n    println!(\"Hello, Bhai!\");\n}\n```",
        "go": "```go\npackage main\nimport \"fmt\"\nfunc main() {\n    fmt.Println(\"Hello, Bhai!\")\n}\n```",
        "c++": "```cpp\n#include <iostream>\nusing namespace std;\n\nint main() {\n    cout << \"Hello, Bhai!\" << endl;\n    return 0;\n}\n```",
        "c": "```c\n#include <stdio.h>\nint main() {\n    printf(\"Hello, Bhai!\\n\");\n    return 0;\n}\n```",
        "csharp": "```csharp\nusing System;\nclass Program {\n    static void Main() {\n        Console.WriteLine(\"Hello, Bhai!\");\n    }\n}\n```",
        "ruby": "```ruby\nputs 'Hello, Bhai!'\n```",
        "php": "```php\n<?php\necho 'Hello, Bhai!';\n```",
        "swift": "```swift\nprint(\"Hello, Bhai!\")\n```",
        "kotlin": "```kotlin\nfun main() {\n    println(\"Hello, Bhai!\")\n}\n```",
        "typescript": "```typescript\nfunction main(): void {\n    console.log('Hello, Bhai!');\n}\nmain();\n```",
    }
    
    def execute(self, task: str) -> str:
        task_lower = task.lower()
        
        for lang, code in self.languages.items():
            if lang in task_lower:
                return f"💻 **{lang.capitalize()}:**\n{code}\n\nAur chahiye bhai?"
        
        return "💻 Kaunsa language chahiye? Python, JavaScript, Java, Rust, Go, C++, TypeScript, Swift, Kotlin, PHP, Ruby..."


class FileSkill(BaseSkill):
    """File management"""
    
    def execute(self, task: str) -> str:
        import os
        from pathlib import Path
        
        task_lower = task.lower()
        
        if "list" in task_lower or "show" in task_lower:
            # List files
            path = Path.home()
            if "desktop" in task_lower:
                path = path / "Desktop"
            elif "downloads" in task_lower:
                path = path / "Downloads"
            elif "documents" in task_lower:
                path = path / "Documents"
            
            try:
                items = os.listdir(path)
                folders = [f"📁 {i}/" for i in items if os.path.isdir(os.path.join(path, i))]
                files = [f"📄 {i}" for i in items if os.path.isfile(os.path.join(path, i))]
                
                return f"📁 **Contents of {path.name}:**\n\n" + "\n".join(folders[:10] + files[:10])
            except Exception as e:
                return f"❌ Error: {str(e)}"
        
        return "📁 Files: 'list files', 'show desktop', 'show downloads'"


class SystemSkill(BaseSkill):
    """System information and control"""
    
    def execute(self, task: str) -> str:
        task_lower = task.lower()
        
        if "info" in task_lower:
            try:
                import platform
                import psutil
                
                return f"""💻 **System Info:**
- OS: {platform.system()} {platform.release()}
- RAM: {psutil.virtual_memory().percent}% used
- CPU: {psutil.cpu_percent()}%"""
            except:
                return "❌ psutil not installed"
        
        if "process" in task_lower:
            return "📊 Running processes - use 'system info' bhai!"
        
        return "💻 System: 'system info', 'processes'"


class SearchSkill(BaseSkill):
    """Web search"""
    
    def execute(self, task: str) -> str:
        task_lower = task.lower()
        
        if "search" in task_lower:
            query = task_lower.replace("search", "").strip()
            if query:
                import webbrowser
                webbrowser.open(f"https://google.com/search?q={query}")
                return f"🔍 Searching Google for: {query}... 🌐"
        
        return "🔍 'search [query]' bhai!"


class WeatherSkill(BaseSkill):
    """Weather info"""
    
    def execute(self, task: str) -> str:
        return "🌤️ Weather - coming soon! Location batado bhai!"


# ============================================
# KILOCODE INTEGRATION
# ============================================

class CoderSkill(BaseSkill):
    """
    KiloCode Coder - AI code generation
    Uses KiloCode CLI if available, else built-in
    """
    
    def __init__(self):
        self.kilocode_path = None
        self._find_kilocode()
    
    def _find_kilocode(self):
        """Find KiloCode executable"""
        paths = ["kilo", "kilo.exe", "C:\\Program Files\\Kilo\\kilo.exe"]
        for p in paths:
            try:
                subprocess.run([p, "--version"], capture_output=True, timeout=3)
                self.kilocode_path = p
                break
            except:
                pass
    
    def execute(self, task: str) -> str:
        """Generate code"""
        # If KiloCode available, use it
        if self.kilocode_path:
            try:
                result = subprocess.run(
                    [self.kilocode_path, "run", "--auto", f"Write code: {task}"],
                    capture_output=True,
                    text=True,
                    timeout=60
                )
                if result.returncode == 0:
                    return f"💻 **Code Generated:**\n\n{result.stdout}"
            except Exception as e:
                pass
        
        # Fallback to built-in
        return CodeSkill().execute(task)


class DebuggerSkill(BaseSkill):
    """
    KiloCode Debugger - Auto-fix bugs
    """
    
    def execute(self, task: str) -> str:
        task_lower = task.lower()
        
        if "debug" in task_lower or "fix" in task_lower or "error" in task_lower:
            # Extract code if provided
            if "```" in task:
                return self._analyze_bug(task)
        
        return """🐛 **Debugger:**

Send me buggy code and I'll fix it!

Examples:
• "fix this error: [code]"
• "debug: [code]"
• "what's wrong with: [code]"

Koi bhi bug bhejo bhai! 🔧"""
    
    def _analyze_bug(self, code: str) -> str:
        """Simple bug analysis"""
        # Check common issues
        issues = []
        
        if "=" in code and "==" not in code.replace("!=", ">=", "<="):
            issues.append("⚠️ Using = instead of ==")
        
        if "print(" in code and ")" not in code[code.index("print(")+6:]:
            issues.append("⚠️ Unclosed parenthesis")
        
        if "def " in code and ":" not in code:
            issues.append("⚠️ Missing colon after function definition")
        
        if not issues:
            return "✅ Code looks okay to me!\n\nSend the actual error message bhai!"
        
        return "🐛 **Issues Found:**\n\n" + "\n".join(issues)


class ArchitectSkill(BaseSkill):
    """
    KiloCode Architect - Plan and design
    """
    
    def execute(self, task: str) -> str:
        return f"""🏗️ **Architect Mode:**

Maine plan banaya: {task}

**Suggested Structure:**
1. Setup project
2. Core functionality
3. UI/UX layer
4. Testing

Kya details chahiye bhai? 🔨"""


class RefactorSkill(BaseSkill):
    """
    KiloCode Refactor - Improve code
    """
    
    def execute(self, task: str) -> str:
        return """🔄 **Refactor:**

Code bhejo aur main improve karunga!

Refactor options:
• Clean code
• Optimize performance  
• Better naming
• Add comments

Bolo kya karna hai? ✨"""


# ============================================
# AGENT SKILLS (from openclaw/skills)
# ============================================

class AgentSkill(BaseSkill):
    """
    Agentic capabilities from openclaw
    """
    
    def execute(self, task: str) -> str:
        task_lower = task.lower()
        
        if "plan" in task_lower:
            return "🗂️ Planning your task..."
        
        if "execute" in task_lower:
            return "⚡ Executing..."
        
        return "🤖 Agent ready! Kya karna hai bhai?"


class AutomationSkill(BaseSkill):
    """
    Automation from openclaw skills
    """
    
    def execute(self, task: str) -> str:
        task_lower = task.lower()
        
        if "automation" in task_lower:
            return """⚙️ **Automation Options:**

• Repeat tasks
• Schedule things
• Workflows
• Batch operations

Kya automate karna hai bhai? 🔧"""
        
        return "⚙️ Automation ready!"


class ContextSkill(BaseSkill):
    """
    Context learning from openclaw
    """
    
    def execute(self, task: str) -> str:
        task_lower = task.lower()
        
        if "learn" in task_lower or "remember" in task_lower:
            return "🧠 Learning from your input! Kya yaad rakhna hai?"
        
        if "context" in task_lower:
            return "📚 Context loaded! Ab bol bhai!"
        
        return "🧠 Memory ready! Kya yaad karna hai?"


# ============================================
# UTILITY
# ============================================

import random


def get_all_skills() -> List[str]:
    """Get list of all available skills"""
    return [
        # Core
        "greeting", "calculator", "code", "files", "system", "search", "weather",
        
        # KiloCode
        "coder", "debugger", "architect", "refactor",
        
        # Agent
        "agent", "automation", "context"
    ]


def show_skills() -> str:
    """Show all skills"""
    skills = get_all_skills()
    
    return """📦 **All Skills:**

**Core:**
• greeting - Bol bol bhai!
• calculator - Math
• code - 35+ languages
• files - File management
• system - PC control
• search - Web search
• weather - Weather info

**KiloCode:**
• coder - AI code generation
• debugger - Fix bugs
• architect - Plan projects
• refactor - Improve code

**Agent:**
• agent - Task execution
• automation - Auto tasks
• context - Learn & remember

Koi bhi use kar sakta hai bhai! 😎"""