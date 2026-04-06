# Frontend Graphics Assets
# Place AI voice assistant images here

# ============================================
# Recommended Image Assets to Add
# ============================================

# 1. Avatar Images (for 3D character)
# avatar_main.png      - Main RAMA avatar (500x500)
# avatar_avatar.png    - Avatar face closeup
# avatar_glow.png      - Glowing version

# 2. Backgrounds
# bg_cyberpunk.png     - Cyberpunk themed background
# bg_nebula.png        - Space/nebula background
# bg_ai.png           - AI neural network background
# bg_dark.png         - Dark gradient background

# 3. UI Elements
# mic_icon.png         - Microphone icon
# speaker_icon.png    - Speaker/sound icon
# brain_icon.png      - Brain/neural icon
# settings_icon.png   - Settings gear icon
# chat_bubble.png     - Chat message bubble
# loading_spinner.png - Loading animation

# 4. Status Indicators
# status_online.png   - Green online indicator
# status_listening.png - Listening animation
# status_thinking.png  - Thinking animation
# status_speaking.png  - Speaking animation

# 5. Skill Icons
# code_icon.png        - Programming icon
# search_icon.png      - Search icon
# file_icon.png        - File manager icon
# system_icon.png      - System info icon
# voice_icon.png       - Voice control icon
# brain_icon.png       - Learning/brain icon

# ============================================
# Image Requirements
# ============================================

# Recommended specs:
# - Format: PNG (with transparency)
# - Size: 256x256 or 512x512 for icons
# - Background: 1920x1080 for wallpapers
# - Style: Semi-transparent, glow effects

# ============================================
# To use images in code:
# ============================================

# from PIL import Image, ImageTk
# 
# # Load image
# img = Image.open("frontend/graphics/avatar_main.png")
# photo = ImageTk.PhotoImage(img)
# 
# # Use in Label
# label = tk.Label(frame, image=photo)
# label.image = photo  # Keep reference!

print("📁 Place your PNG images in frontend/graphics/")
print("📏 Recommended: 256x256 icons, 1920x1080 backgrounds")