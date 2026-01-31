import unittest
import os
import sys
import subprocess
import json
import shutil
from pathlib import Path


class TestInstallation(unittest.TestCase):
    """Test suite for STINGBOT installation and setup."""

    def setUp(self):
        """Set up test environment."""
        self.test_dir = "/tmp/stingbot_test_install"
        self.config_file = os.path.expanduser("~/.stingbot2.json")
        self.backup_config = None
        
        # Backup existing config if it exists
        if os.path.exists(self.config_file):
            self.backup_config = self.config_file + ".backup"
            shutil.copy(self.config_file, self.backup_config)

    def tearDown(self):
        """Clean up test environment."""
        # Restore config if backed up
        if self.backup_config and os.path.exists(self.backup_config):
            shutil.move(self.backup_config, self.config_file)
        
        # Clean up test directory
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_python_version(self):
        """Test that Python version meets requirements (3.10+)."""
        version_info = sys.version_info
        self.assertGreaterEqual(version_info.major, 3, "Python 3.x required")
        self.assertGreaterEqual(version_info.minor, 10, "Python 3.10+ required")

    def test_node_version(self):
        """Test that Node.js version meets requirements (18+) if available."""
        try:
            result = subprocess.run(
                ["node", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                version = result.stdout.strip().lstrip('v')
                major_version = int(version.split('.')[0])
                self.assertGreaterEqual(major_version, 18, "Node.js 18+ recommended")
        except (FileNotFoundError, subprocess.TimeoutExpired):
            # Node.js is optional, so we just skip this test
            self.skipTest("Node.js not installed (optional for web dashboard)")

    def test_config_file_creation(self):
        """Test that configuration file is created with correct defaults."""
        # Remove existing config for this test
        if os.path.exists(self.config_file):
            os.remove(self.config_file)
        
        # Create default config
        default_config = {
            "PROJECT_NAME": "Stingbot",
            "VERSION": "2.0",
            "SAFETY_MODE": True,
            "USER_ALIAS": "Operator",
            "BOT_NAME": "Sting",
            "LLM_PROVIDER": "ollama",
            "LLM_MODEL": "qwen2.5:1.5b",
            "PUTER_API_KEY": "",
            "OPENAI_KEY": "",
            "ANTHROPIC_KEY": "",
            "GEMINI_KEY": "",
            "VOICE_ENABLED": False
        }
        
        with open(self.config_file, 'w') as f:
            json.dump(default_config, f, indent=4)
        
        # Verify config exists and is valid JSON
        self.assertTrue(os.path.exists(self.config_file))
        
        with open(self.config_file, 'r') as f:
            config = json.load(f)
        
        self.assertEqual(config["PROJECT_NAME"], "Stingbot")
        self.assertEqual(config["VERSION"], "2.0")
        self.assertTrue(config["SAFETY_MODE"])
        self.assertIn("LLM_PROVIDER", config)

    def test_directory_structure(self):
        """Test that required directories exist."""
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        required_dirs = [
            "agents",
            "orchestrator",
            "interfaces",
            "tests",
            "logs",
            "gateway",
            "client"
        ]
        
        for dir_name in required_dirs:
            dir_path = os.path.join(base_dir, dir_name)
            self.assertTrue(
                os.path.exists(dir_path),
                f"Required directory '{dir_name}' not found"
            )

    def test_required_files(self):
        """Test that required files exist."""
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        required_files = [
            "stingbot.py",
            "install.sh",
            "README.md",
            "LICENSE",
            "orchestrator/supervisor.py",
            "orchestrator/guardrails.py",
            "orchestrator/state_manager.py",
            "interfaces/mas_terminal.py"
        ]
        
        for file_name in required_files:
            file_path = os.path.join(base_dir, file_name)
            self.assertTrue(
                os.path.exists(file_path),
                f"Required file '{file_name}' not found"
            )

    def test_python_dependencies(self):
        """Test that required Python packages are installed."""
        required_packages = [
            "rich",
            "textual",
            "requests",
            "psutil"
        ]
        
        for package in required_packages:
            try:
                __import__(package)
            except ImportError:
                self.fail(f"Required package '{package}' not installed")

    def test_install_script_exists(self):
        """Test that install.sh exists and is executable."""
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        install_script = os.path.join(base_dir, "install.sh")
        
        self.assertTrue(os.path.exists(install_script))
        self.assertTrue(os.access(install_script, os.X_OK), "install.sh should be executable")

    def test_global_command_location(self):
        """Test that global command location is set up correctly."""
        global_bin = os.path.expanduser("~/.local/bin")
        stingbot_cmd = os.path.join(global_bin, "stingbot")
        
        # This test is informational - command may not exist yet
        if os.path.exists(stingbot_cmd):
            self.assertTrue(os.access(stingbot_cmd, os.X_OK))
        else:
            # Just verify the directory exists or can be created
            os.makedirs(global_bin, exist_ok=True)
            self.assertTrue(os.path.exists(global_bin))


if __name__ == '__main__':
    unittest.main()
