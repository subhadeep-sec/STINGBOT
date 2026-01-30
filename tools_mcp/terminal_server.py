import subprocess
import os
from orchestrator.guardrails import Guardrails

class TerminalServer:
    """Safe shell execution interface for agents."""
    
    def __init__(self):
        self.guard = Guardrails()

    def execute(self, cmd, timeout=300):
        # 1. APPLY GUARDRAILS
        safe, reason = self.guard.filter_action("terminal", cmd)
        if not safe:
            return {"stdout": "", "stderr": f"SECURITY BLOCK: {reason}", "code": 1}

        # 2. EXECUTE
        try:
            # Note: In production, this would run inside a Docker container
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
            return {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "code": result.returncode
            }
        except subprocess.TimeoutExpired:
            return {"stdout": "", "stderr": "Execution TImeout", "code": -1}
        except Exception as e:
            return {"stdout": "", "stderr": str(e), "code": -1}
