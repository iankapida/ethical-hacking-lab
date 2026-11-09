import os
import sys
import json
from datetime import datetime, timezone

def parse_web_telemetry(log_path, threshold=3):
    """
    Parses web server access logs for enumeration and suspicious file access.
    Flags source IPs exceeding the 404/error threshold or accessing sensitive files.
    """
    failed_scans = {}
    incidents = []

    if not os.path.exists(log_path):
        print(f"[-] Error: Telemetry file '{log_path}' not found.")
        return incidents

    try:
        with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                parts = line.split()
                if len(parts) > 8:
                    ip = parts[0]
                    path = parts[6]
                    status = parts[8]

                    # Track 404 Not Found (enumeration scanning)
                    if status == "404":
                        failed_scans[ip] = failed_scans.get(ip, 0) + 1
                    
                    # High severity: direct access to sensitive artifacts like .env
                    elif status == "200" and (".env" in path or "config" in path):
                        incident = {
                            "timestamp": datetime.now(timezone.utc).isoformat(),
                            "threat_type": "Sensitive File Exposure / Enumeration",
                            "source_ip": ip,
                            "target_path": path,
                            "status_code": status,
                            "severity": "HIGH"
                        }
                        if incident not in incidents:
                            incidents.append(incident)

        # Threshold check for broad scanning behavior
        for ip, count in failed_scans.items():
            if count >= threshold:
                incident = {
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "threat_type": "Web Directory Enumeration Scan",
                    "source_ip": ip,
                    "failed_requests": count,
                    "severity": "MEDIUM"
                }
                incidents.append(incident)

    except Exception as e:
        print(f"[-] Error parsing telemetry: {e}")

    return incidents

if __name__ == "__main__":
    log_file = sys.argv[1] if len(sys.argv) > 1 else "attack_telemetry.log"
    
    print(f"[*] Initializing SOC Web Telemetry Analyzer...")
    print(f"[*] Inspecting log source: {log_file}")
    print("-" * 50)
    
    alerts = parse_web_telemetry(log_file)
    
    print(f"[+] Analysis complete. Generated {len(alerts)} security alert(s).")
    if alerts:
        print("\n--- DETECTED THREATS ---")
        for alert in alerts:
            print(f"    [ALERT] {alert['threat_type']} from {alert['source_ip']} - Severity: {alert['severity']}")
