"""
RAMA AI - Text to Speech Module
Handles the assistant's voice output
"""

import os
import threading
import platform


class TextToSpeech:
    """
    Text-to-Speech engine for RAMA
    Handles voice output
    """
    
    def __init__(self, config=None):
        self.config = config or {}
        self.tts_engine = None
        self.tts_available = False
        self.platform = platform.system()
        
        # Settings
        self.rate = self.config.get('voice_rate', 150)
        self.volume = self.config.get('voice_volume', 1.0)
        
        self._init_engine()
    
    def _init_engine(self):
        """Initialize TTS engine"""
        try:
            import pyttsx3
            self.tts_engine = pyttsx3.init()
            
            # Set properties
            self.tts_engine.setProperty('rate', self.rate)
            self.tts_engine.setProperty('volume', self.volume)
            
            # Try to set a good voice
            try:
                voices = self.tts_engine.getProperty('voices')
                for voice in voices:
                    if 'english' in voice.name.lower():
                        self.tts_engine.setProperty('voice', voice.id)
                        break
            except:
                pass
            
            self.tts_available = True
            print("✅ TTS Engine ready!")
            
        except ImportError:
            print("⚠️ pyttsx3 not installed - voice disabled")
            self.tts_available = False
        except Exception as e:
            print(f"⚠️ TTS init error: {e}")
            self.tts_available = False
    
    def speak(self, text, blocking=False):
        """
        Speak the given text
        Args:
            text: Text to speak
            blocking: If True, wait for completion
        """
        if not self.tts_available:
            print(f"🔇 [Muted] {text}")
            return
        
        try:
            if blocking:
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            else:
                # Run in background thread
                thread = threading.Thread(target=self._speak_async, args=(text,))
                thread.daemon = True
                thread.start()
        except Exception as e:
            print(f"❌ TTS error: {e}")
    
    def _speak_async(self, text):
        """Speak in background"""
        try:
            import pyttsx3
            engine = pyttsx3.init()
            engine.setProperty('rate', self.rate)
            engine.setProperty('volume', self.volume)
            engine.say(text)
            engine.runAndWait()
        except:
            pass
    
    def speak_multiple(self, texts):
        """Speak multiple texts in sequence"""
        for text in texts:
            self.speak(text, blocking=True)
    
    def stop(self):
        """Stop speaking"""
        if self.tts_available and self.tts_engine:
            try:
                self.tts_engine.stop()
            except:
                pass


# Windows SAPI fallback (no extra libraries)
class WindowsSAPI:
    """Windows built-in TTS (no install needed)"""
    
    @staticmethod
    def speak(text):
        """Speak using PowerShell"""
        try:
            import subprocess
            text_escaped = text.replace('"', '`"')
            script = f'Add-Type -AssemblyName System.Speech; $speak = New-Object System.Speech.Synthesis.SpeechSynthesizer; $speak.Speak("{text_escaped}")'
            subprocess.Popen(
                ['powershell', '-Command', script],
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            return True
        except:
            return False


if __name__ == "__main__":
    tts = TextToSpeech()
    if tts.tts_available:
        tts.speak("Hello bhai! I am RAMA!", blocking=True)
    else:
        print("Install pyttsx3 for voice: pip install pyttsx3")