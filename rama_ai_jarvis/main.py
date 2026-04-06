"""
RAMA AI - Jarvis-Style Voice Assistant
Main Entry Point
Following the tutorial building sequence

Features:
- Voice-controlled (wake word "Hey Rama")
- Real system commands
- Human-like responses
- Automates tasks
- Runs continuously
"""

import sys
import asyncio
import threading
import time

# Import our modules
from voice import VoiceEngine
from commands import CommandProcessor
from tasks import TaskExecutor


class RAMAAssistant:
    """
    Main RAMA Assistant class
    Combines voice, commands, and tasks
    """
    
    def __init__(self):
        print("🤖 Initializing RAMA AI...")
        
        # Initialize components
        self.voice = VoiceEngine()
        self.commands = CommandProcessor()
        self.tasks = TaskExecutor()
        
        # State
        self.is_listening = False
        self.wake_word = "hey rama"
        
        # Settings
        self.language = "en"
        self.user_name = "bhai"
        
        print("✅ RAMA Ready!\n")
    
    def start(self, voice_mode=True):
        """
        Start RAMA assistant
        Args:
            voice_mode: If True, uses voice I/O. If False, text only.
        """
        self.is_listening = True
        
        # Greeting
        greeting = self.tasks.get_greeting(self.user_name)
        
        if voice_mode and self.voice.tts_available:
            self.voice.speak(greeting)
            print(f"\n🤖 Rama: {greeting}\n")
        else:
            print(f"\n🤖 Rama: {greeting}\n")
        
        # Main loop
        self._main_loop(voice_mode)
    
    def _main_loop(self, voice_mode=True):
        """
        Main continuous listening loop
        Similar to tutorial style
        """
        print("🎤 Listening for 'Hey Rama'...\n")
        
        while self.is_listening:
            try:
                if voice_mode:
                    # Listen for wake word
                    command = self.voice.listen_for_wake_word(self.wake_word)
                    
                    if command:
                        # Process command
                        response = self.commands.process(command)
                        
                        # Execute task if needed
                        task_result = self.tasks.execute(response)
                        
                        # Get final response
                        final_response = task_result if task_result else response
                        
                        # Speak and print
                        print(f"\n🤖 Rama: {final_response}\n")
                        if voice_mode and self.voice.tts_available:
                            self.voice.speak(final_response)
                else:
                    # Text input mode
                    user_input = input(f"You ({self.user_name}): ").strip()
                    
                    if not user_input:
                        continue
                    
                    if user_input.lower() in ['exit', 'quit', 'bye']:
                        self.stop()
                        break
                    
                    # Process text command
                    response = self.commands.process(user_input)
                    task_result = self.tasks.execute(response)
                    final_response = task_result if task_result else response
                    
                    print(f"\n🤖 Rama: {final_response}\n")
                    
            except KeyboardInterrupt:
                self.stop()
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                continue
    
    def stop(self):
        """Stop RAMA assistant"""
        self.is_listening = False
        goodbye = "Alvida bhai! Phir milenge! 👋"
        if self.voice.tts_available:
            self.voice.speak(goodbye)
        print(f"\n🤖 Rama: {goodbye}")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="RAMA AI - Jarvis Style Assistant")
    parser.add_argument("--text", action="store_true", help="Text mode only (no voice)")
    parser.add_argument("--cli", action="store_true", help="CLI mode")
    args = parser.parse_args()
    
    # Create RAMA instance
    rama = RAMAAssistant()
    
    # Start based on mode
    if args.text or args.cli:
        rama.start(voice_mode=False)
    else:
        rama.start(voice_mode=True)


if __name__ == "__main__":
    main()