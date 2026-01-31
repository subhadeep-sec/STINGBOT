from core.llm import LLMAdapter
from orchestrator.state_manager import StateManager
from orchestrator.guardrails import Guardrails
import sys
import os

# Try to import autonomous components
try:
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'agents', 'python-brain'))
    from core.memory_system import MemorySystem
    from core.learning_engine import LearningEngine
    from core.knowledge_base import KnowledgeBase
    from core.autonomous_controller import AutonomousController
    from core.autonomous_controller import AutonomousController
    AUTONOMOUS_MODE = True
except ImportError as e:
    AUTONOMOUS_MODE = False
    print(f"[Supervisor] Running in standard mode (autonomous features unavailable): {e}")

try:
    from agents.reflection_agent import ReflectionAgent
except ImportError:
    ReflectionAgent = None

class Supervisor:
    """The Brain: Decomposes goals, routes to agents, manages mission lifecycle with learning."""

    def __init__(self, workspace_path):
        self.llm = LLMAdapter()
        self.state = StateManager(workspace_path)
        self.guard = Guardrails()
        self.agents = {} # Registered agents: {'web': WebAgent, ...}
        
        # Initialize autonomous components if available
        if AUTONOMOUS_MODE:
            try:
                self.memory = MemorySystem(workspace_path=os.path.join(workspace_path, "memory"))
                self.learning = LearningEngine(self.memory)
                self.controller = AutonomousController(self.memory, self.learning)

                if ReflectionAgent:
                    self.reflection = ReflectionAgent(self.memory, self.learning)
                else:
                    self.reflection = None
                print("[Supervisor] Autonomous AI mode enabled")
            except Exception as e:
                print(f"[Supervisor] Could not initialize autonomous features: {e}")
                # Don't modify global, just set instance vars to None
                self.memory = None
                self.learning = None
                self.controller = None
                self.reflection = None
        else:
            self.memory = None
            self.learning = None
            self.controller = None
            self.reflection = None

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
            
            # Autonomous Proactive Suggestion
            if self.controller:
                 suggestion = self.controller.suggest_next_action(current_state, high_level_goal)
                 if suggestion:
                     print(f"[Autonomy] Supervisor adopting suggestion: {suggestion}")
                     if isinstance(current_state, dict):
                         current_state["internal_memo"] = f"STRONGLY RECOMMENDED NEXT ACTION: {suggestion}"
                     else:
                         current_state += f"\n[INTERNAL MEMO] STRONGLY RECOMMENDED NEXT ACTION: {suggestion}"

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
                
                # Autonomous Health Check
                if self.controller:
                     warnings = self.controller.check_health(result)
                     if warnings:
                         self.state.update_memory("warnings", warnings)

                # Process findings (agents should update nodes/edges too)
            else:
                # Fallback: Handle unknown agent names gracefully
                print(f"[!] Warning: Unknown agent '{agent_name}'. Available: {list(self.agents.keys())}")
                
                # Attempt fuzzy matching
                matched_agent = self._fuzzy_match_agent(agent_name)
                if matched_agent:
                    print(f"[*] Auto-routing to closest match: '{matched_agent}'")
                    result = self.agents[matched_agent].execute(task)
                    self.state.add_edge("supervisor", matched_agent, f"delegate (fuzzy): {task[:50]}", result.get("summary", "Done"))
                else:
                    # Log the failure and continue
                    self.state.update_memory("errors", self.state.memory.get("errors", []) + [
                        f"Turn {turn}: Unknown agent '{agent_name}' requested for task: {task[:100]}"
                    ])

        # Post-mission reflection and learning
        if self.reflection and self.learning:
            mission_data = {
                "mission_id": f"mission_{len(self.memory.episodic_memory.get()['ids']) if self.memory else 0}",
                "goal": high_level_goal,
                "actions_taken": [f"Turn {i}" for i in range(1, turn+1)],
                "tools_used": list(self.agents.keys()),
                "outcome": "success" if "[COMPLETE]" in decision.upper() else "incomplete",
                "time_taken": turn * 30,  # Rough estimate
                "errors": [],
                "findings": ["Mission completed"]
            }
            
            # Reflect on mission
            reflection_result = self.reflection.reflect_on_mission(mission_data)
            print(f"\n[Reflection] Performance: {reflection_result['performance_score']:.2f}/1.0")
            
            # Learn from mission
            learnings = self.learning.analyze_mission(mission_data)
            print(f"[Learning] Extracted {len(learnings.get('techniques_used', []))} techniques")
        
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

    def _fuzzy_match_agent(self, requested_name):
        """Attempt to match a requested agent name to available agents."""
        if not self.agents:
            return None
        
        requested = requested_name.lower().strip()
        
        # Common aliases and variations
        aliases = {
            "web": ["web", "web_pentester", "webpentester", "http", "webapp", "website"],
            "net": ["net", "network", "net_pentester", "netpentester", "nmap", "tcp"],
            "rev": ["rev", "reverse", "rev_engineer", "revengineer", "binary", "malware"],
            "critic": ["critic", "review", "analyze", "verify"],
            "reporter": ["reporter", "report", "document", "summary"]
        }
        
        # Check direct match first
        for agent_key in self.agents.keys():
            if requested == agent_key.lower():
                return agent_key
        
        # Check aliases
        for agent_key, alias_list in aliases.items():
            if requested in alias_list:
                # Find matching registered agent
                for registered in self.agents.keys():
                    if agent_key in registered.lower():
                        return registered
        
        # Substring matching as last resort
        for agent_key in self.agents.keys():
            if requested in agent_key.lower() or agent_key.lower() in requested:
                return agent_key
        
        return None
