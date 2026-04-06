"""
RAMA AI v2.0 - Main Entry Point
Offline AI Voice Assistant for Windows

Usage:
    python main.py           # Start with UI
    python main.py --cli     # Start in CLI mode
    python main.py --headless # Start without UI (for automation)
"""

import asyncio
import argparse
import logging
import sys
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def setup_paths():
    """Setup Python paths"""
    # Add local modules to path
    current = Path(__file__).parent
    sys.path.insert(0, str(current))


async def initialize_system():
    """Initialize all system components"""
    logger.info("🚀 Initializing RAMA AI v2.0...")
    
    # Load config
    config = load_config()
    
    # Initialize components (in order)
    from memory.memory_system import MemorySystem
    memory = MemorySystem()
    await memory.initialize()
    logger.info("✅ Memory initialized")
    
    from core.rag_engine import RAGEngine
    rag = RAGEngine()
    await rag.initialize()
    logger.info("✅ RAG Engine initialized")
    
    from core.brain import Brain
    brain = Brain(config)
    await brain.initialize()
    logger.info("✅ Brain initialized")
    
    from voice.voice_pipeline import VoicePipeline
    voice = VoicePipeline(config)
    await voice.initialize()
    logger.info("✅ Voice Pipeline initialized")
    
    from tasks.task_executor import TaskExecutor
    tasks = TaskExecutor()
    logger.info("✅ Task Executor initialized")
    
    return {
        'config': config,
        'memory': memory,
        'rag': rag,
        'brain': brain,
        'voice': voice,
        'tasks': tasks
    }


def load_config() -> dict:
    """Load or create configuration"""
    config_path = Path("data/config.yaml")
    
    default_config = {
        "llm_model": "llama3.2:1b",
        "ollama_host": "http://localhost:11434",
        "stt_model": "tiny",
        "tts_model": "silero",
        "voice_enabled": False,
        "wake_word": "hey rama",
        "max_memory": 20,
        "embedding_model": "sentence-transformers/all-MiniLM-L6-v2"
    }
    
    if config_path.exists():
        import yaml
        with open(config_path) as f:
            config = yaml.safe_load(f)
            return {**default_config, **config}
    
    # Create default config
    config_path.parent.mkdir(parents=True, exist_ok=True)
    import yaml
    with open(config_path, 'w') as f:
        yaml.dump(default_config, f)
    
    return default_config


async def run_cli(system):
    """Run in CLI mode"""
    from core.brain import Brain
    from voice.voice_pipeline import VoicePipeline
    
    brain = system['brain']
    voice = system['voice']
    
    print("\n" + "="*50)
    print("   RAMA AI v2.0 - CLI Mode")
    print("="*50)
    print("\nType 'exit' to quit, 'voice' to toggle voice")
    print("Type 'help' for commands\n")
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['exit', 'quit']:
                print("👋 Goodbye!")
                break
            
            if user_input.lower() == 'voice':
                voice_enabled = not voice.config.get('voice_enabled', False)
                voice.config['voice_enabled'] = voice_enabled
                print(f"🎤 Voice {'enabled' if voice_enabled else 'disabled'}")
                continue
            
            if user_input.lower() == 'help':
                print("""
📋 Commands:
- voice          : Toggle voice output
- listen         : Start voice listening
- help           : Show this help
- exit           : Quit
- skills         : List all skills
- status         : Show system status
- ingest <file>  : Add document to knowledge
""")
                continue
            
            if user_input.lower() == 'skills':
                print("🎯 Skills: Greeting, Calculator, AppLauncher, FileManager, SystemInfo, Weather, WebSearch, Note, Reminder, Knowledge, Coding, Automation, LocalAI")
                continue
            
            if user_input.lower() == 'status':
                stats = await system['memory'].get_stats()
                print(f"📊 Status: {stats}")
                continue
            
            # Process input
            response = await brain.process(user_input)
            print(f"\nRama: {response}\n")
            
            # Speak if enabled
            if voice.config.get('voice_enabled'):
                await voice.speak(response)
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            logger.error(f"Error: {e}")
            print(f"❌ Error: {e}")


async def run_ui(system):
    """Run with UI"""
    logger.info("🎨 Starting UI...")
    
    # Import and start UI
    from frontend.ui import main as ui_main
    
    # Pass system to UI
    # In a full implementation, would use a global or pass through
    ui_main()


async def run_headless(system):
    """Run headless (for automation/API)"""
    logger.info("🌙 Running in headless mode...")
    
    # Start HTTP API
    from api.server import start_server
    await start_server(system)


async def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="RAMA AI v2.0")
    parser.add_argument('--cli', action='store_true', help='Run in CLI mode')
    parser.add_argument('--headless', action='store_true', help='Run without UI (headless)')
    parser.add_argument('--port', type=int, default=8000, help='API port for headless mode')
    args = parser.parse_args()
    
    try:
        # Setup paths
        setup_paths()
        
        # Initialize system
        system = await initialize_system()
        
        # Run based on mode
        if args.headless:
            await run_headless(system)
        elif args.cli:
            await run_cli(system)
        else:
            await run_ui(system)
            
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        print(f"❌ Error: {e}")
        sys.exit(1)
    finally:
        # Cleanup
        logger.info("🔄 Shutting down...")
        if 'brain' in locals():
            await brain.stop()


if __name__ == "__main__":
    asyncio.run(main())