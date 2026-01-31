import unittest
import sys
import os
import shutil
from unittest.mock import patch, MagicMock

# Add paths for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "agents", "python-brain"))


class TestEndToEnd(unittest.TestCase):
    """End-to-end integration tests for complete mission workflows."""

    def setUp(self):
        """Set up test environment."""
        self.test_dir = "/tmp/stingbot_test_e2e"
        os.makedirs(self.test_dir, exist_ok=True)

    def tearDown(self):
        """Clean up test environment."""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    @patch('orchestrator.supervisor.LLMAdapter')
    @patch('orchestrator.supervisor.Guardrails')
    @patch('orchestrator.supervisor.StateManager')
    @patch('orchestrator.supervisor.AUTONOMOUS_MODE', False)
    def test_complete_mission_workflow(self, mock_state, mock_guard, mock_llm):
        """Test complete mission from initialization to completion."""
        from orchestrator.supervisor import Supervisor
        from agents.web_pentester import WebPentester
        from agents.net_pentester import NetPentester
        from agents.reporter import ReporterAgent
        
        # Configure mocks
        mock_llm_instance = mock_llm.return_value
        mock_llm_instance.query.side_effect = [
            "1. Reconnaissance\\n2. Vulnerability Scan\\n3. Report",  # Decomposition
            "AGENT: net\\nTASK: Scan target network",  # First decision
            "AGENT: web\\nTASK: Test web vulnerabilities",  # Second decision
            "[COMPLETE] Mission objectives achieved"  # Completion
        ]
        
        mock_state_instance = mock_state.return_value
        mock_state_instance.export_summary.return_value = "Mission in progress"
        mock_state_instance.memory = {}
        mock_state_instance.add_edge.return_value = True
        
        mock_guard_instance = mock_guard.return_value
        mock_guard_instance.is_command_safe.return_value = (True, "Safe")
        mock_guard_instance.is_target_safe.return_value = (True, "Safe")
        
        # Initialize supervisor with agents
        supervisor = Supervisor(self.test_dir)
        supervisor.llm = mock_llm_instance
        supervisor.state = mock_state_instance
        supervisor.guard = mock_guard_instance
        
        supervisor.register_agent("web", WebPentester())
        supervisor.register_agent("net", NetPentester())
        supervisor.register_agent("reporter", ReporterAgent(self.test_dir))
        
        # Run mission
        result = supervisor.run_mission("Audit security of test-target.local")
        
        # Verify completion
        self.assertIn("[MISSION COMPLETE]", result)
        
        # Verify LLM was called
        self.assertTrue(mock_llm_instance.query.called)
        
        # Verify state was updated
        self.assertTrue(mock_state_instance.update_memory.called)

    @patch('orchestrator.supervisor.LLMAdapter')
    @patch('orchestrator.supervisor.Guardrails')
    @patch('orchestrator.supervisor.StateManager')
    @patch('orchestrator.supervisor.AUTONOMOUS_MODE', False)
    def test_multi_agent_coordination(self, mock_state, mock_guard, mock_llm):
        """Test coordination between multiple agents."""
        from orchestrator.supervisor import Supervisor
        from agents.web_pentester import WebPentester
        from agents.net_pentester import NetPentester
        from agents.critic import CriticAgent
        
        # Configure mocks for multi-agent scenario
        mock_llm_instance = mock_llm.return_value
        mock_llm_instance.query.side_effect = [
            "Multi-stage plan",  # Decomposition
            "AGENT: net\\nTASK: Initial scan",  # Net agent
            "AGENT: web\\nTASK: Web analysis",  # Web agent
            "AGENT: critic\\nTASK: Review findings",  # Critic agent
            "[COMPLETE] Analysis complete"  # Completion
        ]
        
        mock_state_instance = mock_state.return_value
        mock_state_instance.export_summary.return_value = "Multi-agent state"
        mock_state_instance.memory = {}
        mock_state_instance.add_edge.return_value = True
        
        supervisor = Supervisor(self.test_dir)
        supervisor.llm = mock_llm_instance
        supervisor.state = mock_state_instance
        
        # Register multiple agents
        supervisor.register_agent("web", WebPentester())
        supervisor.register_agent("net", NetPentester())
        supervisor.register_agent("critic", CriticAgent())
        
        result = supervisor.run_mission("Comprehensive security assessment")
        
        self.assertIn("[MISSION COMPLETE]", result)
        
        # Verify multiple agents were involved
        call_count = mock_state_instance.add_edge.call_count
        self.assertGreater(call_count, 0)

    @patch('orchestrator.supervisor.LLMAdapter')
    @patch('orchestrator.supervisor.Guardrails')
    @patch('orchestrator.supervisor.StateManager')
    @patch('orchestrator.supervisor.AUTONOMOUS_MODE', False)
    def test_error_recovery(self, mock_state, mock_guard, mock_llm):
        """Test error recovery and graceful degradation."""
        from orchestrator.supervisor import Supervisor
        from agents.web_pentester import WebPentester
        
        # Configure mocks with an error scenario
        mock_llm_instance = mock_llm.return_value
        mock_llm_instance.query.side_effect = [
            "Error recovery plan",  # Decomposition
            "AGENT: unknown\\nTASK: Invalid task",  # Unknown agent
            "AGENT: web\\nTASK: Fallback task",  # Recovery
            "[COMPLETE] Recovered"  # Completion
        ]
        
        mock_state_instance = mock_state.return_value
        mock_state_instance.export_summary.return_value = "Error state"
        mock_state_instance.memory = {}
        mock_state_instance.add_edge.return_value = True
        
        supervisor = Supervisor(self.test_dir)
        supervisor.llm = mock_llm_instance
        supervisor.state = mock_state_instance
        
        supervisor.register_agent("web", WebPentester())
        
        # Should handle unknown agent gracefully
        result = supervisor.run_mission("Test error recovery")
        
        self.assertIn("[MISSION COMPLETE]", result)

    @patch('orchestrator.supervisor.LLMAdapter')
    @patch('orchestrator.supervisor.Guardrails')
    @patch('orchestrator.supervisor.StateManager')
    @patch('orchestrator.supervisor.AUTONOMOUS_MODE', False)
    def test_state_persistence(self, mock_state, mock_guard, mock_llm):
        """Test that mission state is properly maintained."""
        from orchestrator.supervisor import Supervisor
        from agents.net_pentester import NetPentester
        
        mock_llm_instance = mock_llm.return_value
        mock_llm_instance.query.side_effect = [
            "State test plan",
            "AGENT: net\\nTASK: First task",
            "[COMPLETE] Done"
        ]
        
        mock_state_instance = mock_state.return_value
        mock_state_instance.export_summary.return_value = "State data"
        mock_state_instance.memory = {"test_key": "test_value"}
        mock_state_instance.add_edge.return_value = True
        
        supervisor = Supervisor(self.test_dir)
        supervisor.llm = mock_llm_instance
        supervisor.state = mock_state_instance
        
        supervisor.register_agent("net", NetPentester())
        
        supervisor.run_mission("Test state persistence")
        
        # Verify state operations were called
        self.assertTrue(mock_state_instance.update_memory.called)
        self.assertTrue(mock_state_instance.export_summary.called)

    @patch('orchestrator.supervisor.LLMAdapter')
    @patch('orchestrator.supervisor.Guardrails')
    @patch('orchestrator.supervisor.StateManager')
    @patch('orchestrator.supervisor.AUTONOMOUS_MODE', False)
    def test_max_turns_limit(self, mock_state, mock_guard, mock_llm):
        """Test that missions respect max turns limit."""
        from orchestrator.supervisor import Supervisor
        from agents.web_pentester import WebPentester
        
        # Configure LLM to never complete (testing max turns)
        mock_llm_instance = mock_llm.return_value
        mock_llm_instance.query.return_value = "AGENT: web\\nTASK: Continue"
        
        mock_state_instance = mock_state.return_value
        mock_state_instance.export_summary.return_value = "Ongoing"
        mock_state_instance.memory = {}
        mock_state_instance.add_edge.return_value = True
        
        supervisor = Supervisor(self.test_dir)
        supervisor.llm = mock_llm_instance
        supervisor.state = mock_state_instance
        
        supervisor.register_agent("web", WebPentester())
        
        # Mission should complete after max turns even without [COMPLETE]
        result = supervisor.run_mission("Long running mission")
        
        # Should still return a result
        self.assertIsNotNone(result)

    def test_demo_mission_script(self):
        """Test that demo mission script exists and is valid."""
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        demo_script = os.path.join(base_dir, "demo_mission.py")
        
        self.assertTrue(os.path.exists(demo_script))
        
        # Verify it's valid Python
        with open(demo_script, 'r') as f:
            content = f.read()
            compile(content, demo_script, 'exec')


if __name__ == '__main__':
    unittest.main()
