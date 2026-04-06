"""Enhanced Brain - Smarter, Cleverer, More Intelligent"""

import asyncio
import random
from typing import Dict, Any, Optional, List
from datetime import datetime


class EnhancedBrain:
    """
    Ultra-intelligent AI Brain
    Smarter context understanding, better reasoning, clever responses
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.context = EnhancedContext()
        self.knowledge_base = KnowledgeBase()
        self.reasoning_engine = ReasoningEngine()
        self.conversation_learner = ConversationLearner()
        self.personality = PersonalityEngine()
        self.error_handler = ErrorHandler()
        
    async def initialize(self):
        """Initialize enhanced brain"""
        print("🧠 Initializing Enhanced RAMA Brain...")
        
        # Initialize knowledge base with common facts
        await self.knowledge_base.load_common_knowledge()
        
        # Initialize conversation learner
        await self.conversation_learner.initialize()
        
        print("✅ Enhanced Brain initialized!")
    
    async def process(self, user_input: str, context: Optional[Dict] = None) -> str:
        """Process input with enhanced intelligence"""
        
        # 1. Analyze input for intent and entities
        analysis = await self.reasoning_engine.analyze(user_input)
        
        # 2. Retrieve relevant knowledge
        knowledge = await self.knowledge_base.query(user_input)
        
        # 3. Get conversation context
        conversation_context = self.context.get_context()
        
        # 4. Learn from this interaction
        await self.conversation_learner.record(user_input, "")
        
        # 5. Generate intelligent response
        response = await self._generate_response(
            user_input=user_input,
            analysis=analysis,
            knowledge=knowledge,
            context=conversation_context
        )
        
        # 6. Record successful interaction
        await self.conversation_learner.record_success(user_input, response)
        
        # 7. Update context
        self.context.add_message("user", user_input)
        self.context.add_message("assistant", response)
        
        return response
    
    async def _generate_response(self, user_input: str, analysis: Dict, 
                                   knowledge: List[str], context: str) -> str:
        """Generate intelligent response based on analysis"""
        
        intent = analysis.get("intent", "general")
        entities = analysis.get("entities", [])
        sentiment = analysis.get("sentiment", "neutral")
        
        # Check if we have knowledge about this
        if knowledge:
            return f"{self.personality.get_response(intent)}\n\n💡 {knowledge[0]}"
        
        # Handle specific intents
        if intent == "greeting":
            return self.personality.greet()
        
        if intent == "question":
            # Try to answer from knowledge base
            answer = await self.knowledge_base.answer_question(user_input)
            if answer:
                return f"{self.personality.get_thoughtful_response()}\n\n{answer}"
            return self._smart_fallback(user_input)
        
        if intent == "code":
            return await self._handle_code_request(user_input)
        
        if intent == "calculate":
            return await self._handle_math(user_input)
        
        if intent == "system":
            return await self._handle_system(user_input)
        
        if intent == "help":
            return self._get_help()
        
        # Default clever response
        return self._smart_fallback(user_input)
    
    def _smart_fallback(self, user_input: str) -> str:
        """Generate clever fallback for unknown queries"""
        cleverness = [
            "Interesting question! 🤔 Here's what I think...\n\n",
            "That's a thought-provoking query! 💭 Let me share my perspective...\n\n",
            "I love your curiosity! 🌟 Here's my take...\n\n",
            "You've got me thinking! 🤔 Here's my response...\n\n",
        ]
        
        responses = [
            f"I'm Rama, your AI assistant! I can help with coding, math, system tasks, and much more. Try asking about:\n\n"
            f"• Code in 35+ languages\n• Math calculations\n• System information\n• File management\n• Learning and analysis\n\n"
            f"What would you like to explore?",
            
            f"That's a fascinating question! 🌟 While I don't have a specific answer for that, I can help you with:\n\n"
            f"• Writing or debugging code\n• Calculating complex math\n• Managing files and apps\n• Analyzing and explaining concepts\n\n"
            f"What can I assist you with?",
            
            f"Hmm, that's outside my immediate knowledge, but I'm eager to help! 🎯\n\n"
            f"I specialize in:\n"
            f"• Programming in any language\n• Math and calculations\n• System operations\n• File management\n• Learning and adapting\n\n"
            f"What would you like to try?"
        ]
        
        return random.choice(cleverness) + random.choice(responses)
    
    async def _handle_code_request(self, user_input: str) -> str:
        """Handle code-related requests"""
        # Extract language
        languages = ["python", "javascript", "java", "rust", "go", "c++", "c", "ruby", "php", "typescript", 
                     "swift", "kotlin", "scala", "html", "css", "sql", "bash", "powershell"]
        
        found_lang = None
        for lang in languages:
            if lang in user_input.lower():
                found_lang = lang
                break
        
        if found_lang:
            return self._get_code_example(found_lang)
        return "💻 What programming language would you like to learn about? I know 35+ languages!"
    
    def _get_code_example(self, lang: str) -> str:
        examples = {
            "python": "```python\n# Python Example\ndef greet(name):\n    return f'Hello, {name}! Welcome to Python.'\n\nprint(greet('World'))\n```",
            "javascript": "```javascript\n// JavaScript Example\nconst greet = (name) => {\n    return `Hello, ${name}! Welcome to JS.`;\n};\n\nconsole.log(greet('World'));\n```",
            "rust": "```rust\n// Rust Example\nfn main() {\n    let name = \"World\";\n    println!(\"Hello, {}! Welcome to Rust.\", name);\n}\n```",
            "go": "```go\n// Go Example\npackage main\n\nimport \"fmt\"\n\nfunc main() {\n    name := \"World\"\n    fmt.Printf(\"Hello, %s! Welcome to Go.\\n\", name)\n}\n```",
            "java": "```java\n// Java Example\npublic class Main {\n    public static void main(String[] args) {\n        String name = \"World\";\n        System.out.println(\"Hello, \" + name + \"! Welcome to Java.\");\n    }\n}\n```",
        }
        
        return f"💻 **{lang.capitalize()}** Example:\n\n{examples.get(lang, f'Here is {lang} code!')}\n\nWant to see more? Ask for a function or class!"
    
    async def _handle_math(self, user_input: str) -> str:
        """Handle math calculations"""
        import re
        
        # Extract expression
        expr = re.sub(r'[^0-9+\-*/().=% ]', '', user_input)
        
        if not expr:
            return "🧮 Provide a math expression to calculate!\n\nExample: calculate (15+25)*3 or 2^10"
        
        try:
            result = eval(expr)
            return f"🧮 **Calculation:**\n\n`{expr}` = **{result}**\n\n✨ Want me to do more complex math?"
        except:
            return "🧮 I couldn't parse that expression. Try simpler format!\n\nExample: calculate 2 + 2 or (10 * 5) / 2"
    
    async def _handle_system(self, user_input: str) -> str:
        """Handle system requests"""
        try:
            import psutil
            
            if "cpu" in user_input.lower():
                return f"⚡ **CPU:** {psutil.cpu_count()} cores, {psutil.cpu_percent()}% used"
            
            if "memory" in user_input.lower() or "ram" in user_input.lower():
                mem = psutil.virtual_memory()
                return f"🧠 **RAM:** {mem.percent}% used ({mem.used/1024**3:.1f}/{mem.total/1024**3:.1f} GB)"
            
            if "disk" in user_input.lower():
                disk = psutil.disk_usage('/')
                return f"💾 **Disk:** {disk.percent}% used"
            
            if "info" in user_input.lower():
                import platform
                return f"💻 **System:** {platform.system()} {platform.release()}\nNode: {platform.node()}"
            
        except ImportError:
            pass
        
        return "💻 System info available when psutil is installed!\n\nTry: system info, cpu, memory, or disk"
    
    def _get_help(self) -> str:
        return """🤖 **RAMA AI - Your Intelligent Assistant**

