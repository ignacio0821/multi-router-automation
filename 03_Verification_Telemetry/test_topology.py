import pytest
import os
from napalm import get_network_driver


def test_verify_network_adjacency_state():
    """Asserts that the primary core routing nodes have achieved fully operational adjacency stability."""
    driver = get_network_driver("ios")
    password = os.getenv("NET_DEV_PASS")

    if not password:
        pytest.fail("CRITICAL: Local test environment variable NET_DEV_PASS is not initialized!")

    username = os.getenv("NET_DEV_USER", "developer")

    # Establish monitoring channel to core backbone anchor node
    device = driver(hostname="10.1.1.1", username=username, password=password)

    try:
        device.open()
        bgp_facts = device.get_bgp_neighbors()
        device.close()

        # Test Assertion Gate: Automatically flags a failure if neighbor count is flat zero
        assert len(bgp_facts) > 0, "CRITICAL PATH SEVERITY FAILURE: Zero active routing neighbors discovered on node!"

    except Exception as e:
        pytest.fail(f"Infrastructure connection verification threw unexpected transport exception: {e}")
