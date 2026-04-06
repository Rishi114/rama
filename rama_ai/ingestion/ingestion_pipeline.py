"""Ingestion Pipeline - Knowledge Ingestion System
PDF, Links, Code, Notes - Inspired by NotebookLM"""

import asyncio
import logging
from typing import List, Optional, Dict, Any
from pathlib import Path
import re

logger = logging.getLogger(__name__)


class IngestionPipeline:
    """
    Complete ingestion pipeline for knowledge sources
    """
    
    def __init__(self, rag_engine=None):
        self.rag_engine = rag_engine
        self.pdf_reader = PDFReader()
        self.link_scraper = LinkScraper()
        self.code_parser = CodeParser()
        self.notes_reader = NotesReader()
    
    async def ingest_file(self, file_path: str) -> bool:
        """Ingest a file based on its type"""
        path = Path(file_path)
        suffix = path.suffix.lower()
        
        logger.info(f"📥 Ingesting: {file_path}")
        
        try:
            if suffix == ".pdf":
                text = await self.pdf_reader.read(file_path)
            elif suffix in [".txt", ".md"]:
                text = path.read_text(encoding='utf-8')
            elif suffix in [".doc", ".docx"]:
                text = await self._read_docx(file_path)
            elif suffix == ".html":
                text = await self.link_scraper.scrape_text(file_path)
            else:
                logger.warning(f"Unsupported file type: {suffix}")
                return False
            
            # Add to RAG
            if self.rag_engine and text:
                await self.rag_engine.add_document(text, source=file_path)
                
            logger.info(f"✅ Ingested: {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"Ingestion failed: {e}")
            return False
    
    async def ingest_url(self, url: str) -> bool:
        """Ingest URL content"""
        try:
            text = await self.link_scraper.scrape(url)
            
            if self.rag_engine and text:
                await self.rag_engine.add_document(text, source=url)
                
            logger.info(f"✅ Ingested URL: {url}")
            return True
            
        except Exception as e:
            logger.error(f"URL ingestion failed: {e}")
            return False
    
    async def ingest_code_repo(self, repo_path: str) -> bool:
        """Ingest code repository"""
        try:
            files = await self.code_parser.parse_directory(repo_path)
            
            for file_path, code in files.items():
                if self.rag_engine:
                    await self.rag_engine.add_document(
                        f"File: {file_path}\n\n{code}",
                        source=file_path
                    )
            
            logger.info(f"✅ Ingested code: {repo_path}")
            return True
            
        except Exception as e:
            logger.error(f"Code ingestion failed: {e}")
            return False
    
    async def _read_docx(self, file_path: str) -> str:
        """Read DOCX file"""
        try:
            from docx import Document
            doc = Document(file_path)
            return "\n".join([p.text for p in doc.paragraphs])
        except:
            return ""


class PDFReader:
    """
    PDF reading and text extraction
    """
    
    async def read(self, pdf_path: str) -> str:
        """Read PDF and extract text"""
        try:
            from pypdf import PdfReader
            
            reader = PdfReader(pdf_path)
            text_parts = []
            
            for i, page in enumerate(reader.pages):
                try:
                    text = page.extract_text()
                    if text:
                        text_parts.append(f"--- Page {i+1} ---\n{text}")
                except Exception as e:
                    logger.warning(f"Failed to extract page {i}: {e}")
            
            return "\n\n".join(text_parts)
            
        except Exception as e:
            logger.error(f"PDF read failed: {e}")
            return ""
    
    async def read_with_ocr(self, pdf_path: str) -> str:
        """Read PDF with OCR for scanned documents"""
        # Placeholder for OCR implementation
        logger.info("OCR not implemented yet")
        return await self.read(pdf_path)


class LinkScraper:
    """
    Web link scraping and summarization
    """
    
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
    
    async def scrape(self, url: str) -> str:
        """Scrape URL and extract content"""
        try:
            import aiohttp
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=self.headers) as response:
                    if response.status != 200:
                        logger.warning(f"URL returned {response.status}")
                        return ""
                    
                    html = await response.text()
            
            return self.extract_text(html)
            
        except Exception as e:
            logger.error(f"Scraping failed: {e}")
            return ""
    
    async def scrape_text(self, html_path: str) -> str:
        """Scrape from local HTML file"""
        from bs4 import BeautifulSoup
        
        html = Path(html_path).read_text()
        return self.extract_text(html)
    
    def extract_text(self, html: str) -> str:
        """Extract text from HTML"""
        from bs4 import BeautifulSoup
        
        soup = BeautifulSoup(html, 'html.parser')
        
        # Remove script and style
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get text
        text = soup.get_text(separator='\n')
        
        # Clean up whitespace
        lines = [line.strip() for line in text.split('\n')]
        lines = [line for line in lines if line]
        
        return '\n'.join(lines[:2000])  # Limit length


