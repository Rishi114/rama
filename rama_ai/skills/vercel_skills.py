"""Vercel Skills Integration - Open Agent Skills Ecosystem
Based on npx skills from vercel-labs/skills.git"""

import asyncio
import logging
import subprocess
import json
from typing import Dict, List, Optional, Any
from pathlib import Path

logger = logging.getLogger(__name__)


class SkillManager:
    """
    Skill management system - inspired by Vercel Skills
    Allows installing, listing, and using skills from the open agent ecosystem
    """
    
    def __init__(self, skills_path: str = "data/skills"):
        self.skills_path = Path(skills_path)
        self.skills_path.mkdir(parents=True, exist_ok=True)
        self.installed_skills = {}
        self._load_installed()
    
    def _load_installed(self):
        """Load previously installed skills"""
        meta_file = self.skills_path / "skills.json"
        if meta_file.exists():
            try:
                self.installed_skills = json.loads(meta_file.read_text())
            except:
                self.installed_skills = {}
    
    def _save_installed(self):
        """Save installed skills metadata"""
        meta_file = self.skills_path / "skills.json"
        meta_file.write_text(json.dumps(self.installed_skills, indent=2))
    
    async def install_skill(self, repo_url: str, skill_name: str = None) -> str:
        """
        Install a skill from GitHub or npm
        
        Args:
            repo_url: GitHub shorthand (owner/repo) or full URL
            skill_name: Specific skill name to install
        """
        logger.info(f"📦 Installing skill from: {repo_url}")
        
        # Parse repo URL
        if "/" in repo_url and not repo_url.startswith("http"):
            # GitHub shorthand
            repo_url = f"https://github.com/{repo_url}"
        
        # Try using npx skills if available
        try:
            result = subprocess.run(
                ["npx", "skills", "add", repo_url, "--global"],
                capture_output=True, text=True, timeout=120
            )
            
            if result.returncode == 0:
                self.installed_skills[repo_url] = {
                    "installed_at": str(Path(__file__).stat().st_mtime),
                    "skill_name": skill_name
                }
                self._save_installed()
                return f"✅ Skill installed from {repo_url}"
        except FileNotFoundError:
            pass  # npx not available
        
        # Fallback: Manual download
        return await self._manual_install(repo_url, skill_name)
    
    async def _manual_install(self, repo_url: str, skill_name: str = None) -> str:
        """Manual skill installation without npx"""
        
        # Parse repo info
        if "github.com" in repo_url:
            # Extract owner/repo
            parts = repo_url.rstrip("/").split("/")
            owner = parts[-2]
            repo = parts[-1].replace(".git", "")
            
            clone_path = self.skills_path / repo
            
            try:
                # Clone repo (shallow)
                result = subprocess.run(
                    ["git", "clone", "--depth", "1", repo_url, str(clone_path)],
                    capture_output=True, text=True, timeout=60
                )
                
                if result.returncode == 0:
                    self.installed_skills[repo] = {
                        "path": str(clone_path),
                        "installed_at": str(Path(__file__).stat().st_mtime),
                        "skill_name": skill_name
                    }
                    self._save_installed()
                    
                    # Look for skill files
                    skill_files = list(clone_path.glob("skills/**/*.ts"))
                    if not skill_files:
                        skill_files = list(clone_path.glob("**/*.skill.ts"))
                    
                    return f"""✅ Installed skill from {owner}/{repo}

📁 Location: {clone_path}
📄 Found {len(skill_files)} skill files

Use skills with: 'use skill {repo}'"""
                
            except Exception as e:
                return f"❌ Installation failed: {str(e)}"
        
        return "❌ Invalid repository URL. Use format: owner/repo or full GitHub URL"
    
    async def list_skills(self) -> str:
        """List all installed skills"""
        
        if not self.installed_skills:
            return """📦 **Installed Skills:** None

Install a skill:
- `npx skills add owner/repo` (if npx available)
- Or manually specify GitHub URL

Example: `skill install vercel-labs/agent-skills`"""
        
        output = "📦 **Installed Skills:**\n\n"
        
        for repo, info in self.installed_skills.items():
            path = info.get("path", "npx")
            output += f"• **{repo}**\n"
            output += f"  Location: {path}\n"
            output += f"  Installed: {info.get('installed_at', 'unknown')}\n\n"
        
        return output
    
    async def use_skill(self, skill_name: str, input_text: str) -> str:
        """Use an installed skill to process input"""
        
        # Check if skill is installed
        if skill_name not in self.installed_skills:
            return f"❌ Skill '{skill_name}' not installed. Install with: 'skill install {skill_name}'"
        
        skill_info = self.installed_skills[skill_name]
        skill_path = skill_info.get("path")
        
        if not skill_path or not Path(skill_path).exists():
            return f"❌ Skill path not found: {skill_path}"
        
        # Look for skill definition files
        skill_files = list(Path(skill_path).glob("skills/**/*.ts"))
        
        if not skill_files:
            return f"⚠️ No skill files found in {skill_path}"
        
        return f"🎯 **Skill: {skill_name}**

Processing input: {input_text[:50]}...

Found {len(skill_files)} skill file(s). Skill execution would happen here."


class VerceilSkillsSkill(Skill):
    """
    Skill for managing skills - Vercel Skills integration
    """
    
    def __init__(self):
        super().__init__()
        self.triggers = [
            "skill", "install skill", "list skills", "use skill",
            "add skill", "npx skills", "npm skills"
        ]
        self.skill_manager = None
    
    async def execute(self, input_text: str, context: Any, retrieved_context: str = "") -> str:
        
        # Initialize if needed
        if self.skill_manager is None:
            self.skill_manager = SkillManager()
        
        input_lower = input_text.lower()
        
        # Install skill
        if "install" in input_lower or "add" in input_lower:
            # Extract repo URL
            repo = input_lower.replace("install", "").replace("add", "").replace("skill", "").strip()
            
            if not repo:
                return """📦 **Install Skill:**

Use: `skill install owner/repo`

Example: `skill install vercel-labs/agent-skills`

Or use full URL: `skill install https://github.com/vercel-labs/agent-skills`"""
            
            return await self.skill_manager.install_skill(repo)
        
        # List skills
        if "list" in input_lower:
            return await self.skill_manager.list_skills()
        
        # Use skill
        if "use" in input_lower:
            parts = input_lower.replace("use skill", "").strip().split(" ", 1)
            skill_name = parts[0] if parts else ""
            input_text_param = parts[1] if len(parts) > 1 else ""
            
            if not skill_name:
                return "⚠️ Specify which skill to use: 'skill use <name> <input>'"
            
            return await self.skill_manager.use_skill(skill_name, input_text_param)
        
        return """📦 **Skills Management:**

Commands:
- `skill install <repo>` - Install a skill from GitHub
- `skill list` - List installed skills
- `skill use <name> <input>` - Use an installed skill

Examples:
- `skill install vercel-labs/agent-skills`
- `skill list`
- `skill use my-skill process this`"""