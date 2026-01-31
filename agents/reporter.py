from agents.base_agent import BaseAgent
import os

class ReporterAgent(BaseAgent):
    """Specialist for compiling mission reports."""
    
    def __init__(self, workspace_path):
        super().__init__("Reporter", "Compiles session traces into professional Markdown reports.")
        self.log_dir = os.path.join(workspace_path, "logs")
        os.makedirs(self.log_dir, exist_ok=True)

    def execute(self, mission_data):
        # mission_data contains the summary of the attack graph etc.
        prompt = f"""
        Mission Data: {mission_data}
        
        Task: Create a professional Markdown security report.
        Include Executive Summary, Findings, and Recommendations.
        """
        report_content = self.reason(prompt, system_prompt="You are a STINGBOT SENIOR PENETRATION TESTER.")
        
        report_path = os.path.join(self.log_dir, "mission_report.md")
        with open(report_path, "w") as f:
            f.write(report_content)
        
        return {
            "status": "success",
            "report_path": report_path,
            "summary": f"Report generated at {report_path}"
        }
