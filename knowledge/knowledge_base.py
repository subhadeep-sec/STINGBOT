import chromadb
import os

class KnowledgeBase:
    """Long-term memory using ChromaDB for RAG-based exploit retrieval."""
    
    def __init__(self, db_path):
        self.client = chromadb.PersistentClient(path=db_path)
        self.exploit_collection = self.client.get_or_create_collection("exploits")
        self.cve_collection = self.client.get_or_create_collection("cves")

    def store_exploit(self, pattern, description, success_metadata=None):
        """Store a successful exploit pattern."""
        self.exploit_collection.add(
            documents=[pattern],
            metadatas=[success_metadata or {}],
            ids=[f"exploit_{hash(pattern)}"]
        )

    def search_exploit(self, query, n_results=3):
        """Find similar past exploits."""
        try:
            return self.exploit_collection.query(
                query_texts=[query],
                n_results=n_results
            )
        except:
            return []

    def store_cve(self, cve_id, description):
        self.cve_collection.add(
            documents=[description],
            ids=[cve_id]
        )

    def search_cve(self, query):
        return self.cve_collection.query(
            query_texts=[query],
            n_results=1
        )
