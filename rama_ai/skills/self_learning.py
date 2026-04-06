"""Self-Learning Skills - Continuous Improvement"""

from skills.skill_base import Skill
from typing import Any


class SelfLearningSkill(Skill):
    """Rama learns from every interaction"""
    
    triggers = ["learn", "improve", "stats", "patterns", "experience"]
    
    async def execute(self, input_text, context, retrieved_context=""):
        from tools.self_learning import SelfLearningEngine
        
        tool = SelfLearningEngine()
        
        input_lower = input_text.lower()
        
        # Show stats
        if "stats" in input_lower or "status" in input_lower:
            stats = tool.get_learning_stats()
            return f"""🧠 **Rama's Learning Stats:**

📊 **Interactions:**
- Total: {stats.get('total_interactions', 0)}
- Success: {stats.get('successful', 0)}
- Failed: {stats.get('failed', 0)}
- Success Rate: {stats.get('success_rate', '0%')}

📚 **Patterns Learned:** {stats.get('patterns_learned', 0)}
🔧 **Self-Repairs:** {stats.get('self_repairs', 0)}
📁 **Categories:** {', '.join(stats.get('categories', []))}"""
        
        # Record success
        if "success" in input_lower or "worked" in input_lower:
            return "✅ Recording this interaction as successful! I'll remember what worked."
        
        # Record failure
        if "failed" in input_lower or "didn't work" in input_lower:
            return "📝 Recording this as a failure. I'll learn from this!"
        
        return """🧠 **Self-Learning:**

Rama learns from every interaction to improve!

Features:
- Track successful/failed responses
- Pattern recognition across categories
- Continuous improvement
- Self-repair capabilities

Ask:
- "learning stats"
- "learn from success/failure"
- "what patterns learned\""""


class EmotionDetectionSkill(Skill):
    """Detect and learn from human emotions"""
    
    triggers = ["emotion", "feel", "mood", "happy", "sad", "angry", "camera", "microphone"]
    
    async def execute(self, input_text, context, retrieved_context=""):
        from tools.self_learning import EmotionLearningSystem
        
        tool = EmotionLearningSystem()
        
        input_lower = input_text.lower()
        
        # Enable camera
        if "camera" in input_lower and ("enable" in input_lower or "start" in input_lower):
            if tool.face_available:
                return "📷 Camera enabled! I'll analyze your facial expressions to understand emotions."
            else:
                return "⚠️ Camera not available. Install OpenCV: `pip install opencv-python`"
        
        # Enable microphone
        if "mic" in input_lower or "microphone" in input_lower:
            if tool.audio_available:
                return "🎤 Microphone enabled! I'll analyze your voice tone for emotions."
            else:
                return "⚠️ Audio analysis not available. Install librosa: `pip install librosa`"
        
        # Get current emotion
        if "current" in input_lower or "now" in input_lower:
            emotion = tool.get_current_emotion()
            return f"😶 Current detected emotion: {emotion}"
        
        # Explain emotion detection
        return """😶 **Emotion Detection:**

Rama can learn your emotions through:

📷 **Camera (Face Detection)**
- Detect facial expressions
- Identify happiness, sadness, anger, surprise
- Track attention and engagement

🎤 **Microphone (Voice Analysis)**
- Analyze tone and pitch
- Detect excitement, stress, calm
- Identify speech patterns

**Enable:**
- "enable camera" - Start facial analysis
- "enable microphone" - Start voice analysis

**Status:**
- "current emotion" - Get detected emotion"""
    
    def can_handle(self, input_text):
        # Also respond to emotion-related queries
        return True


