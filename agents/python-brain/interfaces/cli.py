from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text
from rich.live import Live
from rich.table import Table
from rich.columns import Columns
from rich.align import Align
from config.settings import config
import time

console = Console()

# Premium Color Palette (HSL inspired)
COLOR_PRIMARY = "#ff0055"  # Vibrant Neon Pink/Red
COLOR_SECONDARY = "#00f2ff" # Electric Cyan
# Master Color Palette (High-Fidelity Style)
COLOR_PRIMARY = "#ff0055"  # Neon Red/Pink
COLOR_SECONDARY = "#00f2ff" # Cyan
COLOR_ACCENT = "#bc00ff"    # Purple
COLOR_BG = "#0a0a0a"

SCORPION_LOGO = r"""
           ___
        .-'   `'.
       /         \
       |         |
       |         |             __
        \       /           .-'  `'.
         `'---'`           /        \
                          |          |
                          |   _      |
                           \ ( \     /
        _        _         _`'__`'--'`
       ( \      / )    _  / /  \ \
        \ \    / /    / / \ \__/ /
         \ \  / /    / /   `'--'`
          \ \/ /    / /
           \  /    / /
            ||    / /
            ||   / /
            ||  / /
            || / /
            ||/ /
            |  /
            |_/ 
     [ STING NEURAL ENGINE // v2.0 ]
"""

class CLI:
    def banner(self):
        banner_text = Text(SCORPION_LOGO, style=f"bold {COLOR_PRIMARY}")
        console.print(Align.center(banner_text))

    def doctor_report(self, checks):
        """Structured box-drawing report mirroring Stingbot Doctor exactly."""
        console.print(f"┌  [bold white]Stingbot doctor[/]")
        console.print("│")
        
        for title, info in checks.items():
            status = info.get("status", "info")
            color = COLOR_SECONDARY if status == "success" else COLOR_PRIMARY
            
            # Dynamic horizontal line to fill the space
            header_line = "─" * (68 - len(title))
            console.print(f"◇  [bold {color}]{title}[/] {header_line}╮")
            
            for line in info.get("messages", []):
                console.print(f"│  {line}")
                
            console.print(f"├" + "─" * 70 + "╯")
            console.print("│")
            
        console.print("└  [bold green]Doctor complete.[/]")

    def ask_confirm(self, question):
        """Interactive Yes/No prompt mirroring Stingbot standard."""
        console.print(f"◆  [bold white]{question}[/]")
        console.print("│  [bold cyan]● Yes[/] / [dim]○ No[/]")
        choice = Prompt.ask("└ ", choices=["y", "n", "Yes", "No"], default="y")
        return choice.lower().startswith('y')


    def mission_start(self, objective):
        console.rule(f"[bold {COLOR_SECONDARY}] ACTION INITIALIZED: {objective.upper()} [/]")

    def log(self, message, style="white"):
        # Custom logging with timestamps and symbols
        ts = time.strftime("%H:%M:%S")
        prefix = f"[dim][{ts}][/] "
        
        # High-Fidelity Status Icons
        if style == "success": 
            icon = f"[bold green]✓[/] "
            style = "white"
        elif style == "error": 
            icon = "[bold red]✘[/] "
            style = "bold red"
        elif style == "info": 
            icon = f"[{COLOR_SECONDARY}]→[/] "
            style = "dim"
        elif style == "warning":
            icon = "[bold yellow]![/] "
            style = "yellow"
        else: 
            icon = f"[{COLOR_PRIMARY}]»[/] "
            
        console.print(f"{prefix}{icon}[{style}]{message}[/]")

    def pairing_sequence(self):
        """First-time pairing experience similar to Stingbot 1.0."""
        self.log("Establishing Secure Pairing with Neural Engine...", "info")
        time.sleep(0.5)
        self.log("Detected local security environment.", "success")
        self.log("Pairing codes exist because even bots believe in consent—and good security hygiene.", "info")
        
        pairing_code = f"{int(time.time()) % 10000:04d}"
        console.print(Panel(f"[bold white]PAIRING CODE: {pairing_code}[/]", border_style=COLOR_SECONDARY, expand=False))
        
        self.log("Neural link ready for authorization.", "success")

    def mission_end(self, result):
        console.rule(f"[bold {COLOR_PRIMARY}] ACTION CONCLUDED [/]")

    def input(self, prompt_text="stingbot"):
        return Prompt.ask(f"[bold {COLOR_PRIMARY}]{prompt_text}[/] [bold white]❯[/]")

cli = CLI()

