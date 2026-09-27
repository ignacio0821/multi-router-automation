import os
import requests
import urllib3

# Suppress SSL warnings for sandbox controllers
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def deploy_controller_policy():
    """Interacts with a centralized controller API to orchestrate edge device policies."""
    # Pull controller host from system environment
    controller_ip = os.getenv("CISCO_CONTROLLER_IP", "sandboxdnac.cisco.com")
    password = os.getenv("NET_DEV_PASS")

    if not password:
        raise ValueError("CRITICAL: NET_DEV_PASS environment variable is missing!")

    username = os.getenv("NET_DEV_USER", "devnetuser")

    # Step 1: Authenticate and retrieve the API token from the controller
    auth_url = f"https://{controller_ip}/dna/system/api/v1/auth/token"
    print(f"[*] Authenticating with centralized controller at {controller_ip}...")

    try:
        response = requests.post(auth_url, auth=(username, password), verify=False)
        response.raise_for_status()
        token = response.json()["Token"]
        print("[+] Authentication token successfully acquired.")

        # Step 2: Use the token to fetch or push configuration templates across the 5 nodes
        headers = {
            "X-Auth-Token": token,
            "Content-Type": "application/json"
        }

        device_url = f"https://{controller_ip}/dna/intent/api/v1/network-device"
        devices = requests.get(device_url, headers=headers, verify=False)
        print("[+] Managed Edge Inventory discovered via Controller API.")

    except Exception as e:
        print(f"[-] Controller automation failure: {e}")


if __name__ == "__main__":
    deploy_controller_policy()