class CodeParser:
    """
    Code repository parsing and indexing
    """
    
    def __init__(self):
        self.supported_extensions = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.java': 'java',
            '.cpp': 'cpp',
            '.c': 'c',
            '.go': 'go',
            '.rs': 'rust',
            '.rb': 'ruby',
            '.php': 'php',
            '.cs': 'csharp',
            '.swift': 'swift',
            '.kt': 'kotlin',
            '.html': 'html',
            '.css': 'css',
            '.json': 'json',
            '.yaml': 'yaml',
            '.yml': 'yaml',
            '.md': 'markdown',
        }
    
    async def parse_directory(self, dir_path: str) -> Dict[str, str]:
        """Parse entire directory"""
        files = {}
        
        path = Path(dir_path)
        if not path.exists():
            return files
        
        # Skip hidden and common ignore directories
        skip_dirs = {'.git', '__pycache__', 'node_modules', '.venv', 'venv', 'dist', 'build'}
        
        for file_path in path.rglob('*'):
            if file_path.is_file():
                # Check if should skip
                if any(part.startswith('.') or part in skip_dirs for part in file_path.parts):
                    continue
                
                # Check extension
                if file_path.suffix.lower() in self.supported_extensions:
                    try:
                        code = file_path.read_text(encoding='utf-8', errors='ignore')
                        files[str(file_path)] = code
                    except Exception as e:
                        logger.warning(f"Failed to read {file_path}: {e}")
        
        return files
    
    async def parse_file(self, file_path: str) -> Dict[str, Any]:
        """Parse a single code file"""
        path = Path(file_path)
        
        if not path.exists():
            return {}
        
        code = path.read_text(encoding='utf-8', errors='ignore')
        language = self.supported_extensions.get(path.suffix.lower(), 'unknown')
        
        return {
            "path": str(path),
            "language": language,
            "code": code,
            "size": len(code),
            "lines": len(code.split('\n'))
        }
    
    def extract_functions(self, code: str, language: str) -> List[str]:
        """Extract function/method names"""
        functions = []
        
        if language == 'python':
            # Simple regex for Python functions
            pattern = r'def (\w+)\s*\('
            functions = re.findall(pattern, code)
        
        elif language in ['javascript', 'typescript']:
            # Functions and arrow functions
            patterns = [
                r'function\s+(\w+)',
                r'const\s+(\w+)\s*=',
                r'(\w+)\s*\(\s*\)\s*{',
            ]
            for pattern in patterns:
                functions.extend(re.findall(pattern, code))
        
        return functions


class NotesReader:
    """
    Notes ingestion from various formats
    """
    
    def __init__(self):
        self.supported = ['.txt', '.md', '.org', '.note']
    
    async def read_notes(self, file_path: str) -> str:
        """Read notes file"""
        path = Path(file_path)
        
        if path.suffix.lower() not in self.supported:
            logger.warning(f"Unsupported notes format: {path.suffix}")
            return ""
        
        return path.read_text(encoding='utf-8')
    
    def parse_markdown(self, text: str) -> Dict[str, Any]:
        """Parse markdown into structured data"""
        sections = []
        current_section = {"title": "", "content": ""}
        
        for line in text.split('\n'):
            if line.startswith('#'):
                if current_section["title"] or current_section["content"]:
                    sections.append(current_section)
                current_section = {"title": line.strip(), "content": ""}
            else:
                current_section["content"] += line + "\n"
        
        if current_section["title"] or current_section["content"]:
            sections.append(current_section)
        
        return {
            "sections": sections,
            "raw": text
        }