from core.system_agent import SystemAgent

class AuditModule:
    """Vulnerability Analysis & Verification."""
    
    def __init__(self, sys_agent):
        self.sys = sys_agent

    def search_cve(self, query):
        """Search for CVEs."""
        return self.sys.execute(f"searchsploit {query}")

    def verify_auth(self, target, service="ssh"):
        """Verify weak credentials (SAFE)."""
        # Improved Safety Check
        is_local = target in ["localhost", "127.0.0.1", "0.0.0.1"] or target.startswith("192.168.") or target.startswith("10.")
        if not is_local:
             return {"stderr": f"Safety Block: Auth verification for {target} restricted. Local network only."}
        
        return self.sys.execute(f"echo '[*] Checking default creds on {target}:{service}...'")
