from agents.base_agent import BaseAgent

class RevEngineer(BaseAgent):
    """Specialist for binary analysis and reverse engineering."""
    
    def __init__(self):
        super().__init__("Reverse Engineer", "Logic for Ghidra, Radare2, and binary auditing.")

    def execute(self, task):
        # Implementation for rev engineering logic
        prompt = f"""
        Binary Task: {task}
        
        Available Tools: r2, strings, objdump, gdb.
        Determine best analysis command.
        """
        decision = self.reason(prompt)
        
        # Run and return
        result = self.run_cmd(decision)
        summary = self.summarize_result(decision, result)
        
        return {
            "status": "success",
            "summary": summary
        }
