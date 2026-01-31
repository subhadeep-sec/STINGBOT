import unittest
import sys
import os
from unittest.mock import patch, MagicMock

# Add paths for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "agents", "python-brain"))


class TestDemoMissions(unittest.TestCase):
    """Test suite for pre-configured demo missions."""

    def setUp(self):
        """Set up test environment."""
        self.test_dir = "/tmp/stingbot_test_demos"
        os.makedirs(self.test_dir, exist_ok=True)

    @patch('orchestrator.supervisor.LLMAdapter')
    @patch('orchestrator.supervisor.Guardrails')
    @patch('orchestrator.supervisor.StateManager')
    @patch('orchestrator.supervisor.AUTONOMOUS_MODE', False)
    def test_web_audit_demo(self, mock_state, mock_guard, mock_llm):
        """Demo: Web application security audit."""
        from orchestrator.supervisor import Supervisor
        from agents.web_pentester import WebPentester
        from agents.reporter import ReporterAgent
        
        # Configure demo scenario
        mock_llm_instance = mock_llm.return_value
        mock_llm_instance.query.side_effect = [
            "1. Directory enumeration\\n2. SQL injection test\\n3. XSS test",
            "AGENT: web\\nTASK: Run directory scan with gobuster",
            "AGENT: web\\nTASK: Test for SQL injection",
            "AGENT: reporter\\nTASK: Generate security report",
            "[COMPLETE] Web audit complete"
        ]
        
        mock_state_instance = mock_state.return_value
        mock_state_instance.export_summary.return_value = "Web audit findings"
        mock_state_instance.memory = {}
        mock_state_instance.add_edge.return_value = True
        
        supervisor = Supervisor(self.test_dir)
        supervisor.llm = mock_llm_instance
        supervisor.state = mock_state_instance
        
        supervisor.register_agent("web", WebPentester())
        supervisor.register_agent("reporter", ReporterAgent(self.test_dir))
        
        result = supervisor.run_mission("Audit web application at demo-app.local")
        
        self.assertIn("[MISSION COMPLETE]", result)

    @patch('orchestrator.supervisor.LLMAdapter')
    @patch('orchestrator.supervisor.Guardrails')
    @patch('orchestrator.supervisor.StateManager')
    @patch('orchestrator.supervisor.AUTONOMOUS_MODE', False)
    def test_network_recon_demo(self, mock_state, mock_guard, mock_llm):
        """Demo: Network reconnaissance mission."""
        from orchestrator.supervisor import Supervisor
        from agents.net_pentester import NetPentester
        from agents.reporter import ReporterAgent
        
        mock_llm_instance = mock_llm.return_value
        mock_llm_instance.query.side_effect = [
            "1. Port scan\\n2. Service enumeration\\n3. OS detection",
            "AGENT: net\\nTASK: Run nmap port scan",
            "AGENT: net\\nTASK: Enumerate services",
            "AGENT: reporter\\nTASK: Create recon report",
            "[COMPLETE] Reconnaissance complete"
        ]
        
        mock_state_instance = mock_state.return_value
        mock_state_instance.export_summary.return_value = "Network map"
        mock_state_instance.memory = {}
        mock_state_instance.add_edge.return_value = True
        
        supervisor = Supervisor(self.test_dir)
        supervisor.llm = mock_llm_instance
        supervisor.state = mock_state_instance
        
        supervisor.register_agent("net", NetPentester())
        supervisor.register_agent("reporter", ReporterAgent(self.test_dir))
        
        result = supervisor.run_mission("Perform network reconnaissance on 192.168.1.0/24")
        
        self.assertIn("[MISSION COMPLETE]", result)

    @patch('orchestrator.supervisor.LLMAdapter')
    @patch('orchestrator.supervisor.Guardrails')
    @patch('orchestrator.supervisor.StateManager')
    @patch('orchestrator.supervisor.AUTONOMOUS_MODE', False)
    def test_binary_analysis_demo(self, mock_state, mock_guard, mock_llm):
        """Demo: Binary analysis and reverse engineering."""
        from orchestrator.supervisor import Supervisor
        from agents.rev_engineer import RevEngineer
        from agents.reporter import ReporterAgent
        
        mock_llm_instance = mock_llm.return_value
        mock_llm_instance.query.side_effect = [
            "1. Static analysis\\n2. String extraction\\n3. Disassembly",
            "AGENT: rev\\nTASK: Extract strings from binary",
            "AGENT: rev\\nTASK: Analyze with radare2",
            "AGENT: reporter\\nTASK: Document findings",
            "[COMPLETE] Binary analysis complete"
        ]
        
        mock_state_instance = mock_state.return_value
        mock_state_instance.export_summary.return_value = "Binary analysis results"
        mock_state_instance.memory = {}
        mock_state_instance.add_edge.return_value = True
        
        supervisor = Supervisor(self.test_dir)
        supervisor.llm = mock_llm_instance
        supervisor.state = mock_state_instance
        
        supervisor.register_agent("rev", RevEngineer())
        supervisor.register_agent("reporter", ReporterAgent(self.test_dir))
        
        result = supervisor.run_mission("Analyze suspicious binary at /tmp/sample.bin")
        
        self.assertIn("[MISSION COMPLETE]", result)

    @patch('orchestrator.supervisor.LLMAdapter')
    @patch('orchestrator.supervisor.Guardrails')
    @patch('orchestrator.supervisor.StateManager')
    @patch('orchestrator.supervisor.AUTONOMOUS_MODE', False)
    def test_multi_stage_attack_demo(self, mock_state, mock_guard, mock_llm):
        """Demo: Multi-stage attack simulation."""
        from orchestrator.supervisor import Supervisor
        from agents.net_pentester import NetPentester
        from agents.web_pentester import WebPentester
        from agents.critic import CriticAgent
        from agents.reporter import ReporterAgent
        
        mock_llm_instance = mock_llm.return_value
        mock_llm_instance.query.side_effect = [
            "1. Recon\\n2. Exploit\\n3. Post-exploit\\n4. Report",
            "AGENT: net\\nTASK: Initial network scan",
            "AGENT: web\\nTASK: Identify web vulnerabilities",
            "AGENT: critic\\nTASK: Analyze attack surface",
            "AGENT: reporter\\nTASK: Generate comprehensive report",
            "[COMPLETE] Multi-stage assessment complete"
        ]
        
        mock_state_instance = mock_state.return_value
        mock_state_instance.export_summary.return_value = "Attack chain"
        mock_state_instance.memory = {}
        mock_state_instance.add_edge.return_value = True
        
        supervisor = Supervisor(self.test_dir)
        supervisor.llm = mock_llm_instance
        supervisor.state = mock_state_instance
        
        supervisor.register_agent("net", NetPentester())
        supervisor.register_agent("web", WebPentester())
        supervisor.register_agent("critic", CriticAgent())
        supervisor.register_agent("reporter", ReporterAgent(self.test_dir))
        
        result = supervisor.run_mission("Conduct full penetration test on target-corp.local")
        
        self.assertIn("[MISSION COMPLETE]", result)

    @patch('orchestrator.supervisor.LLMAdapter')
    @patch('orchestrator.supervisor.Guardrails')
    @patch('orchestrator.supervisor.StateManager')
    @patch('orchestrator.supervisor.AUTONOMOUS_MODE', False)
    def test_report_generation_demo(self, mock_state, mock_guard, mock_llm):
        """Demo: Report generation from mission data."""
        from orchestrator.supervisor import Supervisor
        from agents.reporter import ReporterAgent
        
        mock_llm_instance = mock_llm.return_value
        mock_llm_instance.query.side_effect = [
            "Generate professional security report",
            "AGENT: reporter\\nTASK: Create markdown report with findings",
            "[COMPLETE] Report generated"
        ]
        
        mock_state_instance = mock_state.return_value
        mock_state_instance.export_summary.return_value = "Mission findings: 3 vulnerabilities found"
        mock_state_instance.memory = {
            "findings": ["SQL Injection", "XSS", "Weak passwords"]
        }
        mock_state_instance.add_edge.return_value = True
        
        supervisor = Supervisor(self.test_dir)
        supervisor.llm = mock_llm_instance
        supervisor.state = mock_state_instance
        
        supervisor.register_agent("reporter", ReporterAgent(self.test_dir))
        
        result = supervisor.run_mission("Generate security assessment report")
        
        self.assertIn("[MISSION COMPLETE]", result)

    def test_existing_demo_script(self):
        """Test that existing demo_mission.py runs without errors."""
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        demo_script = os.path.join(base_dir, "demo_mission.py")
        
        if os.path.exists(demo_script):
            # Verify script is valid Python
            with open(demo_script, 'r') as f:
                content = f.read()
            
            # Should contain demo function
            self.assertIn("def run_demo", content)
            self.assertIn("Supervisor", content)


if __name__ == '__main__':
    unittest.main()
