import sys
import os
from interfaces.cli import cli, console, COLOR_SECONDARY
from rich.panel import Panel
from rich.align import Align
from orchestrator.supervisor import Supervisor

class MASTerminal:
    """Session-based Interactive Terminal for Stingbot MAS."""

    def __init__(self, workspace_path):
        self.workspace = workspace_path
        self.supervisor = Supervisor(workspace_path)
        # We'll need to re-register agents if we want them to stay alive, 
        # or just register them once here.
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
        cli.banner()
        console.print(Align.center(Panel("[bold white]STING NEURAL ARCHITECTURE: VERSION 2.0.0[/]", border_style=COLOR_SECONDARY, expand=False)))
        cli.log("Type 'mission <goal>' to start, 'graph' to see state, or 'exit' to quit.\n")

        while True:
            try:
                user_input = cli.input("mas-terminal").strip()
                if not user_input: continue
                
                cmd_parts = user_input.split(" ", 1)
                cmd = cmd_parts[0].lower()
                args = cmd_parts[1] if len(cmd_parts) > 1 else ""

                if cmd in ['exit', 'quit']:
                    cli.log("Disconnecting from MAS Neural Link...", "info")
                    break
                elif cmd == 'help':
                    self._show_help()
                elif cmd == 'mission':
                    if not args:
                        cli.log("Error: Mission objective required.", "error")
                    else:
                        try:
                            cli.mission_start(args)
                            result = self.supervisor.run_mission(args)
                            cli.log(result, "success")
                            cli.mission_end(result)
                        except KeyboardInterrupt:
                            cli.log("\nMission aborted by operator.", "warning")
                        except Exception as e:
                            cli.log(f"Mission failed: {str(e)}", "error")
                            cli.log("The system remains operational. Try a different objective.", "info")
                elif cmd == 'graph':
                    summary = self.supervisor.state.export_summary()
                    cli.log(f"Attack Graph Summary: {summary}", "info")
                elif cmd == 'memory':
                    cli.log(f"Volatile Memory: {self.supervisor.state.memory}", "info")
                else:
                    # Treat unknown input as a mission objective for speed
                    try:
                        cli.mission_start(user_input)
                        result = self.supervisor.run_mission(user_input)
                        cli.log(result, "success")
                        cli.mission_end(result)
                    except KeyboardInterrupt:
                        cli.log("\nMission aborted by operator.", "warning")
                    except Exception as e:
                        cli.log(f"Command failed: {str(e)}", "error")
                        cli.log("Type 'help' for available commands.", "info")

            except KeyboardInterrupt:
                cli.log("\nEmergency Disconnect.", "error")
                break
            except Exception as e:
                cli.log(f"Terminal Error: {str(e)}", "error")

    def _show_help(self):
        cli.log("MAS Control Commands:", "info")
        cli.log("  mission <goal>  : Start a new Multi-Agent mission")
        cli.log("  graph           : View the current attack graph summary")
        cli.log("  memory          : View short-term mission memory")
        cli.log("  clear           : Reset the current mission state")
        cli.log("  exit            : Disconnect from MAS")
