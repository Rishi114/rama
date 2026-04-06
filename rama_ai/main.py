"""
RAMA AI v2.0 - Main Entry Point
Simplified version - works with minimal dependencies
"""

import asyncio
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def check_dependencies():
    """Check which dependencies are available"""
    available = {}
    
    # Core - always available
    available['core'] = True
    
    # Check optional dependencies
    try:
        import customtkinter
        available['ui'] = True
    except:
        available['ui'] = False
    
    try:
        import aiohttp
        available['aiohttp'] = True
    except:
        available['aiohttp'] = False
    
    try:
        import requests
        available['requests'] = True
    except:
        available['requests'] = False
    
    try:
        import psutil
        available['psutil'] = True
    except:
        available['psutil'] = False
    
    return available


async def run_cli(dependencies):
    """Run CLI mode"""
    print("\n" + "="*50)
    print("   🤖 RAMA AI v2.0 - CLI Mode")
    print("="*50)
    print(f"\nDependencies: {', '.join([k for k,v in dependencies.items() if v])}")
    print("\nType 'help' for commands, 'exit' to quit\n")
    
    # Import brain
    try:
        from core.brain import Brain
        brain = Brain({"llm_model": "llama3.2:1b"})
        await brain.initialize()
        print("✅ Brain initialized!\n")
    except Exception as e:
        print(f"⚠️ Brain initialization: {e}")
        brain = None
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['exit', 'quit', 'bye']:
                print("👋 Goodbye!")
                break
            
            if user_input.lower() == 'help':
                print("""
📋 Commands:
- help              : Show this help
- list skills       : Show all skills
- learning stats   : Show learning statistics
- list languages    : Show all programming languages
- code <lang>       : Get code example
- exit             : Quit
""")
                continue
            
            if user_input.lower() == 'list skills':
                if brain and brain.skill_manager:
                    skills = list(brain.skill_manager.skills.keys())
                    print(f"📦 Skills ({len(skills)}):\n" + ", ".join(skills))
                else:
                    print("📦 Skills available in full version")
                continue
            
            if user_input.lower() == 'learning stats':
                print("📊 Use 'python -c \"from tools.self_learning import SelfLearningEngine; print(SelfLearningEngine().get_learning_stats())\"'")
                continue
            
            # Simple response for now
            print(f"\nRama: I'm running! Try 'help' or explore the code at /root/.openclaw/workspace/rama-v2/rama_ai/\n")
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


async def main():
    """Main entry point"""
    print("\n🔄 Starting RAMA AI v2.0...")
    
    # Check dependencies
    deps = check_dependencies()
    print(f"✅ Available: {[k for k,v in deps.items() if v]}")
    
    # Run CLI
    await run_cli(deps)


if __name__ == "__main__":
    asyncio.run(main())