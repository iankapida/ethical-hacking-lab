import socket
import subprocess
import sys
import threading
from datetime import datetime, timezone

def handle_client(client_socket, client_address):
    """
    Manages an active simulated C2 session, receiving commands and returning output.
    """
    print(f"\n[+] Session established with client: {client_address[0]}:{client_address[1]}")
    client_socket.send(b"[*] Connected to Secure C2 Simulator. Type 'exit' to disconnect.\nC2> ")

    try:
        while True:
            command = client_socket.recv(1024).decode('utf-8').strip()
            if not command:
                break
            
            if command.lower() == 'exit':
                client_socket.send(b"[-] Terminating session...\n")
                break

            # Execute command locally using subprocess for demonstration
            try:
                output = subprocess.check_output(
                    command, 
                    shell=True, 
                    stderr=subprocess.STDOUT, 
                    timeout=5
                )
            except subprocess.CalledProcessError as e:
                output = e.output
            except subprocess.TimeoutExpired:
                output = b"[-] Error: Command execution timed out.\n"
            except Exception as e:
                output = f"[-] Execution Error: {str(e)}\n".encode('utf-8')

            client_socket.send(output + b"\nC2> ")
    except Exception as e:
        print(f"[-] Session error with {client_address[0]}: {e}")
    finally:
        client_socket.close()
        print(f"[-] Session closed for {client_address[0]}")

def start_c2_listener(host="127.0.0.1", port=4444):
    """
    Binds a TCP socket listener to accept incoming simulation connections.
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server.bind((host, port))
        server.listen(5)
        print(f"[*] C2 Simulator Listener active on {host}:{port}")
        print(f"[*] Started at: {datetime.now(timezone.utc).isoformat()}")
        print("[*] Waiting for incoming agent connections... (Press Ctrl+C to stop)")

        while True:
            client_sock, client_addr = server.accept()
            # Handle each client in a separate thread for concurrency
            client_thread = threading.Thread(target=handle_client, args=(client_sock, client_addr))
            client_thread.daemon = True
            client_thread.start()

    except KeyboardInterrupt:
        print("\n[-] C2 Listener manually stopped by operator.")
    except Exception as e:
        print(f"[-] Listener error: {e}")
    finally:
        server.close()
        sys.exit(0)

if __name__ == "__main__":
    host_ip = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
    listen_port = int(sys.argv[2]) if len(sys.argv) > 2 else 4444
    start_c2_listener(host_ip, listen_port)
