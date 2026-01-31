"""
Knowledge Base for STINGBOT
Powered by RAG (Retrieval Augmented Generation) and ChromaDB.

This module manages the long-term knowledge of the agent, including:
- Security concepts and CVEs
- Tool documentation and usage examples
- Best practices and rules of engagement
- Learned facts that aren't specific to a single mission
"""

import chromadb
from chromadb.config import Settings
import json
import os
from typing import List, Dict, Any, Optional
import time

class KnowledgeBase:
    """
    RAG-powered knowledge system for retrieving security information.
    """
    
    def __init__(self, workspace_path: str = "./memory"):
        """Initialize Knowledge Base with ChromaDB."""
        self.workspace_path = workspace_path
        os.makedirs(workspace_path, exist_ok=True)
        
        # Initialize Persistent Client
        self.client = chromadb.PersistentClient(
            path=os.path.join(workspace_path, "knowledge_db"),
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Collections
        self.security_knowledge = self.client.get_or_create_collection(
            name="security_knowledge",
            metadata={"description": "General security knowledge and CVEs"}
        )
        
        self.tool_docs = self.client.get_or_create_collection(
            name="tool_docs",
            metadata={"description": "Documentation for tools"}
        )
        
        print(f"[Knowledge] Initialized. Items: {self.security_knowledge.count()} knowledge, {self.tool_docs.count()} tools")
        
        # Seed basic knowledge if empty
        if self.tool_docs.count() == 0:
            self._seed_basic_knowledge()

    def query_knowledge(self, query: str, n_results: int = 3) -> List[str]:
        """
        Retrieve relevant security knowledge for a query.
        """
        results = self.security_knowledge.query(
            query_texts=[query],
            n_results=min(n_results, self.security_knowledge.count() or 1)
        )
        
        if not results or not results['documents'] or not results['documents'][0]:
            return []
            
        return results['documents'][0]

    def get_tool_usage(self, tool_name: str) -> Dict[str, Any]:
        """
        Get documentation and usage examples for a tool.
        """
        results = self.tool_docs.query(
            query_texts=[tool_name],
            n_results=1,
            where={"tool_name": tool_name}
        )
        
        if results and results['documents'] and results['documents'][0]:
             return {
                 "description": results['documents'][0][0],
                 "metadata": results['metadatas'][0][0]
             }
        
        # Fallback: fuzzy search
        results = self.tool_docs.query(
            query_texts=[f"how to use {tool_name}"],
            n_results=1
        )
        
        if results and results['documents'] and results['documents'][0]:
            return {
                 "description": results['documents'][0][0],
                 "metadata": results['metadatas'][0][0]
             }
             
        return None

    def add_knowledge(self, content: str, category: str, tags: List[str] = None):
        """
        Add new knowledge to the base.
        """
        doc_id = f"know_{int(time.time())}_{hash(content) % 10000}"
        
        self.security_knowledge.add(
            documents=[content],
            metadatas=[{
                "category": category,
                "tags": ",".join(tags or []),
                "added": str(time.time())
            }],
            ids=[doc_id]
        )
        print(f"[Knowledge] Added new entry: {category}")

    def _seed_basic_knowledge(self):
        """Pre-populate with some essential security knowledge."""
        print("[Knowledge] Seeding initial knowledge...")
        
        # Nmap
        self.tool_docs.add(
            documents=["Nmap is a network scanner. Usage: nmap -sV -sC <target>. -sV determines service versions, -sC runs default scripts."],
            metadatas=[{"tool_name": "nmap", "category": "recon"}],
            ids=["tool_nmap"]
        )
        
        # SQLmap
        self.tool_docs.add(
            documents=["SQLmap automates detection and exploitation of SQL injection. Usage: sqlmap -u <url> --batch. Use --wizard for beginner mode."],
            metadatas=[{"tool_name": "sqlmap", "category": "exploitation"}],
            ids=["tool_sqlmap"]
        )
        
        # General Concepts
        self.security_knowledge.add(
            documents=[
                "SQL Injection (SQLi) occurs when user input is improperly neutralized before being included in a database query. Fix: Use parameterized queries.",
                "Cross-Site Scripting (XSS) allows attackers to inject client-side scripts into web pages viewed by other users. Fix: Encode output and validate input.",
                "Reconnaissance is the first phase of an assessment. Passive recon gathers info without interacting directly. Active recon probes the target."
            ],
            metadatas=[
                {"category": "vulnerability", "tags": "sqli,web"},
                {"category": "vulnerability", "tags": "xss,web"},
                {"category": "methodology", "tags": "recon,process"}
            ],
            ids=["concept_sqli", "concept_xss", "concept_recon"]
        )

# Example Usage
if __name__ == "__main__":
    kb = KnowledgeBase(workspace_path="./test_memory")
    
    print("\n--- Testing Knowledge Query ---")
    results = kb.query_knowledge("How do I fix SQL injection?")
    for res in results:
        print(f"- {res}")
        
    print("\n--- Testing Tool Lookup ---")
    nmap_doc = kb.get_tool_usage("nmap")
    print(f"Nmap Doc: {nmap_doc['description']}")
