from netmiko import ConnectHandler
import re
import json
import sys

def get_interfaces_and_ips(conn):
    output = conn.send_command("show ip interface brief")
    interfaces = {}
    for line in output.splitlines():
        if re.match(r'^\S+', line):
            parts = line.split()
            if len(parts) >= 6 and parts[1] != 'unassigned':
                interfaces[parts[0]] = parts[1]
    return interfaces

def get_arp_table(conn):
    output = conn.send_command("show ip arp")
    arps = []
    for line in output.splitlines():
        if re.search(r'\d+\.\d+\.\d+\.\d+', line):
            parts = line.split()
            if len(parts) >= 4:
                arps.append({'ip': parts[0], 'mac': parts[2], 'interface': parts[3]})
    return arps

def build_l3map(device):
    try:
        conn = ConnectHandler(**device)
    except Exception as e:
        print(f"Connection error: {e}")
        return None

    print(f"Connected to {device['ip']}, collecting data...")

    interfaces = get_interfaces_and_ips(conn)
    arp_entries = get_arp_table(conn)
    conn.disconnect()

    return {
        'device_ip': device['ip'],
        'interfaces': interfaces,
        'arp_table': arp_entries,
    }

if __name__ == "__main__":
    device = {
        'device_type': 'cisco_ios',
        'ip': '192.168.1.4',
        'username': 'admin',
        'password': 'password',
    }

    result = build_l3map(device)

    if result:
        with open(f"l3map_{device['ip']}.json", 'w') as f:
            json.dump(result, f, indent=2)
        print(f"Layer 3 map saved to l3map_{device['ip']}.json")
    else:
        print("Failed to retrieve Layer 3 mapping.")
