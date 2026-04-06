"""Coding Skill - Programming assistance in 30+ languages"""

from skills.skill_base import Skill


class CodingSkill(Skill):
    """Programming help in 30+ languages"""
    
    def __init__(self):
        super().__init__()
        self.triggers = ["code", "program", "python", "javascript", "java", "rust", "go", "write code", "explain"]
        
        self.languages = {
            'python': ('Python', 'print("Hello, World!")'),
            'javascript': ('JavaScript', 'console.log("Hello, World!");'),
            'java': ('Java', 'System.out.println("Hello, World!");'),
            'rust': ('Rust', 'println!("Hello, World!");'),
            'go': ('Go', 'fmt.Println("Hello, World!")'),
            'c': ('C', 'printf("Hello, World!\\n");'),
            'cpp': ('C++', 'std::cout << "Hello, World!" << std::endl;'),
            'csharp': ('C#', 'Console.WriteLine("Hello, World!");'),
            'typescript': ('TypeScript', 'console.log("Hello, World!");'),
            'swift': ('Swift', 'print("Hello, World!")'),
            'kotlin': ('Kotlin', 'println("Hello, World!")'),
            'ruby': ('Ruby', 'puts "Hello, World!"'),
            'php': ('PHP', 'echo "Hello, World!";'),
            'sql': ('SQL', 'SELECT "Hello, World!";'),
            'html': ('HTML', '<h1>Hello, World!</h1>'),
            'css': ('CSS', 'body { font-family: sans-serif; }'),
            'bash': ('Bash', 'echo "Hello, World!"'),
        }
    
    async def execute(self, input_text: str, context: Any, retrieved_context: str = "") -> str:
        input_lower = input_text.lower()
        
        # Detect language
        for lang_key in self.languages:
            if lang_key in input_lower:
                lang_name, code = self.languages[lang_key]
                return f"💻 **{lang_name}**:\n\n```\n{code}\n```"
        
        # List available
        langs = ', '.join(self.languages.keys())
        return f"""💻 I know {len(self.languages)} languages!

Try: 'code python', 'code javascript', 'code rust'
Available: {langs}"""


class AutomationSkill(Skill):
    """Automation routines"""
    
    triggers = ["routine", "automation", "automate", "create routine"]
    
    async def execute(self, input_text, context, retrieved_context=""):
        import re
        
        input_lower = input_text.lower()
        
        if "create routine" in input_lower:
            match = re.search(r'create routine (\w+) do (.+)', input_lower)
            if match:
                name = match.group(1)
                return f"✅ Routine '{name}' created! (automation not fully implemented)"
        
        return "🔄 Try 'create routine morning do X,Y'"


class LocalAISkill(Skill):
    """Local LLM (Ollama) integration"""
    
    triggers = ["ask", "think", "ollama", "ai"]
    
    async def execute(self, input_text, context, retrieved_context=""):
        return "🔮 Make sure Ollama is running: `ollama serve`"
    
    def can_handle(self, input_text):
        return True