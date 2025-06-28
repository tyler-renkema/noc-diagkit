# Retrieves CDP neighbor data from a Cisco IOS device and outputs a structured path correlation by interface.
from netmiko import ConnectHandler
import json

# Device connection details (use external config for production)
device = {
    'device_type': 'cisco_ios',
    'ip': '192.168.1.1',
    'username': 'admin',
    'password': 'password',
}

def get_cdp_neighbors(connection):
    output = connection.send_command("show cdp neighbors detail", use_textfsm=True)
    if isinstance(output, list):
        neighbors = []
        for entry in output:
            neighbors.append({
                'local_interface': entry.get('local_port'),
                'neighbor_device': entry.get('destination_host'),
                'neighbor_interface': entry.get('remote_port'),
                'platform': entry.get('platform'),
                'ip_address': entry.get('management_ip'),
            })
        return neighbors
    else:
        return []

def main():
    print("Connecting to device...")
    try:
        connection = ConnectHandler(**device)
        neighbors = get_cdp_neighbors(connection)
        connection.disconnect()

        if not neighbors:
            print("No CDP neighbors found or parsing failed.")
        else:
            print("CDP Neighbor Map:")
            for neighbor in neighbors:
                print(f"{neighbor['local_interface']} -> {neighbor['neighbor_device']} "
                      f"({neighbor['neighbor_interface']}, {neighbor['platform']}, {neighbor['ip_address']})")

            # Optional: save to JSON
            with open('cdp_neighbors.json', 'w') as f:
                json.dump(neighbors, f, indent=2)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
