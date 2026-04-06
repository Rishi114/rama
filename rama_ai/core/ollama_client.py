"""Ollama Client - Local LLM integration"""

import asyncio
import logging
from typing import Optional, List
import json

logger = logging.getLogger(__name__)


class OllamaClient:
    """Client for local Ollama LLM"""
    
    def __init__(self, model: str = "llama3.2:1b", host: str = "http://localhost:11434"):
        self.model = model
        self.host = host
        self.client = None
        self.is_connected = False
    
    async def connect(self) -> bool:
        """Connect to Ollama"""
        try:
            import aiohttp
            self.client = aiohttp.ClientSession()
            
            async with self.client.get(f"{self.host}/api/tags") as response:
                self.is_connected = response.status == 200
                
            if self.is_connected:
                logger.info(f"✅ Connected to Ollama: {self.model}")
            else:
                logger.warning("⚠️ Ollama not running. Start with 'ollama serve'")
                
        except Exception as e:
            logger.warning(f"⚠️ Ollama not available: {e}")
            self.is_connected = False
        
        return self.is_connected
    
    async def generate(self, prompt: str, temperature: float = 0.7) -> str:
        """Generate response from LLM"""
        if not self.is_connected or not self.client:
            return ""
        
        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": temperature
                }
            }
            
            async with self.client.post(
                f"{self.host}/api/generate",
                json=payload
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("response", "")
                    
        except Exception as e:
            logger.error(f"Generation error: {e}")
        
        return ""
    
    async def close(self):
        """Close connection"""
        if self.client:
            await self.client.close()