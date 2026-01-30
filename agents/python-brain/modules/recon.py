from core.system_agent import SystemAgent

class ReconModule:
    """Wrapper for Reconnaissance Tools (Nmap, Subfinder)."""
    
    def __init__(self, sys_agent):
        self.sys = sys_agent

    def scan(self, target):
        """Perform an Nmap scan."""
        # Simple Nmap for now (Safe Mode is handled by SystemAgent)
        print(f"[*] Recon: Scanning {target}...")
        cmd = f"nmap -F {target}" # Fast scan
        return self.sys.execute(cmd)

    def subdomains(self, domain):
        """Find subdomains."""
        # Placeholder for subfinder integration
        return self.sys.execute(f"echo 'Mock Subdomains for {domain}'")
