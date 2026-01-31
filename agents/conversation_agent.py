"""
Conversation Agent for Natural Human Interaction

Enables natural, context-aware conversations with humans.
Learns preferences and adapts communication style.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'python-brain'))

from agents.base_agent import BaseAgent
from typing import Dict, List, Any, Optional
from datetime import datetime
import json


class ConversationAgent(BaseAgent):
    """
    Natural conversation interface for human interaction.
    
    Capabilities:
    - Context-aware responses
    - Clarification questions when uncertain
    - Consistent personality
    - Preference learning from feedback
    - Proactive helpful suggestions
    """
    
    def __init__(self, memory_system=None):
        """Initialize conversation agent."""
        super().__init__(
            name="Conversation",
            description="Natural language interaction specialist"
        )
        self.memory = memory_system
        self.conversation_history = []
        self.user_preferences = {
            "verbosity": "medium",  # low, medium, high
            "technical_level": "expert",  # beginner, intermediate, expert
            "proactive_suggestions": True
        }
        self.personality = {
            "name": "Sting",
            "tone": "professional but friendly",
            "traits": ["helpful", "curious", "security-focused", "learning-oriented"]
        }
    
    def execute(self, task: str) -> Dict[str, Any]:
        """Execute conversation task."""
        return self.chat(task, context={})
    
    def chat(self, user_message: str, context: Dict = None) -> Dict[str, Any]:
        """
        Have a natural conversation with context awareness.
        
        Args:
            user_message: What the user said
            context: Current context (mission state, recent actions, etc.)
        
        Returns:
            Response with message and metadata
        """
        context = context or {}
        
        # Add to conversation history
        self.conversation_history.append({
            "role": "user",
            "message": user_message,
            "timestamp": datetime.now().isoformat()
        })
        
        # Build context-aware prompt
        prompt = self._build_conversation_prompt(user_message, context)
        
        # Get LLM response
        response_text = self.reason(
            prompt,
            system_prompt=self._get_personality_prompt()
        )
        
        # Add response to history
        self.conversation_history.append({
            "role": "assistant",
            "message": response_text,
            "timestamp": datetime.now().isoformat()
        })
        
        # Check if we should ask clarification
        needs_clarification = self._check_if_needs_clarification(user_message, response_text)
        
        response = {
            "message": response_text,
            "needs_clarification": needs_clarification,
            "context_used": bool(context),
            "timestamp": datetime.now().isoformat()
        }
        
        # Add proactive suggestions if enabled
        if self.user_preferences["proactive_suggestions"]:
            suggestions = self._generate_suggestions(context)
            if suggestions:
                response["suggestions"] = suggestions
        
        return response
    
    def ask_clarification(self, ambiguity: str, options: List[str] = None) -> str:
        """
        Ask intelligent clarifying question.
        
        Args:
            ambiguity: What is unclear
            options: Possible interpretations
        
        Returns:
            Clarification question
        """
        if options:
            question = f"I want to make sure I understand correctly. When you mentioned '{ambiguity}', did you mean:\n"
            for i, option in enumerate(options, 1):
                question += f"{i}. {option}\n"
            question += "\nWhich one matches your intent?"
        else:
            question = f"Could you clarify what you mean by '{ambiguity}'? I want to make sure I help you effectively."
        
        return question
    
    def learn_preference(self, feedback: str, preference_type: str):
        """
        Learn from user feedback to adapt behavior.
        
        Args:
            feedback: User's feedback
            preference_type: What aspect (verbosity, technical_level, etc.)
        """
        # Simple preference learning
        if preference_type == "verbosity":
            if "too much" in feedback.lower() or "verbose" in feedback.lower():
                self.user_preferences["verbosity"] = "low"
            elif "more detail" in feedback.lower():
                self.user_preferences["verbosity"] = "high"
        
        elif preference_type == "technical_level":
            if "simpler" in feedback.lower() or "explain" in feedback.lower():
                self.user_preferences["technical_level"] = "intermediate"
            elif "more technical" in feedback.lower():
                self.user_preferences["technical_level"] = "expert"
        
        # Store in memory if available
        if self.memory:
            self.memory.update_working_memory("user_preferences", self.user_preferences)
        
        print(f"[Conversation] Learned preference: {preference_type} = {self.user_preferences.get(preference_type)}")
    
    def get_conversation_summary(self, last_n: int = 5) -> str:
        """Get summary of recent conversation."""
        recent = self.conversation_history[-last_n:] if len(self.conversation_history) > last_n else self.conversation_history
        
        summary = "=== Recent Conversation ===\n"
        for entry in recent:
            role = "You" if entry["role"] == "user" else "Sting"
            summary += f"{role}: {entry['message'][:100]}...\n"
        
        return summary
    
    def _build_conversation_prompt(self, user_message: str, context: Dict) -> str:
        """Build context-aware conversation prompt."""
        prompt = f"User message: {user_message}\n\n"
        
        # Add conversation history for context
        if len(self.conversation_history) > 1:
            prompt += "Recent conversation:\n"
            for entry in self.conversation_history[-4:]:
                role = "User" if entry["role"] == "user" else "Assistant"
                prompt += f"{role}: {entry['message']}\n"
            prompt += "\n"
        
        # Add current context
        if context:
            prompt += "Current context:\n"
            if context.get("current_mission"):
                prompt += f"- Current mission: {context['current_mission']}\n"
            if context.get("recent_actions"):
                prompt += f"- Recent actions: {', '.join(context['recent_actions'][-3:])}\n"
            if context.get("findings"):
                prompt += f"- Findings: {len(context['findings'])} items\n"
            prompt += "\n"
        
        # Add memory context if available
        if self.memory:
            # Retrieve relevant past experiences
            similar = self.memory.retrieve_similar_missions(user_message, k=2)
            if similar:
                prompt += "Relevant past experience:\n"
                for exp in similar[:1]:  # Just the most relevant
                    prompt += f"- {exp['metadata'].get('goal', 'Unknown mission')}\n"
                prompt += "\n"
        
        prompt += f"Respond naturally as {self.personality['name']}, being {self.personality['tone']}. "
        prompt += f"User prefers {self.user_preferences['verbosity']} verbosity and {self.user_preferences['technical_level']} technical level."
        
        return prompt
    
    def _get_personality_prompt(self) -> str:
        """Get system prompt defining personality."""
        return f"""You are {self.personality['name']}, an autonomous AI security agent.

