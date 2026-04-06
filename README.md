# 🤖 RAMA AI v2.0

**Production-Grade, Fully Offline AI Voice Assistant for Windows**

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Architecture](#architecture)
4. [Tech Stack](#tech-stack)
5. [Installation](#installation)
6. [Running RAMA](#running-rama)
7. [Voice Setup](#voice-setup)
8. [Ollama Setup](#ollama-setup)
9. [Skills](#skills)
10. [Configuration](#configuration)
11. [Troubleshooting](#troubleshooting)
12. [Roadmap](#roadmap)
13. [License](#license)

---

## 🎯 Overview

RAMA AI v2.0 is a production-grade, fully offline AI voice assistant built for Windows. It draws inspiration from:

- **Claude Code** - Multi-agent architecture
- **Vercel Skills** - Plugin-based skill system
- **NotebookLM** - RAG document ingestion
- **Agent systems** - Task execution layer

### Key Principles

- 🔒 **100% Offline** - No cloud APIs, all local
- 🧠 **Self-Learning** - Learns from every conversation
- 🎙️ **Voice-Ready** - Full STT/TTS pipeline
- ⚡ **Lightweight** - Runs on 8GB RAM laptop
- 🎭 **Sassy Personality** - Witty, fun responses

---

## ✨ Features

### Core Features

| Feature | Description |
|---------|-------------|
| **AI Brain** | Local LLM via Ollama + RAG retrieval |
| **Voice Pipeline** | Offline STT (Whisper) + TTS (Silero/Coqui) |
| **Memory System** | Short-term (session) + Long-term (SQLite) + Vector (FAISS) |
| **RAG Engine** | PDF, links, code ingestion |
| **Task Execution** | App launch, file ops, system control |
| **Skill System** | 13+ modular plugins |

### Skills (13+)

- 🚀 **AppLauncher** - Open apps (`open notepad`)
- 📁 **FileManager** - List files, create folders
- 💻 **SystemInfo** - CPU, RAM, disk info
- 🧮 **Calculator** - Math operations
- 🌤️ **Weather** - Weather info (mock)
- 🔍 **WebSearch** - Open browser search
- 📝 **Note** - Take notes
- ⏰ **Reminder** - Set reminders
- 🧠 **Knowledge** - Learn facts
- 💻 **Coding** - Code in 30+ languages
- 🔄 **Automation** - Create routines
- 🤖 **LocalAI** - Ollama integration
- 👋 **Greeting** - Friendly chat

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                           FRONTEND                                  │
│   ┌─────────────────────────────────────────────────────────────┐   │
│   │  Desktop UI (CustomTkinter - Dark Theme)                    │   │
│   │  • Chat interface  • Voice controls  • Status display       │   │
│   └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      TASK EXECUTION LAYER                           │
│   ┌──────────────┐ ┌──────────────┐ ┌──────────────┐               │
│   │ System       │ │ App          │ │ File        │               │
│   │ Control      │ │ Automation   │ │ Manager     │               │
│   └──────────────┘ └──────────────┘ └──────────────┘               │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                            AI BRAIN                                  │
│   ┌──────────────┐ ┌──────────────┐ ┌──────────────┐               │
│   │ RAG Engine   │ │ Context      │ │ Local LLM    │               │
│   │ (Retrieval)  │ │ Manager      │ │ (Ollama)     │               │
│   └──────────────┘ └──────────────┘ └──────────────┘               │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                          MEMORY LAYER                               │
│   ┌──────────────┐ ┌──────────────┐ ┌──────────────┐               │
│   │ Short-term   │ │ Long-term    │ │ Vector DB    │               │
│   │ (Session)    │ │ (SQLite)     │ │ (FAISS)      │               │
│   └──────────────┘ └──────────────┘ └──────────────┘               │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         VOICE PIPELINE                              │
│   ┌──────────────┐ ┌──────────────┐ ┌──────────────┐               │
│   │ Wake Word    │ │ STT          │ │ TTS          │               │
│   │ (Porcupine)  │ │ (Whisper)    │ │ (Silero)     │               │
│   └──────────────┘ └──────────────┘ └──────────────┘               │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🔧 Tech Stack

| Component | Technology | Justification |
|-----------|------------|---------------|
| **LLM** | Ollama + GGUF | Fully offline, local inference |
| **STT** | Whisper (tiny) | Offline speech recognition |
| **TTS** | Silero / Coqui | Offline voice synthesis |
| **Wake Word** | Porcupine | Efficient keyword detection |
| **Vector DB** | FAISS | Fast similarity search |
| **Memory** | SQLite | Persistent learning storage |
| **UI** | CustomTkinter | Lightweight, no browser needed |
| **Async** | asyncio | Non-blocking pipelines |
| **RAG** | LangChain | Document retrieval |

---

## 📦 Installation

### Prerequisites

- **Python 3.8+** - [Download Python](https://www.python.org/downloads/)
- **Windows 10/11**
- **8GB RAM** (recommended for LLM)
- **2GB disk space**

### Step 1: Clone Repository

```bash
git clone https://github.com/Rishi114/rama.git
cd rama
```

### Step 2: Create Virtual Environment (Recommended)

```bash
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
cd rama_ai
pip install -r requirements.txt
```

### Step 4: Install Optional Voice Dependencies

For full voice support, install additional packages:

```bash
# For STT (Speech-to-Text)
pip install faster-whisper

# For TTS (Text-to-Speech)  
pip install silero

# For Wake Word
pip install pvporcupine

# For audio playback
pip install sounddevice pyaudio

# For system monitoring
pip install psutil
```

---

## 🚀 Running RAMA

### Option 1: GUI Mode (Recommended)

```bash
cd rama_ai
python main.py
```

This opens the desktop UI with dark theme.

### Option 2: CLI Mode

```bash
cd rama_ai
python main.py --cli
```

Interactive command-line interface.

### Option 3: Headless Mode (API Server)

```bash
cd rama_ai
python main.py --headless --port 8000
```

Runs as HTTP API server (for automation).

---

## 🎙️ Voice Setup

### For Full Voice Support:

1. **Install Audio Libraries**
   ```bash
   pip install pyaudio sounddevice
   ```

2. **Download Models** (first run will download automatically)
   - Whisper (STT) - ~75MB for tiny model
   - Silero (TTS) - ~100MB

3. **Test Microphone**
   ```bash
   python -c "import pyaudio; p = pyaudio.PyAudio(); print('Audio OK')"
   ```

### Simple Mode (No Voice)

RAMA works without voice - just type your messages!

---

## 🤖 Ollama Setup (Optional but Recommended)

For AI responses, install Ollama:

### Step 1: Download Ollama

Visit: https://ollama.ai/download

Or use winget:
```bash
winget install Ollama.Ollama
```

### Step 2: Start Ollama

```bash
ollama serve
```

### Step 3: Pull a Model

```bash
# For 8GB RAM - use small model
ollama pull llama3.2:1b

# For 16GB RAM - use larger model
ollama pull llama3.2:7b
```

### Step 4: Verify

```bash
ollama list
```

Should show the model you pulled.

---

## 🎯 Skills Usage

### Greeting
```
You: hello
Rama: Well, well... look who's awake! 👀
```

### Calculator
```
You: calculate 2+2
Rama: 🔢 2+2 = 4
```

### App Launcher
```
You: open notepad
Rama: 🚀 Launched: notepad
```

### System Info
```
You: system info
Rama: 💻 DESKTOP-XXX | Windows 10
```

### Weather
```
You: weather Tokyo
Rama: 🌤️ Weather for Tokyo: 22°C, Sunny
```

### Web Search
```
You: search Python tutorials
Rama: 🔍 Searching for 'Python tutorials'...
```

### Knowledge (Self-Learning)
```
You: learn that my favorite color is blue
Rama: ✅ Learned: 'favorite color' = 'blue'
```

### Coding
```
You: code python
Rama: 💻 Python:
     print("Hello, World!")
```

---

## ⚙️ Configuration

### Edit `data/config.yaml`

```yaml
# LLM Settings
llm_model: "llama3.2:1b"      # Model to use
ollama_host: "http://localhost:11434"

# Voice Settings
stt_model: "tiny"             # Whisper model size
tts_model: "silero"           # TTS model
voice_enabled: false          # Enable voice I/O
wake_word: "hey rama"         # Wake word

# Memory Settings
max_memory: 20                # Max messages in context
embedding_model: "sentence-transformers/all-MiniLM-L6-v2"
```

### Alternative: Environment Variables

```bash
export RAMA_MODEL=llama3.2:1b
export RAMA_VOICE=true
```

---

## 🔧 Troubleshooting

### Issue: "Module not found"

```bash
# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: Ollama not connecting

```bash
# Check if Ollama is running
ollama serve

# Test connection
curl http://localhost:11434/api/tags
```

### Issue: Voice not working

```bash
# Install audio dependencies
pip install pyaudio

# Windows: may need Visual C++ Redistributable
```

### Issue: Slow performance

```bash
# Use smaller model
# In config.yaml: llm_model: "llama3.2:1b"

# Or in code, initialize with smaller model
```

### Issue: "Permission denied" on clone

```bash
# Clone to your folder
cd C:\Users\YOURNAME\Desktop
git clone https://github.com/Rishi114/rama.git
```

---

## 🗺️ Roadmap

### v2.1 (Planned)
- [ ] Better wake word detection
- [ ] More realistic TTS voices
- [ ] Plugin system for custom skills

### v2.2 (Planned)
- [ ] Better RAG with ChromaDB
- [ ] Code understanding with tree-sitter
- [ ] Multi-language support

### v3.0 (Future)
- [ ] Full voice conversation
- [ ] Computer vision integration
- [ ] Agent orchestration

---

## 📁 Project Structure

```
rama/
├── ARCHITECTURE.md      # Detailed architecture docs
├── rama_ai/             # Main application
│   ├── main.py          # Entry point
│   ├── requirements.txt # Dependencies
│   ├── core/           # AI Brain
│   │   ├── brain.py           # Main processor
│   │   ├── rag_engine.py      # RAG retrieval
│   │   └── ollama_client.py  # Local LLM
│   ├── voice/          # Voice Pipeline
│   │   └── voice_pipeline.py # STT/TTS/Wake
│   ├── memory/         # Memory System
│   │   └── memory_system.py  # Short/Long term
│   ├── ingestion/      # Knowledge Ingestion
│   │   └── ingestion_pipeline.py
│   ├── tasks/          # Task Execution
│   │   └── task_executor.py
│   ├── skills/         # Skills (Plugins)
│   │   ├── greeting.py
│   │   ├── calculator.py
│   │   ├── app_launcher.py
│   │   ├── file_manager.py
│   │   ├── system.py
│   │   ├── utilities.py
│   │   ├── coding.py
│   │   └── skill_base.py
│   └── frontend/      # Desktop UI
│       └── ui.py
└── README.md           # This file
```

---

## 🙏 Credits

- [.NET](https://dotnet.microsoft.com) - WPF (original v1)
- [Ollama](https://ollama.ai) - Local LLM
- [Whisper](https://github.com/openai/whisper) - STT
- [Silero](https://github.com/silero-ai/silero-models) - TTS
- [LangChain](https://github.com/langchain-ai/langchain) - RAG
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) - UI

---

## 📜 License

MIT License - Use freely!

---

**Made with 💜**

For help, open an issue: https://github.com/Rishi114/rama/issues