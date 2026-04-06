"""
RAMA AI - Speech to Text Module
Processes voice input
"""

import speech_recognition as sr
import time


class SpeechToText:
    """
    Speech recognition for RAMA
    Converts voice to text
    """
    
    def __init__(self, config=None):
        self.config = config or {}
        self.recognizer = sr.Recognizer()
        self.microphone = None
        self.mic_available = False
        self.timeout = self.config.get('stt_timeout', 5)
        
        self._init_microphone()
    
    def _init_microphone(self):
        """Initialize microphone"""
        try:
            self.microphone = sr.Microphone()
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            self.mic_available = True
            print("✅ Microphone ready!")
        except ImportError:
            print("⚠️ pyaudio not installed - voice input disabled")
            self.mic_available = False
        except Exception as e:
            print(f"⚠️ Mic init error: {e}")
            self.mic_available = False
    
    def listen(self, timeout=None):
        """
        Listen and convert speech to text
        Args:
            timeout: Max seconds to listen
        Returns:
            Recognized text or None
        """
        if not self.mic_available:
            return None
        
        timeout = timeout or self.timeout
        
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
            print(f"❌ Listen error: {e}")
            return None
    
    def listen_for_wake_word(self, wake_word="hey rama"):
        """
        Listen for wake word and return command
        Args:
            wake_word: The wake word to detect
        Returns:
            Command after wake word
        """
        if not self.mic_available:
            return None
        
        while True:
            try:
                with self.microphone as source:
                    print("🎤 Waiting for command...")
                    audio = self.recognizer.listen(source, timeout=10)
                
                try:
                    text = self.recognizer.recognize_google(audio)
                    text_lower = text.lower()
                    
                    print(f"👂 Heard: {text}")
                    
                    # Check for wake word
                    if wake_word.lower() in text_lower:
                        command = text_lower.replace(wake_word.lower(), "").strip()
                        if command:
                            return command
                        else:
                            return "what"
                    else:
                        continue
                        
                except sr.UnknownValueError:
                    continue
                except sr.RequestError:
                    return None
                    
            except Exception as e:
                print(f"❌ Wake word error: {e}")
                return None
    
    def listen_continuous(self, callback, wake_word="heyrama"):
        """
        Start continuous background listening
        Args:
            callback: Function to call with command
        """
        import threading
        
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


if __name__ == "__main__":
    stt = SpeechToText()
    if stt.mic_available:
        print("Say something...")
        result = stt.listen()
        print(f"You said: {result}")
    else:
        print("Install pyaudio for voice input: pip install pyaudio")