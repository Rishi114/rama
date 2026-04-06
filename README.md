# 🤖 RAMA AI v2.0

## Your Personal AI Assistant - Jarvis Style!

Build your own intelligent voice assistant with brain training capabilities!

---

## 📦 Installation Guide

### Step 1: Prerequisites

**Requirements:**
- Python 3.8+ (3.11/3.12 recommended)
- Windows 10/11
- 4GB RAM minimum (16GB for AI training)

**Download Python:** https://www.python.org/downloads/

⚠️ **Important:** During installation, check **"Add Python to PATH"**

---

### Step 2: Clone or Download

**Option A: Clone Repository**
```cmd
git clone https://github.com/Rishi114/rama.git RAMA_AI
cd RAMA_AI
```

**Option B: Download ZIP**
1. Go to: https://github.com/Rishi114/rama
2. Click **Code** → **Download ZIP**
3. Extract to folder

---

### Step 3: Install Dependencies

Open **Command Prompt** (cmd) and run:

```cmd
cd RAMA_AI
pip install -r requirements.txt
```

**Core Packages (4):**
- pyttsx3 - Text-to-Speech
- speechrecognition - Voice input
- psutil - System info
- requests - Web requests

---

### Step 4: Run RAMA

**Option A: Double-Click Launcher**
```
Double-click: LAUNCH.bat
```

**Option B: Command Line**
```cmd
cd RAMA_AI
python main.py
```

---

## 🎮 How to Use

### Voice Mode (Default)
```
Say "Hey Rama" followed by command!
```

### Text Mode
```cmd
python main.py --text
```

---

## 📋 Available Commands

### 🖥️ Apps
```
• "open notepad"
• "open chrome"
• "open spotify"
• "open calculator"
```

### 🔍 Search
```
• "search python tutorial"
• "search youtube funny videos"
```

### 💻 System
```
• "system info"
• "cpu" or "ram"
• "screenshot"
• "settings"
```

### 💻 Coding
```
• "code python"
• "code javascript"
• "debug this [code]"
• "architect my project"
```

### 🧠 Brain Training
```
• "brain status" - View brain info
• "physics data" - Load physics datasets
• "train brain" - Start training
• "save brain" - Save knowledge
• "load brain" - Load saved brain
• "reset brain" - Clear brain
```

### 🗣️ Languages
```
• "set language hindi"
• "set language marathi"
• "set language english"
```

### 👤 Your Name
```
• "call me bro"
• "call me bhai"
• "call me sir"
```

### 🎤 Voice
```
• "voice on"
• "voice off"
```

### Other
```
• "help"
• "who are you"
• "exit"
```

---

## 🧠 Brain Training System

RAMA can learn and improve from conversations!

### How It Works:
1. **Auto-Learning** - Every conversation improves brain
2. **Accuracy Tracking** - View with "brain status"
3. **Save/Load** - Persist knowledge between sessions

### Commands:
```
brain status   → View accuracy & knowledge
physics data   → Load 15TB physics datasets
save brain     → Save all learning
load brain     → Restore saved brain
reset brain    → Start fresh
```

---

## 🔬 The Well (Physics Data) - Optional

For advanced physics training:

```cmd
pip install the_well
the-well-download --base-path ./data --dataset active_matter
```

**15TB of Physics Datasets:**
- Fluid Dynamics
- Active Matter
- MHD (Magnetohydrodynamics)
- Supernova simulations
- Turbulence
- Acoustic Scattering

---

## 📁 Project Structure

```
RAMA_AI/
├── main.py              # Entry point
├── requirements.txt    # Dependencies
├── .env                # Config
├── LAUNCH.bat          # Easy launcher
│
├── backend/            # Core modules
│   ├── model.py        # Brain
│   ├── skills.py       # All skills
│   ├── automation.py   # System control
│   ├── brain_trainer.py # Brain training
│   ├── chat_bot.py     # Conversation
│   ├── speech_to_text.py
│   ├── text_to_speech.py
│   └── ...
│
├── data/               # Storage
│   ├── chat_log.json
│   ├── my_data.json
│   ├── status.json
│   └── response.json
│
└── frontend/           # GUI
    ├── rama_gui.py
    └── graphics/
```

---

## 🌐 Features

| Feature | Status |
|---------|--------|
| Voice I/O (TTS/STT) | ✅ |
| Wake Word ("Hey Rama") | ✅ |
| 35+ Programming Languages | ✅ |
| 50+ Skills | ✅ |
| Self-Learning Brain | ✅ |
| The Well Physics (15TB) | ✅ |
| KiloCode Integration | ✅ |
| JSON Repair | ✅ |
| Vercel Skills | ✅ |
| Video Learning | ✅ |
| Personality (EN/HI/MR) | ✅ |
| Full PC Control | ✅ |

---

## ❓ Troubleshooting

### "Python not found"
- Reinstall Python and check "Add to PATH"
- Or use: `py main.py` instead of `python main.py`

### Voice not working
- Install pyaudio: `pip install pyaudio`
- Or use text mode: `python main.py --text`

### Permission errors
- Run CMD as Administrator

---

## 📝 Customization

Edit `.env` file:
```
USER_NAME=bhai
USER_LANGUAGE=en
WAKE_WORD=hey rama
VOICE_ENABLED=true
```

---

## 🚀 Ready!

Just run **LAUNCH.bat** and start talking to RAMA! 😎

```
         🤖
        /  \
       | RAMA |
        \__/
```

**Kya karna hai bhai?** 🔥