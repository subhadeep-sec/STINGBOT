from core.llm import LLMAdapter
from core.system_agent import SystemAgent

class BaseAgent:
    """Foundational class for all specialized agents."""
    
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.llm = LLMAdapter()
        self.sys = SystemAgent() # Existing system execution logic

    def execute(self, task):
        """Standard entry point for task execution."""
        raise NotImplementedError("Each agent must implement its own execution logic.")

    def reason(self, prompt, system_prompt=None):
        """Use LLM to decide on next actions."""
        return self.llm.query(prompt, system_prompt=system_prompt or f"You are the STINGBOT {self.name.upper()} Agent.")

    def run_cmd(self, cmd):
        """wrapper for system execution."""
        return self.sys.execute(cmd)

    def summarize_result(self, cmd, result):
        """Use LLM to turn raw output into a technical insight."""
        prompt = f"Command: {cmd}\nOutput: {str(result)[:1200]}\nTask: Technical summary."
        return self.llm.query(prompt, system_prompt="You are a STINGBOT Result Summarizer.")
