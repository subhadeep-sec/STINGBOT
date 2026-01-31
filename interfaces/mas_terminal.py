import sys
import os
import yaml
import time

# Ensure python-brain is in path for CLI imports
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(base_dir, "agents", "python-brain"))

from interfaces.cli import cli, console, COLOR_SECONDARY, COLOR_PRIMARY
from rich.panel import Panel
from rich.align import Align
from rich.markdown import Markdown
from orchestrator.supervisor import Supervisor
from agents.conversation_agent import ConversationAgent
from core.memory_system import MemorySystem

class MASTerminal:
    """Session-based Interactive Terminal for Stingbot MAS with Autonomous Capabilities."""

    def __init__(self, workspace_path):
        self.workspace = workspace_path
        self.supervisor = Supervisor(workspace_path)
        
        # Initialize Autonomous Components
        try:
            self.memory = MemorySystem(workspace_path=os.path.join(workspace_path, "memory"))
            self.conversation = ConversationAgent(memory_system=self.memory)
            self.autonomous_mode = True
        except Exception as e:
            cli.log(f"Warning: Autonomous features limited. {e}", "warning")
            self.autonomous_mode = False
            self.conversation = None

        # Register Agents
        from agents.web_pentester import WebPentester
        from agents.net_pentester import NetPentester
        from agents.rev_engineer import RevEngineer
        from agents.critic import CriticAgent
        from agents.reporter import ReporterAgent

        self.supervisor.register_agent("web", WebPentester())
        self.supervisor.register_agent("net", NetPentester())
        self.supervisor.register_agent("rev", RevEngineer())
        self.supervisor.register_agent("critic", CriticAgent())
        self.supervisor.register_agent("reporter", ReporterAgent(workspace_path))

    def start(self):
        self._show_banner()
        
        # Initial greeting
        if self.autonomous_mode:
            greeting = self.conversation.chat("Hello")
            self._print_agent_response(greeting)
        else:
            cli.log("System Ready. Autonomous modules offline.", "info")

        while True:
            try:
                user_input = cli.input("Sting").strip()
                if not user_input: continue
                
                # Check for special commands first
                cmd_parts = user_input.split(" ", 1)
                cmd = cmd_parts[0].lower()
                args = cmd_parts[1] if len(cmd_parts) > 1 else ""

                if cmd in ['exit', 'quit']:
                    cli.log("Disconnecting from MAS Neural Link...", "info")
                    break
                elif cmd == 'clear':
                    os.system('clear')
                    self._show_banner()
                elif cmd == 'help':
                    self._show_help()
                elif cmd == 'graph':
                    summary = self.supervisor.state.export_summary()
                    cli.log(f"Attack Graph Summary: {summary}", "info")
                elif cmd == 'memory':
                    if self.autonomous_mode:
                        cli.log(self.memory.export_memory_summary(), "info")
                    else:
                        cli.log("Memory module not available.", "warning")
                elif cmd == 'config':
                    self._handle_config(args)
                
                # Default: Treat as conversation / intent
                else:
                    if self.autonomous_mode:
                        self._handle_conversation(user_input)
                    else:
                        # Legacy fallback
                        self._run_legacy_mission(user_input)

            except KeyboardInterrupt:
                cli.log("\nInterrupted.", "warning")
            except Exception as e:
                cli.log(f"System Error: {str(e)}", "error")

    def _handle_conversation(self, user_input):
        """Process natural language input via ConversationAgent."""
        
        # 1. Chat with agent
        with console.status("[bold green]Thinking...[/]", spinner="dots"):
            response = self.conversation.chat(
                user_input, 
                context={"current_state": self.supervisor.state.export_summary()}
            )
        
        # 2. Display response
        self._print_agent_response(response)
        
        # 3. Check for actionable intent (Mission Execution)
        # Simple heuristic: If the user explicitly asks to "run", "scan", "test", or "attack"
        # In a full system, the LLM would return a 'action_required' flag.
        keywords = ["run", "scan", "test", "attack", "exploit", "mission"]
        if any(k in user_input.lower() for k in keywords) and len(user_input) > 10:
             if cli.confirm("Shall I execute this as a mission?"):
                 self._run_mission(user_input)

    def _run_mission(self, goal):
        """Execute a mission via Supervisor."""
        cli.log(f"Initiating Mission: {goal}", "action")
        try:
             result = self.supervisor.run_mission(goal)
             cli.log(result, "success")
             cli.mission_end(result)
             
             # Post-mission reflection in conversation
             if self.autonomous_mode:
                 reflection_msg = self.conversation.chat(
                     "The mission is complete. What do you think?",
                     context={"last_mission_result": "success"} # Simplified
                 )
                 self._print_agent_response(reflection_msg)
                 
        except KeyboardInterrupt:
            cli.log("\nMission aborted by operator.", "warning")
        except Exception as e:
            cli.log(f"Mission failed: {str(e)}", "error")

    def _run_legacy_mission(self, goal):
        """Fallback for non-autonomous mode."""
        if cli.confirm(f"Start mission: '{goal}'?"):
            self._run_mission(goal)

    def _print_agent_response(self, response_obj):
        """Pretty print the agent's response."""
        msg = response_obj.get("message", "")
        suggestions = response_obj.get("suggestions", [])
        
        console.print(Panel(Markdown(msg), title="[bold blue]Sting[/]", border_style="blue"))
        
        if suggestions:
            console.print("\n[italic]Suggestions:[/]")
            for i, sugg in enumerate(suggestions, 1):
                console.print(f"  {i}. {sugg}")
            console.print("")

    def _handle_config(self, args):
        """Handle configuration commands."""
        parts = args.split()
        if not parts:
            cli.log("Usage: config <subcommand> [args]", "warning")
            cli.log("Subcommands: model", "info")
            return

        subcmd = parts[0].lower()
        
        if subcmd == "model":
            if len(parts) < 3:
                cli.log("Usage: config model <provider> <model_name>", "warning")
                cli.log("Providers: gemini, openai, anthropic, ollama, puter", "info")
                return
            
            provider = parts[1].lower()
            model = parts[2]
            
            valid_providers = ["gemini", "openai", "anthropic", "ollama", "puter"]
            if provider not in valid_providers:
                 cli.log(f"Invalid provider. Choose from: {', '.join(valid_providers)}", "error")
                 return

            # Load and update config
            config_path = os.path.expanduser("~/.stingbot2.json")
            try:
                data = {}
                if os.path.exists(config_path):
                    with open(config_path, "r") as f:
                        data = json.load(f)
                
                data["LLM_PROVIDER"] = provider
                data["LLM_MODEL"] = model
                
                with open(config_path, "w") as f:
                    json.dump(data, f, indent=4)
                    
                cli.log(f"Configuration updated: Provider={provider}, Model={model}", "success")
                cli.log("Please RESTART Stingbot to apply changes.", "action")
            except Exception as e:
                cli.log(f"Failed to update config: {e}", "error")
        else:
             cli.log(f"Unknown configuration command: {subcmd}", "warning")

    def _show_banner(self):
        cli.banner()
        console.print(Align.center(Panel("[bold white]STING NEURAL ARCHITECTURE: AUTONOMOUS MODE[/]", border_style=COLOR_SECONDARY, expand=False)))
        cli.log("Talk to Sting naturally. Type 'help' for commands.\n")

    def _show_help(self):
        cli.log("Commands:", "info")
        cli.log("  (Just type)     : Chat with Sting or give instructions")
        cli.log("  graph           : View attack graph")
        cli.log("  memory          : View agent memory stats")
        cli.log("  clear           : Clear screen")
        cli.log("  exit            : Quit")
