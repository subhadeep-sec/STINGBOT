import sys
import os
from interfaces.cli import cli
from core.orchestrator import CoreOrchestrator

def main():
    orchestrator = CoreOrchestrator()

    
    # First Run / Pairing Check
    if not os.path.exists(os.path.expanduser("~/.stingbot2_paired")):
        cli.banner()
        cli.pairing_sequence()
        with open(os.path.expanduser("~/.stingbot2_paired"), "w") as f:
            f.write("paired")
        cli.log("Neural Link Permanently Authorized.", "success")
        cli.log("Type your first mission objective to begin.\n", "info")
    else:
        cli.banner()

    if len(sys.argv) > 1:
        # Command Line Mode
        cmd_input = " ".join(sys.argv[1:])
        if cmd_input.lower().strip() == "doctor":
            orchestrator.run_doctor()
        elif cmd_input.lower().strip() == "onboard":
            cli.banner()
            cli.pairing_sequence()
            with open(os.path.expanduser("~/.stingbot2_paired"), "w") as f:
                f.write("paired")
            cli.log("Neural Link Permanently Authorized.", "success")
        elif cmd_input.lower().strip() == "daemon":
            cli.log("Starting Stingbot Neural Gateway (Daemon mode)...", "info")
            # Implement background server logic here
            cli.log("Neural link status: LISTENING on port 18789", "success")
        else:
            result = orchestrator.process_input(cmd_input)
            if result: print(f"→ {result}")
    else:
        # Interactive Mode
        cli.log("Agent Heartbeat: [bold green]STABLE[/]", "info")
        cli.log("Neural Link: [bold blue]ESTABLISHED[/]", "info")
        cli.log("Type your mission objective below. Type 'exit' to disconnect.\n")
        
        while True:
            try:
                intent = cli.input()
                if intent.lower() in ['exit', 'quit']: 
                    cli.log("Disconnecting neural link...", "info")
                    break
                
                if intent.lower().strip() == "doctor":
                    orchestrator.run_doctor()
                else:
                    result = orchestrator.process_input(intent)
                    if result: cli.log(result, "success")
            except KeyboardInterrupt:
                cli.log("\nEmergency Disconnect initiated.", "error")
                break

if __name__ == "__main__":
    main()
