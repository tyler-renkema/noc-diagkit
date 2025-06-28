# NOC DiagKit

A lightweight, CLI-focused toolkit for small NOCs and infrastructure teams that need to validate and troubleshoot L2–L4 network behavior in mixed, aging, or transitional environments.

Scripts that help you answer:  
**What’s broken?**  
**Where is it?**  
**What changed?**

## Why This Exists

Not every network has full telemetry and not every team has full control. In small environments or partially migrated networks, visibility is often limited and troubleshooting relies on a mix of tribal knowledge, partial configs, and CLI output.

This toolkit provides practical, self-contained tools that:

- Pull current network state from live devices  
- Parse useful diagnostics from CLI and protocol behavior  
- Help validate assumptions and isolate faults  

## Included Tools

| Tool            | Function |
|-----------------|----------|
| `routecheck.py` | Queries a Cisco device to find the next hop to a destination IP |
| `vlanwalk.py`   | Checks which trunk ports allow a given VLAN |
| `macwatch.py`   | Tracks MAC address movement or appearance across switchports |
| `fwprobe.py`    | Sends L4 probes (TCP/UDP) to test connectivity through firewalls or NAT |
| `l3map.py`      | Maps local L3 interfaces and ARP table entries into a structured JSON file |
| `lldptrace.py`  | Retrieves LLDP neighbor info and maps local-to-remote interface relationships |
| `cdptrace.py`   | Correlates CDP neighbors and displays device-to-interface mappings |
| `l3mapviz.py`   | Generates a simple HTML visualization of L3 interfaces and ARP entries |

## Requirements

- Python 3.8+
- Netmiko
- (Optional) PySNMP, Scapy for future expansions

Install dependencies:

```bash
pip install -r requirements.txt
```

Sample `requirements.txt`:

```
netmiko>=4.0
```

## Usage Examples

Check next-hop routing to a host:

```bash
python routecheck.py 10.1.20.15
```

Verify if VLAN 20 is allowed on trunk ports:

```bash
python vlanwalk.py 20
```

Log MAC moves or new devices:

```bash
python macwatch.py
```

Probe L4 connectivity:

```bash
python fwprobe.py tcp 192.0.2.100 443
```

Generate a local L3 interface and ARP map:

```bash
python l3map.py
```

Visualize the L3 map output:

```bash
python l3mapviz.py l3map.json report.html
```

Trace LLDP neighbors:

```bash
python lldptrace.py
```

Trace CDP neighbors:

```bash
python cdptrace.py
```

## Device Configuration

Each script uses a device dictionary with connection parameters:

```python
device = {
    'device_type': 'cisco_ios',
    'ip': '192.168.1.1',
    'username': 'admin',
    'password': 'password',
}
```

For production use, consider securing credentials using environment variables, `.netrc`, or a vault integration.

## Intended Audience

- NOC engineers in small-to-medium environments  
- Infrastructure teams supporting hybrid networks  
- Anyone who still has to troubleshoot real problems on physical gear

## Disclaimer

This project is written for practical operations. It assumes CLI access to devices and may require customization for production environments. Use at your own discretion.

## License

MIT License

## TODO

- Multi-device probing and comparison
