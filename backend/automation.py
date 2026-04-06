"""
RAMA AI - Automation Module
Handles system tasks like opening/closing apps
"""

import os
import subprocess
import platform
import webbrowser
from pathlib import Path


class Automation:
    """
    System automation for RAMA
    Open/close apps, control system
    """
    
    def __init__(self, config=None):
        self.config = config or {}
        self.platform = platform.system()
        
        # App mappings
        self.app_map = {
            'notepad': 'notepad.exe',
            'calculator': 'calc.exe',
            'paint': 'mspaint.exe',
            'chrome': 'chrome',
            'firefox': 'firefox',
            'edge': 'msedge',
            'explorer': 'explorer.exe',
            'cmd': 'cmd.exe',
            'powershell': 'powershell.exe',
            'spotify': 'spotify',
            'discord': 'discord',
            'telegram': 'telegram',
            'vscode': 'code',
            'code': 'code',
            'word': 'winword',
            'excel': 'excel',
            'zoom': 'zoom',
            'teams': 'teams',
            'skype': 'skype',
            'steam': 'steam',
            'vlc': 'vlc',
        }
    
    def open_app(self, app_name):
        """Open an application"""
        app = self.app_map.get(app_name.lower(), app_name)
        
        try:
            if self.platform == "Windows":
                subprocess.Popen(app, shell=True)
            else:
                subprocess.Popen(["open", "-a", app])
            
            return f"✅ Opened {app_name.title()}! 🔥"
        except Exception as e:
            return f"❌ Couldn't open {app_name}: {str(e)}"
    
    def close_app(self, app_name):
        """Close an application"""
        try:
            if self.platform == "Windows":
                subprocess.run(f"taskkill /F /IM {app_name}.exe", shell=True)
            return f"✅ Closed {app_name}"
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def open_website(self, site):
        """Open a website"""
        urls = {
            'youtube': 'https://youtube.com',
            'google': 'https://google.com',
            'github': 'https://github.com',
            'wikipedia': 'https://wikipedia.org',
            'reddit': 'https://reddit.com',
            'twitter': 'https://twitter.com',
            'instagram': 'https://instagram.com',
            'bilibili': 'https://bilibili.com',
        }
        
        url = urls.get(site.lower(), f"https://{site}")
        
        try:
            webbrowser.open(url)
            return f"✅ Opened {site.title()}! 🌐"
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def search_web(self, query, engine='google'):
        """Search the web"""
        if not query:
            return "Kya search karna hai bhai?"
        
        if engine == 'google':
            url = f"https://google.com/search?q={query}"
        elif engine == 'youtube':
            url = f"https://youtube.com/results?search_query={query}"
        elif engine == 'github':
            url = f"https://github.com/search?q={query}"
        else:
            url = f"https://google.com/search?q={query}"
        
        try:
            webbrowser.open(url)
            return f"🔍 Searching {engine} for: {query}... 🌐"
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def list_files(self, path=None):
        """List files in directory"""
        target = path or str(Path.home())
        
        try:
            items = os.listdir(target)
            folders = [f"📁 {i}/" for i in items if os.path.isdir(os.path.join(target, i))]
            files = [f"📄 {i}" for i in items if os.path.isfile(os.path.join(target, i))]
            
            result = f"📁 **Contents:**\n\n"
            result += "\n".join(folders[:10]) + "\n"
            result += "\n".join(files[:10])
            
            return result
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def create_folder(self, name, path=None):
        """Create a folder"""
        target = path or str(Path.home() / "Desktop")
        folder_path = os.path.join(target, name)
        
        try:
            os.makedirs(folder_path, exist_ok=True)
            return f"✅ Created folder: {name}"
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def shutdown(self, delay=60):
        """Shutdown PC"""
        if self.platform != "Windows":
            return "🔧 Only on Windows"
        
        try:
            os.system(f"shutdown /s /t {delay}")
            return f"🔴 Shutting down in {delay} seconds..."
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def restart(self, delay=60):
        """Restart PC"""
        if self.platform != "Windows":
            return "🔧 Only on Windows"
        
        try:
            os.system(f"shutdown /r /t {delay}")
            return f"🔄 Restarting in {delay} seconds..."
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def take_screenshot(self):
        """Take screenshot"""
        if self.platform != "Windows":
            return "📸 Only on Windows"
        
        try:
            import mss
            with mss.mss() as sct:
                sct.shot()
            return "📸 Screenshot saved to Desktop! 🔥"
        except:
            return "📸 Screenshot feature (install mss)"
    
    def open_settings(self):
        """Open Windows settings"""
        if self.platform != "Windows":
            return "🔧 Only on Windows"
        
        try:
            subprocess.Popen("ms-settings:", shell=True)
            return "✅ Opened Settings! ⚙️"
        except Exception as e:
            return f"❌ Error: {str(e)}"


if __name__ == "__main__":
    auto = Automation()
    print(auto.open_app("notepad"))
    print(auto.search_web("python tutorial"))