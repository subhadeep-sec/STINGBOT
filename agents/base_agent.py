from core.llm import LLMAdapter
from core.system_agent import SystemAgent

class BaseAgent:
    """Foundational class for all specialized agents with learning capabilities."""
    
    def __init__(self, name, description, memory_system=None):
        self.name = name
        self.description = description
        self.llm = LLMAdapter()
        self.sys = SystemAgent() # Existing system execution logic
        self.memory = memory_system  # Access to shared memory
        self.execution_history = []  # Track this agent's actions

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
    
    def learn_from_execution(self, task, result, success):
        """Learn from task execution outcome."""
        self.execution_history.append({
            "task": task,
            "result": result,
            "success": success,
            "agent": self.name
        })
        
        # If memory system available, retrieve relevant past experiences
        if self.memory and success:
            # Store successful technique
            self.memory.learn_technique(
                technique=f"{self.name} agent: {task[:50]}",
                context=task,
                success_rate=0.8,
                metadata={"agent": self.name}
            )
