"""
RAMA AI - Real Time Search Engine
Handles live web searches
"""

import webbrowser
import requests
import json
from typing import Dict, List, Optional


class SearchEngine:
    """
    Real-time web search for RAMA
    Handles live searches
    """
    
    def __init__(self, config=None):
        self.config = config or {}
        
        # Search engines
        self.engines = {
            'google': 'https://google.com/search?q={query}',
            'youtube': 'https://youtube.com/results?search_query={query}',
            'github': 'https://github.com/search?q={query}',
            'wikipedia': 'https://en.wikipedia.org/wiki/{query}',
            'reddit': 'https://reddit.com/search?q={query}',
            'twitter': 'https://twitter.com/search?q={query}',
            'bilibili': 'https://search.bilibili.com/search?keyword={query}',
        }
    
    def search(self, query, engine='google', open_browser=True):
        """
        Perform a web search
        Args:
            query: What to search for
            engine: Which search engine (google, youtube, etc.)
            open_browser: If True, opens in browser
        Returns:
            Search result message
        """
        if not query:
            return "Kya search karna hai bhai?"
        
        # Get URL
        template = self.engines.get(engine.lower(), self.engines['google'])
        url = template.format(query=query.replace(' ', '+'))
        
        if open_browser:
            try:
                webbrowser.open(url)
                return f"🔍 Searching {engine} for: {query}... 🌐"
            except Exception as e:
                return f"❌ Search error: {str(e)}"
        
        # Return URL if not opening browser
        return url
    
    def search_google(self, query):
        """Search Google"""
        return self.search(query, 'google')
    
    def search_youtube(self, query):
        """Search YouTube"""
        return self.search(query, 'youtube')
    
    def search_github(self, query):
        """Search GitHub"""
        return self.search(query, 'github')
    
    def search_wikipedia(self, topic):
        """Search Wikipedia"""
        return self.search(topic, 'wikipedia')
    
    def open_website(self, url):
        """Open a specific website"""
        # Add https if missing
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        try:
            webbrowser.open(url)
            return f"✅ Opened! 🌐"
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def get_page_content(self, url, max_chars=2000):
        """Fetch page content (simple)"""
        try:
            response = requests.get(url, timeout=5)
            content = response.text[:max_chars]
            return content
        except Exception as e:
            return f"❌ Error: {str(e)}"


if __name__ == "__main__":
    engine = SearchEngine()
    print(engine.search_google("python tutorial"))
    print(engine.search_youtube("ai tutorial"))