"""Task Execution Layer - System Control & Automation
Windows app automation, file management, system commands"""

import asyncio
import logging
import subprocess
import os
import shutil
from typing import Optional, Dict, Any, List
from pathlib import Path
import platform

logger = logging.getLogger(__name__)


class TaskExecutor:
    """
    Main task execution engine
    Coordinates system control, app automation, and file operations
    """
    
    def __init__(self):
        self.system_control = SystemControl()
        self.app_automation = AppAutomation()
        self.file_manager = FileManager()
        self.automation = AutomationEngine()
    
    async def execute(self, task: str, context: Optional[Dict] = None) -> str:
        """Execute a task based on input"""
        logger.info(f"⚡ Executing task: {task[:50]}...")
        
        # Parse task
        task_lower = task.lower()
        
        # System control
        if any(kw in task_lower for kw in ['system', 'cpu', 'memory', 'disk']):
            return await self.system_control.execute(task)
        
        # App control
        if any(kw in task_lower for kw in ['open', 'launch', 'start', 'run']):
            return await self.app_automation.execute(task)
        
        # File operations
        if any(kw in task_lower for kw in ['list', 'create', 'delete', 'copy', 'move', 'file']):
            return await self.file_manager.execute(task)
        
        # Automation
        if any(kw in task_lower for kw in ['routine', 'automation', 'automate']):
            return await self.automation.execute(task)
        
        return f"Unknown task: {task}"
    
    async def stop(self):
        """Cleanup"""
        logger.info("⚡ Task executor stopping")


