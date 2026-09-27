import os
import json
from napalm import get_network_driver


def audit_routing_state():
    """Connects to multi-hop enterprise nodes to audit active routing state."""
    driver = get_network_driver("ios")
    password = os.getenv("NET_DEV_PASS")

    if not password:
        raise ValueError("CRITICAL EXECUTION ERROR: The NET_DEV_PASS environment variable is missing!")

    # Standard 5-Node Laboratory Backbone Target Array
    nodes = ["10.1.1.1", "10.1.1.2", "10.1.1.3", "10.1.1.4", "10.1.1.5"]
    username = os.getenv("NET_DEV_USER", "developer")

    for ip in nodes:
        print(f"[*] Establishing secure transport channel to node {ip} via NAPALM...")
        try:
            device = driver(hostname=ip, username=username, password=password)
            device.open()

            # Programmatically extract active Layer 3 routing configuration state
            routes = device.get_route_to(destination="0.0.0.0/0")
            print(f"[+] Route verification matrix acquired for {ip}:")
            print(json.dumps(routes, indent=4))

            device.close()
        except Exception as e:
            print(f"[-] Execution failure on node {ip}: {e}")


if __name__ == "__main__":
    audit_routing_state()
