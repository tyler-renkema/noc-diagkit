# Run route checks across multiple devices and compare next-hop results.
from netmiko import ConnectHandler
import sys
import json

# List of devices to check — replace with real data or load from external file
devices = [
    {
        'name': 'core-router-1',
        'device_type': 'cisco_ios',
        'ip': '192.168.1.1',
        'username': 'admin',
        'password': 'password',
    },
    {
        'name': 'core-router-2',
        'device_type': 'cisco_ios',
        'ip': '192.168.1.2',
        'username': 'admin',
        'password': 'password',
    },
]

def check_route(device, target_ip):
    try:
        conn = ConnectHandler(**device)
        output = conn.send_command(f"show ip route {target_ip}")
        conn.disconnect()
        return parse_next_hop(output)
    except Exception as e:
        return f"Error: {e}"

def parse_next_hop(output):
    # Basic parse: look for known format lines
    for line in output.splitlines():
        if "via" in line:
            parts = line.strip().split()
            for i, word in enumerate(parts):
                if word == "via" and i + 1 < len(parts):
                    return parts[i + 1]
    return "No next-hop found"

def main():
    if len(sys.argv) != 2:
        print("Usage: python multicheck.py <destination_ip>")
        sys.exit(1)

    target_ip = sys.argv[1]
    results = {}

    for device in devices:
        name = device.get('name', device['ip'])
        print(f"Querying {name}...")
        next_hop = check_route(device, target_ip)
        results[name] = next_hop

    print("\nRoute Comparison:")
    for name, hop in results.items():
        print(f"{name}: {hop}")

    # Optional: output to JSON file
    with open('multicheck_results.json', 'w') as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    main()
