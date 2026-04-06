"""
RAMA AI - Animated 3D GUI
Modern, Animated, Realistic Interface
"""

import tkinter as tk
from tkinter import ttk
import random
import time
import threading
from datetime import datetime


class AnimatedRamaGUI:
    """RAMA AI - Animated 3D Desktop Interface"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🤖 RAMA AI v2.0 - Jarvis")
        self.root.geometry("1100x750")
        self.root.configure(bg="#0a0a1a")
        
        # Colors - Cyberpunk theme
        self.colors = {
            "bg_dark": "#0a0a1a",
            "bg_medium": "#12122a",
            "bg_light": "#1a1a3a",
            "accent_cyan": "#00ffff",
            "accent_purple": "#9b59b6",
            "accent_pink": "#ff006e",
            "accent_gold": "#ffd700",
            "text_white": "#ffffff",
            "text_gray": "#a0a0a0",
            "glow": "#00ffff",
        }
        
        # State
        self.rama = None
        self.is_listening = False
        self.animation_running = True
        
        # Setup UI
        self._setup_styles()
        self._create_ui()
        self._start_animations()
        
    def _setup_styles(self):
        """Setup custom styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure button style
        style.configure('NeonButton.TButton',
                        background=self.colors['accent_cyan'],
                        foreground=self.colors['bg_dark'],
                        font=('Segoe UI', 11, 'bold'),
                        borderwidth=0,
                        focuscolor='none')
        style.map('NeonButton.TButton',
                background=[('active', self.colors['accent_purple'])])
    
    def _create_ui(self):
        """Create the main UI"""
        
        # ==================== MAIN CONTAINER ====================
        main = tk.Frame(self.root, bg=self.colors['bg_dark'])
        main.pack(fill="both", expand=True)
        
        # ==================== HEADER ====================
        self._create_header(main)
        
        # ==================== CONTENT AREA ====================
        content = tk.Frame(main, bg=self.colors['bg_dark'])
        content.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Left Panel - RAMA Avatar
        self._create_avatar_panel(content)
        
        # Center - Chat Area
        self._create_chat_panel(content)
        
        # Right Panel - Status & Skills
        self._create_status_panel(content)
        
        # ==================== INPUT AREA ====================
        self._create_input_area(main)
        
        # ==================== FOOTER ====================
        self._create_footer(main)
    
    def _create_header(self, parent):
        """Create animated header"""
        header = tk.Frame(parent, bg=self.colors['bg_medium'], height=70)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        # Logo / Title with glow effect
        self.title_label = tk.Label(
            header,
            text="🤖 RAMA AI",
            font=("Segoe UI", 22, "bold"),
            bg=self.colors['bg_medium'],
            fg=self.colors['accent_cyan']
        )
        self.title_label.pack(side="left", padx=20, pady=15)
        
        # Subtitle
        self.subtitle = tk.Label(
            header,
            text=" Jarvis Style Assistant",
            font=("Segoe UI", 12),
            bg=self.colors['bg_medium'],
            fg=self.colors['accent_purple']
        )
        self.subtitle.pack(side="left", pady=15)
        
        # Status indicator with animation
        self.status_frame = tk.Frame(header, bg=self.colors['bg_medium'])
        self.status_frame.pack(side="right", padx=20)
        
        self.status_dot = tk.Canvas(self.status_frame, width=15, height=15, bg=self.colors['bg_medium'], highlightthickness=0)
        self.status_dot.pack(side="right", pady=25)
        
        # Draw glowing circle
        self._draw_glowing_dot()
        
        self.status_text = tk.Label(
            self.status_frame,
            text="Online",
            font=("Segoe UI", 10),
            bg=self.colors['bg_medium'],
            fg="#00ff88"
        )
        self.status_text.pack(side="right", pady=25, padx=5)
    
    def _draw_glowing_dot(self):
        """Draw animated glowing status dot"""
        # Outer glow
        self.status_dot.create_oval(1, 1, 14, 14, fill="#00ff88", outline="")
        # Inner bright
        self.status_dot.create_oval(4, 4, 11, 11, fill="#00ff88", outline="")
    
    def _create_avatar_panel(self, parent):
        """Create RAMA 3D Avatar panel"""
        avatar_frame = tk.Frame(parent, bg=self.colors['bg_medium'], width=280)
        avatar_frame.pack(side="left", fill="y", padx=(0, 10))
        avatar_frame.pack_propagate(False)
        
        # Avatar container with border
        avatar_container = tk.Frame(avatar_frame, bg=self.colors['bg_light'], bd=2, relief="raised")
        avatar_container.pack(pady=15, padx=15, fill="x")
        
        # RAMA Avatar (3D-style circular)
        self.avatar_canvas = tk.Canvas(avatar_container, width=200, height=200, bg=self.colors['bg_dark'], highlightthickness=0)
        self.avatar_canvas.pack(pady=10)
        
        # Draw 3D-style avatar
        self._draw_rama_avatar()
        
        # Name label
        self.avatar_name = tk.Label(
            avatar_container,
            text="RAMA",
            font=("Segoe UI", 16, "bold"),
            bg=self.colors['bg_light'],
            fg=self.colors['accent_cyan']
        )
        self.avatar_name.pack(pady=(0, 5))
        
        # Status label
        self.avatar_status = tk.Label(
            avatar_container,
            text="● Listening",
            font=("Segoe UI", 10),
            bg=self.colors['bg_light'],
            fg="#00ff88"
        )
        self.avatar_status.pack(pady=(0, 10))
        
        # Quick Actions
        tk.Label(avatar_frame, text="⚡ Quick Actions", font=("Segoe UI", 11, "bold"),
                bg=self.colors['bg_medium'], fg=self.colors['text_white']).pack(pady=(10, 5))
        
        quick_actions = [
            ("🎤 Voice", "voice on"),
            ("💻 Code", "code python"),
            ("🔍 Search", "search"),
            ("🧠 Brain", "brain status"),
        ]
        
        for text, cmd in quick_actions:
            btn = tk.Button(avatar_frame, text=text, bg=self.colors['bg_light'],
                          fg=self.colors['text_white'], font=("Segoe UI", 10),
                          relief="flat", cursor="hand2", command=lambda c=cmd: self._quick_action(c))
            btn.pack(pady=2, padx=15, fill="x")
    
    def _draw_rama_avatar(self):
        """Draw animated 3D-style RAMA avatar"""
        # Outer glow ring
        self.avatar_canvas.create_oval(10, 10, 190, 190, fill="", outline=self.colors['accent_cyan'], width=3)
        self.avatar_canvas.create_oval(15, 15, 185, 185, fill="", outline=self.colors['accent_purple'], width=2)
        
        # Main circle (3D effect)
        self.avatar_canvas.create_oval(40, 40, 160, 160, fill=self.colors['bg_dark'], outline="")
        
        # Inner circle
        self.avatar_canvas.create_oval(50, 50, 150, 150, fill="#1a1a3a", outline="")
        
        # Face area
        self.avatar_canvas.create_oval(70, 70, 130, 110, fill=self.colors['accent_cyan'], outline="")
        
        # Eyes
        self.avatar_canvas.create_oval(85, 82, 95, 92, fill="#ffffff", outline="")
        self.avatar_canvas.create_oval(105, 82, 115, 92, fill="#ffffff", outline="")
        
        # Eye pupils
        self.avatar_canvas.create_oval(88, 85, 92, 89, fill=self.colors['bg_dark'], outline="")
        self.avatar_canvas.create_oval(108, 85, 112, 89, fill=self.colors['bg_dark'], outline="")
        
        # Mouth (smile)
        self.avatar_canvas.create_arc(85, 105, 115, 125, start=0, extent=180, fill="", outline=self.colors['accent_cyan'], width=2)
        
        # Antenna on top
        self.avatar_canvas.create_line(100, 40, 100, 20, fill=self.colors['accent_cyan'], width=2)
        self.avatar_canvas.create_oval(95, 15, 105, 25, fill=self.colors['accent_pink'], outline="")
    
    def _create_chat_panel(self, parent):
        """Create chat area"""
        chat_frame = tk.Frame(parent, bg=self.colors['bg_medium'])
        chat_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Chat header
        tk.Label(chat_frame, text="💬 Conversation", font=("Segoe UI", 12, "bold"),
                bg=self.colors['bg_medium'], fg=self.colors['text_white']).pack(pady=(15, 5), padx=15, anchor="w")
        
        # Chat display with styling
        self.chat_frame = tk.Frame(chat_frame, bg=self.colors['bg_dark'], bd=1, relief="sunken")
        self.chat_frame.pack(fill="both", expand=True, padx=15, pady=5)
        
        self.chat_text = tk.Text(
            self.chat_frame,
            bg=self.colors['bg_dark'],
            fg=self.colors['text_white'],
            font=("Segoe UI", 11),
            wrap="word",
            state="disabled",
            bd=0,
            highlightthickness=0
        )
        self.chat_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Configure tags
        self.chat_text.tag_config("user", foreground="#4da6ff", lmargin1=10, lmargin2=10)
        self.chat_text.tag_config("rama", foreground="#ff6b6b", lmargin1=10, lmargin2=10)
        self.chat_text.tag_config("system", foreground="#a0a0a0", lmargin1=10, lmargin2=10)
        self.chat_text.tag_config("command", foreground=self.colors['accent_gold'], lmargin1=10, lmargin2=10)
        
        # Initial message
        self._add_message("🤖 RAMA: Hello bhai! I'm ready! 🎉\n\nType or speak to me!\nTry: 'help' for commands", "system")
    
    def _create_status_panel(self, parent):
        """Create status and skills panel"""
        status_frame = tk.Frame(parent, bg=self.colors['bg_medium'], width=200)
        status_frame.pack(side="right", fill="y")
        status_frame.pack_propagate(False)
        
        # Brain Status
        tk.Label(status_frame, text="🧠 Brain Status", font=("Segoe UI", 11, "bold"),
                bg=self.colors['bg_medium'], fg=self.colors['text_white']).pack(pady=(15, 5), padx=10, anchor="w")
        
        self.brain_info = tk.Label(
            status_frame,
            text="Epochs: 0\nAccuracy: 50%\nKnowledge: 0 facts",
            font=("Segoe UI", 9),
            bg=self.colors['bg_light'],
            fg=self.colors['text_gray'],
            justify="left"
        )
        self.brain_info.pack(pady=5, padx=10, fill="x")
        
        # Skills section
        tk.Label(status_frame, text="🎯 Active Skills", font=("Segoe UI", 11, "bold"),
                bg=self.colors['bg_medium'], fg=self.colors['text_white']).pack(pady=(15, 5), padx=10, anchor="w")
        
        skills_frame = tk.Frame(status_frame, bg=self.colors['bg_medium'])
        skills_frame.pack(pady=5, padx=10, fill="x")
        
        skills_list = [
            ("💻", "Code"), ("🧮", "Math"), ("🔍", "Search"),
            ("🧠", "Learn"), ("🎤", "Voice"), ("📁", "Files"),
            ("💻", "System"), ("🐛", "Debug")
        ]
        
        for icon, name in skills_list:
            tk.Label(skills_frame, text=f"{icon} {name}", font=("Segoe UI", 9),
                    bg=self.colors['bg_light'], fg=self.colors['text_gray']).pack(pady=1, fill="x")
        
        # Language
        tk.Label(status_frame, text="🌐 Language", font=("Segoe UI", 11, "bold"),
                bg=self.colors['bg_medium'], fg=self.colors['text_white']).pack(pady=(15, 5), padx=10, anchor="w")
        
        self.lang_label = tk.Label(status_frame, text="English 🇬🇧",
                font=("Segoe UI", 10), bg=self.colors['bg_light'], fg=self.colors['accent_cyan'])
        self.lang_label.pack(pady=5, padx=10, fill="x")
        
        # Time
        self.time_label = tk.Label(status_frame, text="",
                font=("Segoe UI", 10), bg=self.colors['bg_medium'], fg=self.colors['text_gray'])
        self.time_label.pack(pady=(20, 10))
        self._update_time()
    
    def _create_input_area(self, parent):
        """Create input area with animation"""
        input_frame = tk.Frame(parent, bg=self.colors['bg_medium'], height=80)
        input_frame.pack(fill="x", side="bottom")
        input_frame.pack_propagate(False)
        
        # Input container with glow effect
        input_container = tk.Frame(input_frame, bg=self.colors['bg_light'], bd=1, relief="sunken")
        input_container.pack(fill="x", padx=15, pady=10)
        
        # Mic button
        self.mic_btn = tk.Button(
            input_container,
            text="🎤",
            font=("Segoe UI", 16),
            bg=self.colors['accent_pink'],
            fg=self.colors['text_white'],
            relief="flat",
            cursor="hand2",
            width=4,
            command=self._toggle_voice
        )
        self.mic_btn.pack(side="left", padx=5, pady=5)
        
        # Input box
        self.input_box = tk.Entry(
            input_container,
            bg=self.colors['bg_dark'],
            fg=self.colors['text_white'],
            font=("Segoe UI", 12),
            bd=0,
            insertbackground=self.colors['accent_cyan']
        )
        self.input_box.pack(side="left", fill="x", expand=True, padx=(5, 5), pady=10)
        self.input_box.bind("<Return>", self._send_message)
        
        # Send button
        send_btn = tk.Button(
            input_container,
            text="➤",
            font=("Segoe UI", 14),
            bg=self.colors['accent_cyan'],
            fg=self.colors['bg_dark'],
            relief="flat",
            cursor="hand2",
            width=4,
            command=self._send_message
        )
        send_btn.pack(side="right", padx=5, pady=5)
    
    def _create_footer(self, parent):
        """Create footer with info"""
        footer = tk.Frame(parent, bg=self.colors['bg_medium'], height=30)
        footer.pack(fill="x")
        footer.pack_propagate(False)
        
        self.footer_text = tk.Label(
            footer,
            text="🤖 RAMA AI v2.0 | Brain Training | Voice Enabled | 50+ Skills",
            font=("Segoe UI", 8),
            bg=self.colors['bg_medium'],
            fg=self.colors['text_gray']
        )
        self.footer_text.pack(pady=5)
    
    def _start_animations(self):
        """Start UI animations"""
        self._animate_glow()
        self._animate_avatar()
    
    def _animate_glow(self):
        """Animate glowing effect on status"""
        if not self.animation_running:
            return
        
        # Pulse effect
        colors = ["#00ff88", "#00ffff", "#9b59b6", "#00ff88"]
        current = random.choice(colors)
        
        self.status_dot.delete("all")
        self.status_dot.create_oval(1, 1, 14, 14, fill=current, outline="")
        self.status_dot.create_oval(4, 4, 11, 11, fill=current, outline="")
        
        # Schedule next
        self.root.after(2000, self._animate_glow)
    
    def _animate_avatar(self):
        """Animate avatar"""
        if not self.animation_running:
            return
        
        # Simple breathing animation (color shift)
        colors = [self.colors['accent_cyan'], self.colors['accent_purple'], self.colors['accent_pink']]
        
        # Schedule next
        self.root.after(3000, self._animate_avatar)
    
    def _update_time(self):
        """Update time display"""
        now = datetime.now()
        self.time_label.config(text=f"🕐 {now.strftime('%I:%M %p')}")
        self.root.after(60000, self._update_time)  # Update every minute
    
    def _quick_action(self, command):
        """Handle quick action buttons"""
        self.input_box.delete(0, "end")
        self.input_box.insert(0, command)
        self._send_message()
    
    def _toggle_voice(self):
        """Toggle voice mode"""
        if self.is_listening:
            self.is_listening = False
            self.mic_btn.config(bg=self.colors['accent_pink'])
            self.avatar_status.config(text="● Ready", fg="#00ff88")
        else:
            self.is_listening = True
            self.mic_btn.config(bg="#00ff88")
            self.avatar_status.config(text="● Listening...", fg=self.colors['accent_cyan'])
            self._add_message("🎤 Listening for voice input...", "system")
    
    def _send_message(self, event=None):
        """Send message"""
        message = self.input_box.get().strip()
        if not message:
            return
        
        self.input_box.delete(0, "end")
        
        # Display user message
        self._add_message(f"You: {message}", "user")
        
        # Process with RAMA
        if not self.rama:
            self._init_rama()
        
        # Add animation
        self.avatar_status.config(text="● Thinking...", fg=self.colors['accent_gold'])
        self.root.update()
        
        response = self.rama.process(message)
        
        # Display response
        self._add_message(f"Rama: {response}", "rama")
        
        # Update avatar status
        self.avatar_status.config(text="● Listening", fg="#00ff88")
        
        # Update brain info
        if hasattr(self.rama, 'brain_trainer'):
            status = self.rama.brain_trainer.get_brain_status()
            self.brain_info.config(text=status[:100] + "...")
    
    def _add_message(self, text, tag):
        """Add message to chat"""
        self.chat_text.config(state="normal")
        self.chat_text.insert("end", text + "\n\n", tag)
        self.chat_text.see("end")
        self.chat_text.config(state="disabled")
    
    def _init_rama(self):
        """Initialize RAMA backend"""
        try:
            import sys
            sys.path.insert(0, 'backend')
            from backend.model import RAMAModel
            
            self.rama = RAMAModel({'user_name': 'bhai', 'language': 'en', 'voice_enabled': False})
            self.rama.initialize()
            
            self._add_message("🤖 RAMA AI initialized successfully! 🎉\n", "system")
        except Exception as e:
            self._add_message(f"❌ Init error: {str(e)[:100]}", "system")
    
    def run(self):
        """Run the app"""
        self.root.mainloop()


# Main entry
if __name__ == "__main__":
    app = AnimatedRamaGUI()
    app.run()