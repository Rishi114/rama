"""
RAMA AI - Animated GUI with Image Support
Supports images from graphics folder
"""

import tkinter as tk
from tkinter import ttk
import os
import random
from datetime import datetime
from PIL import Image, ImageTk


class ImageRamaGUI:
    """RAMA AI - GUI with Image Support"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🤖 RAMA AI - Jarvis Assistant")
        self.root.geometry("1200x800")
        self.root.configure(bg="#0a0a1a")
        
        # Graphics path
        self.graphics_path = os.path.join(os.path.dirname(__file__), "graphics")
        
        # Colors
        self.colors = {
            "bg_dark": "#0a0a1a",
            "bg_medium": "#12122a",
            "bg_light": "#1a1a3a",
            "accent_cyan": "#00ffff",
            "accent_purple": "#9b59b6",
            "accent_pink": "#ff006e",
            "text_white": "#ffffff",
            "text_gray": "#a0a0a0",
        }
        
        # Load images
        self.images = {}
        self._load_images()
        
        # State
        self.rama = None
        self.animation_running = True
        
        # Setup
        self._create_ui()
        self._start_animations()
    
    def _load_images(self):
        """Load images from graphics folder"""
        # Try to load images if they exist
        image_files = [
            "avatar.png", "avatar_main.png", "avatar_glow.png",
            "bg_cyberpunk.png", "background.png",
            "mic.png", "mic_icon.png",
            "brain.png", "brain_icon.png",
        ]
        
        for img_file in image_files:
            img_path = os.path.join(self.graphics_path, img_file)
            if os.path.exists(img_path):
                try:
                    img = Image.open(img_path)
                    # Resize if too large
                    if img.size[0] > 400:
                        img = img.resize((400, 400), Image.LANCZOS)
                    self.images[img_file.split('.')[0]] = ImageTk.PhotoImage(img)
                    print(f"✅ Loaded: {img_file}")
                except Exception as e:
                    print(f"⚠️ Could not load {img_file}: {e}")
    
    def _create_placeholder_image(self, size=200, text="RAMA"):
        """Create a placeholder image with text"""
        # Create canvas
        canvas = tk.Canvas(None, width=size, height=size, bg=self.colors['bg_dark'], highlightthickness=0)
        
        # Draw circular background
        canvas.create_oval(10, 10, size-10, size-10, fill=self.colors['bg_medium'], outline=self.colors['accent_cyan'], width=3)
        
        # Draw inner circle
        canvas.create_oval(30, 30, size-30, size-30, fill=self.colors['bg_light'], outline="")
        
        # Draw face circle
        canvas.create_oval(size//3, size//3, 2*size//3, 2*size//3, fill=self.colors['accent_cyan'], outline="")
        
        # Eyes
        eye_y = size//2 - 20
        canvas.create_oval(size//2 - 40, eye_y, size//2 - 20, eye_y + 20, fill="white", outline="")
        canvas.create_oval(size//2 + 20, eye_y, size//2 + 40, eye_y + 20, fill="white", outline="")
        
        # Pupils
        canvas.create_oval(size//2 - 35, eye_y + 5, size//2 - 25, eye_y + 15, fill=self.colors['bg_dark'], outline="")
        canvas.create_oval(size//2 + 25, eye_y + 5, size//2 + 35, eye_y + 15, fill=self.colors['bg_dark'], outline="")
        
        # Mouth
        canvas.create_arc(size//2 - 30, eye_y + 40, size//2 + 30, eye_y + 60, start=0, extent=180, fill="", outline=self.colors['accent_cyan'], width=2)
        
        # Antenna
        canvas.create_line(size//2, 20, size//2, 5, fill=self.colors['accent_cyan'], width=3)
        canvas.create_oval(size//2 - 10, 0, size//2 + 10, 15, fill=self.colors['accent_pink'], outline="")
        
        return canvas
    
    def _create_ui(self):
        """Create the main UI with background image"""
        
        # ==================== BACKGROUND ====================
        # If background image exists, use it
        if "background" in self.images or "bg_cyberpunk" in self.images:
            bg_img = self.images.get("background") or self.images.get("bg_cyberpunk")
            bg_label = tk.Label(self.root, image=bg_img)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        else:
            # Gradient background
            self._create_gradient_background()
        
        # ==================== MAIN CONTAINER ====================
        main = tk.Frame(self.root, bg="")
        main.pack(fill="both", expand=True, padx=20, pady=20)
        
        # ==================== HEADER ====================
        self._create_header(main)
        
        # ==================== CONTENT ====================
        content = tk.Frame(main, bg="")
        content.pack(fill="both", expand=True, pady=15)
        
        # Left - Avatar
        self._create_avatar_section(content)
        
        # Center - Chat
        self._create_chat_section(content)
        
        # Right - Controls
        self._create_controls_section(content)
        
        # ==================== INPUT ====================
        self._create_input_section(main)
    
    def _create_gradient_background(self):
        """Create a gradient-like background"""
        # Dark gradient effect using frames
        for i in range(10):
            alpha = 10 + i * 5
            color = f"#0{i}{i}{i}{i}{i}"
            frame = tk.Frame(self.root, bg=color, height=80)
            frame.pack(fill="x")
    
    def _create_header(self, parent):
        """Create header with logo and status"""
        header = tk.Frame(parent, bg="")
        header.pack(fill="x")
        
        # Logo with image or text
        if "avatar_main" in self.images:
            logo = tk.Label(header, image=self.images["avatar_main"], bg="")
            logo.image = self.images["avatar_main"]
            logo.pack(side="left")
        else:
            # Text logo
            logo = tk.Label(
                header,
                text="🤖 RAMA AI",
                font=("Segoe UI", 28, "bold"),
                bg="",
                fg=self.colors['accent_cyan']
            )
            logo.pack(side="left")
        
        # Title
        title = tk.Label(
            header,
            text=" Jarvis Assistant",
            font=("Segoe UI", 18),
            bg="",
            fg=self.colors['accent_purple']
        )
        title.pack(side="left")
        
        # Status
        status_frame = tk.Frame(header, bg="")
        status_frame.pack(side="right")
        
        self.status_canvas = tk.Canvas(status_frame, width=20, height=20, bg="", highlightthickness=0)
        self.status_canvas.pack(side="right", padx=10)
        self.status_canvas.create_oval(2, 2, 18, 18, fill="#00ff88", outline="")
        
        self.status_label = tk.Label(status_frame, text="Online", font=("Segoe UI", 12), bg="", fg="#00ff88")
        self.status_label.pack(side="right")
    
    def _create_avatar_section(self, parent):
        """Create avatar section with image"""
        avatar_frame = tk.Frame(parent, bg="", width=300)
        avatar_frame.pack(side="left", padx=10)
        avatar_frame.pack_propagate(False)
        
        # Avatar display
        if "avatar" in self.images:
            self.avatar_label = tk.Label(avatar_frame, image=self.images["avatar"], bg="")
            self.avatar_label.image = self.images["avatar"]
            self.avatar_label.pack(pady=20)
        else:
            # Canvas avatar
            self.avatar_canvas = self._create_placeholder_image(250)
            self.avatar_canvas.pack(pady=20)
        
        # Name
        name_label = tk.Label(avatar_frame, text="RAMA", font=("Segoe UI", 20, "bold"), bg="", fg=self.colors['accent_cyan'])
        name_label.pack()
        
        # Status
        self.avatar_status = tk.Label(avatar_frame, text="● Listening", font=("Segoe UI", 12), bg="", fg="#00ff88")
        self.avatar_status.pack()
        
        # Quick buttons with icons
        btn_frame = tk.Frame(avatar_frame, bg="")
        btn_frame.pack(pady=15)
        
        buttons = [
            ("🎤", "Voice"),
            ("🧠", "Brain"),
            ("💻", "Code"),
        ]
        
        for icon, name in buttons:
            btn = tk.Button(btn_frame, text=f"{icon} {name}", font=("Segoe UI", 10),
                          bg=self.colors['bg_light'], fg=self.colors['text_white'],
                          relief="flat", padx=10, pady=5)
            btn.pack(side="left", padx=5)
    
    def _create_chat_section(self, parent):
        """Create chat section"""
        chat_frame = tk.Frame(parent, bg="", width=500)
        chat_frame.pack(side="left", padx=10, fill="both", expand=True)
        chat_frame.pack_propagate(False)
        
        # Title
        tk.Label(chat_frame, text="💬 Conversation", font=("Segoe UI", 14, "bold"),
                bg="", fg=self.colors['text_white']).pack(anchor="w")
        
        # Chat area
        chat_bg = tk.Frame(chat_frame, bg=self.colors['bg_medium'], bd=2, relief="solid")
        chat_bg.pack(fill="both", expand=True, pady=10)
        
        self.chat_text = tk.Text(
            chat_bg,
            bg=self.colors['bg_dark'],
            fg=self.colors['text_white'],
            font=("Segoe UI", 11),
            wrap="word",
            state="disabled",
            bd=0
        )
        self.chat_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Tags
        self.chat_text.tag_config("user", foreground="#4da6ff")
        self.chat_text.tag_config("rama", foreground=self.colors['accent_cyan'])
        self.chat_text.tag_config("system", foreground=self.colors['text_gray'])
        
        # Initial message
        self._add_message("🤖 RAMA: Hello bhai! I'm ready! 🎉\n\nType 'help' for commands!", "system")
    
    def _create_controls_section(self, parent):
        """Create controls section"""
        ctrl_frame = tk.Frame(parent, bg="", width=250)
        ctrl_frame.pack(side="right", padx=10)
        ctrl_frame.pack_propagate(False)
        
        # Brain Status
        tk.Label(ctrl_frame, text="🧠 Brain Status", font=("Segoe UI", 12, "bold"),
                bg="", fg=self.colors['text_white']).pack(anchor="w", pady=(0, 5))
        
        brain_bg = tk.Frame(ctrl_frame, bg=self.colors['bg_medium'], bd=1, relief="solid")
        brain_bg.pack(fill="x", pady=5)
        
        self.brain_label = tk.Label(
            brain_bg,
            text="Training: Active\nEpochs: 0\nAccuracy: 50%\nKnowledge: 0 facts",
            font=("Segoe UI", 10),
            bg=self.colors['bg_medium'],
            fg=self.colors['text_gray'],
            justify="left"
        )
        self.brain_label.pack(padx=10, pady=10)
        
        # Skills
        tk.Label(ctrl_frame, text="🎯 Skills", font=("Segoe UI", 12, "bold"),
                bg="", fg=self.colors['text_white']).pack(anchor="w", pady=(15, 5))
        
        skills_frame = tk.Frame(ctrl_frame, bg=self.colors['bg_medium'], bd=1, relief="solid")
        skills_frame.pack(fill="x", pady=5)
        
        skills = ["💻 Code", "🔍 Search", "🧮 Math", "📁 Files", "🧠 Learn", "🎤 Voice"]
        for skill in skills:
            tk.Label(skills_frame, text=skill, font=("Segoe UI", 10),
                    bg=self.colors['bg_medium'], fg=self.colors['text_gray'],
                    anchor="w").pack(fill="x", padx=10, pady=2)
        
        # Time
        self.time_label = tk.Label(ctrl_frame, text="",
                font=("Segoe UI", 14), bg="", fg=self.colors['accent_cyan'])
        self.time_label.pack(pady=20)
        self._update_time()
    
    def _create_input_section(self, parent):
        """Create input section"""
        input_frame = tk.Frame(parent, bg="", height=60)
        input_frame.pack(fill="x", pady=(10, 0))
        input_frame.pack_propagate(False)
        
        # Input container
        input_bg = tk.Frame(input_frame, bg=self.colors['bg_medium'], bd=2, relief="solid")
        input_bg.pack(fill="x", padx=50)
        
        # Mic button with icon
        if "mic" in self.images:
            mic_btn = tk.Button(input_bg, image=self.images["mic"], bg=self.colors['bg_light'],
                              relief="flat", width=40, height=40)
            mic_btn.image = self.images["mic"]
        else:
            mic_btn = tk.Button(input_bg, text="🎤", font=("Segoe UI", 16),
                              bg=self.colors['accent_pink'], fg="white", relief="flat", width=4)
        mic_btn.pack(side="left", padx=5, pady=5)
        
        # Input box
        self.input_box = tk.Entry(
            input_bg,
            bg=self.colors['bg_dark'],
            fg=self.colors['text_white'],
            font=("Segoe UI", 14),
            bd=0,
            insertbackground=self.colors['accent_cyan']
        )
        self.input_box.pack(side="left", fill="x", expand=True, padx=5)
        self.input_box.bind("<Return>", self._send_message)
        
        # Send button
        send_btn = tk.Button(input_bg, text="➤", font=("Segoe UI", 14),
                            bg=self.colors['accent_cyan'], fg=self.colors['bg_dark'],
                            relief="flat", width=4, command=self._send_message)
        send_btn.pack(side="right", padx=5, pady=5)
    
    def _update_time(self):
        """Update time display"""
        now = datetime.now()
        self.time_label.config(text=now.strftime("%I:%M %p"))
        self.root.after(60000, self._update_time)
    
    def _start_animations(self):
        """Start UI animations"""
        self._animate_status()
    
    def _animate_status(self):
        """Animate status indicator"""
        if not self.animation_running:
            return
        
        colors = ["#00ff88", self.colors['accent_cyan'], self.colors['accent_purple']]
        self.status_canvas.delete("all")
        self.status_canvas.create_oval(2, 2, 18, 18, fill=colors[random.randint(0, 2)], outline="")
        
        self.root.after(1500, self._animate_status)
    
    def _send_message(self, event=None):
        """Send message"""
        message = self.input_box.get().strip()
        if not message:
            return
        
        self.input_box.delete(0, "end")
        
        self._add_message(f"You: {message}", "user")
        self._add_message(f"Rama: Processing... 🎯", "system")
    
    def _add_message(self, text, tag):
        """Add message to chat"""
        self.chat_text.config(state="normal")
        self.chat_text.insert("end", text + "\n\n", tag)
        self.chat_text.see("end")
        self.chat_text.config(state="disabled")
    
    def run(self):
        """Run the app"""
        self.root.mainloop()


# Main
if __name__ == "__main__":
    app = ImageRamaGUI()
    app.run()