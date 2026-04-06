"""Voice Pipeline - Complete Offline Voice System
STT, TTS, and Wake Word Detection"""

import asyncio
import logging
from typing import Optional, Callable, List
import threading
import audioop
import numpy as np

logger = logging.getLogger(__name__)


class VoicePipeline:
    """
    Complete voice pipeline - all offline
    Wake Word → STT → LLM → TTS
    """
    
    def __init__(self, config: dict):
        self.config = config
        self.wake_word = None
        self.stt = None
        self.tts = None
        self.is_listening = False
        self.is_speaking = False
        self.callback: Optional[Callable] = None
        
    async def initialize(self):
        """Initialize all voice components"""
        logger.info("🎙️ Initializing Voice Pipeline...")
        
        # Initialize Wake Word
        from voice.wake_word import WakeWordDetector
        self.wake_word = WakeWordDetector(
            keywords=["hey rama", "rama", "okay rama"],
            sensitivity=0.5
        )
        
        # Initialize STT
        from voice.stt import STTEngine
        self.stt = STTEngine(
            model_size=self.config.get("stt_model", "tiny"),
            device="cpu"
        )
        
        # Initialize TTS
        from voice.tts import TTSEngine
        self.tts = TTSEngine(
            model=self.config.get("tts_model", "silero")
        )
        
        logger.info("✅ Voice Pipeline initialized!")
    
    async def start_listening(self, callback: Callable[[str], None]):
        """Start continuous listening for wake word"""
        self.callback = callback
        self.is_listening = True
        
        logger.info("👂 Listening for wake word...")
        
        # Start in background thread
        loop = asyncio.get_event_loop()
        threading.Thread(
            target=lambda: loop.run_in_executor(None, self._listen_loop),
            daemon=True
        ).start()
    
    def _listen_loop(self):
        """Background listening loop"""
        import pyaudio
        
        p = pyaudio.PyAudio()
        stream = p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=1024
        )
        
        buffer = []
        
        while self.is_listening:
            try:
                data = stream.read(1024, exception_on_overflow=False)
                buffer.append(data)
                
                # Check for wake word every ~1 second
                if len(buffer) >= 16:
                    audio_data = b''.join(buffer[-16:])
                    
                    if self.wake_word.detect(audio_data):
                        logger.info("👋 Wake word detected!")
                        # Get last ~5 seconds of audio
                        full_audio = b''.join(buffer[-80:])
                        
                        # Transcribe
                        if self.stt:
                            text = self.stt.transcribe(full_audio)
                            if text and self.callback:
                                asyncio.run(self.callback(text))
                    
                    buffer = buffer[-20:]  # Keep last 20 chunks
                    
            except Exception as e:
                logger.warning(f"Listen error: {e}")
        
        stream.stop_stream()
        p.terminate()
    
    async def listen_once(self) -> str:
        """Listen once for speech (no wake word)"""
        logger.info("🎤 Listening...")
        
        import pyaudio
        
        p = pyaudio.PyAudio()
        stream = p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=1024
        )
        
        frames = []
        silent_chunks = 0
        max_silent = 30  # ~3 seconds of silence
        
        while True:
            data = stream.read(1024, exception_on_overflow=False)
            frames.append(data)
            
            # Detect silence
            audio_data = np.frombuffer(data, dtype=np.int16)
            if np.abs(audio_data).mean() < 500:
                silent_chunks += 1
            else:
                silent_chunks = 0
            
            if silent_chunks > max_silent:
                break
        
        stream.stop_stream()
        p.terminate()
        
        audio_data = b''.join(frames)
        return self.stt.transcribe(audio_data) if self.stt else ""
    
    async def speak(self, text: str):
        """Speak text aloud"""
        if self.is_speaking:
            logger.warning("Already speaking, skipping...")
            return
        
        self.is_speaking = True
        logger.info(f"🔊 Speaking: {text[:50]}...")
        
        try:
            if self.tts:
                await self.tts.speak(text)
        except Exception as e:
            logger.error(f"TTS error: {e}")
        
        self.is_speaking = False
    
    def stop(self):
        """Stop listening"""
        self.is_listening = False
        logger.info("👂 Stopped listening")


