from agents.base_agent import BaseAgent

class CriticAgent(BaseAgent):
    """Specialist for failure analysis and self-correction."""
    
    def __init__(self):
        super().__init__("Critic", "Analyzes error logs and suggests new exploitation strategies.")

    def execute(self, task):
        # Task for the Critic is usually an error log or a failed attempt description
        prompt = f"""
        Failed Attempt/Error: {task}
        
        Task: Analyze why it failed (e.g., WAF, closed port, patched vulnerability).
        Suggest a new approach or a different obfuscation technique.
        """
        analysis = self.reason(prompt)
        
        return {
            "status": "success",
            "analysis": analysis,
            "summary": f"Critic Analysis: {analysis[:100]}..."
        }
