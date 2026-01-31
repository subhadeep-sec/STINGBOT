import unittest
import sys
import os
from unittest.mock import patch, MagicMock

# Add paths for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "agents", "python-brain"))


class TestAgentsIntegration(unittest.TestCase):
    """Integration tests for multi-agent system."""

    def setUp(self):
        """Set up test environment."""
        self.test_dir = "/tmp/stingbot_test_agents"
        os.makedirs(self.test_dir, exist_ok=True)

    @patch('orchestrator.supervisor.LLMAdapter')
    @patch('orchestrator.supervisor.Guardrails')
    @patch('orchestrator.supervisor.StateManager')
    def test_supervisor_initialization(self, mock_state, mock_guard, mock_llm):
        """Test that Supervisor initializes correctly."""
        from orchestrator.supervisor import Supervisor
        
        supervisor = Supervisor(self.test_dir)
        
        self.assertIsNotNone(supervisor)
        self.assertIsNotNone(supervisor.agents)
        self.assertEqual(len(supervisor.agents), 0)  # No agents registered yet

    @patch('orchestrator.supervisor.LLMAdapter')
    @patch('orchestrator.supervisor.Guardrails')
    @patch('orchestrator.supervisor.StateManager')
    def test_agent_registration(self, mock_state, mock_guard, mock_llm):
        """Test agent registration."""
        from orchestrator.supervisor import Supervisor
        from agents.web_pentester import WebPentester
        from agents.net_pentester import NetPentester
        
        supervisor = Supervisor(self.test_dir)
        
        # Register agents
        supervisor.register_agent("web", WebPentester())
        supervisor.register_agent("net", NetPentester())
        
        self.assertEqual(len(supervisor.agents), 2)
        self.assertIn("web", supervisor.agents)
        self.assertIn("net", supervisor.agents)

    @patch('orchestrator.supervisor.LLMAdapter')
    @patch('orchestrator.supervisor.Guardrails')
    @patch('orchestrator.supervisor.StateManager')
    def test_all_agents_registration(self, mock_state, mock_guard, mock_llm):
        """Test that all agents can be registered."""
        from orchestrator.supervisor import Supervisor
        from agents.web_pentester import WebPentester
        from agents.net_pentester import NetPentester
        from agents.rev_engineer import RevEngineer
        from agents.critic import CriticAgent
        from agents.reporter import ReporterAgent
        
        supervisor = Supervisor(self.test_dir)
        
        # Register all agents
        supervisor.register_agent("web", WebPentester())
        supervisor.register_agent("net", NetPentester())
        supervisor.register_agent("rev", RevEngineer())
        supervisor.register_agent("critic", CriticAgent())
        supervisor.register_agent("reporter", ReporterAgent(self.test_dir))
        
        self.assertEqual(len(supervisor.agents), 5)
        
        expected_agents = ["web", "net", "rev", "critic", "reporter"]
        for agent_name in expected_agents:
            self.assertIn(agent_name, supervisor.agents)

    def test_web_pentester_import(self):
        """Test that WebPentester can be imported and initialized."""
        from agents.web_pentester import WebPentester
        
        agent = WebPentester()
        self.assertIsNotNone(agent)
        self.assertTrue(hasattr(agent, 'execute'))

    def test_net_pentester_import(self):
        """Test that NetPentester can be imported and initialized."""
        from agents.net_pentester import NetPentester
        
        agent = NetPentester()
        self.assertIsNotNone(agent)
        self.assertTrue(hasattr(agent, 'execute'))

    def test_rev_engineer_import(self):
        """Test that RevEngineer can be imported and initialized."""
        from agents.rev_engineer import RevEngineer
        
        agent = RevEngineer()
        self.assertIsNotNone(agent)
        self.assertTrue(hasattr(agent, 'execute'))

    def test_critic_agent_import(self):
        """Test that CriticAgent can be imported and initialized."""
        from agents.critic import CriticAgent
        
        agent = CriticAgent()
        self.assertIsNotNone(agent)
        self.assertTrue(hasattr(agent, 'execute'))

    def test_reporter_agent_import(self):
        """Test that ReporterAgent can be imported and initialized."""
        from agents.reporter import ReporterAgent
        
        agent = ReporterAgent(self.test_dir)
        self.assertIsNotNone(agent)
        self.assertTrue(hasattr(agent, 'execute'))

    @patch('orchestrator.supervisor.LLMAdapter')
    @patch('orchestrator.supervisor.Guardrails')
    @patch('orchestrator.supervisor.StateManager')
    def test_fuzzy_agent_matching(self, mock_state, mock_guard, mock_llm):
        """Test fuzzy agent name matching."""
        from orchestrator.supervisor import Supervisor
        from agents.web_pentester import WebPentester
        from agents.net_pentester import NetPentester
        
        supervisor = Supervisor(self.test_dir)
        supervisor.register_agent("web", WebPentester())
        supervisor.register_agent("net", NetPentester())
        
        # Test exact match
        self.assertEqual(supervisor._fuzzy_match_agent("web"), "web")
        
        # Test alias matching
        self.assertEqual(supervisor._fuzzy_match_agent("network"), "net")
        self.assertEqual(supervisor._fuzzy_match_agent("webapp"), "web")
        
        # Test unknown agent
        self.assertIsNone(supervisor._fuzzy_match_agent("unknown_agent"))

    @patch('orchestrator.supervisor.LLMAdapter')
    @patch('orchestrator.supervisor.Guardrails')
    @patch('orchestrator.supervisor.StateManager')
    def test_mission_decomposition(self, mock_state, mock_guard, mock_llm):
        """Test mission goal decomposition."""
        from orchestrator.supervisor import Supervisor
        
        # Configure mock LLM
        mock_llm_instance = mock_llm.return_value
        mock_llm_instance.query.return_value = "1. Recon 2. Scan 3. Exploit"
        
        supervisor = Supervisor(self.test_dir)
        supervisor.llm = mock_llm_instance
        
        plan = supervisor._decompose_goal("Test mission")
        
        self.assertIsNotNone(plan)
        self.assertIn("Recon", plan)
        self.assertIn("Scan", plan)

    @patch('orchestrator.supervisor.LLMAdapter')
    @patch('orchestrator.supervisor.Guardrails')
    @patch('orchestrator.supervisor.StateManager')
    def test_decision_parsing(self, mock_state, mock_guard, mock_llm):
        """Test parsing of LLM decisions."""
        from orchestrator.supervisor import Supervisor
        
        supervisor = Supervisor(self.test_dir)
        
        # Test valid decision - using actual newlines
        decision = "AGENT: web" + chr(10) + "TASK: scan the target"
        agent, task = supervisor._parse_decision(decision)
        
        self.assertEqual(agent, "web")
        self.assertEqual(task, "scan the target")
        
        # Test decision with extra content
        decision2 = "Some preamble" + chr(10) + "AGENT: net" + chr(10) + "TASK: enumerate ports" + chr(10) + "Some conclusion"
        agent2, task2 = supervisor._parse_decision(decision2)
        
        self.assertEqual(agent2, "net")
        self.assertEqual(task2, "enumerate ports")

    @patch('orchestrator.supervisor.LLMAdapter')
    @patch('orchestrator.supervisor.Guardrails')
    @patch('orchestrator.supervisor.StateManager')
    def test_mission_execution_with_completion(self, mock_state, mock_guard, mock_llm):
        """Test mission execution that completes successfully."""
        from orchestrator.supervisor import Supervisor
        from agents.web_pentester import WebPentester
        
        # Configure mocks
        mock_llm_instance = mock_llm.return_value
        mock_llm_instance.query.side_effect = [
            "1. Initial plan",  # Decomposition
            "[COMPLETE] Mission achieved"  # First decision completes
        ]
        
        mock_state_instance = mock_state.return_value
        mock_state_instance.export_summary.return_value = "Empty state"
        mock_state_instance.memory = {}
        
        supervisor = Supervisor(self.test_dir)
        supervisor.llm = mock_llm_instance
        supervisor.state = mock_state_instance
        supervisor.register_agent("web", WebPentester())
        
        result = supervisor.run_mission("Test goal")
        
        self.assertIn("[MISSION COMPLETE]", result)


if __name__ == '__main__':
    unittest.main()
