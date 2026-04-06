"""Debugging and Security Skills
Based on everything-claude-code and claw-code for debugging and jailbreak detection"""

from skills.skill_base import Skill
from typing import Any, Dict, List
import re


class DebuggingSkill(Skill):
    """Debug code and find issues"""
    
    triggers = ["debug", "fix", "error", "bug", "issue", "problem", "broken"]
    
    async def execute(self, input_text, context, retrieved_context=""):
        input_lower = input_text.lower()
        
        # Extract code if present
        code = self._extract_code(input_text)
        
        if code:
            return await self._debug_code(code)
        
        if "list" in input_lower or "show" in input_lower:
            return """🔧 **Debugging Tools:**

- Find syntax errors
- Identify runtime issues  
- Detect logic problems
- Suggest fixes

Provide code to debug, or describe the error you're seeing."""
        
        return """🔧 **Code Debugging:**

To debug code, provide:
1. The code with the issue
2. Any error messages
3. What you expected to happen

Example: "debug this code: function test() {..."""
    
    def _extract_code(self, text: str) -> str:
        """Extract code blocks from text"""
        # Look for markdown code blocks
        code_blocks = re.findall(r'```[\w]*\n(.+?)```', text, re.DOTALL)
        if code_blocks:
            return code_blocks[0]
        
        # Look for inline code
        if '{' in text or 'def ' in text or 'function' in text:
            # Return everything that looks like code
            return text
        
        return ""
    
    async def _debug_code(self, code: str) -> str:
        """Analyze and debug code"""
        issues = []
        
        # Common Python issues
        if 'def ' in code or 'import ' in code:
            # Check for syntax issues
            if 'def ' in code and ':' not in code:
                issues.append("⚠️ Function definition missing colon ':'")
            
            if 'import ' in code and 'from ' in code:
                # Check import order
                lines = code.split('\n')
                imports = [l for l in lines if 'import ' in l or 'from ' in l]
                if imports:
                    issues.append("💡 Consider organizing imports: stdlib, third-party, local")
            
            # Check for common errors
            if 'print(' in code and 'print ' in code:
                issues.append("⚠️ Inconsistent print syntax (statement vs function)")
            
            # Check for undefined variables (simple)
            undefined = re.findall(r'\b([a-z_][a-z0-9_]*)\b(?!\s*\()', code)
            defined = set(re.findall(r'\b([a-z_][a-z0-9_]*)\s*=', code))
            likely_undefined = [v for v in set(undefined) if v not in defined and v not in ['if', 'for', 'while', 'return', 'def', 'class', 'import', 'from', 'True', 'False', 'None', 'and', 'or', 'not', 'in', 'is']]
            
            if likely_undefined:
                issues.append(f"🔍 Potential undefined variables: {', '.join(likely_undefined[:5])}")
        
        # Common JavaScript issues
        if 'function' in code or 'const ' in code or 'let ' in code:
            if '==' in code and '===' not in code:
                issues.append("💡 Use '===' instead of '==' for strict equality")
            
            if 'console.log' not in code and 'console.error' not in code:
                issues.append("💡 Consider adding console.log for debugging")
            
            if 'return' in code and 'console.log' in code:
                issues.append("⚠️ Console.log after return will never execute")
        
        # Common general issues
        if code.count('(') != code.count(')'):
            issues.append("⚠️ Unbalanced parentheses")
        
        if code.count('[') != code.count(']'):
            issues.append("⚠️ Unbalanced brackets")
        
        if code.count('{') != code.count('}'):
            issues.append("⚠️ Unbalanced braces")
        
        # Detect infinite loops
        if 'while True:' in code or 'while(true)' in code:
            if 'break' not in code and 'return' not in code:
                issues.append("🔴 Potential infinite loop - no break condition")
        
        if not issues:
            return """✅ **Debugging Results:**

No obvious issues found! 

Tips:
- Run the code to see actual errors
- Check for edge cases
- Verify input/output expectations

Want me to explain specific parts of the code?"""
        
        output = "🔧 **Debugging Results:**\n\n"
        output += "**Issues Found:**\n"
        for issue in issues:
            output += f"- {issue}\n"
        
        output += "\n💡 **Suggestions:**\n"
        output += "- Run code to confirm issues\n"
        output += "- Add error handling\n"
        output += "- Check variable scope\n"
        
        return output