class SystemControl:
    """
    System information and control
    """
    
    def __init__(self):
        self.platform = platform.system()
    
    async def execute(self, task: str) -> str:
        """Execute system command"""
        task_lower = task.lower()
        
        if 'info' in task_lower:
            return self.get_system_info()
        
        if 'cpu' in task_lower:
            return self.get_cpu_info()
        
        if 'memory' in task_lower or 'ram' in task_lower:
            return self.get_memory_info()
        
        if 'disk' in task_lower:
            return self.get_disk_info()
        
        if 'uptime' in task_lower:
            return self.get_uptime()
        
        if 'process' in task_lower or 'kill' in task_lower:
            return await self.process_control(task)
        
        return self.get_system_info()
    
    def get_system_info(self) -> str:
        """Get general system info"""
        import psutil
        
        cpu = psutil.cpu_percent()
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        return f"""💻 System Info:
- OS: {platform.system()} {platform.release()}
- Host: {platform.node()}
- CPU: {cpu}% used
- RAM: {memory.percent}% used ({memory.used/1024**3:.1f}/{memory.total/1024**3:.1f} GB)
- Disk: {disk.percent}% used ({disk.used/1024**3:.1f}/{disk.total/1024**3:.1f} GB)"""
    
    def get_cpu_info(self) -> str:
        """Get CPU info"""
        import psutil
        
        cpu_freq = psutil.cpu_freq()
        cpu_count = psutil.cpu_count()
        
        return f"""⚡ CPU:
- Cores: {cpu_count} ({psutil.cpu_count(logical=False)} physical)
- Frequency: {cpu_freq.current:.0f} MHz
- Usage: {psutil.cpu_percent(interval=1)}%
- Per Core: {psutil.cpu_percent(interval=1, percpu=True)}%"""
    
    def get_memory_info(self) -> str:
        """Get memory info"""
        import psutil
        
        vm = psutil.virtual_memory()
        sm = psutil.swap_memory()
        
        return f"""🧠 Memory:
- RAM: {vm.percent}% used
- Available: {vm.available/1024**3:.1f} GB
- Total: {vm.total/1024**3:.1f} GB
- Swap: {sm.percent}% used ({sm.used/1024**3:.1f} GB)"""
    
    def get_disk_info(self) -> str:
        """Get disk info"""
        import psutil
        
        partitions = psutil.disk_partitions()
        
        info = "💾 Disk:\n"
        for partition in partitions:
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                info += f"- {partition.device} ({partition.mountpoint}): {usage.percent}% used\n"
            except:
                pass
        
        return info
    
    def get_uptime(self) -> str:
        """Get system uptime"""
        import psutil
        
        boot_time = psutil.boot_time()
        uptime = datetime.now() - datetime.fromtimestamp(boot_time)
        
        days = uptime.days
        hours, remainder = divmod(uptime.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        return f"⏱️ Uptime: {days}d {hours}h {minutes}m {seconds}s"
    
    async def process_control(self, task: str) -> str:
        """Control processes"""
        # Placeholder - would need more complex implementation
        return "🔧 Process control: Try 'list processes' or 'kill processname'"


class AppAutomation:
    """
    Application launch and control
    """
    
    def __init__(self):
        self.common_apps = {
            'notepad': 'notepad.exe',
            'calculator': 'calc.exe',
            'paint': 'mspaint.exe',
            'explorer': 'explorer.exe',
            'cmd': 'cmd.exe',
            'powershell': 'powershell.exe',
            'chrome': 'chrome',
            'firefox': 'firefox',
            'vscode': 'code',
            'word': 'winword',
            'excel': 'excel',
            'outlook': 'outlook',
        }
    
    async def execute(self, task: str) -> str:
        """Execute app control"""
        task_lower = task.lower()
        
        # Extract app name
        for phrase in ['open ', 'launch ', 'start ', 'run ']:
            if phrase in task_lower:
                app_name = task_lower.split(phrase)[1].strip()
                return await self.launch_app(app_name)
        
        return "Usage: 'open notepad' or 'launch chrome'"
    
    async def launch_app(self, app_name: str) -> str:
        """Launch an application"""
        # Check common apps
        exe = self.common_apps.get(app_name.lower())
        
        if not exe:
            # Try as-is
            exe = app_name
        
        try:
            if self.platform == 'Windows':
                subprocess.Popen(exe, shell=True)
                return f"🚀 Launched: {app_name}"
            else:
                subprocess.Popen(['open', '-a', exe])
                return f"🚀 Launched: {app_name}"
        except Exception as e:
            return f"❌ Failed to launch {app_name}: {str(e)}"


class FileManager:
    """
    File system operations
    """
    
    def __init__(self):
        self.home = Path.home()
    
    async def execute(self, task: str) -> str:
        """Execute file operation"""
        task_lower = task.lower()
        
        if 'list' in task_lower or 'show' in task_lower:
            return await self.list_files(task)
        
        if 'create folder' in task_lower or 'mkdir' in task_lower:
            return await self.create_folder(task)
        
        if 'delete' in task_lower or 'remove' in task_lower:
            return await self.delete_item(task)
        
        if 'copy' in task_lower:
            return await self.copy_file(task)
        
        if 'move' in task_lower:
            return await self.move_file(task)
        
        if 'read' in task_lower:
            return await self.read_file(task)
        
        return "Usage: 'list files', 'create folder X', 'delete file'"
    
    async def list_files(self, task: str) -> str:
        """List files in directory"""
        # Extract path
        path_str = task_lower.replace('list files', '').replace('show files', '').replace('in ', '').strip()
        
        if not path_str:
            path = self.home / 'Desktop'
        else:
            path = Path(path_str)
        
        if not path.exists():
            return f"❌ Directory not found: {path}"
        
        try:
            items = list(path.iterdir())[:20]  # Limit to 20
            
            result = f"📁 {path}:\n"
            for item in items:
                icon = "📁" if item.is_dir() else "📄"
                result += f"{icon} {item.name}\n"
            
            return result
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    async def create_folder(self, task: str) -> str:
        """Create folder"""
        # Extract folder name
        match = task_lower.replace('create folder ', '').replace('mkdir ', '')
        folder_name = match.strip()
        
        if not folder_name:
            return "Usage: 'create folder MyFolder'"
        
        path = self.home / folder_name
        
        try:
            path.mkdir(parents=True, exist_ok=True)
            return f"✅ Created folder: {folder_name}"
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    async def delete_item(self, task: str) -> str:
        """Delete file or folder"""
        return "⚠️ Delete not implemented - use with caution!"
    
    async def copy_file(self, task: str) -> str:
        """Copy file"""
        return "📋 Copy functionality coming soon!"
    
    async def move_file(self, task: str) -> str:
        """Move file"""
        return "📋 Move functionality coming soon!"
    
    async def read_file(self, task: str) -> str:
        """Read file content"""
        return "📖 Read functionality coming soon!"


class AutomationEngine:
    """
    Automation routines and macros
    """
    
    def __init__(self):
        self.routines: Dict[str, List[str]] = {}
    
    async def execute(self, task: str) -> str:
        """Execute or create automation"""
        task_lower = task.lower()
        
        if 'create routine' in task_lower or 'add routine' in task_lower:
            return await self.create_routine(task)
        
        if 'run routine' in task_lower:
            return await self.run_routine(task)
        
        if 'list routine' in task_lower:
            return self.list_routines()
        
        return "Usage: 'create routine morning do X,Y,Z'"
    
    async def create_routine(self, task: str) -> str:
        """Create a new routine"""
        import re
        
        match = re.search(r'create routine (\w+) do (.+)', task_lower)
        if not match:
            return "Usage: 'create routine morning do open browser, check email'"
        
        name = match.group(1)
        actions = [a.strip() for a in match.group(2).split(',')]
        
        self.routines[name] = actions
        
        return f"✅ Created routine '{name}': {', '.join(actions)}"
    
    async def run_routine(self, task: str) -> str:
        """Run a routine"""
        routine_name = task_lower.replace('run routine ', '').strip()
        
        if routine_name not in self.routines:
            return f"❌ Routine '{routine_name}' not found"
        
        results = []
        for action in self.routines[routine_name]:
            results.append(f"▶ {action}")
        
        return f"🔄 Running '{routine_name}':\n" + "\n".join(results)
    
    def list_routines(self) -> str:
        """List all routines"""
        if not self.routines:
            return "No routines created yet"
        
        result = "🔄 Routines:\n"
        for name, actions in self.routines.items():
            result += f"- {name}: {', '.join(actions)}\n"
        
        return result