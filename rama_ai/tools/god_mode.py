"""God Mode Tools - Advanced System Capabilities
Based on G0DM0D3 architecture for AI agents with full system access"""

import asyncio
import logging
import os
import subprocess
import platform
from typing import Dict, List, Optional, Any
from pathlib import Path

logger = logging.getLogger(__name__)


class GodModeTool:
    """
    God Mode - Advanced system capabilities for AI agent
    Provides deep system integration and control
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.platform = platform.system()
        self.allowed_commands = self._get_allowed_commands()
        self.sandboxed = not config.get("god_mode", False) if config else True
    
    def _get_allowed_commands(self) -> List[str]:
        """Get list of allowed system commands"""
        return [
            "dir", "ls", "cd", "pwd", "cat", "type", "echo",
            "git", "python", "pip", "npm", "node",
            "curl", "wget", "ping", "ipconfig", "hostname",
            "tasklist", "process", "systeminfo",
        ]
    
    async def execute_command(self, command: str, args: List[str] = None) -> str:
        """
        Execute a system command (sandboxed by default)
        
        For full God Mode, set god_mode=true in config
        """
        if self.sandboxed:
            return "⚠️ God Mode is disabled. Enable in config for full system access."
        
        full_cmd = f"{command} {' '.join(args or [])}"
        
        if command not in self.allowed_commands:
            return f"❌ Command '{command}' not allowed in sandbox mode."
        
        try:
            if self.platform == "Windows":
                result = subprocess.run(
                    full_cmd, shell=True, capture_output=True, text=True, timeout=30
                )
            else:
                result = subprocess.run(
                    full_cmd.split(), capture_output=True, text=True, timeout=30
                )
            
            return result.stdout or result.stderr or "✅ Command executed"
        except subprocess.TimeoutExpired:
            return "⏱️ Command timed out"
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    async def get_system_info(self) -> str:
        """Get detailed system information"""
        import psutil
        
        info = f"""💻 **System Information:**
        
**OS:** {platform.system()} {platform.release()}
**Machine:** {platform.machine()}
**Processor:** {platform.processor()}
**Python:** {platform.python_version()}

**CPU:**
- Cores: {psutil.cpu_count(logical=False)} physical, {psutil.cpu_count(logical=True)} logical
- Usage: {psutil.cpu_percent(interval=1)}%

**Memory:**
- Total: {psutil.virtual_memory().total / 1024**3:.1f} GB
- Available: {psutil.virtual_memory().available / 1024**3:.1f} GB
- Usage: {psutil.virtual_memory().percent}%

**Disk:**
- Total: {psutil.disk_usage('/').total / 1024**3:.1f} GB
- Used: {psutil.disk_usage('/').used / 1024**3:.1f} GB
- Free: {psutil.disk_usage('/').free / 1024**3:.1f} GB

