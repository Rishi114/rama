"""App Launcher & File & System Skills"""

import subprocess
import platform
from pathlib import Path
from skills.skill_base import Skill


class AppLauncherSkill(Skill):
    """Launch applications on Windows"""
    
    def __init__(self):
        super().__init__()
        self.triggers = ["open", "launch", "start", "run", "execute"]
        
        self.common_apps = {
            'notepad': 'notepad.exe', 'calculator': 'calc.exe',
            'paint': 'mspaint.exe', 'explorer': 'explorer.exe',
            'cmd': 'cmd.exe', 'powershell': 'powershell.exe',
            'chrome': 'chrome', 'firefox': 'firefox', 'edge': 'msedge',
            'vscode': 'code', 'word': 'winword', 'excel': 'excel',
            'spotify': 'spotify', 'discord': 'discord', 'steam': 'steam',
        }
    
    async def execute(self, input_text: str, context: Any, retrieved_context: str = "") -> str:
        input_lower = input_text.lower()
        
        for prefix in ['open ', 'launch ', 'start ', 'run ']:
            if prefix in input_lower:
                app_name = input_lower.split(prefix)[1].strip()
                break
        else:
            app_name = input_lower.replace('open', '').replace('launch', '').replace('start', '').strip()
        
        if not app_name:
            return "🚀 Which app? Try 'open notepad'"
        
        exe = self.common_apps.get(app_name.lower(), app_name)
        
        try:
            if platform.system() == 'Windows':
                subprocess.Popen(exe, shell=True)
            else:
                subprocess.Popen(['open', '-a', exe])
            return f"🚀 Launched: **{app_name}**"
        except Exception as e:
            return f"❌ Couldn't launch: {str(e)}"


class FileManagerSkill(Skill):
    """File system operations"""
    
    triggers = ["list files", "show files", "create folder", "delete file", "file manager"]
    
    async def execute(self, input_text, context, retrieved_context=""):
        input_lower = input_text.lower()
        
        if "list files" in input_lower or "show files" in input_lower:
            path = Path.home() / "Desktop"
            if "in " in input_lower:
                path_str = input_lower.split("in ")[1].strip()
                path = Path(path_str)
            
            if not path.exists():
                return f"❌ Directory not found: {path}"
            
            items = list(path.iterdir())[:15]
            result = f"📁 {path}:\n"
            for item in items:
                icon = "📁" if item.is_dir() else "📄"
                result += f"{icon} {item.name}\n"
            return result
        
        if "create folder" in input_lower:
            folder_name = input_lower.replace("create folder", "").strip()
            if not folder_name:
                return "Usage: 'create folder MyFolder'"
            
            path = Path.home() / folder_name
            try:
                path.mkdir(exist_ok=True)
                return f"✅ Created folder: {folder_name}"
            except Exception as e:
                return f"❌ Error: {str(e)}"
        
        return "📁 Try 'list files' or 'create folder MyFolder'"


class SystemInfoSkill(Skill):
    """System information"""
    
    triggers = ["system info", "cpu", "memory", "ram", "disk", "uptime", "processes"]
    
    async def execute(self, input_text, context, retrieved_context=""):
        import platform
        import psutil
        
        input_lower = input_text.lower()
        
        if "cpu" in input_lower:
            return f"⚡ CPU: {psutil.cpu_count()} cores, {psutil.cpu_percent()}% used"
        
        if "memory" in input_lower or "ram" in input_lower:
            mem = psutil.virtual_memory()
            return f"🧠 RAM: {mem.percent}% used ({mem.used/1024**3:.1f}/{mem.total/1024**3:.1f} GB)"
        
        if "disk" in input_lower:
            disk = psutil.disk_usage('/')
            return f"💾 Disk: {disk.percent}% used ({disk.used/1024**3:.1f}/{disk.total/1024**3:.1f} GB)"
        
        return f"💻 {platform.node()} | {platform.system()} {platform.release()}"