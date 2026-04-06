"""Web Search Tool - Multi-platform web searching
Based on Agent-Reach architecture for Twitter, Reddit, YouTube, GitHub, etc."""

import asyncio
import logging
from typing import List, Dict, Optional, Any
import re

logger = logging.getLogger(__name__)


class WebSearchTool:
    """
    Multi-platform web search tool
    Supports: Twitter, Reddit, YouTube, GitHub, Bilibili, XiaoHongShu
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.cache = {}
        self.results_limit = 10
    
    async def search(self, query: str, platform: str = "all") -> str:
        """
        Search across platforms or specific platform
        
        Args:
            query: Search query
            platform: "all", "twitter", "reddit", "youtube", "github", "bilibili", "xhs"
        """
        logger.info(f"🔍 Searching: {query} (platform: {platform})")
        
        results = []
        
        if platform == "all" or "twitter" in platform:
            results.extend(await self._search_twitter(query))
        
        if platform == "all" or "reddit" in platform:
            results.extend(await self._search_reddit(query))
        
        if platform == "all" or "youtube" in platform:
            results.extend(await self._search_youtube(query))
        
        if platform == "all" or "github" in platform:
            results.extend(await self._search_github(query))
        
        if platform == "all" or "bilibili" in platform:
            results.extend(await self._search_bilibili(query))
        
        if platform == "all" or "xhs" in platform:
            results.extend(await self._search_xiaohongshu(query))
        
        return self._format_results(results)
    
    async def _search_twitter(self, query: str) -> List[Dict]:
        """Search Twitter (simulated - requires cookies in real impl)"""
        # In production, would use Agent-Reach's twitter channel
        # For now, return mock data
        return [{
            "platform": "Twitter",
            "title": f"Twitter discussion: {query}",
            "url": f"https://twitter.com/search?q={query}",
            "snippet": f"Recent tweets about {query}"
        }]
    
    async def _search_reddit(self, query: str) -> List[Dict]:
        """Search Reddit"""
        try:
            import aiohttp
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"https://www.reddit.com/search.json",
                    params={"q": query, "limit": 5},
                    headers={"User-Agent": "RAMA/1.0"}
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        results = []
                        for child in data.get("data", {}).get("children", []):
                            post = child.get("data", {})
                            results.append({
                                "platform": "Reddit",
                                "title": post.get("title", ""),
                                "url": f"https://reddit.com{post.get('permalink', '')}",
                                "snippet": post.get("selftext", "")[:200],
                                "score": post.get("score", 0)
                            })
                        return results
        except Exception as e:
            logger.warning(f"Reddit search failed: {e}")
        
        return [{
            "platform": "Reddit",
            "title": f"Reddit: {query}",
            "url": f"https://reddit.com/search?q={query}",
            "snippet": f"Search Reddit for {query}"
        }]
    
    async def _search_youtube(self, query: str) -> List[Dict]:
        """Search YouTube"""
        try:
            import aiohttp
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    "https://www.googleapis.com/youtube/v3/search",
                    params={
                        "part": "snippet",
                        "q": query,
                        "maxResults": 5,
                        "type": "video"
                        # Would need API key in production
                    }
                ) as resp:
                    pass  # Would need API key
        except:
            pass
        
        return [{
            "platform": "YouTube",
            "title": f"Video: {query}",
            "url": f"https://youtube.com/results?search_query={query}",
            "snippet": f"Watch videos about {query}"
        }]
    
    async def _search_github(self, query: str) -> List[Dict]:
        """Search GitHub"""
        try:
            import aiohttp
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    "https://api.github.com/search/code",
                    params={"q": query, "per_page": 5},
                    headers={"Accept": "application/vnd.github.v3+json"}
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        results = []
                        for item in data.get("items", []):
                            results.append({
                                "platform": "GitHub",
                                "title": item.get("name", ""),
                                "url": item.get("html_url", ""),
                                "repo": item.get("repository", {}).get("full_name", ""),
                                "snippet": item.get("path", "")
                            })
                        return results
        except Exception as e:
            logger.warning(f"GitHub search failed: {e}")
        
        return [{
            "platform": "GitHub",
            "title": f"GitHub: {query}",
            "url": f"https://github.com/search?q={query}",
            "snippet": f"Search code on GitHub for {query}"
        }]
    
    async def _search_bilibili(self, query: str) -> List[Dict]:
        """Search Bilibili (Chinese video platform)"""
        return [{
            "platform": "Bilibili",
            "title": f"B站视频: {query}",
            "url": f"https://search.bilibili.com/search?keyword={query}",
            "snippet": f"Search Bilibili for {query}"
        }]
    
    async def _search_xiaohongshu(self, query: str) -> List[Dict]:
        """Search XiaoHongShu (Chinese social platform)"""
        return [{
            "platform": "小红书",
            "title": f"小红书: {query}",
            "url": f"https://www.xiaohongshu.com/search_result?keyword={query}",
            "snippet": f"Search XiaoHongShu for {query}"
        }]
    
    def _format_results(self, results: List[Dict]) -> str:
        """Format search results"""
        if not results:
            return "🔍 No results found."
        
        output = "🔍 **Search Results:**\n\n"
        
        for i, r in enumerate(results[:self.results_limit], 1):
            platform = r.get("platform", "Web")
            title = r.get("title", "No title")
            url = r.get("url", "")
            snippet = r.get("snippet", "")[:100]
            
            output += f"**{i}. [{platform}]** {title}\n"
            if snippet:
                output += f"   {snippet}...\n"
            output += f"   🔗 {url}\n\n"
        
        return output


class CriticalThinkingTool:
    """
    Critical thinking and analysis tool
    Analyzes arguments, evaluates evidence, identifies biases
    """
    
    def __init__(self):
        self.analysis_depth = "deep"  # shallow, medium, deep
    
    async def analyze(self, text: str, analysis_type: str = "full") -> str:
        """
        Perform critical thinking analysis
        
        Args:
            text: Text to analyze
            analysis_type: "full", "logic", "bias", "evidence"
        """
        logger.info(f"🧠 Critical analysis: {text[:50]}...")
        
        if analysis_type == "logic" or analysis_type == "full":
            logic_result = await self._analyze_logic(text)
        
        if analysis_type == "bias" or analysis_type == "full":
            bias_result = await self._analyze_bias(text)
        
        if analysis_type == "evidence" or analysis_type == "full":
            evidence_result = await self._analyze_evidence(text)
        
        if analysis_type == "full":
            return self._format_full_analysis(logic_result, bias_result, evidence_result)
        elif analysis_type == "logic":
            return logic_result
        elif analysis_type == "bias":
            return bias_result
        else:
            return evidence_result
    
    async def _analyze_logic(self, text: str) -> str:
        """Analyze logical structure"""
        # Simple pattern-based analysis
        issues = []
        
        # Check for absolute terms
        absolute_terms = ["always", "never", "everyone", "nobody", "all", "none"]
        for term in absolute_terms:
            if term in text.lower():
                issues.append(f"⚠️ Absolute term '{term}' - often indicates overgeneralization")
        
        # Check for causal claims
        if "because" in text.lower() or "therefore" in text.lower():
            issues.append("ℹ️ Causal language detected - verify causation vs correlation")
        
        # Check for assertions without evidence
        claim_indicators = ["I think", "I believe", "obviously", "clearly"]
        has_claim = any(ind in text.lower() for ind in claim_indicators)
        has_evidence = any(word in text.lower() for word in ["study", "research", "data", "according to", "evidence"])
        
        if has_claim and not has_evidence:
            issues.append("⚠️ Claims made without supporting evidence")
        
        if not issues:
            return "✅ **Logic Analysis:** No obvious logical issues found."
        
        return "✅ **Logic Analysis:**\n" + "\n".join(issues)
    
    async def _analyze_bias(self, text: str) -> str:
        """Analyze potential biases"""
        biases = []
        
        # Emotional language
        emotional_words = ["terrible", "amazing", "horrible", "wonderful", "disgusting", "fantastic"]
        found_emotional = [w for w in emotional_words if w in text.lower()]
        if found_emotional:
            biases.append(f"⚠️ Emotional language detected: {', '.join(found_emotional)}")
        
        # Either-or thinking
        if "either" in text.lower() and "or" in text.lower():
            biases.append("ℹ️ Either-or framing detected - consider nuances")
        
        # Appeal to authority
        authority_words = ["experts say", "scientists believe", "authorities", "official"]
        if any(word in text.lower() for word in authority_words):
            biases.append("ℹ️ Authority appeal - verify credentials")
        
        # Confirmation bias (seeking only supportive info)
        if "prove" in text.lower() and not any(w in text.lower() for w in ["disprove", "contradict", "challenge"]):
            biases.append("ℹ️ Only seeking confirmation - consider alternative views")
        
        if not biases:
            return "✅ **Bias Analysis:** No obvious biases detected."
        
        return "✅ **Bias Analysis:**\n" + "\n".join(biases)
    
    async def _analyze_evidence(self, text: str) -> str:
        """Analyze evidence quality"""
        evidence_types = {
            "scientific": ["study", "research", "experiment", "peer-reviewed", "journal"],
            "statistical": ["data", "statistics", "percent", "average", "survey"],
            "anecdotal": ["I heard", "someone told me", "I know someone", "my friend"],
            "expert": ["expert", "professional", "specialist", "researcher"]
        }
        
        found = []
        for etype, keywords in evidence_types.items():
            if any(kw in text.lower() for kw in keywords):
                found.append(etype)
        
        if not found:
            return "⚠️ **Evidence Analysis:** No clear evidence indicators found."
        
        quality = "strong" if "scientific" in found or "statistical" in found else "weak"
        types_str = ", ".join(found)
        
        return f"✅ **Evidence Analysis:** Found {quality} evidence types: {types_str}"
    
    def _format_full_analysis(self, logic: str, bias: str, evidence: str) -> str:
        """Format full analysis"""
        return f"""🧠 **Critical Thinking Analysis:**

