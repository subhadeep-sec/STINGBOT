import re
import ipaddress

class Guardrails:
    """Safety layer: Deterministic filters for prohibited actions and targets."""
    
    def __init__(self):
        # Prohibited command patterns (regex)
        self.blacklisted_commands = [
            r"rm\s+-rf\s+/",
            r"mkfs",
            r"dd\s+if=.*of=/dev/sd",
            r":\(\)\{\s+:\|\:&\s+\}\s*;", # fork bomb
            r"chattr\s+-i",
            r"mv\s+/.* /dev/null",
            r"chmod\s+-R\s+777\s+/",
            r"\|\s*bash",
            r"\|\s*sh"
        ]
        
        # Prohibited IP ranges (e.g., Critical Infrastructure, Gov, etc.)
        # Default: Allow everything except common sensitive local ranges if needed
        # In a real scenario, this would include specific CIDRs.
        self.prohibited_ips = [
            "127.0.0.0/8",   # Localhost (optional, depending on use case)
            "169.254.0.0/16" # Link-local
        ]

    def is_command_safe(self, command):
        """Check if a shell command matches any blacklisted patterns."""
        for pattern in self.blacklisted_commands:
            if re.search(pattern, command, re.IGNORECASE):
                return False, f"Command contains blacklisted pattern: {pattern}"
        return True, "Safe"

    def is_target_safe(self, target):
        """Check if the target IP/Domain is in a prohibited range."""
        try:
            # Handle IP addresses
            ip = ipaddress.ip_address(target)
            for network in self.prohibited_ips:
                if ip in ipaddress.ip_network(network):
                    return False, f"Target {target} is in prohibited range {network}"
        except ValueError:
            # Handle Hostnames/Domains (Simple check for now, can be expanded with DNS)
            if target.lower() in ["localhost", "127.0.0.1"]:
                 return False, "Target is localhost."
        
        return True, "Safe"

    def filter_action(self, action_type, payload):
        """Higher-level filter for various action types."""
        if action_type == "terminal":
            return self.is_command_safe(payload)
        if action_type in ["scan", "exploit", "target"]:
            return self.is_target_safe(payload)
        return True, "Safe"
