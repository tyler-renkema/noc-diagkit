import socket
import sys
import time

def tcp_probe(host, port, timeout=3):
    try:
        with socket.create_connection((host, port), timeout=timeout) as s:
            print(f"[TCP] Connected to {host}:{port}")
            return True
    except socket.timeout:
        print(f"[TCP] Timeout connecting to {host}:{port}")
    except socket.error as e:
        print(f"[TCP] Error connecting to {host}:{port} — {e}")
    return False

def udp_probe(host, port, timeout=3):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.settimeout(timeout)
            s.sendto(b'probe', (host, port))
            # Expect ICMP port unreachable or no response
            try:
                data, _ = s.recvfrom(1024)
                print(f"[UDP] Received response from {host}:{port}")
            except socket.timeout:
                print(f"[UDP] No response from {host}:{port} (possibly open or silently dropped)")
    except Exception as e:
        print(f"[UDP] Error sending to {host}:{port} — {e}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python fwprobe.py <tcp|udp> <host> <port>")
        sys.exit(1)

    proto = sys.argv[1].lower()
    target_host = sys.argv[2]
    target_port = int(sys.argv[3])

    print(f"[{time.ctime()}] Starting probe to {target_host}:{target_port} using {proto.upper()}")

    if proto == 'tcp':
        tcp_probe(target_host, target_port)
    elif proto == 'udp':
        udp_probe(target_host, target_port)
    else:
        print("Unsupported protocol. Use 'tcp' or 'udp'.")
