"""Complete System Control - Full PC Access
RAMA can control entire desktop/laptop like a real human"""

import os
import subprocess
import platform
import webbrowser
import threading
import time
from pathlib import Path
from typing import List, Dict, Optional
import shutil


class CompleteSystemControl:
    """
    Full system control - everything on PC accessible
    Like a real human using the computer
    """
    
    def __init__(self):
        self.platform = platform.system()
        self.home = str(Path.home())
        self.desktop = os.path.join(self.home, "Desktop")
        self.documents = os.path.join(self.home, "Documents")
        self.downloads = os.path.join(self.home, "Downloads")
    
    # ============================================
    # FILE & FOLDER OPERATIONS
    # ============================================
    
    def list_files(self, path: str = None, show_hidden: bool = False) -> str:
        """List files in directory like 'ls' or 'dir'"""
        target = path if path else self.desktop
        
        if not os.path.exists(target):
            return f"❌ Path not found: {target}"
        
        try:
            items = os.listdir(target)
            
            if not items:
                return f"📁 Empty folder: {target}"
            
            # Separate files and folders
            folders = []
            files = []
            
            for item in items:
                if not show_hidden and item.startswith('.'):
                    continue
                full_path = os.path.join(target, item)
                if os.path.isdir(full_path):
                    folders.append(f"📁 {item}/")
                else:
                    size = os.path.getsize(full_path)
                    files.append(f"📄 {item} ({self._format_size(size)})")
            
            result = f"📁 **Contents of:** `{target}`\n\n"
            
            if folders:
                result += "**Folders:**\n" + "\n".join(f"  {f}") + "\n\n"
            if files:
                result += "**Files:**\n" + "\n".join(f"  {f}") + "\n\n"
            
            result += f"Total: {len(folders)} folders, {len(files)} files"
            
            return result
            
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def create_folder(self, name: str, path: str = None) -> str:
        """Create a new folder"""
        target = os.path.join(path if path else self.desktop, name)
        
        try:
            os.makedirs(target, exist_ok=True)
            return f"✅ Created folder: {name} at {target}"
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def delete_file(self, path: str) -> str:
        """Delete file or folder"""
        try:
            if os.path.isdir(path):
                shutil.rmtree(path)
                return f"✅ Deleted folder: {path}"
            else:
                os.remove(path)
                return f"✅ Deleted file: {path}"
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def open_file(self, path: str) -> str:
        """Open file with default application"""
        try:
            if self.platform == "Windows":
                os.startfile(path)
            elif self.platform == "Darwin":
                subprocess.run(["open", path])
            else:
                subprocess.run(["xdg-open", path])
            return f"✅ Opened: {path}"
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def read_file(self, path: str, lines: int = 50) -> str:
        """Read text file content"""
        try:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.readlines()[:lines]
            
            return f"📄 **File:** `{path}`\n\n" + "".join(content)
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def write_file(self, path: str, content: str) -> str:
        """Write content to file"""
        try:
            Path(path).parent.mkdir(parents=True, exist_ok=True)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            return f"✅ Written to: {path}"
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def copy_file(self, source: str, dest: str) -> str:
        """Copy file or folder"""
        try:
            if os.path.isdir(source):
                shutil.copytree(source, dest)
            else:
                shutil.copy2(source, dest)
            return f"✅ Copied: {source} → {dest}"
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def move_file(self, source: str, dest: str) -> str:
        """Move file or folder"""
        try:
            shutil.move(source, dest)
            return f"✅ Moved: {source} → {dest}"
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def search_files(self, query: str, path: str = None) -> str:
        """Search for files"""
        target = path if path else self.home
        results = []
        
        try:
            for root, dirs, files in os.walk(target):
                for file in files:
                    if query.lower() in file.lower():
                        results.append(os.path.join(root, file))
                
                if len(results) > 20:
                    break
                    
            if not results:
                return f"🔍 No files found matching: {query}"
            
            return f"🔍 **Found {len(results)} files:**\n\n" + "\n".join(f"  {r}" for r in results[:10])
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    # ============================================
    # APP & SOFTWARE OPERATIONS
    # ============================================
    
    def open_app(self, app_name: str) -> str:
        """Open application by name"""
        app_map = {
            "notepad": "notepad.exe",
            "calculator": "calc.exe",
            "paint": "mspaint.exe",
            "explorer": "explorer.exe",
            "cmd": "cmd.exe",
            "powershell": "powershell.exe",
            "chrome": "chrome",
            "browser": "chrome",
            "firefox": "firefox",
            "edge": "msedge",
            "vscode": "code",
            "vs code": "code",
            "word": "winword",
            "excel": "excel",
            "powerpoint": "powerpnt",
            "outlook": "outlook",
            "spotify": "spotify",
            "discord": "discord",
            "telegram": "telegram",
            "whatsapp": "whatsapp",
            "zoom": "zoom",
            "teams": "teams",
            "skype": "skype",
            "steam": "steam",
            "spotify": "spotify",
            "vlc": "vlc",
            "media player": "wmplayer",
        }
        
        # Check if app in map
        exe = app_map.get(app_name.lower())
        
        if not exe:
            # Try as executable name
            exe = app_name
        
        try:
            if self.platform == "Windows":
                subprocess.Popen(exe, shell=True)
            else:
                subprocess.Popen(["open", "-a", exe])
            
            return f"✅ Opened: {app_name.title()} 🚀"
        except Exception as e:
            return f"❌ Couldn't open {app_name}: {str(e)}\n\n💡 Try: 'open notepad', 'open chrome', 'open vscode'"
    
    def close_app(self, app_name: str) -> str:
        """Close application"""
        try:
            if self.platform == "Windows":
                subprocess.run(f"taskkill /F /IM {app_name}.exe", shell=True)
            return f"✅ Closed: {app_name}"
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def list_apps(self) -> str:
        """List installed applications"""
        # Common apps
        apps = [
            ("Chrome", "Web Browser"),
            ("Firefox", "Web Browser"),
            ("Microsoft Edge", "Web Browser"),
            ("VS Code", "Code Editor"),
            ("Notepad", "Text Editor"),
            ("Calculator", "Utility"),
            ("Spotify", "Music"),
            ("Discord", "Chat"),
            ("Telegram", "Messaging"),
            ("WhatsApp", "Messaging"),
            ("Zoom", "Video Call"),
            ("Teams", "Video Call"),
            ("Word", "Office"),
            ("Excel", "Office"),
            ("PowerPoint", "Office"),
        ]
        
        result = "📦 **Installed Apps:**\n\n"
        for name, desc in apps:
            result += f"• **{name}** - {desc}\n"
        
        return result
    
    # ============================================
    # BROWSER & INTERNET OPERATIONS
    # ============================================
    
    def open_browser(self, url: str = None) -> str:
        """Open web browser"""
        browser = webbrowser.get()
        
        if url:
            browser.open(url)
            return f"✅ Opened: {url} 🌐"
        else:
            browser.open("about:blank")
            return "✅ Opened browser! 🌐"
    
    def search_web(self, query: str) -> str:
        """Search the web"""
        # Try different search engines
        engines = [
            f"https://www.google.com/search?q={query}",
            f"https://duckduckgo.com/?q={query}",
            f"https://www.bing.com/search?q={query}"
        ]
        
        try:
            webbrowser.open(engines[0])
            return f"🔍 Searching Google for: {query}... 🌐"
        except Exception as e:
            return f"❌ Search error: {str(e)}"
    
    def open_website(self, url: str) -> str:
        """Open specific website"""
        # Add https if missing
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        
        try:
            webbrowser.open(url)
            return f"✅ Opened: {url} 🌐"
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def get_browser_tabs(self) -> str:
        """Get open browser tabs (Windows)"""
        try:
            if self.platform != "Windows":
                return "🔧 Only available on Windows"
            
            # Use PowerShell to get chrome tabs
            script = '''
            $chrome = Get-Process chrome -ErrorAction SilentlyContinue
            if ($chrome) {
                $chrome.MainWindowTitle | Where-Object {$_ -ne ""}
            }
            '''
            
            result = subprocess.run(
                ["powershell", "-Command", script],
                capture_output=True, text=True
            )
            
            tabs = result.stdout.strip().split('\n')
            tabs = [t.strip() for t in tabs if t.strip()]
            
            if not tabs:
                return "🔍 No browser tabs open"
            
            return "🔗 **Open Tabs:**\n\n" + "\n".join(f"  • {t}" for t in tabs[:10])
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    # ============================================
    # SYSTEM OPERATIONS
    # ============================================
    
    def get_system_info(self) -> str:
        """Get complete system information"""
        import psutil
        
        # CPU
        cpu = psutil.cpu_percent(interval=1)
        cpu_count = psutil.cpu_count()
        
        # Memory
        mem = psutil.virtual_memory()
        
        # Disk
        disk = psutil.disk_usage('/')
        
        # Battery (if available)
        try:
            battery = psutil.sensors_battery()
            battery_info = f"\n🔋 Battery: {battery.percent}%" if battery else "\n🔋 No battery"
        except:
            battery_info = ""
        
        return f"""💻 **System Information:**

**Computer:**
- OS: {platform.system()} {platform.release()}
- Machine: {platform.machine()}
- Node: {platform.node()}

**CPU:**
- Cores: {cpu_count}
- Usage: {cpu}%

**Memory (RAM):**
- Total: {mem.total / 1024**3:.1f} GB
- Used: {mem.used / 1024**3:.1f} GB ({mem.percent}%)
- Free: {mem.available / 1024**3:.1f} GB

**Storage:**
- Total: {disk.total / 1024**3:.1f} GB
- Used: {disk.used / 1024**3:.1f} GB ({disk.percent}%)
- Free: {disk.free / 1024**3:.1f} GB{battery_info}

**Python:** {platform.python_version()}"""
    
    def get_running_processes(self) -> str:
        """Get running processes"""
        try:
            import psutil
            
            processes = []
            for p in psutil.process_iter(['name', 'cpu_percent']):
                try:
                    processes.append({
                        'name': p.info['name'],
                        'cpu': p.info['cpu_percent'] or 0
                    })
                except:
                    pass
            
            # Sort by CPU
            processes.sort(key=lambda x: x['cpu'], reverse=True)
            
            result = "📊 **Top Processes:**\n\n"
            result += f"{'Name':<30} {'CPU%':<10}\n"
            result += "-" * 40 + "\n"
            
            for proc in processes[:15]:
                result += f"{proc['name'][:28]:<30} {proc['cpu']:.1f}\n"
            
            return result
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def take_screenshot(self) -> str:
        """Take screenshot"""
        try:
            if self.platform == "Windows":
                import mss
                with mss.mss() as sct:
                    sct.shot()
                return "📸 Screenshot saved to Desktop!"
            else:
                return "🔧 Screenshot only on Windows (install mss)"
        except:
            return "📸 Screenshot feature - install mss: pip install mss"
    
    def open_settings(self) -> str:
        """Open Windows settings"""
        try:
            if self.platform == "Windows":
                subprocess.Popen("ms-settings:", shell=True)
                return "✅ Opened Settings! ⚙️"
            return "🔧 Only on Windows"
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def shutdown_pc(self, delay: int = 0) -> str:
        """Shutdown computer"""
        try:
            if self.platform == "Windows":
                os.system(f"shutdown /s /t {delay}")
                return f"🔴 Shutting down in {delay} seconds..."
            return "🔧 Only on Windows"
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def restart_pc(self, delay: int = 0) -> str:
        """Restart computer"""
        try:
            if self.platform == "Windows":
                os.system(f"shutdown /r /t {delay}")
                return f"🔄 Restarting in {delay} seconds..."
            return "🔧 Only on Windows"
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    # ============================================
    # QUICK PATHS
    # ============================================
    
    def go_to_desktop(self) -> str:
        return self.list_files(self.desktop)
    
    def go_to_documents(self) -> str:
        return self.list_files(self.documents)
    
    def go_to_downloads(self) -> str:
        return self.list_files(self.downloads)
    
    def go_to_home(self) -> str:
        return self.list_files(self.home)
    
    # ============================================
    # HELPER
    # ============================================
    
    def _format_size(self, size: int) -> str:
        """Format file size"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f}{unit}"
            size /= 1024
        return f"{size:.1f}TB"


# Global system control
system = CompleteSystemControl()


# Convenience functions
def handle_system_command(command: str) -> str:
    """Handle system-related commands"""
    cmd = command.lower()
    
    # File operations
    if "list files" in cmd or "show files" in cmd:
        path = None
        if "desktop" in cmd:
            path = system.desktop
        elif "download" in cmd:
            path = system.downloads
        elif "document" in cmd:
            path = system.documents
        return system.list_files(path)
    
    if "create folder" in cmd or "new folder" in cmd:
        name = cmd.replace("create folder", "").replace("new folder", "").strip()
        return system.create_folder(name)
    
    if "search file" in cmd or "find" in cmd:
        query = cmd.replace("search file", "").replace("find", "").strip()
        return system.search_files(query)
    
    # App operations
    if cmd.startswith("open "):
        app = cmd.replace("open ", "").strip()
        return system.open_app(app)
    
    if "close " in cmd:
        app = cmd.replace("close ", "").strip()
        return system.close_app(app)
    
    # Browser operations
    if "search" in cmd and "web" in cmd:
        query = cmd.replace("search web", "").replace("search", "").strip()
        return system.search_web(query)
    
    if cmd.startswith("open "):
        if "." in cmd:
            url = cmd.replace("open ", "").strip()
            return system.open_website(url)
    
    # System info
    if "system info" in cmd or "my pc" in cmd:
        return system.get_system_info()
    
    if "process" in cmd or "running apps" in cmd:
        return system.get_running_processes()
    
    # Settings
    if "settings" in cmd:
        return system.open_settings()
    
    # Screenshot
    if "screenshot" in cmd:
        return system.take_screenshot()
    
    return None