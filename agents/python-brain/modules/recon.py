from core.system_agent import SystemAgent
import re

class ReconModule:
    """Wrapper for Reconnaissance Tools (Nmap, Subfinder, DNS)."""
    
    def __init__(self, sys_agent):
        self.sys = sys_agent

    def scan(self, target, scan_type="fast"):
        """Perform an Nmap scan with configurable intensity."""
        print(f"[*] Recon: Scanning {target} ({scan_type})...")
        
        scan_profiles = {
            "fast": f"nmap -F -T4 {target}",
            "standard": f"nmap -sV -sC {target}",
            "full": f"nmap -sV -sC -p- -T4 {target}",
            "stealth": f"nmap -sS -T2 -f {target}",
            "udp": f"nmap -sU --top-ports 100 {target}",
            "vuln": f"nmap -sV --script vuln {target}"
        }
        
        cmd = scan_profiles.get(scan_type, scan_profiles["fast"])
        return self.sys.execute(cmd)

    def subdomains(self, domain):
        """Find subdomains using multiple techniques."""
        print(f"[*] Recon: Enumerating subdomains for {domain}...")
        
        results = {"domain": domain, "subdomains": [], "methods": []}
        
        # Method 1: Subfinder (if available)
        subfinder_result = self.sys.execute(f"which subfinder && subfinder -d {domain} -silent 2>/dev/null | head -50")
        if subfinder_result.get("code") == 0 and subfinder_result.get("stdout"):
            subs = [s.strip() for s in subfinder_result["stdout"].split("\n") if s.strip() and domain in s]
            results["subdomains"].extend(subs)
            results["methods"].append("subfinder")
        
        # Method 2: Amass (passive, if available)
        amass_result = self.sys.execute(f"which amass && timeout 60 amass enum -passive -d {domain} 2>/dev/null | head -50")
        if amass_result.get("code") == 0 and amass_result.get("stdout"):
            subs = [s.strip() for s in amass_result["stdout"].split("\n") if s.strip() and domain in s]
            results["subdomains"].extend(subs)
            results["methods"].append("amass")
        
        # Method 3: DNS brute force with common prefixes
        common_prefixes = ["www", "mail", "ftp", "admin", "api", "dev", "staging", "test", 
                          "blog", "shop", "store", "cdn", "assets", "static", "ns1", "ns2",
                          "vpn", "remote", "portal", "webmail", "smtp", "pop", "imap"]
        
        dns_found = []
        for prefix in common_prefixes[:10]:  # Limit to avoid long execution
            subdomain = f"{prefix}.{domain}"
            dns_result = self.sys.execute(f"host {subdomain} 2>/dev/null | grep -q 'has address' && echo {subdomain}")
            if dns_result.get("code") == 0 and dns_result.get("stdout", "").strip():
                dns_found.append(subdomain)
        
        if dns_found:
            results["subdomains"].extend(dns_found)
            results["methods"].append("dns_bruteforce")
        
        # Method 4: Certificate Transparency logs
        ct_result = self.sys.execute(f"curl -s 'https://crt.sh/?q=%25.{domain}&output=json' 2>/dev/null | grep -oP '\"name_value\":\"[^\"]+\"' | cut -d'\"' -f4 | sort -u | head -30")
        if ct_result.get("code") == 0 and ct_result.get("stdout"):
            ct_subs = [s.strip() for s in ct_result["stdout"].split("\n") if s.strip() and domain in s and "*" not in s]
            results["subdomains"].extend(ct_subs)
            results["methods"].append("certificate_transparency")
        
        # Deduplicate results
        results["subdomains"] = list(set(results["subdomains"]))
        results["count"] = len(results["subdomains"])
        
        return results

    def dns_lookup(self, target):
        """Perform comprehensive DNS reconnaissance."""
        print(f"[*] Recon: DNS lookup for {target}...")
        
        results = {"target": target, "records": {}}
        
        record_types = ["A", "AAAA", "MX", "NS", "TXT", "SOA", "CNAME"]
        
        for rtype in record_types:
            cmd = f"dig +short {target} {rtype} 2>/dev/null"
            res = self.sys.execute(cmd)
            if res.get("stdout", "").strip():
                results["records"][rtype] = res["stdout"].strip().split("\n")
        
        # Reverse DNS if A record found
        if results["records"].get("A"):
            for ip in results["records"]["A"][:2]:
                rev_cmd = f"dig +short -x {ip} 2>/dev/null"
                rev_res = self.sys.execute(rev_cmd)
                if rev_res.get("stdout", "").strip():
                    results["records"]["PTR"] = results["records"].get("PTR", [])
                    results["records"]["PTR"].append(f"{ip} -> {rev_res['stdout'].strip()}")
        
        return results

    def whois_lookup(self, target):
        """Perform WHOIS lookup."""
        print(f"[*] Recon: WHOIS lookup for {target}...")
        return self.sys.execute(f"whois {target} 2>/dev/null | head -80")

    def port_discovery(self, target, top_ports=1000):
        """Fast port discovery using masscan or nmap."""
        print(f"[*] Recon: Port discovery on {target}...")
        
        # Try masscan first (faster for large scans)
        masscan_check = self.sys.execute("which masscan")
        if masscan_check.get("code") == 0:
            return self.sys.execute(f"sudo masscan {target} -p1-65535 --rate=1000 2>/dev/null | head -100")
        
        # Fallback to nmap
        return self.sys.execute(f"nmap -p- --min-rate=1000 -T4 {target} 2>/dev/null")
