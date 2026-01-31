"""
Autonomous Controller for STINGBOT

This module acts as the "agency" layer, providing proactive behavior,
self-monitoring, and curiosity-driven exploration.
It sits alongside the Supervisor to suggest high-level actions.
"""

import random
from typing import List, Dict, Any, Optional

class AutonomousController:
    """
    Drives autonomous behavior and decision making.
    """
    
    def __init__(self, memory_system, learning_engine, config: Dict = None):
        self.memory = memory_system
        self.learning = learning_engine
        self.config = config or {}
        
        # Autonomy state
        self.exploration_rate = self.config.get("exploration_rate", 0.1)
        self.max_consecutive = self.config.get("max_consecutive_tasks", 5)
        self.consecutive_count = 0
        
    def suggest_next_action(self, state_summary: str, current_goal: str) -> Optional[str]:
        """
        Proactively suggest the next high-level action based on state and memory.
        """
        # 1. Safety Check: Prevent infinite loops
        if self.consecutive_count >= self.max_consecutive:
            print("[Autonomy] Reached max consecutive actions. Pausing for human review.")
            return None
            
        # 2. Curiosity: Randomly explore new method?
        if random.random() < self.exploration_rate:
            exploration = self._get_exploration_idea()
            if exploration:
                print(f"[Autonomy] Curiosity triggered! Suggesting: {exploration}")
                self.consecutive_count += 1
                return exploration

        # 3. Memory-based Suggestion
        # Consult learning engine for strategy
        strategy = self.learning.get_recommended_strategy(current_goal)
        if strategy and strategy.get("confidence", 0) > 0.7:
             techs = strategy.get("recommended_techniques", [])
             if techs:
                 best_tech = techs[0]['technique']
                 print(f"[Autonomy] High confidence strategy found from memory: {best_tech}")
                 self.consecutive_count += 1
                 return f"Execute proven technique: {best_tech}"

        # 4. Standard Heuristics (Fallback)
        # If nothing specific from memory, rely on standard methodology logic
        # (This is usually handled by the Supervisor's LLM, so we return None to let it decide)
        return None

    def check_health(self, last_result: Dict) -> List[str]:
        """
        Monitor agent performance and return warnings if needed.
        """
        warnings = []
        
        # Check for repeated failures
        if last_result.get("status") == "failed":
            warnings.append("Last action failed. Consider changing approach.")
            
        # Check for empty findings in a "scan"
        if "scan" in str(last_result).lower() and not last_result.get("findings"):
             warnings.append("Scan yielded no results. Target might be down or blocking us.")
             
        if warnings:
            print(f"[Autonomy] Self-Check Warnings: {warnings}")
            
        return warnings

    def reset_counter(self):
        """Reset the consecutive action counter (e.g., after human interaction)."""
        self.consecutive_count = 0

    def _get_exploration_idea(self) -> Optional[str]:
        """Generate a 'curious' exploration idea."""
        ideas = [
            "Check for backup files (.bak, .old)",
            "Analyze HTTP headers for security misconfigurations",
            "Check for robots.txt and sitemap.xml",
            "Fingerprint the operating system using TTL",
            "passive DNS lookup"
        ]
        return random.choice(ideas)
