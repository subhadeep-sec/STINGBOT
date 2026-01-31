"""
Learning Engine for Autonomous AI Agent

Analyzes mission outcomes, identifies patterns, and extracts learnings
to improve agent performance over time.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import json
from collections import defaultdict


class LearningEngine:
    """
    Analyzes experiences and extracts learnings to improve agent behavior.
    
    Capabilities:
    - Experience replay and analysis
    - Pattern recognition across missions
    - Technique extraction and refinement
    - Tool effectiveness tracking
    - Strategy adaptation
    """
    
    def __init__(self, memory_system):
        """Initialize learning engine with memory system."""
        self.memory = memory_system
        self.tool_stats = defaultdict(lambda: {"successes": 0, "failures": 0, "total": 0})
        self.technique_registry = {}
        self.pattern_cache = []
    
    def analyze_mission(self, mission_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze a completed mission and extract learnings.
        
        Args:
            mission_result: Dictionary containing:
                - goal: Mission objective
                - actions: List of actions taken
                - tools_used: Tools employed
                - outcome: Success/failure
                - findings: What was discovered
                - errors: Any errors encountered
        
        Returns:
            Dictionary of extracted learnings
        """
        learnings = {
            "techniques_used": [],
            "effective_tools": [],
            "patterns_identified": [],
            "improvements": [],
            "timestamp": datetime.now().isoformat()
        }
        
        # Analyze tool effectiveness
        for tool in mission_result.get("tools_used", []):
            self._update_tool_stats(tool, mission_result.get("outcome") == "success")
            
            # If tool was effective, record it
            if mission_result.get("outcome") == "success":
                learnings["effective_tools"].append({
                    "tool": tool,
                    "context": mission_result.get("goal", ""),
                    "success_rate": self._get_tool_success_rate(tool)
                })
        
        # Extract techniques from successful actions
        if mission_result.get("outcome") == "success":
            techniques = self._extract_techniques(mission_result)
            learnings["techniques_used"] = techniques
            
            # Store techniques in memory
            for technique in techniques:
                self.memory.learn_technique(
                    technique=technique["name"],
                    context=technique["context"],
                    success_rate=technique.get("confidence", 0.7),
                    metadata={"source": "mission_analysis"}
                )
        
        # Identify patterns
        patterns = self._identify_patterns(mission_result)
        learnings["patterns_identified"] = patterns
        
        # Generate improvement suggestions
        if mission_result.get("errors"):
            improvements = self._suggest_improvements(mission_result)
            learnings["improvements"] = improvements
        
        # Store mission in episodic memory
        self.memory.store_mission({
            "goal": mission_result.get("goal", ""),
            "actions": mission_result.get("actions", []),
            "outcome": mission_result.get("outcome", "unknown"),
            "learnings": json.dumps(learnings),
            "success": mission_result.get("outcome") == "success",
            "timestamp": datetime.now().isoformat()
        })
        
        print(f"[Learning] Analyzed mission: {len(learnings['techniques_used'])} techniques, {len(learnings['effective_tools'])} effective tools")
        
        return learnings
    
    def identify_patterns(self, min_occurrences: int = 3) -> List[Dict]:
        """
        Identify recurring patterns across multiple missions.
        
        Args:
            min_occurrences: Minimum times a pattern must occur
        
        Returns:
            List of identified patterns
        """
        # Retrieve all missions
        all_missions = self.memory.episodic_memory.get()
        
        if not all_missions or not all_missions['metadatas']:
            return []
        
        # Analyze for patterns
        patterns = defaultdict(int)
        
        for metadata in all_missions['metadatas']:
            if metadata.get('success') == 'True':
                goal = metadata.get('goal', '')
                # Simple pattern: goal type
                if 'sql' in goal.lower():
                    patterns['sql_injection_testing'] += 1
                if 'xss' in goal.lower():
                    patterns['xss_testing'] += 1
                if 'scan' in goal.lower():
                    patterns['reconnaissance'] += 1
        
        # Filter by minimum occurrences
        significant_patterns = [
            {"pattern": name, "occurrences": count, "confidence": min(count / 10, 1.0)}
            for name, count in patterns.items()
            if count >= min_occurrences
        ]
        
        self.pattern_cache = significant_patterns
        print(f"[Learning] Identified {len(significant_patterns)} significant patterns")
        
        return significant_patterns
    
    def get_recommended_strategy(self, goal: str) -> Dict[str, Any]:
        """
        Recommend strategy based on learned experiences.
        
        Args:
            goal: Current mission goal
        
        Returns:
            Recommended strategy with tools and techniques
        """
        # Retrieve similar past missions
        similar_missions = self.memory.retrieve_similar_missions(goal, k=5)
        
        # Retrieve relevant techniques
        techniques = self.memory.retrieve_relevant_techniques(goal, k=3)
        
        # Compile recommendation
        recommendation = {
            "suggested_tools": [],
            "recommended_techniques": [],
            "confidence": 0.0,
            "based_on_missions": len(similar_missions)
        }
        
        # Extract tools from successful similar missions
        successful_tools = set()
        for mission in similar_missions:
            if mission['metadata'].get('success') == 'True':
                # Would extract tools from mission data
                successful_tools.add("nmap")  # Placeholder
        
        recommendation["suggested_tools"] = list(successful_tools)
        
        # Add techniques
        recommendation["recommended_techniques"] = [
            {
                "technique": t['metadata'].get('technique', 'Unknown'),
                "success_rate": float(t['metadata'].get('success_rate', 0.5))
            }
            for t in techniques
        ]
        
        # Calculate confidence based on similar missions
        if similar_missions:
            recommendation["confidence"] = min(len(similar_missions) / 5, 1.0)
        
        print(f"[Learning] Generated strategy recommendation (confidence: {recommendation['confidence']:.2f})")
        
        return recommendation
    
    def update_technique_effectiveness(self, technique_name: str, success: bool):
        """Update effectiveness tracking for a technique."""
        if technique_name not in self.technique_registry:
            self.technique_registry[technique_name] = {
                "successes": 0,
                "failures": 0,
                "total": 0
            }
        
        self.technique_registry[technique_name]["total"] += 1
        if success:
            self.technique_registry[technique_name]["successes"] += 1
        else:
            self.technique_registry[technique_name]["failures"] += 1
    
    def get_learning_summary(self) -> str:
        """Generate human-readable learning summary."""
        stats = self.memory.get_memory_stats()
        patterns = self.pattern_cache
        
        summary = f"""
=== LEARNING ENGINE SUMMARY ===
Total Missions Analyzed: {stats['episodic_count']}
Techniques Learned: {stats['semantic_count']}
Patterns Identified: {len(patterns)}

Top Tools by Success Rate:
"""
        # Add top tools
        sorted_tools = sorted(
            self.tool_stats.items(),
            key=lambda x: x[1]['successes'] / max(x[1]['total'], 1),
            reverse=True
        )[:5]
        
        for tool, stats in sorted_tools:
            success_rate = stats['successes'] / max(stats['total'], 1)
            summary += f"  - {tool}: {success_rate*100:.1f}% ({stats['total']} uses)\n"
        
        return summary
    
    def _extract_techniques(self, mission_result: Dict) -> List[Dict]:
        """Extract techniques from mission actions."""
        techniques = []
        
        # Simple technique extraction based on actions
        actions = mission_result.get("actions", [])
        goal = mission_result.get("goal", "")
        
        if any("sql" in action.lower() for action in actions):
            techniques.append({
                "name": "SQL Injection Testing",
                "context": goal,
                "confidence": 0.8
            })
        
        if any("xss" in action.lower() for action in actions):
            techniques.append({
                "name": "XSS Testing",
                "context": goal,
                "confidence": 0.8
            })
        
        return techniques
    
    def _identify_patterns(self, mission_result: Dict) -> List[str]:
        """Identify patterns in mission execution."""
        patterns = []
        
        # Pattern: Reconnaissance before exploitation
        actions = mission_result.get("actions", [])
        if len(actions) > 1:
            if any("scan" in a.lower() for a in actions[:2]):
                patterns.append("reconnaissance_first")
        
        return patterns
    
    def _suggest_improvements(self, mission_result: Dict) -> List[str]:
        """Suggest improvements based on errors."""
        improvements = []
        errors = mission_result.get("errors", [])
        
        for error in errors:
            if "timeout" in str(error).lower():
                improvements.append("Increase timeout values for network operations")
            if "permission" in str(error).lower():
                improvements.append("Check tool permissions and sudo requirements")
        
        return improvements
    
    def _update_tool_stats(self, tool: str, success: bool):
        """Update tool effectiveness statistics."""
        self.tool_stats[tool]["total"] += 1
        if success:
            self.tool_stats[tool]["successes"] += 1
        else:
            self.tool_stats[tool]["failures"] += 1
    
    def _get_tool_success_rate(self, tool: str) -> float:
        """Get success rate for a tool."""
        stats = self.tool_stats.get(tool, {"successes": 0, "total": 0})
        if stats["total"] == 0:
            return 0.0
        return stats["successes"] / stats["total"]


# Example usage
if __name__ == "__main__":
    from memory_system import MemorySystem
    
    # Initialize
    memory = MemorySystem(workspace_path="./test_memory")
    learning = LearningEngine(memory)
    
    # Analyze a mission
    mission = {
        "goal": "Test web application for SQL injection",
        "actions": ["nmap scan", "nikto scan", "sqlmap test"],
        "tools_used": ["nmap", "nikto", "sqlmap"],
        "outcome": "success",
        "findings": ["SQL injection in login form"],
        "errors": []
    }
    
    learnings = learning.analyze_mission(mission)
    print(json.dumps(learnings, indent=2))
    
    # Get recommendation for similar goal
    recommendation = learning.get_recommended_strategy("SQL injection testing")
    print(json.dumps(recommendation, indent=2))
    
    # Print summary
    print(learning.get_learning_summary())
