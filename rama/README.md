# 📖 RAMA AI - Complete Documentation Guide

## Table of Contents
1. [Overview](#overview)
2. [Features](#features)
3. [Installation Guide](#installation-guide)
4. [Commands Reference](#commands-reference)
5. [Architecture](#architecture)
6. [Customization](#customization)
7. [Future Improvements](#future-improvements)

---

## 🌟 Overview

**Rama** is a self-learning AI assistant built with Python that runs 100% offline. It features a sassy personality, learns from every interaction, and can be extended with custom skills.

### Key Highlights
- 🎭 **Sassy Personality** - Witty, helpful, with attitude
- 🧠 **Self-Learning** - SQLite database learns patterns
- 🔒 **100% Local** - No cloud, no API keys needed
- 🛠️ **Extensible** - Build custom skills easily
- 🎙️ **Voice Ready** - Optional TTS/STT support

---

## 🎯 Features

### Core Features

| Feature | Description | Status |
|---------|-------------|--------|
| **Self-Learning** | SQLite database tracks interactions, learns patterns | ✅ |
| **Personality Engine** | Sassy responses, mood tracking, witty remarks | ✅ |
| **Skill System** | 16 built-in skills + custom skill support | ✅ |
| **Memory** | Short-term (conversation) + long-term (SQLite) | ✅ |
| **Link Analysis** | Detect technologies, analyze URLs | ✅ |
| **Ollama Integration** | Local LLM AI (optional) | ✅ |
| **Voice I/O** | TTS/STT support (optional) | ✅ |
| **System Tray** | Background operation | ✅ |

### Built-in Skills (16)

#### 🔧 System Skills
1. **App Launcher** - Launch Windows apps (open notepad, launch chrome)
2. **File Manager** - List, create, delete files/folders
3. **System Info** - CPU, memory, disk, network, uptime

#### 🌤️ Utility Skills
4. **Calculator** - Math calculations, conversions
5. **Weather** - Get weather for any location (wttr.in)
6. **Web Search** - Open browser with search query
7. **Notes** - Create, list, search, delete notes
8. **Reminders** - Set timed reminders

#### 🧠 AI & Learning Skills
9. **Greeting** - Friendly conversation
10. **Knowledge** - Learn and store facts (learn that X is Y)
11. **Profile** - User preferences and settings
12. **Automation** - Create and run routines
13. **Coding** - 30+ programming languages reference
14. **Link Analyzer** - Understand shared URLs
15. **Skill Creator** - Build new skills
16. **Local AI** - Ollama integration

### Technical Features

- **Python 3.8+** compatible
- **SQLite** for persistent learning
- **Async I/O** for performance
- **Modular architecture** - Easy to extend
- **CLI Interface** - Runs in terminal
- **Optional GUI** - Can integrate with WPF/Electron

---

## 📥 Installation Guide

### Prerequisites

```bash
# Python 3.8 or higher
python --version  # Should show 3.8+
```

### Step 1: Clone Repository

```bash
git clone https://github.com/Rishi114/rama.git
cd rama
```

### Step 2: Install Dependencies

```bash
# Core dependencies (required)
pip install aiohttp psutil

# Voice support (optional but recommended)
pip install pyttsx3 speech-recognition

# For better TTS (optional - online)
pip install gtts
```

### Step 3: Run Rama

```bash
# Basic run
python rama.py

# With voice (after installing pyttsx3)
# Just run - voice will auto-enable if available
```

### First Run

```
➤ Hello! I'm Rama - Your AI Assistant!

🎭 Personality: Sassy & self-learning
🧠 Self-Learning: Gets smarter every conversation!
🗄️ Memory: SQLite database for persistent learning

━━━━━━━━━━━━━━━━━━━━━━━━
📦 BUILT-IN SKILLS:
━━━━━━━━━━━━━━━━━━━━━━━━

🔧 System:
• App Launcher - Open apps
• File Manager - Manage files
• System Info - Computer diagnostics

🌤️ Utilities:
• Web Search, Weather, Notes
• Reminders, Calculator

🧠 AI & Learning:
• Knowledge, Profile, Automation
• Coding, Skill Creator, Local AI
```

---

## 📝 Commands Reference

### 🔧 System Commands

| Command | Description | Example |
|---------|-------------|---------|
| `open [app]` | Launch application | `open notepad` |
| `launch [app]` | Launch application | `launch chrome` |
| `list files [path]` | List directory contents | `list files Documents` |
| `create folder [name]` | Create new folder | `create folder Projects` |
| `delete file [path]` | Delete a file | `delete file temp.txt` |
| `open folder [name]` | Open in Explorer | `open folder Desktop` |
| `system info` | Full system info | `system info` |
| `cpu` | CPU information | `cpu` |
| `memory` | RAM usage | `memory` |
| `disk` | Disk space | `disk` |
| `uptime` | System uptime | `uptime` |
| `ip address` | Network info | `ip address` |

### 🌤️ Utility Commands

| Command | Description | Example |
|---------|-------------|---------|
| `weather [city]` | Get weather | `weather Tokyo` |
| `search [topic]` | Search web | `search Python tutorials` |
| `calculate [math]` | Math calculation | `calculate 2+2*3` |
| `note: [text]` | Create note | `note: buy groceries` |
| `list notes` | Show all notes | `list notes` |
| `remind me in [X] minutes to [task]` | Set reminder | `remind me in 10 minutes to call mom` |

### 🧠 AI & Learning Commands

| Command | Description | Example |
|---------|-------------|---------|
| `learn that [X] is [Y]` | Teach Rama a fact | `learn that coffee is hot` |
| `what is [X]?` | Ask learned fact | `what is coffee?` |
| `list knowledge` | Show all learned facts | `list knowledge` |
| `profile` | Show your profile | `profile` |
| `update profile [key] = [value]` | Update settings | `update profile name = John` |
| `create routine [name] do [steps]` | Create automation | `create routine morning do open browser, play music` |
| `run [routine]` | Execute routine | `run morning` |
| `list routines` | Show all routines | `list routines` |
| `code [language]` | Get code template | `code python` |
| `explain [language]` | Learn about language | `explain rust` |
| `skill template` | Get skill template | `skill template` |
| `create skill [name] that [description]` | Create new skill | `create skill JokeTeller that tells jokes` |

### 🎙️ Voice Commands

| Command | Description |
|---------|-------------|
| Say "hey rama" | Activate voice input |
| Voice responses | Rama speaks responses |

---

## 🏗️ Architecture

```
rama/
├── rama.py              # Main entry point
├── core/                # Core AI components
│   ├── brain.py         # Main processing engine
│   ├── learner.py       # Self-learning (SQLite)
│   ├── personality.py   # Sassy personality
│   ├── skill_manager.py # Skill loading/routing
│   ├── memory.py        # Conversation memory
│   ├── link_analyzer.py # URL analysis
│   ├── voice_manager.py # Voice I/O
│   ├── ollama_client.py # Local LLM
│   └── skill_base.py    # Skill interface
├── skills/              # Built-in skills (16)
│   ├── greeting.py
│   ├── calculator.py
│   ├── app_launcher.py
│   ├── file_manager.py
│   ├── system_info.py
│   ├── weather.py
│   ├── web_search.py
│   ├── note.py
│   ├── reminder.py
│   ├── knowledge.py
│   ├── profile.py
│   ├── automation.py
│   ├── coding.py
│   ├── link_skill.py
│   ├── skill_creator.py
│   └── local_ai.py
├── data/                # User data (auto-created)
│   ├── rama_learning.db # SQLite learning DB
│   ├── notes.json
│   ├── reminders.json
│   ├── knowledge.json
│   ├── profile.json
│   └── automations.json
└── requirements.txt     # Python dependencies
```

### Data Flow

```
User Input
    ↓
Brain.process()
    ↓
1. Check learned patterns (Learner)
    ↓
2. Find best skill (SkillManager)
    ↓
3. Execute skill → Response
    ↓
4. Learn from interaction (Learner)
    ↓
5. Add personality (PersonalityEngine)
    ↓
Response + Speak (VoiceManager)
```

---

## 🎨 Customization

### Customize Personality

Edit `core/personality.py`:

```python
# Adjust sass level (1-10)
self.sass_level = 7  # Default

# Change responses in _RESPONSES dict
```

### Add Custom Skill

1. Create file in `skills/my_skill.py`:

```python
from core.skill_base import SkillBase

class MySkill(SkillBase):
    @property
    def name(self) -> str:
        return "My Skill"
    
    @property
    def description(self) -> str:
        return "Does something cool"
    
    @property
    def triggers(self) -> list:
        return ["my trigger", "do something"]
    
    def can_handle(self, input_text: str) -> bool:
        return "my trigger" in input_text.lower()
    
    async def execute(self, input_text: str, memory) -> str:
        return "Hello from my custom skill!"
```

2. Add to `core/skill_manager.py` in `_load_skills()`:

```python
from skills.my_skill import MySkill
self.skills.append(MySkill())
```

3. Restart Rama

### Configure Profile

```bash
# Update settings
update profile name = YourName
update profile email = you@example.com
update profile location = YourCity
update profile voice = on
update profile wake_word = hey rama
```

---

## 🚀 Future Improvements

### Phase 1: Enhanced Core
- [ ] **Plugin System** - Load skills from external folders without code changes
- [ ] **Plugin Manager** - GUI to enable/disable skills
- [ ] **Event System** - React to system events (file changes, etc.)

### Phase 2: UI/UX
- [ ] **GUI Interface** - Web-based or Electron UI
- [ ] **Tray Icon** - System tray with menu
- [ ] **Dark/Light Theme** - UI customization
- [ ] **Animations** - Arc reactor style animations

### Phase 3: Integration
- [ ] **Smart Home** - MQTT, Home Assistant integration
- [ ] **Email** - Read/send emails locally
- [ ] **Calendar** - Google Calendar / local calendar
- [ ] **Notifications** - Read system notifications

### Phase 4: Advanced AI
- [ ] **Fine-tuned Model** - Custom trained model
- [ ] **RAG** - PDF/Document knowledge base
- [ ] **Voice Cloning** - Custom voice with Coqui/Respeecher
- [ ] **Multi-language** - Better translation

### Phase 5: Desktop Integration
- [ ] **Window Control** - Move/resize windows
- [ ] **Hotkeys** - Global keyboard shortcuts
- [ ] **Clipboard** - Monitor and act on clipboard
- [ ] **Screenshots** - OCR and analysis

### Suggestions & Ideas

1. **Context Awareness** - Remember previous conversations
2. **Task Planning** - Break complex tasks into steps
3. **Web Dashboard** - Control via browser
4. **Mobile App** - Control from phone
5. **Plugin Store** - Share skills with others
6. **Privacy Dashboard** - See what Rama has learned
7. **Export/Import** - Backup and restore settings
8. **Skill Ratings** - Rate skill responses
9. **Custom Wake Words** - Train custom wake words
10. **Offline Translation** - Use local translation models

---

## 🔧 Troubleshooting

### Voice Not Working
```bash
pip install pyttsx3
# Or for online TTS:
pip install gtts
```

### Ollama Not Detected
```bash
# Install Ollama from ollama.ai
ollama serve
# Rama auto-detects on restart
```

### Database Errors
```bash
# Delete learning database to reset
rm -rf ~/.rama/data/rama_learning.db
```

### Port Already in Use
```bash
# Check what's using the port
lsof -i :11434
```

---

## 📄 License

**MIT License** - Use freely, modify, distribute!

---

## 🙏 Acknowledgments

- **wttr.in** - Weather data
- **Ollama** - Local LLM
- **pyttsx3** - Offline TTS
- **All contributors** - Feedback and ideas

---

**Created with ❤️ for the AI Assistant community**

* Rama learns from you - teach her well! 🤖💜