class WakeWordDetector:
    """
    Wake word detection using Porcupine
    Alternative: use webrtc-noise-gain or custom model
    """
    
    def __init__(self, keywords: List[str] = None, sensitivity: float = 0.5):
        self.keywords = keywords or ["hey rama"]
        self.sensitivity = sensitivity
        self.porcupine = None
        self._initialize()
    
    def _initialize(self):
        try:
            import pvporcupine
            import struct
            
            # Create keyword paths (would need actual .ppn files)
            # For now, use a simple energy-based detection
            self.use_simple = True
            logger.info("👂 Wake word detector ready (simple mode)")
            
        except Exception as e:
            logger.warning(f"Wake word init failed: {e}")
            self.use_simple = True
    
    def detect(self, audio_data: bytes) -> bool:
        """Detect wake word in audio"""
        if self.use_simple:
            # Simple energy-based detection
            try:
                audio = np.frombuffer(audio_data, dtype=np.int16)
                energy = np.abs(audio).mean()
                
                # Adjust threshold based on sensitivity
                threshold = 2000 * (1 - self.sensitivity)
                
                return energy > threshold
            except:
                return False
        
        return False


class STTEngine:
    """
    Speech-to-Text using Whisper (offline)
    """
    
    def __init__(self, model_size: str = "tiny", device: str = "cpu"):
        self.model_size = model_size
        self.device = device
        self.model = None
        self._initialize()
    
    def _initialize(self):
        try:
            # Try faster-whisper first (more efficient)
            from faster_whisper import WhisperModel
            
            self.model = WhisperModel(
                self.model_size,
                device=self.device,
                compute_type="int8"
            )
            logger.info(f"✅ STT loaded: {self.model_size}")
            
        except Exception as e:
            logger.warning(f"faster-whisper failed: {e}")
            try:
                # Fallback to openai-whisper
                import whisper
                self.model = whisper.load_model(self.model_size, device=self.device)
                logger.info(f"✅ STT loaded (whisper): {self.model_size}")
            except Exception as e2:
                logger.error(f"STT init failed: {e2}")
                self.model = None
    
    def transcribe(self, audio_data: bytes) -> str:
        """Transcribe audio to text"""
        if not self.model:
            return ""
        
        try:
            import io
            import wave
            
            # Convert raw audio to WAV
            buffer = io.BytesIO()
            with wave.open(buffer, 'wb') as wav:
                wav.setnchannels(1)
                wav.setsampwidth(2)
                wav.setframerate(16000)
                wav.writeframes(audio_data)
            
            buffer.seek(0)
            
            # Transcribe
            if hasattr(self.model, 'transcribe'):
                # faster-whisper
                result, _ = self.model.transcribe(buffer)
                return result.text.strip()
            else:
                # openai-whisper
                result = self.model.transcribe(buffer)
                return result["text"].strip()
                
        except Exception as e:
            logger.warning(f"Transcription failed: {e}")
            return ""


class TTSEngine:
    """
    Text-to-Speech using Silero (offline)
    """
    
    def __init__(self, model: str = "silero", voice: str = "en_0"):
        self.model_name = model
        self.voice = voice
        self.model = None
        self.device = "cpu"
        self._initialize()
    
    def _initialize(self):
        try:
            import torch
            import silero
            
            # Load model
            self.model, self.example_text = silero.load(
                model=self.model_name,
                device=self.device
            )
            logger.info(f"✅ TTS loaded: {self.model_name}")
            
        except Exception as e:
            logger.warning(f"TTS init failed: {e}")
            # Fallback: use pyttsx3 (system TTS)
            try:
                import pyttsx3
                self.tts3 = pyttsx3.init()
                self.use_tts3 = True
                logger.info("✅ TTS loaded: pyttsx3")
            except:
                self.model = None
    
    async def speak(self, text: str):
        """Speak text"""
        if hasattr(self, 'use_tts3') and self.use_tts3:
            # Use pyttsx3
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, lambda: self.tts3.say(text))
            await loop.run_in_executor(None, self.tts3.runAndWait)
            return
        
        if not self.model:
            logger.warning("No TTS available")
            return
        
        try:
            import torch
            import sounddevice as sd
            
            # Generate audio
            audio = self.model.apply_tts(
                text=text,
                speaker=self.voice,
                sample_rate=48000
            )
            
            # Play audio
            audio_np = audio.cpu().numpy()
            
            def play():
                sd.play(audio_np, 48000)
                sd.wait()
            
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, play)
            
        except Exception as e:
            logger.error(f"TTS speak failed: {e}")