**What I can do:**

💻 **Coding**
- Write code in 35+ languages
- Debug and fix errors
- Explain code concepts
- Example: "code python", "debug this"

🧮 **Math**
- Calculate expressions
- Example: "calculate 2+2*10"

📁 **Files**
- List files, create folders
- Example: "list files", "create folder"

💻 **System**
- Get system info, processes
- Launch apps, run commands
- Example: "cpu info", "open notepad"

🧠 **Learning**
- Learn from conversations
- Remember facts
- Improve over time

🌐 **Search**
- Search the web
- Example: "search Python"

🎙️ **Voice**
- Voice input/output (optional)

**Just ask me anything!**"""


class EnhancedContext:
    """Enhanced context with smarter memory"""
    
    def __init__(self):
        self.messages = []
        self.important_info = {}
    
    def add_message(self, role: str, content: str):
        self.messages.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
        
        # Extract important info
        self._extract_important_info(content, role)
        
        # Keep last 50 messages
        if len(self.messages) > 50:
            self.messages = self.messages[-50:]
    
    def _extract_important_info(self, content: str, role: str):
        """Extract important info like names, preferences"""
        if role != "user":
            return
        
        # Simple pattern matching for important info
        import re
        
        # Name patterns
        name_match = re.search(r'my name is (\w+)', content.lower())
        if name_match:
            self.important_info["name"] = name_match.group(1)
        
        # Favorite patterns
        fav_match = re.search(r'favorite is (\w+)', content.lower())
        if fav_match:
            self.important_info["favorite"] = fav_match.group(1)
    
    def get_context(self) -> str:
        return "\n".join(f"{m['role']}: {m['content'][:100]}" for m in self.messages[-10:])


class KnowledgeBase:
    """Smart knowledge base with common facts"""
    
    def __init__(self):
        self.facts = {}
        self.qa_pairs = {}
    
    async def load_common_knowledge(self):
        """Load common knowledge"""
        self.facts = {
            "who are you": "I'm RAMA, an intelligent AI assistant!",
            "what are you": "I'm RAMA - an AI that learns, helps with coding, math, and much more!",
            "your name": "I'm RAMA! Your personal AI assistant.",
            "python": "Python is a versatile programming language known for simplicity and readability.",
            "javascript": "JavaScript is the language of the web - used for websites, servers, and apps!",
            "rust": "Rust is a systems programming language focused on safety and performance.",
            "ai": "Artificial Intelligence is the simulation of human intelligence by machines!",
            "machine learning": "Machine Learning is AI that learns from data to make predictions!",
            "github": "GitHub is a platform for version control and collaboration!",
            "git": "Git is a version control system for tracking code changes!",
        }
        
        self.qa_pairs = {
            "hello": ["Hey there! 👋 How can I help?", "Yo! ✨ What's up?", "Hi! 🎉 Ready to help!"],
            "hi": ["Hey! 👋 What's on your mind?", "Hi there! ✨", "Yo! 🔥 What's up?"],
            "how are you": ["I'm doing great! Thanks for asking! 😄", "Fantastic! ✨ Ready to help!", "Wonderful! 🎉 How can I assist?"],
            "thanks": ["You're welcome! 😊 Anything else?", "No problem! 🌟 Happy to help!", "Glad I could help! 💫"],
        }
    
    async def query(self, text: str) -> List[str]:
        """Query knowledge base"""
        text_lower = text.lower()
        results = []
        
        for key, value in self.facts.items():
            if key in text_lower:
                results.append(value)
        
        return results
    
    async def answer_question(self, question: str) -> Optional[str]:
        """Answer questions from knowledge"""
        question_lower = question.lower()
        
        # Check qa_pairs
        for q, answers in self.qa_pairs.items():
            if q in question_lower:
                return random.choice(answers)
        
        # Check facts
        for key, value in self.facts.items():
            if key in question_lower:
                return value
        
        return None


class ReasoningEngine:
    """Engine for analyzing and reasoning about user input"""
    
    def __init__(self):
        self.intent_patterns = {
            "greeting": ["hello", "hi", "hey", "good morning", "howdy"],
            "question": ["what", "how", "why", "when", "where", "who", "which", "?"],
            "code": ["code", "program", "function", "class", "write", "debug", "syntax"],
            "calculate": ["calculate", "compute", "math", "+", "-", "*", "/", "^", "="],
            "system": ["system", "cpu", "memory", "ram", "disk", "process", "info"],
            "file": ["file", "folder", "directory", "list", "create", "delete"],
            "search": ["search", "find", "google", "look up"],
            "help": ["help", "commands", "what can you do"],
            "learn": ["learn", "remember", "know", "teach me"],
            "emotion": ["feel", "happy", "sad", "angry", "emotion"],
        }
    
    async def analyze(self, text: str) -> Dict:
        """Analyze text for intent and entities"""
        text_lower = text.lower()
        
        # Detect intent
        intent = "general"
        for intent_name, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if pattern in text_lower:
                    intent = intent_name
                    break
        
        # Detect entities (simple)
        entities = []
        common_entities = ["python", "javascript", "java", "rust", "go", "windows", "linux"]
        for entity in common_entities:
            if entity in text_lower:
                entities.append(entity)
        
        # Detect sentiment (simple)
        sentiment = "neutral"
        positive_words = ["great", "awesome", "love", "thanks", "good", "amazing"]
        negative_words = ["bad", "hate", "wrong", "error", "fail", "broken"]
        
        for word in positive_words:
            if word in text_lower:
                sentiment = "positive"
        for word in negative_words:
            if word in text_lower:
                sentiment = "negative"
        
        return {
            "intent": intent,
            "entities": entities,
            "sentiment": sentiment,
            "original": text
        }


class ConversationLearner:
    """Learn from conversations to improve"""
    
    def __init__(self):
        self.history = []
        self.successes = {}
    
    async def initialize(self):
        """Initialize"""
        pass
    
    async def record(self, user_input: str, response: str):
        """Record conversation"""
        self.history.append({
            "input": user_input,
            "response": response,
            "timestamp": datetime.now().isoformat()
        })
        
        # Keep last 100
        if len(self.history) > 100:
            self.history = self.history[-100:]
    
    async def record_success(self, input_text: str, response: str):
        """Record successful interaction"""
        # Extract first few words as pattern
        key = " ".join(input_text.lower().split()[:2])
        
        if key not in self.successes:
            self.successes[key] = 0
        self.successes[key] += 1


class PersonalityEngine:
    """Engine for personality and clever responses"""
    
    def __init__(self):
        self.greetings = [
            "Well, well... look who's awake! 👀",
            "Hey there, superstar! ✨",
            "Yo! Ready to rock? 🚀",
            "Hello, human! 😄 What can I do for you?",
            "Ah, our paths cross again! 🌟",
        ]
        
        self.thoughtful = [
            "💭 Let me think about that...",
            "🤔 Interesting question...",
            "✨ Great thinking!",
            "🌟 You've got my attention!",
            "💡 Here's my take...",
        ]
    
    def greet(self) -> str:
        return random.choice(self.greetings)
    
    def get_response(self, intent: str) -> str:
        return random.choice(self.thoughtful)
    
    def get_thoughtful_response(self) -> str:
        return random.choice(self.thoughtful)


class ErrorHandler:
    """Handle errors gracefully"""
    
    async def handle(self, error: Exception, context: str) -> str:
        """Handle error and provide helpful response"""
        return f"Oops! Something went wrong: {str(error)[:100]}...\n\nBut don't worry, I'm still here! 🎉\nTry again or ask something else!"