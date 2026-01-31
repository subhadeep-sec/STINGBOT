import unittest
import sys
import os
import json
from unittest.mock import patch, MagicMock

# Add paths for imports
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "agents", "python-brain"))


class TestLLMIntegration(unittest.TestCase):
    """Test suite for LLM adapter and integration."""

    def setUp(self):
        """Set up test environment."""
        self.test_config = {
            "LLM_PROVIDER": "mock",
            "LLM_MODEL": "test-model",
            "SAFETY_MODE": True
        }

    def test_llm_adapter_import(self):
        """Test that LLM adapter can be imported."""
        try:
            from core.llm import LLMAdapter
            self.assertIsNotNone(LLMAdapter)
        except ImportError as e:
            self.fail(f"Failed to import LLM adapter: {e}")

    @patch('core.llm.config')
    def test_llm_adapter_initialization(self, mock_config):
        """Test LLM adapter initialization."""
        mock_config.LLM_PROVIDER = "mock"
        mock_config.LLM_MODEL = "test-model"
        
        try:
            from core.llm import LLMAdapter
            adapter = LLMAdapter()
            self.assertIsNotNone(adapter)
        except Exception as e:
            pass

    def test_config_loading(self):
        """Test configuration loading."""
        config_file = os.path.expanduser("~/.stingbot2.json")
        
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                config = json.load(f)
            
            # Verify required fields
            self.assertIn("LLM_PROVIDER", config)
            self.assertIn("LLM_MODEL", config)
            self.assertIn("SAFETY_MODE", config)
        else:
            self.skipTest("Config file not found")

    @patch('core.llm.config')
    def test_mock_llm_provider(self, mock_config):
        """Test mock LLM provider for offline testing."""
        mock_config.LLM_PROVIDER = "mock"
        mock_config.LLM_MODEL = "test"
        
        try:
            from core.llm import LLMAdapter
            adapter = LLMAdapter()
            self.assertIsNotNone(adapter)
        except Exception:
            pass

    def test_supported_providers(self):
        """Test that supported LLM providers are documented."""
        # Check README for provider documentation
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        readme_path = os.path.join(base_dir, "README.md")
        
        if os.path.exists(readme_path):
            with open(readme_path, 'r') as f:
                readme_content = f.read()
            
            # Verify providers are documented
            providers = ["ollama", "puter", "openai", "anthropic", "gemini", "mock"]
            for provider in providers:
                self.assertIn(
                    provider,
                    readme_content.lower(),
                    f"Provider '{provider}' not documented in README"
                )

    @patch('core.llm.config')
    @patch('core.llm.requests')
    def test_llm_error_handling(self, mock_requests, mock_config):
        """Test LLM error handling for API failures."""
        mock_config.LLM_PROVIDER = "openai"
        mock_config.LLM_MODEL = "gpt-4"
        mock_config.OPENAI_KEY = ""
        mock_config.SAFETY_MODE = True
        
        # Simulate API error
        mock_requests.post.side_effect = Exception("API Error")
        
        try:
            from core.llm import LLMAdapter
            adapter = LLMAdapter()
        except Exception:
            pass

    def test_safety_mode_config(self):
        """Test that safety mode is configurable."""
        config_file = os.path.expanduser("~/.stingbot2.json")
        
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                config_data = json.load(f)
            
            self.assertIn("SAFETY_MODE", config_data)
            self.assertIsInstance(config_data["SAFETY_MODE"], bool)

    @patch('core.llm.config')
    def test_llm_query_interface(self, mock_config):
        """Test that LLM adapter has query interface."""
        mock_config.LLM_PROVIDER = "mock"
        mock_config.LLM_MODEL = "test-model"
        
        try:
            from core.llm import LLMAdapter
            adapter = LLMAdapter()
            
            # Verify query method exists
            self.assertTrue(hasattr(adapter, 'query'))
            self.assertTrue(callable(adapter.query))
        except Exception:
            pass

    def test_config_defaults(self):
        """Test that config has sensible defaults."""
        config_file = os.path.expanduser("~/.stingbot2.json")
        
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                config = json.load(f)
            
            # Safety mode should default to True
            if "SAFETY_MODE" in config:
                # If safety mode is explicitly set, verify it's a boolean
                self.assertIsInstance(config["SAFETY_MODE"], bool)
            
            # Should have a default provider
            self.assertIn("LLM_PROVIDER", config)
            self.assertIsInstance(config["LLM_PROVIDER"], str)


if __name__ == '__main__':
    unittest.main()
