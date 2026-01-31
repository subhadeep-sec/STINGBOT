"""
Knowledge Base for STINGBOT
Powered by RAG (Retrieval Augmented Generation) and ChromaDB.

This module manages the long-term knowledge of the agent, including:
- Security concepts and CVEs
- Tool documentation and usage examples
- Best practices and rules of engagement
- Learned facts that aren't specific to a single mission
"""

try:
    import chromadb
    from chromadb.config import Settings
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False
    print("[Knowledge] ChromaDB not available - switching to Lite Mode (JSON)")

import json
import os
from typing import List, Dict, Any, Optional
import time

class KnowledgeBase:
    """
    RAG-powered knowledge system for retrieving security information.
    Supports ChromaDB vector storage with a JSON fallback for lite mode.
    """
    
    def __init__(self, workspace_path: str = "./memory"):
        """Initialize Knowledge Base with persistent storage."""
        self.workspace_path = workspace_path
        os.makedirs(workspace_path, exist_ok=True)
        self.lite_mode = not CHROMADB_AVAILABLE
        
        if not self.lite_mode:
            try:
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
            except Exception as e:
                print(f"[Knowledge] Failed to init ChromaDB: {e}. Switching to Lite Mode.")
                self.lite_mode = True
        
        if self.lite_mode:
            self.knowledge_file = os.path.join(workspace_path, "knowledge.json")
            self.tools_file = os.path.join(workspace_path, "tools.json")
            self._load_lite_knowledge()

        # Seed basic knowledge if empty
        if self.lite_mode:
            if not self.local_tools:
                self._seed_basic_knowledge()
        else:
            if self.tool_docs.count() == 0:
                self._seed_basic_knowledge()
        
        count_k = len(self.local_knowledge) if self.lite_mode else self.security_knowledge.count()
        count_t = len(self.local_tools) if self.lite_mode else self.tool_docs.count()
        print(f"[Knowledge] Initialized. Items: {count_k} knowledge, {count_t} tools ({'LITE' if self.lite_mode else 'VECTOR'})")

    def _load_lite_knowledge(self):
        """Load knowledge from JSON files for lite mode."""
        self.local_knowledge = []
        self.local_tools = []
        
        if os.path.exists(self.knowledge_file):
            try:
                with open(self.knowledge_file, 'r') as f:
                    self.local_knowledge = json.load(f)
            except: pass
            
        if os.path.exists(self.tools_file):
            try:
                with open(self.tools_file, 'r') as f:
                    self.local_tools = json.load(f)
            except: pass
    
    def _save_lite_knowledge(self):
        """Save knowledge to JSON files."""
        with open(self.knowledge_file, 'w') as f:
            json.dump(self.local_knowledge, f, indent=2)
        with open(self.tools_file, 'w') as f:
            json.dump(self.local_tools, f, indent=2)

    def query_knowledge(self, query: str, n_results: int = 3) -> List[str]:
        """
        Retrieve relevant security knowledge for a query.
        """
        if self.lite_mode:
            results = []
            query_terms = query.lower().split()
            for item in self.local_knowledge:
                score = 0
                content = (item['metadata']['category'] + " " + item['document']).lower()
                for term in query_terms:
                    if term in content:
                        score += 1
                if score > 0:
                    results.append({
                        "content": item['document'],
                        "score": score
                    })
            results.sort(key=lambda x: x['score'], reverse=True)
            return [r['content'] for r in results[:n_results]]

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
        if self.lite_mode:
            tool_name_lower = tool_name.lower()
            for item in self.local_tools:
                if item['metadata']['tool_name'].lower() == tool_name_lower:
                    return {
                        "description": item['document'],
                        "metadata": item['metadata']
                    }
            # Fuzzy match
            for item in self.local_tools:
                if tool_name_lower in item['document'].lower():
                    return {
                        "description": item['document'],
                        "metadata": item['metadata']
                    }
            return None

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
        
        metadata = {
            "category": category,
            "tags": ",".join(tags or []),
            "added": str(time.time())
        }
        
        if self.lite_mode:
            self.local_knowledge.append({
                "id": doc_id,
                "document": content,
                "metadata": metadata
            })
            self._save_lite_knowledge()
        else:
            self.security_knowledge.add(
                documents=[content],
                metadatas=[metadata],
                ids=[doc_id]
            )
        print(f"[Knowledge] Added new entry: {category}")

    def _seed_basic_knowledge(self):
        """Pre-populate with some essential security knowledge."""
        print("[Knowledge] Seeding initial knowledge...")
        
        tools = [
            {
                "id": "tool_nmap",
                "document": "Nmap is a network scanner. Usage: nmap -sV -sC <target>. -sV determines service versions, -sC runs default scripts.",
                "metadata": {"tool_name": "nmap", "category": "recon"}
            },
            {
                "id": "tool_sqlmap",
                "document": "SQLmap automates detection and exploitation of SQL injection. Usage: sqlmap -u <url> --batch. Use --wizard for beginner mode.",
                "metadata": {"tool_name": "sqlmap", "category": "exploitation"}
            }
        ]
        
        knowledge = [
            {
                "id": "concept_sqli",
                "document": "SQL Injection (SQLi) occurs when user input is improperly neutralized before being included in a database query. Fix: Use parameterized queries.",
                "metadata": {"category": "vulnerability", "tags": "sqli,web"}
            },
            {
                "id": "concept_xss",
                "document": "Cross-Site Scripting (XSS) allows attackers to inject client-side scripts into web pages viewed by other users. Fix: Encode output and validate input.",
                "metadata": {"category": "vulnerability", "tags": "xss,web"}
            },
            {
                "id": "concept_recon",
                "document": "Reconnaissance is the first phase of an assessment. Passive recon gathers info without interacting directly. Active recon probes the target.",
                "metadata": {"category": "methodology", "tags": "recon,process"}
            }
        ]
        
        if self.lite_mode:
            self.local_tools.extend(tools)
            self.local_knowledge.extend(knowledge)
            self._save_lite_knowledge()
        else:
            for t in tools:
                self.tool_docs.add(documents=[t["document"]], metadatas=[t["metadata"]], ids=[t["id"]])
            for k in knowledge:
                self.security_knowledge.add(documents=[k["document"]], metadatas=[k["metadata"]], ids=[k["id"]])

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
