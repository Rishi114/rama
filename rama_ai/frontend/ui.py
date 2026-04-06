"""RAMA AI v2.0 - Main UI
Desktop UI using CustomTkinter"""

import customtkinter as ctk
from typing import Optional
import threading
import logging

logger = logging.getLogger(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)


class RAMAUI(ctk.CTk):
    """
    Main RAMA AI Desktop UI
    Dark theme with Arc reactor style
    """
    
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title("RAMA AI v2.0")
        self.geometry("1000x700")
        self.resizable(True, True)
        
        # Set theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        
        # Configure grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Components
        self.brain = None
        self.voice = None
        self.is_processing = False
        
        # Build UI
        self._build_sidebar()
        self._build_main_area()
        self._build_input_area()
        
        # Start
        self.after(1000, self._on_load)
    
    def _build_sidebar(self):
        """Build left sidebar"""
        self.sidebar = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.sidebar.grid(row=0, column=0, rowspan=3, sticky="nsew")
        self.sidebar.grid_rowconfigure(10, weight=1)
        
        # Logo
        logo_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        logo_frame.grid(row=0, column=0, padx=20, pady=20)
        
        logo = ctk.CTkLabel(
            logo_frame,
            text="🤖",
            font=ctk.CTkFont(size=60)
        )
        logo.pack()
        
        title = ctk.CTkLabel(
            logo_frame,
            text="RAMA AI",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.pack()
        
        subtitle = ctk.CTkLabel(
            logo_frame,
            text="v2.0",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        subtitle.pack()
        
        # Status
        status_frame = ctk.CTkFrame(self.sidebar)
        status_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        
        self.status_label = ctk.CTkLabel(
            status_frame,
            text="● Online",
            text_color="green",
            font=ctk.CTkFont(size=12)
        )
        self.status_label.pack(anchor="w", padx=10, pady=5)
        
        # Skills section
        skills_label = ctk.CTkLabel(
            self.sidebar,
            text="SKILLS",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="gray"
        )
        skills_label.grid(row=2, column=0, padx=20, pady=(20, 5), sticky="w")
        
        # Skill buttons
        skills = [
            ("🚀 App Launcher", self.on_skill_click),
            ("📁 File Manager", self.on_skill_click),
            ("💻 System Info", self.on_skill_click),
            ("🧮 Calculator", self.on_skill_click),
            ("🌤️ Weather", self.on_skill_click),
            ("🔍 Web Search", self.on_skill_click),
            ("💻 Coding", self.on_skill_click),
            ("🧠 Knowledge", self.on_skill_click),
        ]
        
        for i, (text, command) in enumerate(skills):
            btn = ctk.CTkButton(
                self.sidebar,
                text=text,
                command=command,
                fg_color="transparent",
                border_width=1,
                border_color="#3B3B5C",
                hover_color="#2B2B4C",
                height=35,
                anchor="w"
            )
            btn.grid(row=3 + i, column=0, padx=20, pady=3, sticky="ew")
        
        # Bottom controls
        bottom_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        bottom_frame.grid(row=20, column=0, padx=20, pady=20, sticky="s")
        
        self.mic_button = ctk.CTkButton(
            bottom_frame,
            text="🎤 Voice",
            command=self.toggle_voice,
            fg_color="#7C3AED",
            height=40
        )
        self.mic_button.pack(fill="x", pady=5)
        
        self.listen_button = ctk.CTkButton(
            bottom_frame,
            text="👂 Listen",
            command=self.start_listening,
            fg_color="transparent",
            border_width=1,
            border_color="#3B3B5C",
            height=35
        )
        self.listen_button.pack(fill="x", pady=5)
    
    def _build_main_area(self):
        """Build main chat area"""
        self.chat_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent"
        )
        self.chat_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.chat_frame.grid_columnconfigure(0, weight=1)
        
        # Welcome message
        self.add_message("🤖", "RAMA", "✨ Hello! I'm RAMA AI v2.0!\n\nYour offline AI assistant with:\n• 🧠 Self-learning\n• 🎙️ Voice support\n• 💻 30+ coding languages\n• 🔧 Task automation\n\nType a message or click a skill!", False)
    
    def _build_input_area(self):
        """Build bottom input area"""
        self.input_frame = ctk.CTkFrame(self, height=80)
        self.input_frame.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
        self.input_frame.grid_columnconfigure(0, weight=1)
        
        self.input_box = ctk.CTkTextbox(
            self.input_frame,
            font=ctk.CTkFont(size=14),
            border_width=0,
            fg_color="#1E1E2E",
            height=50
        )
        self.input_box.grid(row=0, column=0, padx=(10, 5), pady=10, sticky="ew")
        self.input_box.bind("<Return>", self.on_enter)
        
        self.send_button = ctk.CTkButton(
            self.input_frame,
            text="➤",
            width=60,
            fg_color="#7C3AED",
            command=self.send_message
        )
        self.send_button.grid(row=0, column=1, padx=(5, 10), pady=10)
    
    def _on_load(self):
        """Called after UI loads"""
        logger.info("🎉 RAMA UI loaded!")
        # Initialize brain in background
        threading.Thread(target=self._init_brain, daemon=True).start()
    
    def _init_brain(self):
        """Initialize AI brain"""
        try:
            # This would initialize the brain in a real implementation
            # from core.brain import Brain
            # self.brain = Brain({})
            # asyncio.run(self.brain.initialize())
            pass
        except Exception as e:
            logger.warning(f"Brain init: {e}")
    
    def add_message(self, emoji: str, name: str, text: str, is_user: bool):
        """Add a message to the chat"""
        # Container
        frame = ctk.CTkFrame(self.chat_frame, fg_color="transparent")
        frame.pack(fill="x", pady=5)
        
        # Color based on user/assistant
        if is_user:
            bg = "#7C3AED"
            anchor = "e"
        else:
            bg = "#1E1E2E"
            anchor = "w"
        
        # Message bubble
        bubble = ctk.CTkFrame(
            frame,
            fg_color=bg,
            corner_radius=15
        )
        bubble.pack(side="right" if is_user else "left", padx=10)
        
        # Header
        header = ctk.CTkLabel(
            bubble,
            text=f"{emoji} {name}",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#A855F7" if not is_user else "white"
        )
        header.pack(anchor="w", padx=15, pady=(10, 5))
        
        # Content
        content = ctk.CTkLabel(
            bubble,
            text=text,
            font=ctk.CTkFont(size=13),
            justify="left" if not is_user else "right",
            wraplength=500
        )
        content.pack(anchor="w", padx=15, pady=(0, 10))
    
    def on_enter(self, event=None):
        """Handle Enter key"""
        self.send_message()
        return "break"
    
    def send_message(self):
        """Send user message"""
        text = self.input_box.get("1.0", "end").strip()
        if not text:
            return
        
        # Add user message
        self.add_message("👤", "You", text, True)
        self.input_box.delete("1.0", "end")
        
        # Show typing
        self.after(100, lambda: self.add_message("🤖", "RAMA", "💭 Thinking...", False))
        
        # Process in background
        threading.Thread(target=self._process_message, args=(text,), daemon=True).start()
    
    def _process_message(self, text: str):
        """Process message in background"""
        try:
            # Process with brain (placeholder)
            response = self._get_response(text)
            
            # Update UI
            self.after(0, lambda: self._show_response(response))
            
        except Exception as e:
            logger.error(f"Process error: {e}")
            self.after(0, lambda: self._show_response(f"❌ Error: {str(e)}"))
    
    def _get_response(self, text: str) -> str:
        """Get response from brain"""
        # Placeholder - in real impl would call brain.process()
        text_lower = text.lower()
        
        if "help" in text_lower:
            return """📋 Here's what I can do:

**Skills:**
• 🚀 Open apps - "open notepad"
• 📁 List files - "list files"
• 💻 System info - "system info"
• 🧮 Calculate - "calculate 2+2"
• 🌤️ Weather - "weather Tokyo"
• 🔍 Search - "search Python"
• 💻 Code - "code python"
• 🧠 Learn - "learn that X is Y"

**Voice:**
• Click 🎤 to toggle voice output
• Click 👂 to start listening

**Tips:**
• Say "help" anytime for this list"""
        
        # Simple responses
        responses = {
            "hello": "Hey there! 👋 I'm RAMA!",
            "hi": "Yo! ✨ What's up?",
            "who are you": "I'm RAMA, your AI assistant! 🤖",
            "thanks": "You're welcome! 😄 Anything else?",
            "bye": "See ya! 👋 Talk later!",
        }
        
        for key, value in responses.items():
            if key in text_lower:
                return value
        
        return f"💬 You said: {text}\n\nTry 'help' to see what I can do!"
    
    def _show_response(self, response: str):
        """Show response in chat"""
        # Remove typing indicator (last message)
        for widget in self.chat_frame.winfo_children():
            if "Thinking" in str(widget):
                widget.destroy()
        
        self.add_message("🤖", "RAMA", response, False)
    
    def on_skill_click(self):
        """Handle skill button click"""
        # Show skill help
        self.add_message("💡", "RAMA", "Click a skill button to see its commands!", False)
    
    def toggle_voice(self):
        """Toggle voice output"""
        logger.info("🎤 Voice toggled")
        self.add_message("🎤", "RAMA", "Voice output toggled!", False)
    
    def start_listening(self):
        """Start voice listening"""
        logger.info("👂 Starting listening...")
        self.add_message("👂", "RAMA", "Listening... (Voice input would start here)", False)


def main():
    """Entry point"""
    app = RAMAUI()
    app.mainloop()


if __name__ == "__main__":
    main()