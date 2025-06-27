from netmiko import ConnectHandler
import json
import os
import time

DATA_FILE = "macwatch_snapshot.json"

def fetch_mac_table(device):
    try:
        conn = ConnectHandler(**device)
        output = conn.send_command("show mac address-table")
        conn.disconnect()
    except Exception as e:
        print(f"Connection error: {e}")
        return {}

    mac_table = {}
    for line in output.splitlines():
        if "DYNAMIC" in line:
            parts = line.split()
            if len(parts) >= 4:
                mac = parts[1]
                interface = parts[-1]
                mac_table[mac] = interface
    return mac_table

def load_previous_snapshot():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_snapshot(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def compare_snapshots(old, new):
    moved = {}
    new_macs = []

    for mac, intf in new.items():
        if mac not in old:
            new_macs.append((mac, intf))
        elif old[mac] != intf:
            moved[mac] = (old[mac], intf)

    return new_macs, moved

if __name__ == "__main__":
    device = {
        'device_type': 'cisco_ios',
        'ip': '192.168.1.3',
        'username': 'admin',
        'password': 'password',
    }

    print(f"[{time.ctime()}] Connecting to device...")
    current = fetch_mac_table(device)
    previous = load_previous_snapshot()

    new_macs, moved_macs = compare_snapshots(previous, current)

    if new_macs:
        print("New MAC addresses detected:")
        for mac, intf in new_macs:
            print(f"  {mac} on {intf}")

    if moved_macs:
        print("MAC address moves detected:")
        for mac, (old_intf, new_intf) in moved_macs.items():
            print(f"  {mac} moved from {old_intf} to {new_intf}")

    if not new_macs and not moved_macs:
        print("No changes detected.")

    save_snapshot(current)
