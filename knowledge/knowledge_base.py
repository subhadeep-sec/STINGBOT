"""
Knowledge Base with RAG (Retrieval Augmented Generation)

Provides security knowledge, tool documentation, and learned insights
using vector similarity search and LLM generation.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'agents', 'python-brain'))

try:
    import chromadb
    from chromadb.config import Settings
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False

from typing import Dict, List, Any
import json


class KnowledgeBase:
    """
    RAG-powered knowledge system for security testing.
    
    Contains:
    - Security testing techniques
    - Tool documentation
    - CVE and vulnerability information
    - Best practices
    - Learned insights from missions
    """
    
    def __init__(self, workspace_path: str = "./knowledge"):
        """Initialize knowledge base."""
        self.workspace_path = workspace_path
        os.makedirs(workspace_path, exist_ok=True)
        
        if not CHROMADB_AVAILABLE:
            print("[Knowledge] ChromaDB not available - using fallback mode")
            self.knowledge_store = None
            self.fallback_knowledge = self._load_fallback_knowledge()
            return
        
        # Initialize ChromaDB
        self.client = chromadb.PersistentClient(
            path=os.path.join(workspace_path, "chroma_kb"),
            settings=Settings(anonymized_telemetry=False)
        )
        
        self.knowledge_store = self.client.get_or_create_collection(
            name="security_knowledge",
            metadata={"description": "Security testing knowledge base"}
        )
        
        # Load initial knowledge if empty
        if self.knowledge_store.count() == 0:
            self._load_initial_knowledge()
        
        print(f"[Knowledge] Initialized with {self.knowledge_store.count()} knowledge items")
    
    def query(self, question: str, k: int = 3) -> Dict[str, Any]:
        """
        Query knowledge base using RAG.
        
        Args:
            question: User's question
            k: Number of relevant documents to retrieve
        
        Returns:
            Answer with sources
        """
        if not CHROMADB_AVAILABLE or not self.knowledge_store:
            return self._fallback_query(question)
        
        # Retrieve relevant knowledge
        results = self.knowledge_store.query(
            query_texts=[question],
            n_results=min(k, self.knowledge_store.count())
        )
        
        if not results or not results['documents'][0]:
            return {"answer": "No relevant knowledge found", "sources": []}
        
        # Compile context from retrieved documents
        context = "\\n\\n".join(results['documents'][0])
        
        # Generate answer using LLM (would integrate with LLMAdapter)
        answer = f"Based on knowledge base:\\n{context[:500]}..."
        
        sources = [
            {
                "content": doc[:200],
                "metadata": meta
            }
            for doc, meta in zip(results['documents'][0], results['metadatas'][0])
        ]
        
        return {
            "answer": answer,
            "sources": sources,
            "confidence": 0.8
        }
    
    def add_knowledge(self, content: str, metadata: Dict = None):
        """Add new knowledge to the base."""
        if not CHROMADB_AVAILABLE or not self.knowledge_store:
            return
        
        doc_id = f"kb_{self.knowledge_store.count() + 1}"
        
        self.knowledge_store.add(
            documents=[content],
            metadatas=[metadata or {}],
            ids=[doc_id]
        )
        
        print(f"[Knowledge] Added new knowledge: {content[:50]}...")
    
    def get_tool_documentation(self, tool_name: str) -> str:
        """Get documentation for a specific tool."""
        tool_docs = {
            "nmap": """
Nmap - Network Mapper
Usage: nmap [options] target
Common options:
  -sV: Version detection
  -sS: SYN scan
  -p-: Scan all ports
  -A: Aggressive scan (OS detection, version, scripts)
Example: nmap -sV -p- target.com
""",
            "nikto": """
Nikto - Web Server Scanner
Usage: nikto -h target
Options:
  -h: Target host
  -p: Port
  -ssl: Force SSL
Example: nikto -h https://target.com
""",
            "sqlmap": """
SQLMap - SQL Injection Tool
Usage: sqlmap -u URL [options]
Options:
  -u: Target URL
  --dbs: Enumerate databases
  --tables: Enumerate tables
  --dump: Dump data
Example: sqlmap -u "http://target.com/page?id=1" --dbs
"""
        }
        
        return tool_docs.get(tool_name.lower(), f"No documentation available for {tool_name}")
    
    def get_technique_info(self, technique: str) -> Dict:
        """Get information about a security testing technique."""
        techniques = {
            "sql_injection": {
                "name": "SQL Injection",
                "description": "Injecting SQL commands into input fields",
                "common_payloads": ["' OR '1'='1", "1' UNION SELECT NULL--"],
                "tools": ["sqlmap", "burp suite"],
                "severity": "High"
            },
            "xss": {
                "name": "Cross-Site Scripting",
                "description": "Injecting malicious scripts into web pages",
                "common_payloads": ["<script>alert(1)</script>", "<img src=x onerror=alert(1)>"],
                "tools": ["burp suite", "xsser"],
                "severity": "Medium to High"
            }
        }
        
        return techniques.get(technique.lower(), {"name": technique, "description": "Unknown technique"})
    
    def _load_initial_knowledge(self):
        """Load initial security knowledge."""
        initial_knowledge = [
            {
                "content": "SQL Injection is a code injection technique that exploits vulnerabilities in database queries. Test login forms with payloads like ' OR '1'='1",
                "metadata": {"category": "vulnerability", "type": "sql_injection"}
            },
            {
                "content": "XSS (Cross-Site Scripting) allows attackers to inject malicious scripts. Test input fields with <script>alert(1)</script>",
                "metadata": {"category": "vulnerability", "type": "xss"}
            },
            {
                "content": "Nmap is essential for network reconnaissance. Use -sV for version detection and -p- for all ports",
                "metadata": {"category": "tool", "name": "nmap"}
            },
            {
                "content": "Always start with reconnaissance before exploitation. Gather information about target infrastructure first",
                "metadata": {"category": "best_practice", "phase": "reconnaissance"}
            },
            {
                "content": "Check for common vulnerabilities: SQL injection, XSS, CSRF, authentication bypass, directory traversal",
                "metadata": {"category": "checklist", "type": "web_app"}
            }
        ]
        
        for item in initial_knowledge:
            self.add_knowledge(item["content"], item["metadata"])
    
    def _load_fallback_knowledge(self) -> Dict:
        """Load fallback knowledge when ChromaDB unavailable."""
        return {
            "sql_injection": "SQL Injection testing involves injecting SQL commands into input fields",
            "xss": "Cross-Site Scripting allows injecting malicious scripts into web pages",
            "nmap": "Nmap is a network scanning tool for reconnaissance"
        }
    
    def _fallback_query(self, question: str) -> Dict:
        """Fallback query when ChromaDB unavailable."""
        question_lower = question.lower()
        
        for key, value in self.fallback_knowledge.items():
            if key in question_lower:
                return {
                    "answer": value,
                    "sources": [{"content": value, "metadata": {"type": key}}],
                    "confidence": 0.5
                }
        
        return {
            "answer": "Knowledge base unavailable - ChromaDB not installed",
            "sources": [],
            "confidence": 0.0
        }


# Example usage
if __name__ == "__main__":
    kb = KnowledgeBase(workspace_path="./test_knowledge")
    
    # Query knowledge
    result = kb.query("How do I test for SQL injection?")
    print(f"Answer: {result['answer']}")
    print(f"Sources: {len(result['sources'])}")
    
    # Get tool documentation
    print(kb.get_tool_documentation("nmap"))
    
    # Get technique info
    info = kb.get_technique_info("sql_injection")
    print(json.dumps(info, indent=2))
