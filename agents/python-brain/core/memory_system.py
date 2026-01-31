"""
Advanced Memory System for Autonomous AI Agent

Provides episodic, semantic, and working memory.
Supports ChromaDB vector storage with a JSON fallback for lite mode.
"""

try:
    import chromadb
    from chromadb.config import Settings
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False
    print("[Memory] ChromaDB not available - switching to Lite Mode (JSON)")

import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
import hashlib


class MemorySystem:
    """
    Multi-layered memory system for autonomous learning.
    
    Components:
    - Episodic Memory: Complete mission experiences with outcomes
    - Semantic Memory: Learned concepts, techniques, and patterns
    - Working Memory: Current mission context and state
    """
    
    def __init__(self, workspace_path: str = "./memory"):
        """Initialize memory system with persistent storage."""
        self.workspace_path = workspace_path
        os.makedirs(workspace_path, exist_ok=True)
        self.lite_mode = not CHROMADB_AVAILABLE
        
        if not self.lite_mode:
            try:
                # Initialize ChromaDB client
                self.client = chromadb.PersistentClient(
                    path=os.path.join(workspace_path, "chroma_db"),
                    settings=Settings(anonymized_telemetry=False)
                )
                
                # Create collections
                self.episodic_memory = self.client.get_or_create_collection(
                    name="episodic_memory",
                    metadata={"description": "Mission experiences and outcomes"}
                )
                
                self.semantic_memory = self.client.get_or_create_collection(
                    name="semantic_memory",
                    metadata={"description": "Learned techniques and concepts"}
                )
            except Exception as e:
                print(f"[Memory] Failed to init ChromaDB: {e}. Switching to Lite Mode.")
                self.lite_mode = True
        
        if self.lite_mode:
            self.episodic_file = os.path.join(workspace_path, "episodic.json")
            self.semantic_file = os.path.join(workspace_path, "semantic.json")
            self._load_lite_memory()

        # Working memory (in-memory, not persisted)
        self.working_memory = {
            "current_mission": None,
            "context": {},
            "recent_actions": []
        }
        
        count_e = len(self.local_episodic) if self.lite_mode else self.episodic_memory.count()
        count_s = len(self.local_semantic) if self.lite_mode else self.semantic_memory.count()
        print(f"[Memory] Initialized with {count_e} episodic and {count_s} semantic memories ({'LITE' if self.lite_mode else 'VECTOR'})")
    
    def _load_lite_memory(self):
        """Load memory from JSON files for lite mode."""
        self.local_episodic = []
        self.local_semantic = []
        
        if os.path.exists(self.episodic_file):
            try:
                with open(self.episodic_file, 'r') as f:
                    self.local_episodic = json.load(f)
            except: pass
            
        if os.path.exists(self.semantic_file):
            try:
                with open(self.semantic_file, 'r') as f:
                    self.local_semantic = json.load(f)
            except: pass
    
    def _save_lite_memory(self):
        """Save memory to JSON files."""
        with open(self.episodic_file, 'w') as f:
            json.dump(self.local_episodic, f, indent=2)
        with open(self.semantic_file, 'w') as f:
            json.dump(self.local_semantic, f, indent=2)
            
    def store_mission(self, mission_data: Dict[str, Any]) -> str:
        """Store a complete mission as episodic memory."""
        mission_id = self._generate_id(mission_data.get("goal", "") + str(datetime.now()))
        
        entry = {
            "id": mission_id,
            "document": f"Mission: {mission_data.get('goal')}...",
            "metadata": {
                "mission_id": mission_id,
                "goal": mission_data.get("goal", ""),
                "outcome": mission_data.get("outcome", ""),
                "timestamp": mission_data.get("timestamp", datetime.now().isoformat()),
                "success": str(mission_data.get("success", False))
            }
        }

        if self.lite_mode:
            self.local_episodic.append(entry)
            self._save_lite_memory()
        else:
            self.episodic_memory.add(
                documents=[entry["document"]],
                metadatas=[entry["metadata"]],
                ids=[mission_id]
            )
        
        print(f"[Memory] Stored mission: {mission_id[:8]}...")
        return mission_id
    
    def learn_technique(self, technique: str, context: str, success_rate: float, metadata: Dict = None) -> str:
        """Store a learned technique."""
        technique_id = self._generate_id(technique + context)
        
        meta = metadata or {}
        meta.update({
            "technique_id": technique_id,
            "technique": technique,
            "success_rate": str(success_rate),
            "timestamp": datetime.now().isoformat()
        })
        
        entry = {
            "id": technique_id,
            "document": f"Technique: {technique}\nContext: {context}",
            "metadata": meta
        }
        
        if self.lite_mode:
            self.local_semantic.append(entry)
            self._save_lite_memory()
        else:
            self.semantic_memory.add(
                documents=[entry["document"]],
                metadatas=[entry["metadata"]],
                ids=[technique_id]
            )
        
        return technique_id
    
    def retrieve_similar_missions(self, query: str, k: int = 5) -> List[Dict]:
        """Retrieve similar past missions."""
        if self.lite_mode:
            # Simple keyword matching for lite mode
            results = []
            query_terms = query.lower().split()
            for item in self.local_episodic:
                score = 0
                content = (item['metadata']['goal'] + " " + item['document']).lower()
                for term in query_terms:
                    if term in content:
                        score += 1
                if score > 0:
                    results.append({
                        "content": item['document'],
                        "metadata": item['metadata'],
                        "score": score
                    })
            
            # Sort by score
            results.sort(key=lambda x: x['score'], reverse=True)
            return results[:k]
            
        else:
            # Vector search
            count = self.episodic_memory.count()
            if count == 0:
                return []
                
            results = self.episodic_memory.query(
                query_texts=[query],
                n_results=min(k, count)
            )
            if not results or not results['documents'][0]:
                return []
            
            output = []
            for i, doc in enumerate(results['documents'][0]):
                output.append({
                    "content": doc,
                    "metadata": results['metadatas'][0][i]
                })
            return output
    
    def retrieve_relevant_techniques(self, context: str, k: int = 3) -> List[Dict]:
        """Retrieve relevant techniques."""
        if self.lite_mode:
            results = []
            context_lower = context.lower()
            for item in self.local_semantic:
                if item['metadata']['technique'].lower() in context_lower or \
                   context_lower in item['document'].lower():
                    results.append({
                        "content": item['document'],
                        "metadata": item['metadata']
                    })
            return results[:k]
        else:
            if self.semantic_memory.count() == 0: return []
            results = self.semantic_memory.query(
                query_texts=[context],
                n_results=min(k, self.semantic_memory.count())
            )
            if not results or not results['documents'][0]: return []
            output = []
            for i, doc in enumerate(results['documents'][0]):
                output.append({
                    "content": doc,
                    "metadata": results['metadatas'][0][i]
                })
            return output

    def update_working_memory(self, key: str, value: Any):
        self.working_memory[key] = value
    
    def get_working_memory(self, key: str = None) -> Any:
        if key: return self.working_memory.get(key)
        return self.working_memory
        
    def get_memory_stats(self) -> Dict[str, Any]:
        if self.lite_mode:
            return {
                "episodic_count": len(self.local_episodic),
                "semantic_count": len(self.local_semantic),
                "total_memories": len(self.local_episodic) + len(self.local_semantic)
            }
        else:
            return {
                "episodic_count": self.episodic_memory.count(),
                "semantic_count": self.semantic_memory.count(),
                "total_memories": self.episodic_memory.count() + self.semantic_memory.count()
            }

    def _generate_id(self, content: str) -> str:
        return hashlib.md5(content.encode()).hexdigest()
