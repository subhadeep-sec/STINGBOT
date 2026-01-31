import pytest
import os
import shutil
import sys
import unittest.mock

# Add python-brain to path
sys.path.insert(0, os.path.join(os.getcwd(), 'agents', 'python-brain'))

from core.knowledge_base import KnowledgeBase

class TestKnowledgeBase:
    @pytest.fixture
    def kb(self):
        test_dir = "./test_kb_sys"
        if os.path.exists(test_dir):
            shutil.rmtree(test_dir)
            
        with unittest.mock.patch('chromadb.PersistentClient') as mock_client, \
             unittest.mock.patch('chromadb.utils.embedding_functions.ONNXMiniLM_L6_V2'):
             
            # Setup mock collections
            mock_kb = unittest.mock.MagicMock()
            mock_kb.count.return_value = 3
            mock_kb.query.return_value = {
                'documents': [['SQL Injection (SQLi) occurs when... Custom Exploit X is dangerous']], 
                'metadatas': [[{'category': 'general'}]]
            }
            
            mock_tools = unittest.mock.MagicMock()
            mock_tools.count.return_value = 2
            mock_tools.query.return_value = {
                'documents': [['Nmap is a network scanner. Usage: nmap -sV -sC <target>.']], 
                'metadatas': [[{'tool_name': 'nmap', 'category': 'recon'}]]
            }
            
            def get_coll(name, **kwargs):
                if name == "security_knowledge": return mock_kb
                return mock_tools
                
            mock_client.return_value.get_or_create_collection.side_effect = get_coll
            
            base = KnowledgeBase(workspace_path=test_dir)
            yield base
        
        if os.path.exists(test_dir):
            shutil.rmtree(test_dir)

    def test_seed_knowledge(self, kb):
        # Should have seeded knowledge
        results = kb.query_knowledge("What is SQL Injection?")
        assert len(results) > 0
        assert "SQL Injection (SQLi) occurs" in results[0]

    def test_tool_usage(self, kb):
        nmap = kb.get_tool_usage("nmap")
        assert nmap is not None
        assert "Nmap is a network scanner" in nmap['description']

    def test_add_custom_knowledge(self, kb):
        kb.add_knowledge(
            content="Custom Exploit X is dangerous",
            category="exploit",
            tags=["custom", "dangerous"]
        )
        
        results = kb.query_knowledge("Custom Exploit")
        assert len(results) > 0
        assert "Custom Exploit X" in results[0]
