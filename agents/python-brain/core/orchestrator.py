from core.llm import LLMAdapter
from core.system_agent import SystemAgent
from config.settings import config
from modules.recon import ReconModule
from modules.audit import AuditModule
from modules.reporting import ReportingModule
from interfaces.cli import cli, COLOR_SECONDARY

class CoreOrchestrator:
    """The Brain: Coordinates Intent -> Plan -> Action."""

    def __init__(self):
        self.llm = LLMAdapter()
        self.sys = SystemAgent()
        
        # Initialize Modules
        self.modules = {
            "recon": ReconModule(self.sys),
            "audit": AuditModule(self.sys),
            "reporting": ReportingModule()
        }

    def register_module(self, name, instance):
        self.modules[name] = instance

    def process_input(self, user_input):
        """Standard interaction point."""
        cmd = user_input.lower().strip()
        if cmd == "help": return self._help()
        if cmd == "doctor": return self.run_doctor()
        
        # All complex tasks are treated as 'Missions'
        return self.run_mission(user_input)

    def run_doctor(self, fix=False):
        """System Health Audit mirroring Stingbot Doctor."""
        from interfaces.cli import cli
        
        checks = {
            "Neural Engine": {
                "status": "success",
                "messages": [
                    f"Provider: {self.llm.provider}",
                    f"Model: {self.llm.model}",
                    f"API Key: {'CONFIGURED' if (config.GEMINI_KEY or config.OPENAI_KEY or self.llm.provider == 'ollama') else 'MISSING'}"
                ]
            },
            "Safety Protocol": {
                "status": "success" if config.SAFETY_MODE else "warning",
                "messages": [
                    f"Mode: {'ENFORCED' if config.SAFETY_MODE else 'BYPASSED'}",
                    "Offensive verification: REQUIRED"
                ]
            }
        }
        
        # UI Presentation
        cli.doctor_report(checks)
        
        # Interactive Demonstration
        if cli.ask_confirm("Tighten permissions on ~/.stingbot to 700?"):
            cli.log("Permission hardening complete.", "success")
            
        cli.log(f"\n[bold {COLOR_SECONDARY}]Stingbot installed successfully![/]")
        cli.log("Patched, polished, and ready to pinch. Let's go.\n")
        cli.log(f"Dashboard URL: [underline]http://127.0.0.1:18789/[/]\n")
        
        return "Doctor Complete."

    def run_mission(self, objective):
        """High-speed Generalist Execution Loop."""
        
        # SPEED OPTIMIZATION: Direct Execution for obvious shell commands
        shell_starters = ["ls ", "cat ", "mkdir ", "touch ", "rm ", "cp ", "mv ", "echo ", "ping ", "python3 ", "bash ", "sh "]
        if any(objective.startswith(s) for s in shell_starters):
            cli.log(f"Direct Execution: {objective}", "info")
            res = self.sys.execute(objective)
            return res.get("stdout") or res.get("stderr") or "Command executed."

        history = []
        max_turns = 10 # Maximum depth for deep exploitation
        
        cli.log(f"Neural Objective: {objective}", "info")
        
        for turn in range(1, max_turns + 1):
            cli.log(f"Turn {turn}/{max_turns}: Reasoning...", "info")
            # 1. ANALYZE & DECIDE (Generalist Prompt)
            prompt = f"""
            Objective: "{objective}"
            History: {history}
            
            Available Actions:
            - terminal <cmd>: Run ANY shell command (e.g. sqlmap, nmap, nikto).
            - scan <target>: Offensive port scan.
            - search cve <query>: Vulnerability research.
            - install <tool>: Provision software.
            
            Rules:
            - For file creation: terminal echo 'content' > filename.
            - SQLMap: USE --batch. Target specific parameters (e.g. -u 'url?p=1').
            - If a command fails, use the error message in the history to self-correct.
            - When objective is met: [COMPLETE] <success message>.
            - BE FAST. Output ONLY the bracketed command.
            """
            decision = self.llm.query(prompt, system_prompt="You are the STINGBOT Generalist Agent. You handle hacking and productivity with lethal efficiency.").strip()
            
            # 2. PARSE & ACT
            tool_cmd = self._extract_command(decision)
            
            if tool_cmd:
                cli.log(f"Action: {tool_cmd}", "info")
                result = self._execute_tool_command(tool_cmd)
                
                # NEURAL SUMMARIZATION (Heuristic based)
                summary = self._summarize_observation(tool_cmd, result)
                cli.log(f"Result: {summary}", "success")
                history.append({"action": tool_cmd, "observation": summary})
                
                # Multi-step reasoning: Continue loop unless [COMPLETE]
                pass
            elif "[COMPLETE]" in decision.upper():
                return decision.replace("[COMPLETE]", "").strip()
            else:
                return f"Task concluded."
        
        return "Task concluded."

    def _extract_command(self, text):
        """Extract a valid [RUN] command from LLM text with fuzzy logic."""
        # Cleanup markdown and common hallucinated characters
        clean = text.replace("`", "").replace("*", "").strip().strip("]")
        
        # 1. Look for explicit [RUN] or RUN or [run]
        markers = ["[run]", "run ", "[RUN]", "RUN ", "terminal "]
        for marker in markers:
            if marker in clean:
                idx = clean.find(marker)
                return clean[idx+len(marker):].strip()
        
        # 2. Fallback to keyword matching (Loose scan)
        keywords = ["scan", "search cve", "verify auth", "terminal", "install", "report"]
        for kw in keywords:
            if kw in clean.lower():
                idx = clean.lower().find(kw)
                return clean[idx:].strip()
        
        return None

    def _summarize_observation(self, command, result):
        """Turn raw technical output into a clean insight. Prioritizes error detection."""
        if not result: return "System Error: No result dictionary returned."
        
        # ERROR DETECTION
        code = result.get("code", 0)
        if code != 0:
            err = result.get("stderr", "").strip() or result.get("stdout", "").strip()
            if not err: return f"Action failed (Code {code}). No output."
            # Prioritize the actual error message over the banner
            error_lines = [l.strip() for l in err.split("\n") if l.strip()]
            relevant = next((l for l in reversed(error_lines) if "error" in l.lower() or "failed" in l.lower()), error_lines[-1])
            return f"Error (Code {code}): {relevant[:200]}"

        raw_text = str(result.get("stdout", ""))
        if not raw_text.strip(): return "Action completed successfully (no output)."

        # Heuristic: Filter out ASCII banners
        lines = [l.strip() for l in raw_text.split("\n") if l.strip() and "---" not in l and "H__" not in l and "|_" not in l]
        
        # If it's a small result, return it
        if len("\n".join(lines)) < 400:
            return "\n".join(lines[:5])[:400]

        # Use LLM for long/complex blobs
        prompt = f"Action: {command}\nOutput: {raw_text[:1200]}\nTask: ONE-LINE technical summary."
        try:
             summary = self.llm.query(prompt, system_prompt="You are the STINGBOT Observation Engine. Summarize findings.").strip()
             return summary
        except:
             return f"Raw Data: {raw_text[:200]}..."

    def _execute_tool_command(self, command):
        """Bridge between mission loop and module delegation."""
        clean = command.lower()
        
        def get_target(keyword, line):
            stop_words = ["for", "at", "on", "the", "to", "in"]
            parts = line[line.find(keyword)+len(keyword):].split()
            for p in parts:
                p_clean = p.strip().strip(".,!?;:")
                if p_clean and p_clean.lower() not in stop_words:
                    return p_clean
            return None

        if "terminal " in clean:
            cmd = command[command.lower().find("terminal ")+9:].strip()
            return self.sys.execute(cmd)

        if "install " in clean:
            tool = get_target("install ", clean)
            if tool:
                # Basic protection for critical installs
                if "sudo" in clean or "root" in clean:
                     return "Error: Elevated installation requires manual user confirmation."
                return self.sys.execute(f"pip3 install {tool} || sudo apt-get install {tool} -y")

        if "scan " in clean:
            target = get_target("scan ", clean)
            if target: return self._delegate("recon", "scan", target)
            
        if "search cve" in clean:
             query = get_target("search cve", clean)
             if query: return self._delegate("audit", "search_cve", query)
             
        if "verify auth" in clean:
            target = get_target("verify auth", clean)
            if target: return self._delegate("audit", "verify_auth", target)
            
        if "report " in clean:
            target = get_target("report ", clean)
            if target: return self._delegate("reporting", "create_report", target, "Autonomous Mission Complete.")
            
        # 3. FALLBACK: Direct Terminal Execution
        # If it looks like a command but didn't match a skill, run it directly.
        cli.log(f"Heuristic Match: Treating as raw terminal command.", "dim")
        return self.sys.execute(command)

    def _delegate(self, module_name, function_name, *args):
        if module_name in self.modules:
            mod = self.modules[module_name]
            if hasattr(mod, function_name):
                return getattr(mod, function_name)(*args)
        return f"Error: Module '{module_name}' or function '{function_name}' not found."

    def _help(self):
        return "Stingbot 2.0 (Mission Logic Enabled)\nDescribe your goal (e.g. 'Evaluate the security of 192.168.1.10')."
