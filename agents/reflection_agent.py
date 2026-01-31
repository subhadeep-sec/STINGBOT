"""
Reflection Agent for Self-Analysis and Improvement

Analyzes mission performance, identifies mistakes, and suggests improvements.
Implements meta-learning to help the agent learn how to learn better.
"""

from typing import Dict, List, Any
from datetime import datetime
import json


class ReflectionAgent:
    """
    Enables the agent to reflect on its own performance and improve.
    
    Capabilities:
    - Post-mission performance analysis
    - Mistake identification and learning
    - Strategy refinement suggestions
    - Meta-learning (learning about learning)
    """
    
    def __init__(self, memory_system, learning_engine):
        """Initialize reflection agent with memory and learning systems."""
        self.memory = memory_system
        self.learning = learning_engine
        self.reflection_history = []
    
    def reflect_on_mission(self, mission_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform deep reflection on a completed mission.
        
        Args:
            mission_data: Complete mission information including:
                - goal: Mission objective
                - actions_taken: List of actions
                - outcome: Success/failure
                - time_taken: Duration
                - errors: Any errors encountered
                - findings: What was discovered
        
        Returns:
            Reflection analysis with insights and improvements
        """
        reflection = {
            "mission_id": mission_data.get("mission_id", "unknown"),
            "timestamp": datetime.now().isoformat(),
            "performance_score": 0.0,
            "what_went_well": [],
            "what_went_wrong": [],
            "key_learnings": [],
            "improvement_suggestions": [],
            "meta_insights": []
        }
        
        # Analyze what went well
        if mission_data.get("outcome") == "success":
            reflection["what_went_well"].append("Mission objective achieved")
            reflection["performance_score"] += 0.5
            
            if mission_data.get("findings"):
                reflection["what_went_well"].append(
                    f"Discovered {len(mission_data.get('findings', []))} findings"
                )
                reflection["performance_score"] += 0.3
        
        # Analyze what went wrong
        errors = mission_data.get("errors", [])
        if errors:
            for error in errors:
                reflection["what_went_wrong"].append(f"Error encountered: {error}")
                reflection["performance_score"] -= 0.1
        
        # Check efficiency
        time_taken = mission_data.get("time_taken", 0)
        if time_taken > 300:  # More than 5 minutes
            reflection["what_went_wrong"].append("Mission took longer than expected")
            reflection["improvement_suggestions"].append(
                "Optimize reconnaissance phase to reduce time"
            )
        
        # Extract key learnings
        learnings = self._extract_learnings(mission_data)
        reflection["key_learnings"] = learnings
        
        # Generate improvement suggestions
        improvements = self._generate_improvements(mission_data, reflection)
        reflection["improvement_suggestions"].extend(improvements)
        
        # Meta-learning insights
        meta_insights = self._meta_learn(mission_data, reflection)
        reflection["meta_insights"] = meta_insights
        
        # Store reflection
        self.reflection_history.append(reflection)
        
        # Update memory with reflection
        self.memory.update_working_memory("last_reflection", reflection)
        
        print(f"[Reflection] Performance score: {reflection['performance_score']:.2f}")
        print(f"[Reflection] {len(reflection['key_learnings'])} learnings, {len(reflection['improvement_suggestions'])} improvements")
        
        return reflection
    
    def identify_recurring_mistakes(self, lookback: int = 10) -> List[Dict]:
        """
        Identify patterns in mistakes across recent missions.
        
        Args:
            lookback: Number of recent reflections to analyze
        
        Returns:
            List of recurring mistake patterns
        """
        recent_reflections = self.reflection_history[-lookback:]
        
        # Count mistake types
        mistake_patterns = {}
        for reflection in recent_reflections:
            for mistake in reflection.get("what_went_wrong", []):
                if mistake in mistake_patterns:
                    mistake_patterns[mistake] += 1
                else:
                    mistake_patterns[mistake] = 1
        
        # Filter recurring (appears 2+ times)
        recurring = [
            {"mistake": mistake, "occurrences": count}
            for mistake, count in mistake_patterns.items()
            if count >= 2
        ]
        
        if recurring:
            print(f"[Reflection] Identified {len(recurring)} recurring mistakes")
        
        return recurring
    
    def suggest_strategy_refinements(self) -> List[str]:
        """
        Suggest refinements to overall strategy based on reflections.
        
        Returns:
            List of strategy refinement suggestions
        """
        refinements = []
        
        # Analyze performance trends
        if len(self.reflection_history) >= 5:
            recent_scores = [r["performance_score"] for r in self.reflection_history[-5:]]
            avg_score = sum(recent_scores) / len(recent_scores)
            
            if avg_score < 0.5:
                refinements.append(
                    "Overall performance below target - consider reviewing tool selection"
                )
            
            # Check if improving or declining
            if len(recent_scores) >= 3:
                if recent_scores[-1] < recent_scores[-3]:
                    refinements.append(
                        "Performance declining - review recent changes to approach"
                    )
        
        # Check for common improvement suggestions
        all_suggestions = []
        for reflection in self.reflection_history[-10:]:
            all_suggestions.extend(reflection.get("improvement_suggestions", []))
        
        # Find most common
        suggestion_counts = {}
        for suggestion in all_suggestions:
            suggestion_counts[suggestion] = suggestion_counts.get(suggestion, 0) + 1
        
        common_suggestions = [
            f"Frequently suggested: {suggestion}"
            for suggestion, count in suggestion_counts.items()
            if count >= 3
        ]
        
        refinements.extend(common_suggestions)
        
        return refinements
    
    def consolidate_learnings(self) -> Dict[str, Any]:
        """
        Consolidate learnings from multiple reflections into actionable insights.
        
        Returns:
            Consolidated learning summary
        """
        if not self.reflection_history:
            return {"status": "No reflections to consolidate"}
        
        consolidation = {
            "total_reflections": len(self.reflection_history),
            "average_performance": 0.0,
            "top_learnings": [],
            "critical_improvements": [],
            "success_patterns": [],
            "timestamp": datetime.now().isoformat()
        }
        
        # Calculate average performance
        scores = [r["performance_score"] for r in self.reflection_history]
        consolidation["average_performance"] = sum(scores) / len(scores)
        
        # Aggregate all learnings
        all_learnings = []
        for reflection in self.reflection_history:
            all_learnings.extend(reflection.get("key_learnings", []))
        
        # Get most common learnings (simplified)
        learning_counts = {}
        for learning in all_learnings:
            learning_counts[learning] = learning_counts.get(learning, 0) + 1
        
        consolidation["top_learnings"] = sorted(
            learning_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]
        
        # Identify success patterns
        successful_reflections = [
            r for r in self.reflection_history
            if r["performance_score"] >= 0.7
        ]
        
        if successful_reflections:
            consolidation["success_patterns"] = [
                "High success rate when reconnaissance is thorough",
                "Better outcomes with systematic approach"
            ]
        
        print(f"[Reflection] Consolidated {len(self.reflection_history)} reflections")
        
        return consolidation
    
    def get_reflection_summary(self) -> str:
        """Generate human-readable reflection summary."""
        if not self.reflection_history:
            return "[Reflection] No reflections yet"
        
        recent = self.reflection_history[-1]
        consolidation = self.consolidate_learnings()
        
        summary = f"""
=== REFLECTION SUMMARY ===
Last Mission Performance: {recent['performance_score']:.2f}/1.0

What Went Well:
{chr(10).join(f"  ✓ {item}" for item in recent['what_went_well'])}

Areas for Improvement:
{chr(10).join(f"  ✗ {item}" for item in recent['what_went_wrong'])}

Key Learnings:
{chr(10).join(f"  • {item}" for item in recent['key_learnings'])}

Overall Performance: {consolidation['average_performance']:.2f}/1.0
Total Reflections: {consolidation['total_reflections']}
"""
        return summary
    
    def _extract_learnings(self, mission_data: Dict) -> List[str]:
        """Extract key learnings from mission data."""
        learnings = []
        
        # Learning from success
        if mission_data.get("outcome") == "success":
            tools_used = mission_data.get("tools_used", [])
            if tools_used:
                learnings.append(
                    f"Effective tool combination: {', '.join(tools_used[:3])}"
                )
        
        # Learning from findings
        findings = mission_data.get("findings", [])
        if findings:
            learnings.append(
                f"Discovered {len(findings)} vulnerabilities/findings"
            )
        
        # Learning from errors
        errors = mission_data.get("errors", [])
        if errors:
            learnings.append(
                f"Encountered {len(errors)} errors - need better error handling"
            )
        
        return learnings
    
    def _generate_improvements(self, mission_data: Dict, reflection: Dict) -> List[str]:
        """Generate specific improvement suggestions."""
        improvements = []
        
        # Based on performance score
        if reflection["performance_score"] < 0.5:
            improvements.append("Review and refine mission approach")
        
        # Based on errors
        if mission_data.get("errors"):
            improvements.append("Implement better error handling and recovery")
        
        # Based on time
        if mission_data.get("time_taken", 0) > 300:
            improvements.append("Optimize tool execution order for efficiency")
        
        return improvements
    
    def _meta_learn(self, mission_data: Dict, reflection: Dict) -> List[str]:
        """Meta-learning: learn about the learning process itself."""
        meta_insights = []
        
        # Analyze learning effectiveness
        if len(self.reflection_history) >= 3:
            recent_scores = [r["performance_score"] for r in self.reflection_history[-3:]]
            
            # Check if learning is effective (improving over time)
            if recent_scores[-1] > recent_scores[0]:
                meta_insights.append(
                    "Learning process is effective - performance improving"
                )
            else:
                meta_insights.append(
                    "Learning process needs adjustment - performance not improving"
                )
        
        # Analyze reflection quality
        if len(reflection["key_learnings"]) < 2:
            meta_insights.append(
                "Need to extract more detailed learnings from missions"
            )
        
        return meta_insights


# Example usage
if __name__ == "__main__":
    from memory_system import MemorySystem
    from learning_engine import LearningEngine
    
    # Initialize
    memory = MemorySystem(workspace_path="./test_memory")
    learning = LearningEngine(memory)
    reflection = ReflectionAgent(memory, learning)
    
    # Reflect on a mission
    mission = {
        "mission_id": "test_001",
        "goal": "SQL injection testing",
        "actions_taken": ["nmap", "nikto", "sqlmap"],
        "tools_used": ["nmap", "nikto", "sqlmap"],
        "outcome": "success",
        "time_taken": 180,
        "errors": [],
        "findings": ["SQL injection in login", "XSS in search"]
    }
    
    analysis = reflection.reflect_on_mission(mission)
    print(json.dumps(analysis, indent=2))
    
    # Get summary
    print(reflection.get_reflection_summary())
