import sys
import urllib.request
import urllib.error
import json
from datetime import datetime, timezone

def check_endpoint(base_url, path):
    """
    Sends an HTTP GET request to the target path and returns the status code.
    Handles connection errors, HTTP errors, and timeouts gracefully.
    """
    url = f"{base_url.rstrip('/')}/{path.lstrip('/')}"
    try:
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'Mozilla/5.0 (SecurityAuditor/1.0)'}
        )
        with urllib.request.urlopen(req, timeout=3.0) as response:
            return response.status
    except urllib.error.HTTPError as e:
        # Captures server error codes (e.g., 403 Forbidden, 404 Not Found)
        return e.code
    except urllib.error.URLError:
        # Host is unreachable or connection refused
        return None
    except Exception:
        return None

def run_fuzzer(target_url, wordlist):
    """
    Iterates through the wordlist, checks endpoints against the target URL,
    and logs active/notable directories and files.
    """
    print(f"\n[*] Initializing Web Application Fuzzer...")
    print(f"[*] Target URL: {target_url}")
    print(f"[*] Scan initiated at: {datetime.now(timezone.utc).isoformat()}")
    print("-" * 60)

    discovered_endpoints = []

    try:
        for path in wordlist:
            print(f"[*] Testing path: /{path}...", end="\r")
            status = check_endpoint(target_url, path)
            
            if status:
                # Log notable status codes indicating presence or protection
                if status in [200, 301, 302, 403]:
                    print(f"[+] [FOUND] /{path} -> HTTP Status: {status}")
                    finding = {
                        "path": f"/{path}",
                        "status_code": status,
                        "timestamp": datetime.now(timezone.utc).isoformat()
                    }
                    discovered_endpoints.append(finding)
    except KeyboardInterrupt:
        print("\n[-] Fuzzing manually aborted by user.")
        sys.exit(1)

    print("-" * 60)
    print(f"[+] Fuzzing complete. Discovered {len(discovered_endpoints)} notable endpoint(s).")
    return discovered_endpoints

def save_fuzz_report(findings, output_path="fuzz_report.json"):
    """Saves discovered web endpoints into a structured JSON report."""
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(findings, f, indent=4)
        print(f"[+] Fuzzing report successfully generated: {output_path}")
    except Exception as e:
        print(f"[-] Failed to save JSON report: {e}")

if __name__ == "__main__":
    # Accept target URL from command line or default to local test server
    target = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8080"
    
    # Core wordlist representing high-value sensitive web artifacts
    common_paths = [
        "admin",
        "login",
        "dashboard",
        "config.json",
        ".env",
        "robots.txt",
        "backup.zip",
        "api/v1/status",
        "uploads",
        "server-status"
    ]
    
    results = run_fuzzer(target, common_paths)
    if results:
        save_fuzz_report(results)
