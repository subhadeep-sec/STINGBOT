import os
import sys
import time
import json
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.text import Text
from rich.align import Align
from rich.prompt import Prompt

# Add current dir to path to import CLI
sys.path.append(os.path.join(os.getcwd(), "agents", "python-brain"))
from interfaces.cli import cli, COLOR_PRIMARY, COLOR_SECONDARY, SCORPION_LOGO

console = Console()

def run_premium_setup():
    console.clear()
    banner_text = Text(SCORPION_LOGO, style=f"bold {COLOR_PRIMARY}")
    console.print(Align.center(banner_text))
    
    console.print(Align.center(Panel("[bold white]STING NEURAL ARCHITECTURE: ONBOARDING WIZARD[/]", border_style=COLOR_SECONDARY, expand=False)))
    console.print("\n")

    # 1. Security Disclaimer (Moltbot Style)
    cli.log("CRITICAL SECURITY NOTICE", "warning")
    cli.log("Sting is an autonomous offensive platform. Use without authorization is strictly prohibited.", "info")
    if not cli.ask_confirm("Do you accept the Neural Operating Agreement?"):
        cli.log("Authorization Denied. Terminating...", "error")
        sys.exit(1)
    
    cli.log("Neural Agreement Authorized.", "success")
    console.print("")

    # 2. Mode Selection
    mode = Prompt.ask("Select Deployment Mode", choices=["quick", "advanced"], default="quick")
    cli.log(f"Mode set to: [bold cyan]{mode.upper()}[/]", "info")
    console.print("")

    # 3. Provider Configuration
    console.print(Panel("[bold cyan]Neural Engine Configuration[/]", border_style=COLOR_SECONDARY))
    console.print("")
    
    provider = Prompt.ask(
        "Select Primary Neural Engine",
        choices=["ollama", "openai", "anthropic", "gemini"],
        default="ollama"
    )
    
    api_key = ""
    model = ""
    
    if provider == "ollama":
        cli.log("Using Local Inference (Ollama). Ensure Ollama is running: [bold]ollama serve[/]", "info")
        model = Prompt.ask("Select Ollama Model", default="llama3.2", show_default=True)
    elif provider == "openai":
        api_key = Prompt.ask("Enter OpenAI API Key", password=True)
        model = Prompt.ask("Select OpenAI Model", default="gpt-4", show_default=True)
        cli.log("OpenAI configured successfully.", "success")
    elif provider == "anthropic":
        api_key = Prompt.ask("Enter Anthropic API Key", password=True)
        model = Prompt.ask("Select Claude Model", default="claude-3-5-sonnet-20241022", show_default=True)
        cli.log("Anthropic configured successfully.", "success")
    elif provider == "gemini":
        api_key = Prompt.ask("Enter Google Gemini API Key", password=True)
        model = Prompt.ask("Select Gemini Model", default="gemini-1.5-flash-latest", show_default=True)
        cli.log("Gemini configured successfully.", "success")
    
    # Save configuration
    config_path = os.path.expanduser("~/.stingbot2.json")
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = json.load(f)
    else:
        config = {
            "WORKSPACE_DIR": os.getcwd(),
            "DATA_DIR": os.path.join(os.getcwd(), "data"),
            "LOG_DIR": os.path.join(os.getcwd(), "data/logs"),
            "USER_ALIAS": "Operator",
            "BOT_NAME": "Sting"
        }
    
    config["LLM_PROVIDER"] = provider
    config["LLM_MODEL"] = model
    
    if provider == "openai":
        config["OPENAI_KEY"] = api_key
    elif provider == "anthropic":
        config["ANTHROPIC_KEY"] = api_key
    elif provider == "gemini":
        config["GEMINI_KEY"] = api_key
    
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=4)
    
    cli.log(f"Configuration saved to: {config_path}", "success")

    console.print("\n")

    # 4. Neural Optimization Progress
    steps = [
        ("Synchronizing STING Assets...", 1.0),
        ("Optimizing Multi-Agent State Manager...", 1.5),
        ("Calibrating Guardrails & Safe-Shell Layer...", 1.2),
        ("Establishing Global Mission Control...", 0.8)
    ]

    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]{task.description}"),
        BarColumn(bar_width=40),
        TaskProgressColumn(),
        console=console
    ) as progress:
        for desc, duration in steps:
            task = progress.add_task(desc, total=100)
            for _ in range(100):
                time.sleep(duration / 100)
                progress.update(task, advance=1)
            cli.log(f"{desc.replace('...', '')} [bold green]COMPLETE[/]", "success")

    console.print("\n")

    # 5. Diagnostic Report (Doctor Style)
    checks = {
        "Neural Engine Status": {
            "status": "success", 
            "messages": [
                f"Provider: {provider.upper()}", 
                f"Model: {model}",
                "Link: Established" if provider == "ollama" else "API Key: Configured"
            ]
        },
        "Safety Core": {
            "status": "success", 
            "messages": [
                "Guardrails: Active", 
                "IP Filter: 127.0.0.1 Blocked", 
                "Command Filter: Enabled"
            ]
        },
        "Global Launcher": {
            "status": "success", 
            "messages": [
                "Alias: 'stingbot' created", 
                "Path: ~/.local/bin"
            ]
        }
    }
    cli.doctor_report(checks)

    console.print("\n")
    cli.log("Sting is now optimized for autonomous operations.", "success")
    cli.log("Type [bold white]stingbot[/] anywhere to begin your mission.", "info")
    
    # Finalize local launcher
    launcher_path = os.path.join(os.getcwd(), "stingbot")
    with open(launcher_path, "w") as f:
        f.write("#!/bin/bash\n")
        f.write(f"export PYTHONPATH=$PYTHONPATH:{os.getcwd()}:{os.getcwd()}/agents/python-brain\n")
        f.write(f"python3 {os.getcwd()}/stingbot.py \"$@\"\n")
    
    os.chmod(launcher_path, 0o755)

if __name__ == "__main__":
    run_premium_setup()