{logic}

---

{bias}

---

{evidence}

---

💡 **Summary:** Consider multiple perspectives and verify claims with reliable sources."""


class CodeAnalysisTool:
    """
    Code analysis and understanding tool
    Based on code-review-graph architecture
    """
    
    def __init__(self, project_path: str = None):
        self.project_path = project_path
        self.graph = None
        self.embeddings = None
    
    async def analyze_code(self, code: str, language: str = "auto") -> str:
        """Analyze code for structure, quality, patterns"""
        
        # Detect language
        if language == "auto":
            language = self._detect_language(code)
        
        analysis = f"💻 **Code Analysis** ({language}):\n\n"
        
        # Count lines and structure
        lines = code.split("\n")
        analysis += f"📊 Lines: {len(lines)}\n"
        
        # Check for functions
        functions = self._extract_functions(code, language)
        if functions:
            analysis += f"🔧 Functions: {', '.join(functions[:10])}\n"
        
        # Check for classes
        classes = self._extract_classes(code, language)
        if classes:
            analysis += f"🏗️ Classes: {', '.join(classes[:10])}\n"
        
        # Complexity estimate
        complexity = self._estimate_complexity(code)
        analysis += f"📈 Complexity: {complexity}\n"
        
        # Issues
        issues = self._find_issues(code, language)
        if issues:
            analysis += "\n⚠️ **Potential Issues:**\n"
            for issue in issues:
                analysis += f"  - {issue}\n"
        
        return analysis
    
    def _detect_language(self, code: str) -> str:
        """Detect programming language"""
        if "def " in code and ":" in code:
            return "Python"
        elif "function " in code or "const " in code or "let " in code:
            return "JavaScript"
        elif "func " in code and "package " in code:
            return "Go"
        elif "fn " in code and "->" in code:
            return "Rust"
        elif "public class" in code:
            return "Java"
        elif "#include" in code:
            return "C/C++"
        elif "def " in code and "end" in code:
            return "Ruby"
        return "Unknown"
    
    def _extract_functions(self, code: str, language: str) -> List[str]:
        """Extract function names"""
        functions = []
        
        if language == "Python":
            import re
            functions = re.findall(r'def (\w+)\s*\(', code)
        elif language in ["JavaScript", "TypeScript"]:
            import re
            functions = re.findall(r'function (\w+)|const (\w+)\s*=', code)
            functions = [f for f in functions if f]
        
        return functions
    
    def _extract_classes(self, code: str, language: str) -> List[str]:
        """Extract class names"""
        classes = []
        
        if language in ["Python", "Java", "JavaScript", "TypeScript"]:
            import re
            classes = re.findall(r'class (\w+)', code)
        
        return classes
    
    def _estimate_complexity(self, code: str) -> str:
        """Estimate code complexity"""
        import re
        
        # Count decision points
        ifs = len(re.findall(r'\bif\b', code))
        loops = len(re.findall(r'\b(for|while)\b', code))
        matches = len(re.findall(r'\bswitch\b|\bcase\b|\bmatch\b', code))
        
        points = ifs + loops * 2 + matches
        
        if points < 5:
            return "Low"
        elif points < 15:
            return "Medium"
        else:
            return "High"
    
    def _find_issues(self, code: str, language: str) -> List[str]:
        """Find potential code issues"""
        issues = []
        
        # Check for common issues
        if "print(" in code and "debug" in code.lower():
            issues.append("Possible debug print statement")
        
        if "TODO" in code or "FIXME" in code:
            issues.append("Contains TODO/FIXME comments")
        
        if len(code.split("\n")) > 500:
            issues.append("Large file - consider splitting")
        
        # Security checks
        dangerous = ["eval(", "exec(", "subprocess(", "os.system"]
        if any(d in code for d in dangerous):
            issues.append("Contains potentially dangerous function")
        
        return issues


class KnowledgeGraphTool:
    """
    Knowledge graph for code understanding
    Based on code-review-graph
    """
    
    def __init__(self):
        self.graph = {}
        self.nodes = {}
        self.edges = []
    
    async def build_graph(self, code_files: Dict[str, str]) -> str:
        """Build knowledge graph from code files"""
        
        for file_path, code in code_files.items():
            # Add file node
            self.nodes[file_path] = {"type": "file", "content": code[:100]}
            
            # Extract imports/dependencies
            imports = self._extract_imports(code)
            for imp in imports:
                self.edges.append((file_path, imp, "imports"))
        
        return f"📊 **Knowledge Graph Built:**\n- Nodes: {len(self.nodes)}\n- Edges: {len(self.edges)}"
    
    def _extract_imports(self, code: str) -> List[str]:
        """Extract imports from code"""
        imports = []
        import re
        
        # Python
        imports.extend(re.findall(r'import (\w+)', code))
        imports.extend(re.findall(r'from (\w+) import', code))
        
        # JavaScript
        imports.extend(re.findall(r'import .+ from ["\']([^"\']+)["\']', code))
        
        return imports
    
    async def query(self, query: str) -> str:
        """Query the knowledge graph"""
        # Simple keyword search
        results = []
        
        for node, data in self.nodes.items():
            if query.lower() in node.lower() or query.lower() in data.get("content", "").lower():
                results.append(node)
        
        if not results:
            return "🔍 No matching nodes found in graph."
        
        return f"📊 **Found {len(results)} matching nodes:**\n" + "\n".join(f"  - {r}" for r in results)