import pytest
import os
import shutil
import sys
import unittest.mock

# Add python-brain to path
sys.path.insert(0, os.path.join(os.getcwd(), 'agents', 'python-brain'))

from core.memory_system import MemorySystem
from datetime import datetime

class TestMemorySystem:
    @pytest.fixture
    def memory(self):
        test_dir = "./test_memory_sys"
        if os.path.exists(test_dir):
            shutil.rmtree(test_dir)
        
        with unittest.mock.patch('chromadb.PersistentClient') as mock_client, \
             unittest.mock.patch('chromadb.utils.embedding_functions.ONNXMiniLM_L6_V2'):
            
            # Setup mock collections
            mock_episodic = unittest.mock.MagicMock()
            mock_episodic.count.return_value = 1
            mock_episodic.query.return_value = {
                'documents': [['Test mission content']], 
                'metadatas': [[{'goal': 'Test SQL Injection'}]],
                'ids': [['id1']]
            }
            
            mock_semantic = unittest.mock.MagicMock()
            mock_semantic.count.return_value = 1
            mock_semantic.query.return_value = {
                'documents': [['Blind SQLi technique']], 
                'metadatas': [[{'technique': 'Blind SQLi'}]],
                'ids': [['id2']]
            }
            
            def get_coll(name, **kwargs):
                if name == "episodic_memory": return mock_episodic
                return mock_semantic
                
            mock_client.return_value.get_or_create_collection.side_effect = get_coll
            
            mem = MemorySystem(workspace_path=test_dir)
            yield mem
        
        if os.path.exists(test_dir):
            shutil.rmtree(test_dir)

    def test_store_and_retrieve_mission(self, memory):
        mission = {
            "goal": "Test SQL Injection",
            "actions": ["scan", "attack"],
            "outcome": "success",
            "learnings": "Found param vuln",
            "success": True
        }
        
        # Store
        mid = memory.store_mission(mission)
        assert mid is not None
        
        # Retrieve similar
        similar = memory.retrieve_similar_missions("SQL Injection", k=1)
        assert len(similar) == 1
        assert similar[0]['metadata']['goal'] == "Test SQL Injection"

    def test_learn_technique(self, memory):
        tid = memory.learn_technique(
            technique="Blind SQLi",
            context="Login page",
            success_rate=0.9
        )
        assert tid is not None
        
        # Retrieve relevant
        relevant = memory.retrieve_relevant_techniques("Login page", k=1)
        assert len(relevant) == 1
        assert relevant[0]['metadata']['technique'] == "Blind SQLi"
