"""
RAMA Voice Engine
Speech Recognition + Text-to-Speech + Wake Word Detection
Following the tutorial voice system setup
"""

import speech_recognition as sr
import pyttsx3
import threading
import time
import re


class VoiceEngine:
    """
    Voice I/O engine for RAMA
    Handles speech recognition and text-to-speech
    """
    
    def __init__(self):
        # Initialize speech recognizer
        self.recognizer = sr.Recognizer()
        
        # TTS engine
        self.tts_engine = None
        self.tts_available = False
        
        # Microphone
        self.microphone = None
        self.mic_available = False
        
        # Initialize components
        self._init_tts()
        self._init_mic()
        
        print("🎤 Voice Engine initialized")
    
    def _init_tts(self):
        """Initialize text-to-speech engine"""
        try:
            self.tts_engine = pyttsx3.init()
            
            # Set properties
            self.tts_engine.setProperty('rate', 150)
            self.tts_engine.setProperty('volume', 1.0)
            
            # Try to get a good voice
            voices = self.tts_engine.getProperty('voices')
            for voice in voices:
                if 'english' in voice.name.lower():
                    self.tts_engine.setProperty('voice', voice.id)
                    break
            
            self.tts_available = True
            print("✅ TTS (Text-to-Speech) ready!")
            
        except Exception as e:
            print(f"⚠️ TTS not available: {e}")
            self.tts_available = False
    
    def _init_mic(self):
        """Initialize microphone"""
        try:
            self.microphone = sr.Microphone()
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            self.mic_available = True
            print("✅ Microphone ready!")
        except Exception as e:
            print(f"⚠️ Microphone not available: {e}")
            self.mic_available = False
    
    def speak(self, text, blocking=False):
        """
        Convert text to speech
        Args:
            text: Text to speak
            blocking: If True, wait for speech to finish
        """
        if not self.tts_available:
            print(f"🔇 [TTS off] {text}")
            return
        
        try:
            if blocking:
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            else:
                # Run in separate thread
                thread = threading.Thread(target=self._speak_thread, args=(text,))
                thread.daemon = True
                thread.start()
        except Exception as e:
            print(f"❌ TTS Error: {e}")
    
    def _speak_thread(self, text):
        """Speak in background thread"""
        try:
            engine = pyttsx3.init()
            engine.say(text)
            engine.runAndWait()
        except:
            pass
    
    def listen(self, timeout=5):
        """
        Listen for speech and convert to text
        Args:
            timeout: Max seconds to listen
        Returns:
            Recognized text or None
        """
        if not self.mic_available:
            return None
        
        try:
            with self.microphone as source:
                print("🎤 Listening...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=timeout)
            
            # Try Google Speech Recognition
            try:
                text = self.recognizer.recognize_google(audio)
                print(f"👂 Heard: {text}")
                return text
            except sr.UnknownValueError:
                print("😕 Couldn't understand")
                return None
            except sr.RequestError:
                print("❌ Speech service unavailable")
                return None
                
        except Exception as e:
            print(f"❌ Listen Error: {e}")
            return None
    
    def listen_for_wake_word(self, wake_word="hey rama"):
        """
        Listen for wake word and return command after it
        Args:
            wake_word: The wake word to detect
        Returns:
            Command after wake word, or full speech if wake word detected
        """
        if not self.mic_available:
            print("⚠️ No microphone - using text mode")
            return None
        
        while True:
            try:
                with self.microphone as source:
                    print("🎤 Waiting for command...")
                    audio = self.recognizer.listen(source, timeout=10)
                
                # Recognize speech
                try:
                    text = self.recognizer.recognize_google(audio)
                    text_lower = text.lower()
                    
                    print(f"👂 Heard: {text}")
                    
                    # Check for wake word
                    if wake_word.lower() in text_lower:
                        # Extract command after wake word
                        command = text_lower.replace(wake_word.lower(), "").strip()
                        
                        if command:
                            return command
                        else:
                            # Just wake word, ask what to do
                            return "what"
                    else:
                        # No wake word, ignore
                        continue
                        
                except sr.UnknownValueError:
                    continue
                except sr.RequestError:
                    print("❌ Speech service error")
                    return None
                    
            except Exception as e:
                print(f"❌ Wake word error: {e}")
                return None
    
    def listen_continuous(self, callback, wake_word="hey rama"):
        """
        Continuous listening in background
        Args:
            callback: Function to call with recognized command
            wake_word: Wake word to detect
        """
        def listen_loop():
            while True:
                try:
                    command = self.listen_for_wake_word(wake_word)
                    if command:
                        callback(command)
                except Exception as e:
                    print(f"❌ Continuous listen error: {e}")
                    time.sleep(1)
        
        thread = threading.Thread(target=listen_loop, daemon=True)
        thread.start()


# Test function
if __name__ == "__main__":
    print("🧪 Testing RAMA Voice Engine...")
    
    voice = VoiceEngine()
    
    if voice.tts_available:
        print("\nTesting TTS...")
        voice.speak("Hello bhai! I am RAMA, your voice assistant!", blocking=True)
    
    print("\n✅ Voice Engine ready!")
    print("Use: from voice import VoiceEngine")