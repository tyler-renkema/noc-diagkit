from netmiko import ConnectHandler
import re
import sys

def get_next_hop(device, destination):
    try:
        conn = ConnectHandler(**device)
        output = conn.send_command(f"show ip route {destination}")
        conn.disconnect()
    except Exception as e:
        print(f"Connection error: {e}")
        sys.exit(1)

    # Extract next-hop info from output
    match = re.search(r"via ([\d.]+),", output)
    if match:
        next_hop = match.group(1)
        print(f"Next hop to {destination}: {next_hop}")
    else:
        print(f"No route to {destination} found.")

if __name__ == "__main__":
    # Define your Cisco device
    device = {
        'device_type': 'cisco_ios',
        'ip': '192.168.1.1',
        'username': 'admin',
        'password': 'password',
    }

    if len(sys.argv) != 2:
        print("Usage: python routecheck.py <destination_ip>")
        sys.exit(1)

    target = sys.argv[1]
    get_next_hop(device, target)
