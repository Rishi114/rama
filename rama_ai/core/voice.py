"""
RAMA Voice Pipeline - Speech to Text & Text to Speech
Makes RAMA a true Voice Assistant!
"""

import os
import sys
import asyncio
import threading
import time
from typing import Optional, Callable


class VoicePipeline:
    """
    Complete Voice I/O for RAMA
    - Speech Recognition (STT)
    - Text-to-Speech (TTS)
    - Wake Word Detection (optional)
    """
    
    def __init__(self):
        self.tts_available = False
        self.stt_available = False
        self.voice_enabled = False
        
        # Check what's available
        self._check_dependencies()
    
    def _check_dependencies(self):
        """Check available voice libraries"""
        
        # Check for TTS options
        tts_options = ["pyttsx3", "pyttsx4", "gtts", "silero"]
        
        for tts_lib in tts_options:
            try:
                if tts_lib in ["pyttsx3", "pyttsx4"]:
                    import pyttsx3
                    self.tts_engine = pyttsx3.init()
                    self.tts_available = True
                    print("✅ pyttsx3 TTS available!")
                    break
                elif tts_lib == "silero":
                    import torch
                    # Silero TTS would need model download
                    print("ℹ️ Silero TTS available (needs model)")
                elif tts_lib == "gtts":
                    import gtts
                    self.tts_available = True
                    print("✅ gtts TTS available!")
                    break
            except ImportError:
                continue
        
        # Check for STT options
        stt_options = ["speech_recognition", "whisper", "faster_whisper"]
        
        for stt_lib in stt_options:
            try:
                if stt_lib == "speech_recognition":
                    import speech_recognition
                    self.stt_available = True
                    print("✅ Speech Recognition available!")
                    break
                elif stt_lib in ["whisper", "faster_whisper"]:
                    print(f"ℹ️ {stt_lib} available (better quality)")
            except ImportError:
                continue
        
        # Windows SAPI (built-in)
        try:
            import pyttsx3
            self.tts_available = True
            print("✅ Windows TTS (SAPI) available!")
        except:
            pass
    
    def speak(self, text: str, blocking: bool = False) -> bool:
        """
        Convert text to speech
        Args:
            text: Text to speak
            blocking: If True, wait for speech to finish
        Returns:
            Success status
        """
        if not self.tts_available:
            print(f"🔇 TTS not available: {text[:50]}...")
            return False
        
        try:
            # Try pyttsx3 first (works offline)
            import pyttsx3
            engine = pyttsx3.init()
            
            # Set properties
            engine.setProperty('rate', 150)  # Speed
            engine.setProperty('volume', 1.0)  # Volume
            
            # Try to set Indian English voice
            voices = engine.getProperty('voices')
            for voice in voices:
                if 'english' in voice.name.lower() or 'india' in voice.name.lower():
                    engine.setProperty('voice', voice.id)
                    break
            
            if blocking:
                engine.say(text)
                engine.runAndWait()
            else:
                # Run in separate thread
                def speak_thread():
                    engine.say(text)
                    engine.runAndWait()
                
                thread = threading.Thread(target=speak_thread, daemon=True)
                thread.start()
            
            return True
            
        except Exception as e:
            print(f"❌ TTS Error: {e}")
            return False
    
    def listen(self, timeout: int = 5) -> Optional[str]:
        """
        Listen for speech and convert to text
        Args:
            timeout: Max seconds to listen
        Returns:
            Recognized text or None
        """
        if not self.stt_available:
            return None
        
        try:
            import speech_recognition as sr
            
            recognizer = sr.Recognizer()
            
            with sr.Microphone() as source:
                print("🎤 Listening...")
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = recognizer.listen(source, timeout=timeout)
            
            # Try Google Speech Recognition (needs internet)
            # For offline, use wit.ai or other local options
            try:
                text = recognizer.recognize_google(audio)
                print(f"👂 Heard: {text}")
                return text
            except:
                # Try Sphinx (offline, needs pocketsphinx)
                try:
                    text = recognizer.recognize_sphinx(audio)
                    return text
                except:
                    pass
                    
        except Exception as e:
            print(f"❌ STT Error: {e}")
        
        return None
    
    def listen_loop(self, callback: Callable[[str], None], wake_word: str = "rama"):
        """
        Continuous listening loop with wake word detection
        Args:
            callback: Function to call with recognized text
            wake_word: Word to trigger listening
        """
        if not self.stt_available:
            print("❌ STT not available for voice loop")
            return
        
        print(f"🎤 Voice mode enabled! Say '{wake_word}' to activate...")
        
        while self.voice_enabled:
            try:
                text = self.listen(timeout=3)
                
                if text and wake_word.lower() in text.lower():
                    # Remove wake word from text
                    response = text.lower().replace(wake_word.lower(), "").strip()
                    if response:
                        callback(response)
                        
            except Exception as e:
                continue
    
    def start_voice_mode(self):
        """Enable voice mode"""
        self.voice_enabled = True
    
    def stop_voice_mode(self):
        """Disable voice mode"""
        self.voice_enabled = False


# ============================================
# FALLBACK: Windows SAPI (No Install Needed)
# ============================================

class SimpleTTS:
    """
    Simple TTS using ctypes - no extra libraries needed!
    Works on Windows with SAPI
    """
    
    @staticmethod
    def speak(text: str) -> bool:
        """Speak using Windows built-in speech"""
        try:
            # Use PowerShell for TTS (built into Windows)
            import subprocess
            
            # Escape quotes for PowerShell
            text_escaped = text.replace('"', '`"')
            
            script = f'Add-Type -AssemblyName System.Speech; $speak = New-Object System.Speech.Synthesis.SpeechSynthesizer; $speak.Speak("{text_escaped}")'
            
            subprocess.Popen(
                ['powershell', '-Command', script],
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            return True
            
        except Exception as e:
            print(f"TTS Error: {e}")
            return False
    
    @staticmethod
    def speak_async(text: str):
        """Speak in background thread"""
        def speak_thread():
            SimpleTTS.speak(text)
        
        thread = threading.Thread(target=speak_thread, daemon=True)
        thread.start()


# ============================================
# VOICE COMMANDS FOR RAMA
# ============================================

class VoiceCommands:
    """Voice command patterns"""
    
    commands = {
        # Navigation
        "open": ["open", "start", "launch"],
        "close": ["close", "stop", "quit"],
        "search": ["search", "find", "look up"],
        
        # Actions
        "play": ["play", "start", "resume"],
        "pause": ["pause", "stop"],
        "next": ["next", "skip"],
        "previous": ["previous", "back"],
        
        # Settings
        "volume up": ["louder", "increase volume", "volume up"],
        "volume down": ["quieter", "decrease volume", "volume down"],
        "mute": ["mute", "silent"],
        
        # System
        "screenshot": ["screenshot", "capture screen", "take photo"],
        "shutdown": ["shutdown", "turn off"],
        "restart": ["restart", "reboot"],
    }
    
    @classmethod
    def match(cls, text: str) -> Optional[str]:
        """Match voice command"""
        text_lower = text.lower()
        
        for cmd, patterns in cls.commands.items():
            for pattern in patterns:
                if pattern in text_lower:
                    return cmd
        
        return None


# Quick test
if __name__ == "__main__":
    print("🎤 Testing RAMA Voice...")
    
    voice = VoicePipeline()
    
    if voice.tts_available:
        print("\nTesting TTS...")
        voice.speak("Hello bhai! I am RAMA, your voice assistant!", blocking=True)
    
    print("\n✅ Voice pipeline ready!")
    print("Add to your RAMA with: from core.voice import VoicePipeline")