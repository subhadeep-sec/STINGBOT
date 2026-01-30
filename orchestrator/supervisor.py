from core.llm import LLMAdapter
from orchestrator.state_manager import StateManager
from orchestrator.guardrails import Guardrails

class Supervisor:
    """The Brain: Decomposes goals, routes to agents, and manages the mission life cycle."""

    def __init__(self, workspace_path):
        self.llm = LLMAdapter()
        self.state = StateManager(workspace_path)
        self.guard = Guardrails()
        self.agents = {} # Registered agents: {'web': WebAgent, ...}

    def register_agent(self, name, agent_instance):
        self.agents[name] = agent_instance

    def run_mission(self, high_level_goal):
        """Main execution loop for a mission."""
        self.state.update_memory("mission_goal", high_level_goal)
        
        # 1. INITIAL ANALYSIS & DECOMPOSITION
        plan = self._decompose_goal(high_level_goal)
        self.state.update_memory("initial_plan", plan)
        
        # 2. EXECUTION LOOP
        max_turns = 15
        for turn in range(1, max_turns + 1):
            print(f"[*] Turn {turn}/{max_turns}: Reasoning...")
            current_state = self.state.export_summary()
            
            # Decide next step
            decision_prompt = f"""
            Mission Goal: {high_level_goal}
            Current State: {current_state}
            Available Agents: {list(self.agents.keys())}
            
            Task: What is the next step? Choose an agent and a task for it.
            Alternatively, if the goal is met, output [COMPLETE].
            
            Output format: 
            AGENT: <agent_name>
            TASK: <specific instructions>
            """
            decision = self.llm.query(decision_prompt, system_prompt="You are the STINGBOT MISSION SUPERVISOR.")
            print(f"[>] Decision: {decision.splitlines()[0]}...") # Print first line of decision
            
            if "[COMPLETE]" in decision.upper():
                 break
            
            # Parse decision
            agent_name, task = self._parse_decision(decision)
            
            if agent_name in self.agents:
                agent = self.agents[agent_name]
                # Safety check before delegation if targeting a specific IP
                # (Guardrails are also implemented inside agents/tools)
                
                result = agent.execute(task)
                
                # Update state
                self.state.add_edge("supervisor", agent_name, f"delegate: {task[:50]}", result.get("summary", "Done"))
                # Process findings (agents should update nodes/edges too)
            else:
                 # Fallback or error handling
                 pass

        return "[MISSION COMPLETE] Report generated in logs."

    def _decompose_goal(self, goal):
        """Use LLM to break down goal into initial sub-tasks."""
        prompt = f"Goal: {goal}\nDecompose this into a list of technical stages (Recon, Vulnerability Discovery, etc.)."
        return self.llm.query(prompt)

    def _parse_decision(self, text):
        """Extract AGENT and TASK from LLM output."""
        agent = "unknown"
        task = ""
        for line in text.split("\n"):
            if line.startswith("AGENT:"): agent = line.split(":", 1)[1].strip().lower()
            if line.startswith("TASK:"): task = line.split(":", 1)[1].strip()
        return agent, task
