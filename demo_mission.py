import sys
import os
from unittest.mock import MagicMock, patch

# Add necessary paths
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "agents/python-brain"))

from orchestrator.supervisor import Supervisor
from agents.web_pentester import WebPentester
from agents.net_pentester import NetPentester

def run_demo():
    print("🦂 STINGBOT MAS DEMO MODE")
    print("------------------------")
    
    # Mocking dependencies for the demo
    with patch('orchestrator.supervisor.LLMAdapter') as MockLLM:
        # Configure Mock LLM responses
        mock_llm_inst = MockLLM.return_value
        mock_llm_inst.query.side_effect = [
            # 1. Decomposition response
            "1. Recon (Network)\n2. Vulnerability Audit (Web)\n3. Exploitation",
            # 2. First decision
            "AGENT: net\nTASK: run nmap -sV target.com",
            # 3. Completion
            "[COMPLETE] Mission Objective Achieved."
        ]
        
        supervisor = Supervisor("/tmp/stingbot_demo")
        supervisor.register_agent("web", WebPentester())
        supervisor.register_agent("net", NetPentester())
        
        goal = "Audit the security of company-internal-target.com"
        print(f"User Goal: {goal}\n")
        
        # Step 1: Decomposition
        print("[Supervisor] Decomposing goal...")
        plan = supervisor._decompose_goal(goal)
        print(f"Generated Plan:\n{plan}\n")
        
        # Step 2: Routing simulation
        print("[Supervisor] Routing first task...")
        decision = supervisor.llm.query("What next?")
        agent_name, task = supervisor._parse_decision(decision)
        print(f"Assigned Agent: {agent_name}")
        print(f"Assigned Task: {task}\n")
        
        if agent_name in ["net", "web"]:
             print(f"[{agent_name.upper()} Agent] Received task. Executing reasoning loop...")
             print(f"[{agent_name.upper()} Agent] Decision: Running specialized command...")
        
        print("\n[Supervisor] Mission status: Success.")

if __name__ == "__main__":
    run_demo()
