import sys
import socket
from datetime import datetime

def scan_port(target_ip, port):
    """
    Attempts a TCP connection to a specific port on the target IP.
    Returns True if open, False otherwise.
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.0)
        result = s.connect_ex((target_ip, port))
        s.close()
        return result == 0
    except socket.error:
        return False

def run_recon(target_ip, ports):
    """
    Scans a list of specified ports on the target host.
    """
    print(f"\n[*] Starting Reconnaissance on Target: {target_ip}")
    print(f"[*] Scan initiated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 50)
    
    open_ports = []

    try:
        for port in ports:
            print(f"[*] Scanning port {port}...", end="\r")
            if scan_port(target_ip, port):
                print(f"[+] [OPEN] Port {port} is accepting connections.")
                open_ports.append(port)
    except KeyboardInterrupt:
        print("\n[-] Scan manually aborted by user.")
        sys.exit(1)

    print("-" * 50)
    print(f"[+] Recon complete. Found {len(open_ports)} open port(s).")
    return open_ports

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
    
    # Expanded common ports list including 8080 for testing local web servers
    target_ports = [21, 22, 80, 443, 3306, 8080]
    
    run_recon(target, target_ports)
