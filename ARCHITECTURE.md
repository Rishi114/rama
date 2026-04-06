# 🤖 RAMA AI v2.0 - Architecture Documentation

## 📋 System Overview

**RAMA AI v2.0** is a production-grade, fully offline AI voice assistant for Windows. Built with inspiration from:
- Vercel Skills (plugin architecture)
- Claude Code (multi-agent system)
- NotebookLM (RAG pipelines)
- Agent systems (task execution)

---

## 🏗️ Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                              FRONTEND                                    │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │  UI (Tk)    │  │  Voice UI   │  │  Status     │  │  Logs       │     │
│  │  Window     │  │  Waveform   │  │  Display    │  │  Viewer     │     │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘     │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         TASK EXECUTION LAYER                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │ System      │  │ App         │  │ File        │  │ Automation  │     │
│  │ Control     │  │ Automation  │  │ Manager     │  │ Engine      │     │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘     │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                            AI BRAIN                                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │ RAG Engine  │  │ Context     │  │ Local LLM   │  │ Skill      │     │
│  │ (Retrieval) │  │ Manager     │  │ (Ollama)    │  │ Manager    │     │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘     │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                           MEMORY LAYER                                   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │ Short-term  │  │ Long-term   │  │ Vector DB   │  │ SQLite      │     │
│  │ (Session)   │  │ (Persistent)│  │ (FAISS)    │  │ (Learning)  │     │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘     │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                          VOICE PIPELINE                                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │ Wake Word   │  │ STT         │  │ LLM         │  │ TTS         │     │
│  │ (Porcupine) │  │ (Whisper)   │  │ (Ollama)    │  │ (Coqui)     │     │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘     │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         INGESTION PIPELINE                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │ PDF         │  │ Link        │  │ Code        │  │ Notes       │     │
│  │ Reader      │  │ Scraper     │  │ Parser      │  │ Reader      │     │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘     │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 📁 Module Structure

```
/rama-ai
├── main.py                 # Entry point
├── requirements.txt        # Dependencies
├── config.yaml             # Configuration
│
├── core/                   # AI Brain
│   ├── __init__.py
│   ├── brain.py           # Main AI processor
│   ├── rag_engine.py      # RAG retrieval
│   ├── context_manager.py # Context management
│   └── skill_manager.py   # Skill/plugin system
│
├── voice/                 # Voice Pipeline
│   ├── __init__.py
│   ├── wake_word.py       # Wake word detection
│   ├── stt.py            # Speech-to-text
│   ├── tts.py            # Text-to-speech
│   └── voice_pipeline.py # Orchestration
│
├── memory/                # Memory System
│   ├── __init__.py
│   ├── short_term.py     # Session memory
│   ├── long_term.py     # Persistent memory
│   ├── vector_store.py  # FAISS vector DB
│   └── sqlite_store.py  # SQLite learning
│
├── ingestion/             # Knowledge Ingestion
│   ├── __init__.py
│   ├── pdf_reader.py     # PDF processing
│   ├── link_scraper.py   # Web scraping
│   ├── code_parser.py   # Code indexing
│   └── notes_reader.py  # Notes ingestion
│
├── tasks/                 # Task Execution
│   ├── __init__.py
│   ├── system_control.py # System commands
│   ├── app_automation.py # App control
│   ├── file_manager.py   # File operations
│   └── automation.py     # Automation engine
│
├── frontend/              # UI Layer
│   ├── __init__.py
│   ├── ui.py             # Main UI
│   ├── voice_display.py # Voice visualization
│   └── log_viewer.py    # Log display
│
└── data/                  # Data Storage
    ├── embeddings/       # Vector embeddings
    ├── memory.db         # SQLite database
    └── config/           # Configuration
```

---

## 🔧 Tech Stack

| Component | Technology | Justification |
|-----------|------------|----------------|
| **LLM** | Ollama + GGUF | Fully offline, local inference |
| **STT** | Whisper (tiny) | Offline speech recognition |
| **TTS** | Coqui TTS / Piper | Offline voice synthesis |
| **Wake Word** | Porcupine | Efficient keyword detection |
| **Vector DB** | FAISS | Fast similarity search |
| **Memory** | SQLite | Persistent learning storage |
| **UI** | Tkinter / CustomTkinter | Lightweight, no browser needed |
| **Async** | asyncio | Non-blocking pipelines |
| **RAG** | LangChain (local) | Document retrieval |

---

## 🎯 Key Features

### 1. Voice Pipeline (Offline)
- **Wake Word**: "Hey Rama" detection
- **STT**: Whisper tiny for local transcription
- **LLM**: Ollama (llama3.2:1b for 8GB RAM)
- **TTS**: Piper/Coqui for voice output

### 2. Memory System
- **Short-term**: Current conversation context
- **Long-term**: SQLite-stored facts
- **Vector**: FAISS for semantic search
- **Learning**: Auto-improve from interactions

### 3. RAG Engine
- PDF ingestion with chunking
- Link scraping and summarization
- Code repository indexing
- Notes/document processing

### 4. Task Execution
- Windows app automation
- File system operations
- System command execution
- Custom automation routines

### 5. Skill System
- Plugin-based architecture
- Dynamic skill loading
- Custom skill creation
- Skill versioning

---

## 🚀 Performance Targets

| Metric | Target |
|--------|--------|
| **RAM Usage** | < 4GB (8GB laptop) |
| **Cold Start** | < 3 seconds |
| **Voice Latency** | < 500ms |
| **LLM Response** | Streaming |
| **Offline** | 100% |

---

## 📦 Dependencies

```txt
# Core
asyncio
pydantic
pyyaml
sqlalchemy

# AI/ML
langchain
langchain-community
faiss-cpu
sentence-transformers
numpy

# Voice (Offline)
whisper          # STT
tts               # TTS (coqui/piper)
pvporcupine      # Wake word

# Ingestion
pypdf
beautifulsoup4
chromadb

# UI
customtkinter
matplotlib

# Data
sqlite3
```

---

## 🔄 Continuous Learning

1. **Capture**: Every conversation stored
2. **Analyze**: Extract key facts
3. **Store**: SQLite + Vector DB
4. **Retrieve**: RAG for context
5. **Improve**: Feedback loop

---

## 📝 API Design

### Main Brain
```python
class Brain:
    async def process(input: str) -> str
    async def learn(input: str, output: str)
    async def retrieve(query: str) -> List[str]
```

### Voice Pipeline
```python
class VoicePipeline:
    async def listen() -> str  # Until wake word
    async def transcribe(audio) -> str
    async def speak(text: str)
```

### Task Engine
```python
class TaskEngine:
    async def execute(task: str) -> str
    def register_skill(skill: Skill)
```

---

## 🛠️ Build & Run

```bash
# Install
pip install -r requirements.txt

# Run
python main.py

# Build exe
pyinstaller main.py --onefile --noconsole
```

---

## 📜 License

MIT License - Use freely!

---

**Architecture inspired by**: Vercel Skills, Claude Code, NotebookLM, Agent-Reach, minGPT