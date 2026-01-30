import json

class ToolWrappers:
    """Standardizes CLI tool outputs into clean JSON for agents."""

    @staticmethod
    def parse_nmap(output):
        # Very simple heuristic parser for demonstration
        ports = []
        for line in output.split("\n"):
            if "/tcp" in line and "open" in line:
                ports.append(line.strip())
        return {"open_ports": ports}

    @staticmethod
    def parse_sqlmap(output):
        is_vuln = "is vulnerable" in output.lower()
        return {"vulnerable": is_vuln, "raw_signal": "VULN_FOUND" if is_vuln else "SAFE"}

    @staticmethod
    def wrap(tool_name, raw_output):
        if tool_name == "nmap": return ToolWrappers.parse_nmap(raw_output)
        if tool_name == "sqlmap": return ToolWrappers.parse_sqlmap(raw_output)
        return {"raw": raw_output[:500]}
