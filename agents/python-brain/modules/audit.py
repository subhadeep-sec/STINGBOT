from core.system_agent import SystemAgent

class AuditModule:
    """Vulnerability Analysis & Verification."""
    
    def __init__(self, sys_agent):
        self.sys = sys_agent

    def search_cve(self, query):
        """Search for CVEs using multiple sources."""
        results = {"query": query, "sources": {}}
        
        # Searchsploit (Exploit-DB local copy)
        searchsploit_result = self.sys.execute(f"searchsploit {query} 2>/dev/null | head -50")
        if searchsploit_result.get("code") == 0:
            results["sources"]["searchsploit"] = searchsploit_result.get("stdout", "")
        
        # NVD API lookup (if curl available)
        nvd_result = self.sys.execute(f"curl -s 'https://services.nvd.nist.gov/rest/json/cves/2.0?keywordSearch={query}' 2>/dev/null | head -100")
        if nvd_result.get("code") == 0 and "CVE" in nvd_result.get("stdout", ""):
            results["sources"]["nvd"] = "NVD results available (parsed externally)"
        
        return results

    def verify_auth(self, target, service="ssh"):
        """Verify weak credentials (SAFE - local networks only)."""
        # Improved Safety Check
        is_local = (
            target in ["localhost", "127.0.0.1", "0.0.0.1"] or 
            target.startswith("192.168.") or 
            target.startswith("10.") or
            target.startswith("172.16.") or
            target.startswith("172.17.") or
            target.startswith("172.18.") or
            target.startswith("172.19.") or
            target.startswith("172.2") or
            target.startswith("172.3")
        )
        if not is_local:
            return {"stderr": f"Safety Block: Auth verification for {target} restricted. Local network only.", "code": 1}
        
        # Service-specific credential checks
        checks = {
            "ssh": f"hydra -L /usr/share/wordlists/metasploit/unix_users.txt -P /usr/share/wordlists/metasploit/unix_passwords.txt -t 4 -e nsr {target} ssh 2>/dev/null | head -20",
            "ftp": f"hydra -L /usr/share/wordlists/metasploit/unix_users.txt -P /usr/share/wordlists/metasploit/unix_passwords.txt -t 4 -e nsr {target} ftp 2>/dev/null | head -20",
            "http": f"curl -s -o /dev/null -w '%{{http_code}}' http://{target}/admin 2>/dev/null",
            "mysql": f"mysql -h {target} -u root --password='' -e 'SELECT 1' 2>/dev/null && echo 'MySQL: No password on root!'",
            "smb": f"smbclient -L {target} -N 2>/dev/null | head -20"
        }
        
        cmd = checks.get(service, f"echo '[*] Checking default creds on {target}:{service}...'")
        return self.sys.execute(cmd)

    def nikto_scan(self, target):
        """Run Nikto web vulnerability scanner."""
        if not self.sys.check_tool("nikto"):
            return {"stderr": "Nikto not installed. Install with: apt install nikto", "code": 1}
        
        return self.sys.execute(f"nikto -h {target} -Tuning 123bde -maxtime 120 2>/dev/null")

    def ssl_check(self, target):
        """Check SSL/TLS configuration."""
        results = {"target": target, "checks": {}}
        
        # Check certificate
        cert_result = self.sys.execute(f"echo | openssl s_client -connect {target}:443 2>/dev/null | openssl x509 -noout -dates -subject 2>/dev/null")
        if cert_result.get("code") == 0:
            results["checks"]["certificate"] = cert_result.get("stdout", "")
        
        # Check supported protocols
        protocols = ["ssl3", "tls1", "tls1_1", "tls1_2", "tls1_3"]
        supported = []
        for proto in protocols:
            proto_check = self.sys.execute(f"echo | timeout 5 openssl s_client -{proto} -connect {target}:443 2>/dev/null | grep -q 'CONNECTED' && echo {proto}")
            if proto_check.get("stdout", "").strip():
                supported.append(proto)
        results["checks"]["protocols"] = supported
        
        return results

    def security_headers_check(self, target):
        """Check HTTP security headers."""
        headers_to_check = [
            "Strict-Transport-Security",
            "X-Content-Type-Options",
            "X-Frame-Options",
            "X-XSS-Protection",
            "Content-Security-Policy",
            "Referrer-Policy",
            "Permissions-Policy"
        ]
        
        result = self.sys.execute(f"curl -sI {target} 2>/dev/null | head -30")
        response_headers = result.get("stdout", "")
        
        findings = {"target": target, "present": [], "missing": []}
        for header in headers_to_check:
            if header.lower() in response_headers.lower():
                findings["present"].append(header)
            else:
                findings["missing"].append(header)
        
        return findings
