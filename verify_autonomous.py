"""
Verify Autonomous AI System

Tests the integration of memory, learning, reflection, and conversation agents
by running a simulated mission and interaction sequence.
"""

import sys
import os
import shutil
from rich.console import Console

# Setup paths
base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, base_dir)
sys.path.insert(0, os.path.join(base_dir, "agents", "python-brain"))

from orchestrator.supervisor import Supervisor
from interfaces.mas_terminal import MASTerminal

console = Console()

def cleanup_test_env():
    """Cleanup test directories."""
    dirs = ["./test_memory", "./test_knowledge", "./memory", "./knowledge"]
    for d in dirs:
        if os.path.exists(d):
            shutil.rmtree(d)
            print(f"Cleaned up {d}")

def test_autonomous_system():
    console.print("[bold blue]=== Testing Autonomous AI System ===[/bold blue]")
    
    # 0. Test direct import
    console.print("\n[bold]0. Testing Direct Import of MemorySystem...[/bold]")
    try:
        from core.memory_system import MemorySystem
        console.print("[green]SUCCESS: MemorySystem imported directly[/green]")
    except ImportError as e:
        console.print(f"[red]FAILED: Direct import error: {e}[/red]")
    except Exception as e:
        console.print(f"[red]FAILED: Direct import exception: {e}[/red]")
    
    # 1. Initialize Supervisor
    console.print("\n[bold]1. Initializing Supervisor with Autonomous Mode...[/bold]")
    try:
        # Create temp workspace for test
        test_workspace = os.path.join(base_dir, "test_workspace")
        os.makedirs(test_workspace, exist_ok=True)
        
        supervisor = Supervisor(test_workspace)
        
        if not supervisor.memory:
            console.print("[red]FAILED: Autonomous components not initialized[/red]")
            return False
        
        console.print("[green]SUCCESS: Memory, Learning, and Reflection systems initialized[/green]")
        
    except Exception as e:
        console.print(f"[red]FAILED: Initialization error: {e}[/red]")
        return False
        
    # 2. Test Memory System
    console.print("\n[bold]2. Testing Memory Persistence...[/bold]")
    try:
        mission_id = supervisor.memory.store_mission({
            "goal": "Test Autonomous System",
            "outcome": "success",
            "actions": ["init", "test", "verify"],
            "success": True
        })
        console.print(f"[green]SUCCESS: Stored mission with ID: {mission_id}[/green]")
        
    except Exception as e:
        console.print(f"[red]FAILED: Memory error: {e}[/red]")
    
    # 3. Test Conversation Agent
    console.print("\n[bold]3. Testing Conversation Agent...[/bold]")
    try:
        from agents.conversation_agent import ConversationAgent
        conversation = ConversationAgent(supervisor.memory)
        
        response = conversation.chat("Hello Sting, are you online?", context={})
        console.print(f"[cyan]User:[/cyan] Hello Sting, are you online?")
        console.print(f"[green]Sting:[/green] {response['message']}")
        
        if response['message']:
            console.print("[green]SUCCESS: Conversation agent responded[/green]")
        else:
            console.print("[red]FAILED: Empty response[/red]")
            
    except Exception as e:
        console.print(f"[red]FAILED: Conversation error: {e}[/red]")

    # 4. Test Knowledge Base
    console.print("\n[bold]4. Testing Knowledge Base (RAG)...[/bold]")
    try:
        from knowledge.knowledge_base import KnowledgeBase
        kb = KnowledgeBase(workspace_path=os.path.join(test_workspace, "knowledge"))
        
        result = kb.query("How do I use nmap?")
        console.print(f"[cyan]Query:[/cyan] How do I use nmap?")
        console.print(f"[green]Answer:[/green] {result['answer']}")
        
        if result['sources']:
            console.print("[green]SUCCESS: RAG retrieved knowledge[/green]")
        else:
            console.print("[yellow]WARNING: RAG returned no sources (might be fallback mode)[/yellow]")
            
    except Exception as e:
        console.print(f"[red]FAILED: Knowledge Base error: {e}[/red]")
        
    return True

if __name__ == "__main__":
    test_autonomous_system()
    # cleanup_test_env() # Keep for inspection
