from netmiko import ConnectHandler
# Retrieves LLDP neighbor information from a Cisco IOS device and maps local interfaces to remote neighbors.
import json

# Device connection details (use external config for production)
device = {
    'device_type': 'cisco_ios',
    'ip': '192.168.1.1',
    'username': 'admin',
    'password': 'password',
}

def get_lldp_neighbors(connection):
    output = connection.send_command("show lldp neighbors detail", use_textfsm=True)
    if isinstance(output, list):
        neighbors = []
        for entry in output:
            neighbors.append({
                'local_interface': entry.get('local_interface'),
                'neighbor_device': entry.get('neighbor'),
                'neighbor_interface': entry.get('neighbor_interface'),
                'neighbor_port_id': entry.get('neighbor_portid'),
            })
        return neighbors
    else:
        return []

def main():
    print("Connecting to device...")
    try:
        connection = ConnectHandler(**device)
        neighbors = get_lldp_neighbors(connection)
        connection.disconnect()

        if not neighbors:
            print("No LLDP neighbors found or parsing failed.")
        else:
            print("LLDP Neighbor Map:")
            for neighbor in neighbors:
                print(f"{neighbor['local_interface']} -> {neighbor['neighbor_device']} ({neighbor['neighbor_interface']} / {neighbor['neighbor_port_id']})")

            # Optional: save to JSON
            with open('lldp_neighbors.json', 'w') as f:
                json.dump(neighbors, f, indent=2)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
