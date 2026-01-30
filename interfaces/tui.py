from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Log, Input, Static
from textual.containers import Vertical
from core.orchestrator import CoreOrchestrator

class StingbotDashboard(App):
    CSS = """
    Screen { background: #0a0a0a; }
    #log { border: solid #ff0055; height: 1fr; background: #0f172a; color: #00f2ff; }
    #input { dock: bottom; border: double #bc00ff; background: #1e293b; color: white; }
    .header { text-align: center; color: #ff0055; padding: 1; border-bottom: solid #00f2ff; text-style: bold; }
    """

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Vertical(
            Static("S T I N G B O T // M I S S I O N  C O N T R O L", classes="header"),
            Log(id="log"),
            Input(placeholder="Command Intent...", id="input")
        )
        yield Footer()

    def on_mount(self):
        self.orchestrator = CoreOrchestrator()
        self.query_one(Log).write("Stingbot System Online.")

    def on_input_submitted(self, event: Input.Submitted):
        cmd = event.value
        self.query_one(Input).value = ""
        self.query_one(Log).write(f"> {cmd}")
        
        # Process in background (simplified for sync)
        res = self.orchestrator.process_input(cmd)
        self.query_one(Log).write(str(res))

if __name__ == "__main__":
    StingbotDashboard().run()