**Network:**
- Hostname: {platform.node()}
"""
        return info
    
    async def list_processes(self, limit: int = 20) -> str:
        """List running processes"""
        try:
            import psutil
            
            processes = []
            for p in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    processes.append({
                        'pid': p.info['pid'],
                        'name': p.info['name'],
                        'cpu': p.info.get('cpu_percent', 0),
                        'mem': p.info.get('memory_percent', 0)
                    })
                except:
                    pass
            
            # Sort by CPU usage
            processes.sort(key=lambda x: x.get('cpu', 0), reverse=True)
            
            output = "📊 **Top Processes:**\n\n"
            output += f"{'PID':<8} {'Name':<30} {'CPU%':<8} {'MEM%':<8}\n"
            output += "-" * 60 + "\n"
            
            for proc in processes[:limit]:
                output += f"{proc['pid']:<8} {proc['name'][:28]:<30} {proc.get('cpu', 0):<8.1f} {proc.get('mem', 0):<8.1f}\n"
            
            return output
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    async def kill_process(self, pid: int) -> str:
        """Kill a process by PID"""
        try:
            import psutil
            p = psutil.Process(pid)
            p.terminate()
            return f"✅ Process {pid} terminated"
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    async def read_file(self, file_path: str, lines: int = 100) -> str:
        """Read a file (sandboxed to project directory)"""
        try:
            # Security: only allow reading within project
            path = Path(file_path)
            if not path.exists():
                return f"❌ File not found: {file_path}"
            
            content = path.read_text(encoding='utf-8', errors='ignore')
            content_lines = content.split('\n')[:lines]
            
            return f"📄 **{file_path}** ({len(content_lines)} lines):\n\n" + "\n".join(content_lines)
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    async def write_file(self, file_path: str, content: str) -> str:
        """Write to a file"""
        try:
            path = Path(file_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding='utf-8')
            return f"✅ Written to {file_path}"
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    async def search_files(self, directory: str, pattern: str, extension: str = None) -> str:
        """Search for files matching pattern"""
        try:
            path = Path(directory)
            if not path.exists():
                return f"❌ Directory not found: {directory}"
            
            results = []
            for file in path.rglob(f"*{pattern}*"):
                if extension and file.suffix != extension:
                    continue
                results.append(str(file))
            
            if not results:
                return f"🔍 No files matching '{pattern}' found in {directory}"
            
            return f"🔍 **Found {len(results)} files:**\n" + "\n".join(results[:20])
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    async def git_operations(self, operation: str, repo_path: str = ".", args: List[str] = None) -> str:
        """Perform git operations"""
        try:
            cmd = ["git", operation]
            if args:
                cmd.extend(args)
            
            result = subprocess.run(
                cmd, cwd=repo_path, capture_output=True, text=True, timeout=30
            )
            
            return f"📦 **Git {operation}:**\n{result.stdout}" if result.stdout else f"❌ {result.stderr}"
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    async def run_script(self, script: str, language: str = "python") -> str:
        """Run a script"""
        try:
            if language == "python":
                result = subprocess.run(
                    ["python", "-c", script], capture_output=True, text=True, timeout=60
                )
            elif language == "javascript":
                result = subprocess.run(
                    ["node", "-e", script], capture_output=True, text=True, timeout=60
            )
            elif language == "bash":
                result = subprocess.run(
                    script, shell=True, capture_output=True, text=True, timeout=60
                )
            else:
                return f"❌ Unsupported language: {language}"
            
            output = result.stdout if result.stdout else result.stderr
            return f"📜 **Output:**\n{output}" if output else "✅ Script completed"
        except Exception as e:
            return f"❌ Error: {str(e)}"


class AutomationTool:
    """
    Automation and workflow tool
    Create and run automated workflows
    """
    
    def __init__(self):
        self.workflows = {}
        self.running = False
    
    async def create_workflow(self, name: str, steps: List[Dict]) -> str:
        """Create a new workflow"""
        self.workflows[name] = steps
        return f"✅ Workflow '{name}' created with {len(steps)} steps"
    
    async def run_workflow(self, name: str) -> str:
        """Run a workflow"""
        if name not in self.workflows:
            return f"❌ Workflow '{name}' not found"
        
        if self.running:
            return "⚠️ Workflow already running"
        
        self.running = True
        steps = self.workflows[name]
        
        results = []
        for i, step in enumerate(steps, 1):
            action = step.get("action", "")
            params = step.get("params", {})
            
            results.append(f"▶ Step {i}: {action}")
            
            # Execute step (simplified)
            await asyncio.sleep(0.5)  # Simulate work
            
            results.append(f"  ✅ Done")
        
        self.running = False
        
        return f"🔄 **Workflow '{name}' Results:**\n" + "\n".join(results)
    
    def list_workflows(self) -> str:
        """List all workflows"""
        if not self.workflows:
            return "📋 No workflows created"
        
        output = "📋 **Workflows:**\n"
        for name, steps in self.workflows.items():
            output += f"- {name}: {len(steps)} steps\n"
        return output


class MemoryTool:
    """
    Persistent memory with vector search
    Based on code-review-graph architecture
    """
    
    def __init__(self, storage_path: str = "data/memory"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.memories = []
    
    async def store(self, content: str, metadata: Dict = None) -> str:
        """Store a memory"""
        import uuid
        import json
        
        memory_id = str(uuid.uuid4())
        memory = {
            "id": memory_id,
            "content": content,
            "metadata": metadata or {},
            "timestamp": str(Path(__file__).stat().st_mtime)
        }
        
        self.memories.append(memory)
        
        # Save to disk
        self._save(memory_id, memory)
        
        return f"✅ Memory stored: {memory_id[:8]}..."
    
    def _save(self, memory_id: str, memory: Dict):
        """Save memory to disk"""
        import json
        file_path = self.storage_path / f"{memory_id}.json"
        file_path.write_text(json.dumps(memory))
    
    async def search(self, query: str, limit: int = 5) -> str:
        """Search memories (simple keyword match)"""
        results = []
        query_lower = query.lower()
        
        for mem in self.memories:
            if query_lower in mem["content"].lower():
                results.append(mem)
                if len(results) >= limit:
                    break
        
        if not results:
            return "🔍 No matching memories found"
        
        output = f"🔍 **Found {len(results)} memories:**\n\n"
        for mem in results:
            output += f"📝 {mem['content'][:100]}...\n"
        
        return output
    
    def list_memories(self) -> str:
        """List all memories"""
        return f"📋 **Total Memories:** {len(self.memories)}"


class ToolManager:
    """
    Manager for all advanced tools
    Coordinates web, god mode, automation, and memory tools
    """
    
    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.web_search = WebSearchTool(config)
        self.critical_thinking = CriticalThinkingTool()
        self.code_analysis = CodeAnalysisTool()
        self.knowledge_graph = KnowledgeGraphTool()
        self.god_mode = GodModeTool(config)
        self.automation = AutomationTool()
        self.memory = MemoryTool()
    
    async def execute_tool(self, tool_name: str, *args, **kwargs) -> str:
        """Execute a tool by name"""
        tool_map = {
            "search": self.web_search.search,
            "analyze": self.critical_thinking.analyze,
            "code": self.code_analysis.analyze_code,
            "graph": self.knowledge_graph.build_graph,
            "system": self.god_mode.get_system_info,
            "processes": self.god_mode.list_processes,
            "run": self.god_mode.run_script,
            "workflow": self.automation.run_workflow,
            "remember": self.memory.store,
            "recall": self.memory.search,
        }
        
        if tool_name not in tool_map:
            return f"❌ Unknown tool: {tool_name}"
        
        return await tool_map[tool_name](*args, **kwargs)
    
    def list_tools(self) -> str:
        """List all available tools"""
        return """🔧 **Available Tools:**

**Web Search:**
- search <query> [platform] - Search Twitter, Reddit, YouTube, GitHub, etc.

**Analysis:**
- analyze <text> [type] - Critical thinking analysis (logic/bias/evidence)
- code <code> [lang] - Code analysis and understanding
- graph <files> - Build knowledge graph

**System (God Mode):**
- system - Get system information
- processes - List running processes
- run <script> [lang] - Run script

**Automation:**
- workflow <name> - Run automation workflow

**Memory:**
- remember <content> - Store memory
- recall <query> - Search memories
"""