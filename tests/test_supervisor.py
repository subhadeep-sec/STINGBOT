import unittest
from unittest.mock import MagicMock, patch
from orchestrator.supervisor import Supervisor

class TestSupervisor(unittest.TestCase):
    def setUp(self):
        self.test_dir = "/tmp/stingbot_test_supervisor"
        # Properly mock dependencies to avoid side effects
        with patch('orchestrator.supervisor.LLMAdapter'), \
             patch('orchestrator.supervisor.Guardrails'), \
             patch('orchestrator.supervisor.StateManager'):
            self.sup = Supervisor(self.test_dir)

    def test_decomposition(self):
        # Mock the LLMAdapter instance's query method
        self.sup.llm.query.return_value = "1. Recon\n2. Vuln Scan"
        res = self.sup._decompose_goal("Test Goal")
        self.assertIn("Recon", res)

    def test_parse_decision(self):
        decision = "AGENT: web\nTASK: run nikto on target"
        agent, task = self.sup._parse_decision(decision)
        self.assertEqual(agent, "web")
        self.assertEqual(task, "run nikto on target")

    def test_mission_loop_completion(self):
        # Mock decomposition and then a [COMPLETE] decision
        self.sup.llm.query.side_effect = ["Plan: Stage 1", "[COMPLETE] Mission Met"]
        res = self.sup.run_mission("Short Mission")
        self.assertIn("[MISSION COMPLETE]", res)

    def test_multi_turn_mission(self):
        # Test mission with multiple turns
        self.sup.llm.query.side_effect = [
            "Plan: Multi-turn mission",
            "AGENT: web\nTASK: First task",
            "AGENT: net\nTASK: Second task",
            "[COMPLETE] Mission complete"
        ]
        res = self.sup.run_mission("Multi-turn Mission")
        self.assertIn("[MISSION COMPLETE]", res)

    def test_unknown_agent_handling(self):
        # Test handling of unknown agent names
        self.sup.llm.query.side_effect = [
            "Plan: Test unknown",
            "AGENT: unknown_agent\nTASK: Some task",
            "[COMPLETE] Done"
        ]
        # Should not crash with unknown agent
        res = self.sup.run_mission("Test Unknown Agent")
        self.assertIsNotNone(res)

if __name__ == '__main__':
    unittest.main()
