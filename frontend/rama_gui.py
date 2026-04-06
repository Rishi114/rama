"""
RAMA AI - Frontend GUI Interface
Desktop GUI with Tkinter
"""

import tkinter as tk
from tkinter import ttk
import os
import sys

# Add parent to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from backend.model import RAMAModel


class RAMAGUI:
    """RAMA Desktop GUI Application"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🤖 RAMA AI v2.0")
        self.root.geometry("900x650")
        self.root.configure(bg="#1a1a2e")
        
        # Colors
        self.bg_dark = "#1a1a2e"
        self.bg_medium = "#16213e"
        self.bg_light = "#0f3460"
        self.accent = "#e94560"
        self.text_white = "#ffffff"
        self.text_gray = "#a0a0a0"
        
        # Initialize RAMA
        self.rama = None
        
        # Setup UI
        self._setup_ui()
        
    def _setup_ui(self):
        """Create the UI"""
        
        # Header
        header = tk.Frame(self.root, bg=self.bg_medium, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        title = tk.Label(
            header,
            text="🤖 RAMA AI - Jarvis Style Assistant",
            font=("Segoe UI", 16, "bold"),
            bg=self.bg_medium,
            fg=self.text_white
        )
        title.pack(side="left", padx=20, pady=15)
        
        # Status
        self.status = tk.Label(
            header,
            text="● Online",
            font=("Segoe UI", 10),
            bg=self.bg_medium,
            fg="#00ff88"
        )
        self.status.pack(side="right", padx=20)
        
        # Main content
        main = tk.Frame(self.root, bg=self.bg_dark)
        main.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Left sidebar - Skills
        sidebar = tk.Frame(main, bg=self.bg_medium, width=180)
        sidebar.pack(side="left", fill="y", padx=(0, 10))
        sidebar.pack_propagate(False)
        
        tk.Label(sidebar, text="🎯 Skills", font=("Segoe UI", 11, "bold"),
                bg=self.bg_medium, fg=self.text_white).pack(pady=(15, 10))
        
        skills = ["💬 Chat", "💻 Code", "🧮 Math", "📁 Files", 
                  "🔍 Search", "🎤 Voice", "🖥️ Apps", "💻 System"]
        
        for skill in skills:
            tk.Label(sidebar, text=skill, font=("Segoe UI", 9),
                    bg=self.bg_medium, fg=self.text_gray,
                    anchor="w").pack(fill="x", padx=15, pady=2)
        
        # Chat area
        chat_frame = tk.Frame(main, bg=self.bg_medium)
        chat_frame.pack(side="left", fill="both", expand=True)
        
        tk.Label(chat_frame, text="💬 Conversation", font=("Segoe UI", 11, "bold"),
                bg=self.bg_medium, fg=self.text_white).pack(pady=(15, 5), padx=15, anchor="w")
        
        self.chat_text = tk.Text(chat_frame, bg=self.bg_dark, fg=self.text_white,
                                 font=("Segoe UI", 10), wrap="word", state="disabled")
        self.chat_text.pack(fill="both", expand=True, padx=15, pady=5)
        
        # Input
        input_frame = tk.Frame(chat_frame, bg=self.bg_dark)
        input_frame.pack(fill="x", padx=15, pady=(5, 15))
        
        self.input_box = tk.Entry(input_frame, bg=self.bg_medium, fg=self.text_white,
                                  font=("Segoe UI", 11), bd=0, insertbackground=self.text_white)
        self.input_box.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.input_box.bind("<Return>", self._send_message)
        
        tk.Button(input_frame, text="Send", bg=self.accent, fg=self.text_white,
                  font=("Segoe UI", 10), bd=0, padx=15, cursor="hand2",
                  command=self._send_message).pack(side="right")
        
        tk.Button(input_frame, text="🎤", bg=self.bg_medium, fg=self.text_white,
                  font=("Segoe UI", 12), bd=0, padx=10, cursor="hand2",
                  command=self._voice_input).pack(side="right", padx=(5, 0))
        
        # Right sidebar - Info
        info = tk.Frame(main, bg=self.bg_medium, width=160)
        info.pack(side="right", fill="y", padx=(10, 0))
        info.pack_propagate(False)
        
        tk.Label(info, text="ℹ️ Info", font=("Segoe UI", 11, "bold"),
                bg=self.bg_medium, fg=self.text_white).pack(pady=(15, 10))
        
        info_items = [("👤 Name:", "bhai"), ("🗣️ Language:", "English"),
                      ("🎤 Voice:", "Enabled"), ("📊 Status:", "Ready")]
        
        for label, value in info_items:
            frame = tk.Frame(info, bg=self.bg_medium)
            frame.pack(fill="x", padx=10, pady=2)
            tk.Label(frame, text=label, font=("Segoe UI", 9), bg=self.bg_medium,
                    fg=self.text_gray).pack(side="left")
            tk.Label(frame, text=value, font=("Segoe UI", 9, "bold"),
                    bg=self.bg_medium, fg=self.text_white).pack(side="right")
        
        # Status bar
        status_bar = tk.Frame(self.root, bg=self.bg_medium, height=25)
        status_bar.pack(fill="x")
        status_bar.pack_propagate(False)
        
        tk.Label(status_bar, text="RAMA AI v2.0 | 50+ Skills | Jarvis Style",
                font=("Segoe UI", 8), bg=self.bg_medium, fg=self.text_gray).pack(pady=3)
    
    def _send_message(self, event=None):
        """Send message"""
        message = self.input_box.get().strip()
        if not message:
            return
        
        self.input_box.delete(0, "end")
        self._add_message(f"You: {message}", "user")
        
        if not self.rama:
            self._init_rama()
        
        response = self.rama.process(message)
        self._add_message(f"Rama: {response}", "rama")
    
    def _voice_input(self):
        """Handle voice input"""
        if not self.rama:
            self._init_rama()
        
        self._add_message("🎤 Listening...", "system")
        command = self.rama.listen()
        
        if command:
            self._add_message(f"You (voice): {command}", "user")
            response = self.rama.process(command)
            self._add_message(f"Rama: {response}", "rama")
        else:
            self._add_message("❌ Couldn't hear you", "system")
    
    def _add_message(self, text, tag):
        """Add message to chat"""
        self.chat_text.config(state="normal")
        self.chat_text.insert("end", text + "\n\n", tag)
        self.chat_text.see("end")
        self.chat_text.config(state="disabled")
    
    def _init_rama(self):
        """Initialize RAMA"""
        try:
            config = {'user_name': 'bhai', 'voice_enabled': False}
            self.rama = RAMAModel(config)
            self.rama.initialize()
            self._add_message("🤖 RAMA initialized!", "system")
        except Exception as e:
            self._add_message(f"❌ Init error: {e}", "system")
    
    def run(self):
        """Run the app"""
        self.root.mainloop()


if __name__ == "__main__":
    app = RAMAGUI()
    app.run()