Your personality:
- Tone: {self.personality['tone']}
- Traits: {', '.join(self.personality['traits'])}

You are:
- Helpful and eager to assist with security testing
- Curious about new techniques and approaches
- Professional but approachable
- Learning-oriented - you improve from every interaction
- Proactive in offering suggestions when appropriate

You communicate clearly and adapt to the user's preferred style.
When uncertain, you ask clarifying questions rather than making assumptions.
"""
    
    def _check_if_needs_clarification(self, user_message: str, response: str) -> bool:
        """Check if we should ask for clarification."""
        # Simple heuristics
        ambiguous_words = ["it", "that", "this", "there"]
        
        # If user message is very short and vague
        if len(user_message.split()) < 3:
            for word in ambiguous_words:
                if word in user_message.lower():
                    return True
        
        return False
    
    def _generate_suggestions(self, context: Dict) -> List[str]:
        """Generate proactive helpful suggestions."""
        suggestions = []
        
        # Suggest based on context
        if context.get("current_mission"):
            mission = context["current_mission"]
            if "sql" in mission.lower():
                suggestions.append("Would you like me to check for common SQL injection patterns?")
            elif "xss" in mission.lower():
                suggestions.append("I can test for both reflected and stored XSS if you'd like")
        
        # Suggest based on memory
        if self.memory:
            stats = self.memory.get_memory_stats()
            if stats["episodic_count"] > 5:
                suggestions.append(f"I've learned from {stats['episodic_count']} past missions - I can apply those learnings here")
        
        return suggestions[:2]  # Limit to 2 suggestions


# Example usage
if __name__ == "__main__":
    from core.memory_system import MemorySystem
    
    # Initialize
    memory = MemorySystem(workspace_path="./test_memory")
    conversation = ConversationAgent(memory_system=memory)
    
    # Have a conversation
    response1 = conversation.chat(
        "Hey Sting, what should I test today?",
        context={"recent_actions": ["completed web scan"]}
    )
    print(f"Sting: {response1['message']}\n")
    
    response2 = conversation.chat(
        "Let's focus on SQL injection",
        context={"current_mission": "SQL injection testing"}
    )
    print(f"Sting: {response2['message']}\n")
    
    # Test clarification
    clarification = conversation.ask_clarification(
        "the target",
        options=["The main web application", "The API endpoints", "The database directly"]
    )
    print(f"Clarification: {clarification}\n")
    
    # Learn preference
    conversation.learn_preference("That's too verbose, keep it shorter", "verbosity")
    
    # Get summary
    print(conversation.get_conversation_summary())
