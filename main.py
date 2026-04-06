"""
RAMA AI - Main Entry Point
The primary entry point for the assistant
"""

import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Import model (brain)
from backend.model import RAMAModel


def load_config():
    """Load configuration from .env"""
    config = {
        'user_name': 'bhai',
        'language': 'en',
        'wake_word': 'hey rama',
        'voice_enabled': True,
    }
    
    # Try to load from .env
    env_file = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_file):
        with open(env_file) as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    config[key.lower()] = value
    
    return config


def run_voice_mode(rama):
    """Run in voice mode with wake word"""
    print("\n🎤 Voice Mode - Say 'Hey Rama' to activate!\n")
    
    greeting = rama.get_greeting()
    print(f"🤖 Rama: {greeting}\n")
    rama.speak(greeting)
    
    while True:
        try:
            command = rama.listen_for_wake_word()
            
            if command:
                print(f"\n👤 You: {command}")
                
                response = rama.process(command)
                print(f"🤖 Rama: {response}\n")
                
                rama.speak(response)
                
        except KeyboardInterrupt:
            print("\n👋 Bye bhai!")
            break


def run_text_mode(rama):
    """Run in text/CLI mode"""
    print("\n📝 Text Mode - Type your commands!\n")
    
    greeting = rama.get_greeting()
    print(f"🤖 Rama: {greeting}\n")
    
    while True:
        try:
            user_input = input(f"You ({rama.user_name}): ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['exit', 'quit', 'bye']:
                print("\n👋 Alvida bhai!")
                break
            
            response = rama.process(user_input)
            print(f"\n🤖 Rama: {response}\n")
            
        except KeyboardInterrupt:
            print("\n👋 Bye!")
            break


def main():
    """Main entry point"""
    print("\n" + "="*50)
    print("   🤖 RAMA AI v2.0 - Jarvis Style Assistant")
    print("="*50 + "\n")
    
    # Load config
    config = load_config()
    
    # Initialize RAMA brain
    print("🧠 Initializing RAMA Brain...")
    rama = RAMAModel(config)
    
    if not rama.initialize():
        print("❌ Failed to initialize RAMA")
        return
    
    print("✅ RAMA Ready!\n")
    
    # Choose mode
    if config.get('voice_enabled', True):
        run_voice_mode(rama)
    else:
        run_text_mode(rama)


if __name__ == "__main__":
    main()