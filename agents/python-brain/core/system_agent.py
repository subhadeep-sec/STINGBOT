import subprocess
import os
from config.settings import config

class SystemAgent:
    """Safe abstraction for OS interactions."""
    
    def __init__(self):
        self.safety_mode = config.SAFETY_MODE

    def execute(self, cmd):
        """Run a shell command safely."""
        # Safety Protocol
        if self.safety_mode:
            forbidden = ["rm -rf", "mkfs", ":(){ :|:& };:"]
            if any(f in cmd for f in forbidden):
                return {"stdout": "", "stderr": "Command blocked by Safety Protocol.", "code": 1}

        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=300)
            return {
                "stdout": result.stdout, 
                "stderr": result.stderr, 
                "code": result.returncode
            }
        except Exception as e:
            return {"stdout": "", "stderr": str(e), "code": -1}

    def check_tool(self, tool_name):
        """Verify if a tool is installed."""
        return self.execute(f"which {tool_name}").get("code") == 0