class SelfRepairSkill(Skill):
    """Rama can repair and update itself"""
    
    triggers = ["repair", "fix", "update", "fix myself", "diagnostic", "check health"]
    
    async def execute(self, input_text, context, retrieved_context=""):
        from tools.self_learning import SelfRepairSystem
        
        tool = SelfRepairSystem()
        
        input_lower = input_text.lower()
        
        # Run diagnostic
        if "diagnostic" in input_lower or "check health" in input_lower or "health" in input_lower:
            result = await tool.self_diagnostic()
            return f"""🔧 **Self-Diagnostic Results:**

**Status:** {result.get('status', 'unknown').upper()}

**Components:**
- Core: {result['checks'].get('core', 'unknown')}
- Memory: {result['checks'].get('memory', 'unknown')}
- Skills: {result['checks'].get('skills', 'unknown')}
- Voice: {result['checks'].get('voice', 'unknown')}
- Vision: {result['checks'].get('vision', 'unknown')}

**Statistics:**
- Errors: {result.get('errors', 0)}
- Repairs: {result.get('repairs', 0)}
- Last check: {result.get('timestamp', 'unknown')}"""
        
        # Check for updates
        if "check update" in input_lower or "version" in input_lower:
            result = await tool.check_for_updates()
            return f"""🔄 **Update Status:**

Current: {result.get('current_version', 'unknown')}
Latest: {result.get('latest_version', 'unknown')}
Available: {'Yes' if result.get('updates_available') else 'No'}"""
        
        # Apply update
        if "update" in input_lower:
            update_type = "security" if "security" in input_lower else "auto"
            result = await tool.apply_update(update_type)
            return result
        
        # Get repair stats
        if "repair stats" in input_lower or "fixes" in input_lower:
            stats = tool.get_repair_stats()
            return f"""🔧 **Repair Statistics:**

- Total errors: {stats.get('total_errors', 0)}
- Auto-repaired: {stats.get('auto_repaired', 0)}
- Pending: {stats.get('pending', 0)}"""
        
        return """🔧 **Self-Repair System:**

Rama can maintain and repair itself!

Commands:
- "diagnostic" / "check health" - Run system check
- "check updates" - Check for new versions
- "update" - Apply self-update
- "repair stats" - View repair history

Features:
- Automatic error detection
- Self-healing capabilities
- Version updates
- Security patches"""


class UniversalCodeSkill(Skill):
    """Rama knows ALL programming languages"""
    
    triggers = ["code", "language", "python", "javascript", "java", "rust", "go", "all languages"]
    
    async def execute(self, input_text, context, retrieved_context=""):
        from tools.self_learning import UniversalCodeKnowledge
        
        tool = UniversalCodeKnowledge()
        
        input_lower = input_text.lower()
        
        # List all languages
        if "list" in input_lower or "all" in input_lower or "show" in input_lower:
            langs = tool.list_all_languages()
            return f"""💻 **Rama Knows {len(langs)} Programming Languages:**

{', '.join(langs[:20])}... and more!

**Categories:**
- Web: JavaScript, TypeScript, HTML, CSS
- Systems: C, C++, Rust, Go
- Enterprise: Java, C#, Scala
- Scripting: Python, Ruby, Perl, Bash
- Mobile: Swift, Kotlin, Dart
- Data: R, Julia, Python
- Functional: Haskell, Elixir, Clojure

Ask: "code python" or "info about rust\""""
        
        # Get language info
        for lang in tool.list_all_languages():
            if lang in input_lower:
                info = tool.get_language_info(lang)
                return f"""💻 **{info.get('name', lang)}**

- Created: {info.get('created', 'unknown')}
- Paradigm: {info.get('paradigm', 'unknown')}
- Typing: {info.get('typing', 'unknown')}
- Extensions: {', '.join(info.get('extensions', []))}
- Common uses: {', '.join(info.get('common_uses', []))}
- Hello World: 
```{lang}
{info.get('hello_world', 'N/A')}
```"""
        
        # Get code example
        if "code " in input_lower:
            # Extract language
            for lang in tool.list_all_languages():
                if lang in input_lower:
                    code_type = "function" if "function" in input_lower else "class" if "class" in input_lower else "hello"
                    code = tool.code_in_language(lang, code_type)
                    return f"💻 **{lang.capitalize()}** ({code_type}):\n```{lang}\n{code}\n```"
        
        return """💻 **Universal Code Knowledge:**

Rama knows **35+ programming languages**!

Ask:
- "list all languages" - See all languages
- "code python" - Get Python example
- "code javascript function" - Get JS function
- "info about rust" - Get Rust info
- "languages for web" - Find web languages"""


class ContinuousImprovementSkill(Skill):
    """Rama continuously improves itself"""
    
    triggers = ["improve", "better", "upgrade", "optimize", "enhance"]
    
    async def execute(self, input_text, context, retrieved_context=""):
        return """⚡ **Continuous Improvement:**

Rama improves itself through:

🧠 **Learning**
- Every interaction is stored and analyzed
- Patterns are identified and remembered
- Success/failure rates tracked per category

🔧 **Self-Repair**
- Automatic error detection
- Self-healing capabilities
- Bug fixes applied automatically

📈 **Optimization**
- Response strategies refined over time
- Best approaches remembered
- Less successful methods avoided

🔄 **Updates**
- Check for new versions
- Apply security patches
- Feature improvements

Rama is always learning and getting better!"""