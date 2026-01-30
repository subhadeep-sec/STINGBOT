import sys
import os

# Add root and python-brain to path for MAS imports
base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(base_dir)
sys.path.append(os.path.join(base_dir, "agents", "python-brain"))

from interfaces.mas_terminal import MASTerminal

def main():
    workspace = os.path.dirname(os.path.abspath(__file__))
    
    if len(sys.argv) > 1:
        # Command line mode remains for automation
        from orchestrator.supervisor import Supervisor
        from agents.web_pentester import WebPentester
        from agents.net_pentester import NetPentester
        from agents.rev_engineer import RevEngineer
        from agents.critic import CriticAgent
        from agents.reporter import ReporterAgent

        supervisor = Supervisor(workspace)
        supervisor.register_agent("web", WebPentester())
        supervisor.register_agent("net", NetPentester())
        supervisor.register_agent("rev", RevEngineer())
        supervisor.register_agent("critic", CriticAgent())
        supervisor.register_agent("reporter", ReporterAgent(workspace))

        goal = " ".join(sys.argv[1:])
        print(f"Starting Mission: {goal}")
        result = supervisor.run_mission(goal)
        print(result)
    else:
        # NEW: Interactive Mode
        terminal = MASTerminal(workspace)
        terminal.start()

if __name__ == "__main__":
    main()
