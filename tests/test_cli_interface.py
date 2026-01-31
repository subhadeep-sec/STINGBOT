import unittest
import sys
import os
from unittest.mock import patch, MagicMock
from io import StringIO

# Add paths for imports
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "agents", "python-brain"))


class TestCLIInterface(unittest.TestCase):
    """Test suite for CLI and interactive terminal interface."""

    def setUp(self):
        """Set up test environment."""
        self.test_dir = "/tmp/stingbot_test_cli"
        os.makedirs(self.test_dir, exist_ok=True)

    def test_cli_import(self):
        """Test that CLI module can be imported."""
        try:
            from interfaces.cli import cli, console
            self.assertIsNotNone(cli)
            self.assertIsNotNone(console)
        except ImportError as e:
            self.fail(f"Failed to import CLI module: {e}")

    def test_mas_terminal_import(self):
        """Test that MAS Terminal can be imported."""
        try:
            from interfaces.mas_terminal import MASTerminal
            self.assertIsNotNone(MASTerminal)
        except ImportError as e:
            self.fail(f"Failed to import MAS Terminal: {e}")

    @patch('orchestrator.supervisor.LLMAdapter')
    @patch('orchestrator.supervisor.Guardrails')
    @patch('orchestrator.supervisor.StateManager')
    def test_mas_terminal_initialization(self, mock_state, mock_guard, mock_llm):
        """Test that MAS Terminal initializes correctly."""
        from interfaces.mas_terminal import MASTerminal
        
        terminal = MASTerminal(self.test_dir)
        
        self.assertIsNotNone(terminal.supervisor)
        self.assertIsNotNone(terminal.workspace)
        self.assertEqual(terminal.workspace, self.test_dir)

    @patch('orchestrator.supervisor.LLMAdapter')
    @patch('orchestrator.supervisor.Guardrails')
    @patch('orchestrator.supervisor.StateManager')
    def test_agent_registration(self, mock_state, mock_guard, mock_llm):
        """Test that agents are registered in MAS Terminal."""
        from interfaces.mas_terminal import MASTerminal
        
        terminal = MASTerminal(self.test_dir)
        
        # Check that agents are registered
        expected_agents = ["web", "net", "rev", "critic", "reporter"]
        for agent_name in expected_agents:
            self.assertIn(
                agent_name,
                terminal.supervisor.agents,
                f"Agent '{agent_name}' not registered"
            )

    def test_cli_banner_function(self):
        """Test that CLI banner function exists and is callable."""
        try:
            from interfaces.cli import cli
            self.assertTrue(hasattr(cli, 'banner'))
            self.assertTrue(callable(cli.banner))
        except ImportError:
            self.skipTest("CLI module not available")

    def test_cli_log_function(self):
        """Test that CLI log function exists and is callable."""
        try:
            from interfaces.cli import cli
            self.assertTrue(hasattr(cli, 'log'))
            self.assertTrue(callable(cli.log))
        except ImportError:
            self.skipTest("CLI module not available")

    def test_cli_input_function(self):
        """Test that CLI input function exists and is callable."""
        try:
            from interfaces.cli import cli
            self.assertTrue(hasattr(cli, 'input'))
            self.assertTrue(callable(cli.input))
        except ImportError:
            self.skipTest("CLI module not available")

    @patch('orchestrator.supervisor.LLMAdapter')
    @patch('orchestrator.supervisor.Guardrails')
    @patch('orchestrator.supervisor.StateManager')
    def test_help_command(self, mock_state, mock_guard, mock_llm):
        """Test that help command is available."""
        from interfaces.mas_terminal import MASTerminal
        
        terminal = MASTerminal(self.test_dir)
        
        # Verify help method exists
        self.assertTrue(hasattr(terminal, '_show_help'))
        self.assertTrue(callable(terminal._show_help))

    def test_main_entry_point(self):
        """Test that main entry point exists."""
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        stingbot_py = os.path.join(base_dir, "stingbot.py")
        
        self.assertTrue(os.path.exists(stingbot_py))
        
        # Check that it has a main function
        with open(stingbot_py, 'r') as f:
            content = f.read()
            self.assertIn("def main()", content)
            self.assertIn("if __name__ == \"__main__\":", content)

    def test_command_line_mode(self):
        """Test that command line mode is supported."""
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        stingbot_py = os.path.join(base_dir, "stingbot.py")
        
        with open(stingbot_py, 'r') as f:
            content = f.read()
            # Should support command line arguments
            self.assertIn("sys.argv", content)
            self.assertIn("Supervisor", content)

    def test_interactive_mode(self):
        """Test that interactive mode is supported."""
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        stingbot_py = os.path.join(base_dir, "stingbot.py")
        
        with open(stingbot_py, 'r') as f:
            content = f.read()
            # Should support interactive terminal
            self.assertIn("MASTerminal", content)


if __name__ == '__main__':
    unittest.main()