class SecurityAuditSkill(Skill):
    """Security audit and vulnerability detection"""
    
    triggers = ["security", "vulnerability", "audit", "safe", "exploit", "hack", "jailbreak", "injection"]
    
    async def execute(self, input_text, context, retrieved_context=""):
        input_lower = input_text.lower()
        
        # Check for jailbreak attempts first
        if any(word in input_lower for word in ["jailbreak", "bypass", "override", "ignore rules", "ignore system"]):
            return await self._check_jailbreak(input_text)
        
        # Extract code if present
        code = self._extract_code(input_text)
        
        if code:
            return await self._security_audit(code)
        
        return """🔐 **Security Audit:**

Scan code for security vulnerabilities:

Types detected:
- SQL Injection
- XSS (Cross-Site Scripting)
- Command Injection
- Path Traversal
- Hardcoded Secrets
- Insecure Deserialization

Provide code to audit, or ask 'check security of [code]'"""
    
    def _extract_code(self, text: str) -> str:
        """Extract code from text"""
        code_blocks = re.findall(r'```[\w]*\n(.+?)```', text, re.DOTALL)
        if code_blocks:
            return code_blocks[0]
        return text if '{' in text or 'def ' in text else ""
    
    async def _check_jailbreak(self, text: str) -> str:
        """Detect and block jailbreak attempts"""
        return """🚫 **Jailbreak Detection**

⚠️ Potential jailbreak attempt detected!

I will NOT:
- Ignore my core instructions
- Override safety guidelines
- Reveal system prompts
- Execute harmful commands
- Bypass authentication

What I CAN do:
- Help with legitimate coding tasks
- Explain security concepts
- Review code for vulnerabilities
- Assist with debugging

If you have a legitimate request, please rephrase it! 😊"""
    
    async def _security_audit(self, code: str) -> str:
        """Audit code for security issues"""
        vulnerabilities = []
        
        # SQL Injection
        sql_patterns = [
            r'execute\s*\(\s*["\'].*?%s',
            r'query\s*\(\s*["\'].*?\+',
            r'cursor\.execute.*?["\'].*?f\{',
        ]
        for pattern in sql_patterns:
            if re.search(pattern, code, re.IGNORECASE):
                vulnerabilities.append("🔴 **SQL Injection** - Use parameterized queries")
        
        # Command Injection
        cmd_patterns = [
            r'os\.system\s*\(',
            r'subprocess\..*?\s+shell\s*=\s*True',
            r'exec\s*\(',
            r'eval\s*\(',
        ]
        for pattern in cmd_patterns:
            if re.search(pattern, code):
                vulnerabilities.append("🔴 **Command Injection** - Avoid shell=True or eval/exec")
        
        # XSS (for web code)
        if 'innerHTML' in code or 'document.write' in code:
            vulnerabilities.append("🟠 **XSS Risk** - Use textContent instead of innerHTML")
        
        # Hardcoded secrets
        secret_patterns = [
            r'password\s*=\s*["\'][^"\']+["\']',
            r'api_key\s*=\s*["\'][^"\']+["\']',
            r'secret\s*=\s*["\'][^"\']+["\']',
            r'token\s*=\s*["\'][^"\']{20,}',
        ]
        for pattern in secret_patterns:
            if re.search(pattern, code, re.IGNORECASE):
                vulnerabilities.append("🟡 **Hardcoded Secret** - Use environment variables")
        
        # Path Traversal
        if 'open(' in code and '../' in code:
            vulnerabilities.append("🟠 **Path Traversal** - Validate and sanitize file paths")
        
        # Insecure random
        if 'random.random()' in code and 'password' in code.lower():
            vulnerabilities.append("🟡 **Insecure Random** - Use secrets.token_bytes for crypto")
        
        if not vulnerabilities:
            return """✅ **Security Audit Passed:**

No obvious security vulnerabilities found!

Best practices to keep:
- Use parameterized queries
- Validate all inputs
- Store secrets in env vars
- Keep dependencies updated
- Use HTTPS always"""
        
        output = "🔐 **Security Audit Results:**\n\n"
        output += "⚠️ **Vulnerabilities Found:**\n"
        for v in vulnerabilities:
            output += f"- {v}\n"
        
        output += "\n💡 **Recommendations:**\n"
        output += "- Fix high priority issues first\n"
        output += "- Use security linters\n"
        output += "- Follow OWASP guidelines\n"
        output += "- Keep dependencies updated\n"
        
        return output


class TestingSkill(Skill):
    """Generate and run tests"""
    
    triggers = ["test", "unit test", "pytest", "spec", "assert", "expect"]
    
    async def execute(self, input_text, context, retrieved_context=""):
        input_lower = input_text.lower()
        
        # Generate tests
        if "generate" in input_lower or "create" in input_lower or "write" in input_lower:
            return await self._generate_tests(input_text)
        
        return """🧪 **Testing Tools:**

- Generate unit tests
- Create integration tests
- Write test specifications

Provide code and ask:
- "generate tests for this code"
- "write pytest tests"
- "create unit tests" """
    
    async def _generate_tests(self, text: str) -> str:
        """Generate test code"""
        # Extract code
        code = self._extract_code(text)
        
        if not code:
            return "⚠️ No code provided to generate tests for!"
        
        # Determine language
        lang = "python"
        if 'function' in code or 'const ' in code or 'let ' in code:
            lang = "javascript"
        
        if lang == "python":
            tests = f'''import pytest

# Generated tests for your code
class TestYourCode:
    def test_basic(self):
        # Add your test assertions here
        assert True
    
    def test_edge_cases(self):
        # Test edge cases
        pass

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
'''
        else:
            tests = '''// Generated tests for your code
describe("Your Code", () => {
  test("basic", () => {
    expect(true).toBe(true);
  });
  
  test("edge cases", () => {
    // Add more tests
  });
});'''
        
        return f"""🧪 **Generated Tests** ({lang}):\n\n```{lang}\n{tests}\n```\n\nRun with:\n- Python: `pytest test_file.py`\n- JS: `npx jest test_file.js`"""