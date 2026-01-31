import json
import re

class ToolWrappers:
    """Standardizes CLI tool outputs into clean JSON for agents."""

    @staticmethod
    def parse_nmap(output):
        """Parse nmap output into structured data."""
        result = {
            "open_ports": [],
            "hosts": [],
            "services": [],
            "os_detection": None
        }
        
        current_host = None
        for line in output.split("\n"):
            line = line.strip()
            
            # Host detection
            if "Nmap scan report for" in line:
                match = re.search(r'for\s+(\S+)', line)
                if match:
                    current_host = match.group(1)
                    result["hosts"].append(current_host)
            
            # Port detection
            if "/tcp" in line or "/udp" in line:
                parts = line.split()
                if len(parts) >= 3 and ("open" in line or "filtered" in line):
                    port_info = {
                        "port": parts[0],
                        "state": parts[1],
                        "service": parts[2] if len(parts) > 2 else "unknown",
                        "version": " ".join(parts[3:]) if len(parts) > 3 else "",
                        "host": current_host
                    }
                    result["open_ports"].append(port_info)
                    if port_info["state"] == "open":
                        result["services"].append(f"{port_info['service']}:{port_info['port']}")
            
            # OS detection
            if "OS details:" in line or "Running:" in line:
                result["os_detection"] = line.split(":", 1)[1].strip() if ":" in line else line
        
        return result

    @staticmethod
    def parse_sqlmap(output):
        """Parse sqlmap output for vulnerabilities."""
        result = {
            "vulnerable": False,
            "injection_types": [],
            "parameters": [],
            "dbms": None,
            "databases": [],
            "tables": []
        }
        
        output_lower = output.lower()
        
        # Vulnerability detection
        if "is vulnerable" in output_lower or "injectable" in output_lower:
            result["vulnerable"] = True
        
        # Injection type detection
        injection_types = ["boolean-based", "time-based", "error-based", "union-based", "stacked queries"]
        for inj_type in injection_types:
            if inj_type in output_lower:
                result["injection_types"].append(inj_type)
        
        # Parameter detection
        param_match = re.findall(r"Parameter:\s*(\S+)", output)
        result["parameters"] = list(set(param_match))
        
        # DBMS detection
        dbms_match = re.search(r"back-end DBMS:\s*(.+)", output, re.IGNORECASE)
        if dbms_match:
            result["dbms"] = dbms_match.group(1).strip()
        
        # Database enumeration
        db_matches = re.findall(r"\[\*\]\s*(\w+)\s*$", output, re.MULTILINE)
        if db_matches:
            result["databases"] = db_matches
        
        return result

    @staticmethod
    def parse_nikto(output):
        """Parse nikto output for web vulnerabilities."""
        result = {
            "target": None,
            "server": None,
            "vulnerabilities": [],
            "interesting_files": [],
            "warnings": []
        }
        
        for line in output.split("\n"):
            line = line.strip()
            
            # Target info
            if "+ Target IP:" in line or "+ Target Hostname:" in line:
                result["target"] = line.split(":", 1)[1].strip()
            
            # Server info
            if "+ Server:" in line:
                result["server"] = line.split(":", 1)[1].strip()
            
            # Vulnerability detection
            if "+ OSVDB-" in line or "vulnerability" in line.lower():
                result["vulnerabilities"].append(line)
            
            # Interesting files
            if "/admin" in line or "/backup" in line or ".bak" in line or ".old" in line:
                result["interesting_files"].append(line)
            
            # Warnings
            if "WARNING" in line or "POSSIBLE" in line:
                result["warnings"].append(line)
        
        return result

    @staticmethod
    def parse_gobuster(output):
        """Parse gobuster directory enumeration output."""
        result = {
            "directories": [],
            "files": [],
            "status_codes": {}
        }
        
        for line in output.split("\n"):
            match = re.search(r'/(\S+)\s+\(Status:\s*(\d+)\)', line)
            if match:
                path = "/" + match.group(1)
                status = match.group(2)
                
                if path.endswith("/"):
                    result["directories"].append({"path": path, "status": status})
                else:
                    result["files"].append({"path": path, "status": status})
                
                if status not in result["status_codes"]:
                    result["status_codes"][status] = 0
                result["status_codes"][status] += 1
        
        return result

    @staticmethod
    def parse_enum4linux(output):
        """Parse enum4linux SMB enumeration output."""
        result = {
            "target": None,
            "shares": [],
            "users": [],
            "groups": [],
            "os_info": None,
            "domain": None
        }
        
        for line in output.split("\n"):
            line = line.strip()
            
            # Share detection
            if "Sharename" not in line and ("\\\\" in line or "///" in line):
                match = re.search(r'[\\/]+(\S+)', line)
                if match:
                    result["shares"].append(match.group(1))
            
            # User detection
            user_match = re.search(r'user:\[(.*?)\]', line, re.IGNORECASE)
            if user_match:
                result["users"].append(user_match.group(1))
            
            # OS info
            if "OS=" in line or "OS:" in line:
                result["os_info"] = line
            
            # Domain info
            domain_match = re.search(r'Domain:\s*(\S+)', line)
            if domain_match:
                result["domain"] = domain_match.group(1)
        
        # Deduplicate
        result["shares"] = list(set(result["shares"]))
        result["users"] = list(set(result["users"]))
        
        return result

    @staticmethod
    def parse_hydra(output):
        """Parse hydra brute force output."""
        result = {
            "success": False,
            "credentials": [],
            "host": None,
            "service": None
        }
        
        for line in output.split("\n"):
            # Successful credential
            if "[" in line and "]" in line and "login:" in line.lower():
                result["success"] = True
                match = re.search(r'host:\s*(\S+).*login:\s*(\S+).*password:\s*(\S+)', line, re.IGNORECASE)
                if match:
                    result["credentials"].append({
                        "host": match.group(1),
                        "username": match.group(2),
                        "password": match.group(3)
                    })
            
            # Service detection
            if "Hydra" in line and "starting" in line.lower():
                service_match = re.search(r'Hydra.*\((\w+)\)', line)
                if service_match:
                    result["service"] = service_match.group(1)
        
        return result

    @staticmethod
    def wrap(tool_name, raw_output):
        """Universal wrapper for tool output parsing."""
        parsers = {
            "nmap": ToolWrappers.parse_nmap,
            "sqlmap": ToolWrappers.parse_sqlmap,
            "nikto": ToolWrappers.parse_nikto,
            "gobuster": ToolWrappers.parse_gobuster,
            "dirb": ToolWrappers.parse_gobuster,  # Similar output format
            "enum4linux": ToolWrappers.parse_enum4linux,
            "hydra": ToolWrappers.parse_hydra,
        }
        
        parser = parsers.get(tool_name.lower())
        if parser:
            try:
                return parser(raw_output)
            except Exception as e:
                return {"error": str(e), "raw": raw_output[:500]}
        
        return {"raw": raw_output[:1000], "lines": len(raw_output.split("\n"))}
