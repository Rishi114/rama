"""RAG Engine - Retrieval-Augmented Generation
Inspired by NotebookLM's document ingestion"""

import asyncio
import logging
from typing import List, Optional
from pathlib import Path

logger = logging.getLogger(__name__)


class RAGEngine:
    """
    Retrieval-Augmented Generation Engine
    Handles document ingestion, chunking, and retrieval
    """
    
    def __init__(self, embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.embedding_model = embedding_model
        self.embeddings = None
        self.vector_store = None
        self.document_chunks = []
        self.chunk_size = 512
        self.chunk_overlap = 50
    
    async def initialize(self):
        """Initialize embedding model and vector store"""
        logger.info("📚 Initializing RAG Engine...")
        
        try:
            from langchain_community.embeddings import HuggingFaceEmbeddings
            from langchain_community.vectorstores import FAISS
            
            self.embeddings = HuggingFaceEmbeddings(
                model_name=self.embedding_model,
                model_kwargs={'device': 'cpu'}
            )
            
            # Try to load existing vector store
            store_path = Path("data/embeddings/faiss_index")
            if store_path.exists():
                self.vector_store = FAISS.load_local(
                    str(store_path), 
                    self.embeddings,
                    allow_dangerous_deserialization=True
                )
                logger.info(f"✅ Loaded existing vector store with {self.vector_store.index.ntotal} documents")
            else:
                logger.info("📚 No existing vector store, starting fresh")
                
        except Exception as e:
            logger.warning(f"RAG initialization failed: {e}")
    
    async def add_document(self, text: str, source: str = "unknown"):
        """Add a document to the knowledge base"""
        from langchain.text_splitter import RecursiveCharacterTextSplitter
        
        # Split into chunks
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap
        )
        
        chunks = splitter.split_text(text)
        
        # Store metadata
        for i, chunk in enumerate(chunks):
            self.document_chunks.append({
                "content": chunk,
                "source": source,
                "chunk_id": i
            })
        
        # Add to vector store
        if self.embeddings:
            from langchain_community.vectorstores import FAISS
            
            if self.vector_store is None:
                self.vector_store = FAISS.from_texts(chunks, self.embeddings)
            else:
                self.vector_store.add_texts(chunks)
            
            # Save
            await self._save_vector_store()
        
        logger.info(f"✅ Added {len(chunks)} chunks from {source}")
    
    async def _save_vector_store(self):
        """Persist vector store to disk"""
        if self.vector_store:
            Path("data/embeddings").mkdir(parents=True, exist_ok=True)
            self.vector_store.save_local("data/embeddings/faiss_index")
    
    async def retrieve(self, query: str, top_k: int = 5) -> List[str]:
        """Retrieve relevant documents"""
        if not self.vector_store:
            return []
        
        try:
            docs = self.vector_store.similarity_search(query, k=top_k)
            return [doc.page_content for doc in docs]
        except Exception as e:
            logger.warning(f"Retrieval failed: {e}")
            return []
    
    async def ingest_pdf(self, pdf_path: str):
        """Ingest PDF document"""
        try:
            from pypdf import PdfReader
            
            reader = PdfReader(pdf_path)
            text = ""
            
            for page in reader.pages:
                text += page.extract_text() + "\n"
            
            await self.add_document(text, source=pdf_path)
            logger.info(f"✅ Ingested PDF: {pdf_path}")
            
        except Exception as e:
            logger.error(f"PDF ingestion failed: {e}")
    
    async def ingest_file(self, file_path: str):
        """Ingest various file types"""
        path = Path(file_path)
        
        if path.suffix == ".pdf":
            await self.ingest_pdf(file_path)
        elif path.suffix in [".txt", ".md"]:
            text = path.read_text()
            await self.add_document(text, source=file_path)
        else:
            logger.warning(f"Unsupported file type: {path.suffix}")
    
    async def ingest_url(self, url: str):
        """Scrape and ingest URL content"""
        try:
            import aiohttp
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    text = await response.text()
                    
            # Simple HTML to text
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(text, 'html.parser')
            content = soup.get_text(separator='\n', strip=True)
            
            await self.add_document(content[:10000], source=url)
            logger.info(f"✅ Ingested URL: {url}")
            
        except Exception as e:
            logger.error(f"URL ingestion failed: {e}")
    
    def get_stats(self) -> dict:
        """Get RAG statistics"""
        return {
            "total_chunks": len(self.document_chunks),
            "sources": list(set(c["source"] for c in self.document_chunks)),
            "vector_store_size": self.vector_store.index.ntotal if self.vector_store else 0
        }