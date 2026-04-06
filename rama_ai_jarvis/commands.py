"""
RAMA Command Processor
Processes and maps commands to tasks
Following the tutorial command handling style
"""

import re
from datetime import datetime


class CommandProcessor:
    """
    Process commands and map to actions
    Similar to tutorial's if-else command system
    """
    
    def __init__(self):
        # Command patterns for matching
        self.patterns = {
            # Open apps
            'open_notepad': ['open notepad', 'notepad', 'text editor'],
            'open_youtube': ['open youtube', 'youtube', 'play video'],
            'open_chrome': ['open chrome', 'chrome', 'browser'],
            'open_explorer': ['open explorer', 'file explorer', 'my files'],
            'open_calc': ['open calculator', 'calculator', 'calc'],
            'open.spotify': ['open spotify', 'spotify', 'music'],
            
            # Search
            'search_google': ['search google for', 'google', 'search for'],
            'search_youtube': ['search youtube for', 'find youtube'],
            'wikipedia': ['wikipedia', 'who is', 'what is'],
            
            # System
            'time': ['time', 'what time', 'current time'],
            'date': ['date', 'what date', 'today date'],
            'day': ['day', 'what day', 'which day'],
            'system_info': ['system info', 'pc info', 'computer info'],
            'screenshot': ['screenshot', 'capture screen', 'take photo'],
            
            # Shutdown/Restart
            'shutdown': ['shutdown', 'turn off', 'power off'],
            'restart': ['restart', 'reboot', 'restart pc'],
            
            # Weather
            'weather': ['weather', 'temperature', 'forecast'],
            
            # Help
            'help': ['help', 'commands', 'what can you do', 'list commands'],
            
            # Who are you
            'who_are_you': ['who are you', 'what are you', 'introduce yourself'],
            
            # Exit
            'exit': ['exit', 'quit', 'bye', 'goodbye', 'sleep'],
        }
        
        print("📋 Command Processor initialized")
    
    def process(self, user_input):
        """
        Process user input and return action
        Similar to tutorial: if-else structure
        """
        if not user_input:
            return "What do you want bhai?"
        
        text = user_input.lower().strip()
        
        # Check each pattern
        for action, keywords in self.patterns.items():
            for keyword in keywords:
                if keyword in text:
                    return self._handle_action(action, text)
        
        # No match - use AI
        return f"cmd:{text}"
    
    def _handle_action(self, action, text):
        """
        Handle specific action
        Returns command string for task executor
        """
        # Open commands
        if action == 'open_notepad':
            return "task:open_app:notepad"
        
        if action == 'open_youtube':
            return "task:open_website:youtube"
        
        if action == 'open_chrome':
            return "task:open_app:chrome"
        
        if action == 'open_explorer':
            return "task:open_app:explorer"
        
        if action == 'open_calc':
            return "task:open_app:calculator"
        
        if action == 'open.spotify':
            return "task:open_app:spotify"
        
        # Search commands
        if action == 'search_google':
            query = text.replace('search google for', '').replace('google', '').strip()
            return f"task:search:google:{query}"
        
        if action == 'search_youtube':
            query = text.replace('search youtube for', '').replace('youtube', '').strip()
            return f"task:search:youtube:{query}"
        
        if action == 'wikipedia':
            query = text.replace('wikipedia', '').replace('who is', '').replace('what is', '').strip()
            return f"task:wikipedia:{query}"
        
        # System commands
        if action == 'time':
            return "task:time"
        
        if action == 'date':
            return "task:date"
        
        if action == 'day':
            return "task:day"
        
        if action == 'system_info':
            return "task:system_info"
        
        if action == 'screenshot':
            return "task:screenshot"
        
        if action == 'shutdown':
            return "task:shutdown"
        
        if action == 'restart':
            return "task:restart"
        
        if action == 'weather':
            return "task:weather"
        
        if action == 'help':
            return "task:help"
        
        if action == 'who_are_you':
            return "task:who_are_you"
        
        if action == 'exit':
            return "task:exit"
        
        return "unknown"
    
    def add_command(self, keywords, action):
        """
        Add custom command
        Args:
            keywords: List of trigger words
            action: Action to return
        """
        self.patterns[action] = keywords


# Test
if __name__ == "__main__":
    processor = CommandProcessor()
    
    # Test commands
    test_commands = [
        "open notepad",
        "search google for python",
        "what is the time",
        "who are you",
        "help",
    ]
    
    print("🧪 Testing Command Processor...\n")
    
    for cmd in test_commands:
        result = processor.process(cmd)
        print(f"Input: {cmd}")
        print(f"Output: {result}\n")