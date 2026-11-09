# SOC Incident Response Playbook: Web Enumeration & Secret Exposure

## 1. Trigger & Alert Scenarios
* **Alert ID:** `DET-001` — Sensitive File Exposure / Enumeration Detected
* **Severity:** HIGH
* **Log Source:** Web Server Access Telemetry (`attack_telemetry.log`)

## 2. Tier 1 Analyst Triage Protocol

### Step A: Identification & Verification
1. Extract the Source IP address and timestamp from `attack_telemetry.log`.
2. Verify if the target URI is a known sensitive configuration file (e.g., `/.env`, `/robots.txt`, `/admin`).
3. Check HTTP status code patterns (e.g., repeated `404 Not Found` followed by `200 OK` on sensitive endpoints).

### Step B: Threat Intelligence Enrichment
1. Cross-reference the Source IP against AbuseIPDB / VirusTotal to check for prior malicious activity.
2. Determine if the traffic represents an automated web scanner based on User-Agent telemetry and request rate.

## 3. Containment & Mitigation Steps
1. **Firewall Block:** Drop traffic from the attacking IP using `iptables` or cloud WAF:
   ```bash
   sudo iptables -A INPUT -s <Attacker_IP> -j DROP
