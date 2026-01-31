from agents.base_agent import BaseAgent
import os

class RevEngineer(BaseAgent):
    """Specialist for binary analysis and reverse engineering."""
    
    def __init__(self):
        super().__init__("Reverse Engineer", "Logic for Ghidra, Radare2, and binary auditing.")
        self.analysis_history = []

    def execute(self, task):
        """Execute reverse engineering tasks with multi-step analysis."""
        
        # 1. ANALYZE TASK & SELECT TOOL
        prompt = f"""
        Reverse Engineering Task: {task}
        Previous Analysis: {self.analysis_history[-3:] if self.analysis_history else 'None'}
        
        Available Tools and Use Cases:
        - strings <file>: Extract readable strings (first step for unknown binaries)
        - file <file>: Identify file type and architecture
        - readelf -h <file>: ELF header information
        - objdump -d <file>: Disassemble binary
        - objdump -t <file>: Symbol table
        - r2 -c "aaa; afl" <file>: Radare2 function analysis
        - r2 -c "aaa; pdf @main" <file>: Disassemble main function
        - r2 -c "aaa; iz" <file>: Strings in data sections
        - nm <file>: List symbols
        - ltrace <file>: Library call tracing
        - strace <file>: System call tracing
        - checksec --file=<file>: Security features check (NX, PIE, etc.)
        - gdb -batch -ex "info functions" <file>: List functions via GDB
        
        Output ONLY the command to run, or [COMPLETE] if analysis is sufficient.
        Choose the most appropriate tool for the current analysis stage.
        """
        decision = self.reason(prompt).strip()
        
        if "[COMPLETE]" in decision.upper():
            return {
                "status": "complete",
                "summary": decision,
                "history": self.analysis_history
            }

        # 2. CLEAN AND VALIDATE COMMAND
        cmd = self._clean_command(decision)
        
        if not cmd:
            return {
                "status": "failed",
                "cmd": decision,
                "summary": "Failed to parse valid command from LLM response."
            }

        # 3. RUN COMMAND
        result = self.run_cmd(cmd)
        
        # 4. SUMMARIZE FINDINGS
        summary = self.summarize_result(cmd, result)
        
        # Store in analysis history for multi-step reasoning
        self.analysis_history.append({
            "cmd": cmd,
            "summary": summary[:200],
            "success": result.get("code") == 0
        })
        
        return {
            "status": "success" if result.get("code") == 0 else "failed",
            "cmd": cmd,
            "stdout": result.get("stdout"),
            "stderr": result.get("stderr"),
            "summary": summary
        }

    def _clean_command(self, text):
        """Extract and sanitize command from LLM response."""
        # Remove markdown artifacts
        clean = text.replace("`", "").replace("*", "").strip()
        
        # Take first line only (LLM might add explanations)
        cmd = clean.split("\n")[0].strip()
        
        # Basic validation - must contain a known tool
        valid_tools = ["strings", "file", "readelf", "objdump", "r2", "radare2", 
                       "nm", "ltrace", "strace", "checksec", "gdb", "hexdump", 
                       "xxd", "binwalk"]
        
        if any(tool in cmd.lower() for tool in valid_tools):
            return cmd
        
        return None

    def analyze_binary(self, filepath):
        """High-level method for comprehensive binary analysis."""
        if not os.path.exists(filepath):
            return {"status": "failed", "summary": f"File not found: {filepath}"}
        
        # Reset history for new analysis
        self.analysis_history = []
        
        # Run standard analysis pipeline
        results = []
        
        # Step 1: File identification
        results.append(self.execute(f"Identify the file type of {filepath}"))
        
        # Step 2: String extraction
        results.append(self.execute(f"Extract interesting strings from {filepath}"))
        
        # Step 3: Security analysis
        results.append(self.execute(f"Check security features of binary {filepath}"))
        
        # Step 4: Function analysis
        results.append(self.execute(f"List and analyze functions in {filepath}"))
        
        return {
            "status": "complete",
            "filepath": filepath,
            "results": results,
            "history": self.analysis_history
        }
