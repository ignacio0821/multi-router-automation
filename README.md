
# Multi-Router Path Convergence Automation Engine

Active CI Pipeline Status: [![NetDevOps Core CI Pipeline](https://github.com)](https://github.com)

An enterprise NetDevOps automation infrastructure designed to programmatically manage, audit, and validate multi-path routing policies across a 5-node network topology using RESTCONF, YANG data models, and NAPALM.

## 🏛️ Core Architectural Convergence Logic (Gates 0-4)

The infrastructure enforces path selection and dynamic failover by leveraging the strict linear evaluation order of the Cisco IOS XE routing engine:

```text
  [Inbound Packet]
         |
         v
  +-----------------------+

  |  Gate 0: Prefix Match | --> Is prefix length an exact match?
  +-----------------------+     (e.g., /24 vs /24) -> YES: Move to Gate 1.
         |
         v
  +-----------------------+

  | Gate 1: Admin Dist   | --> Primary: Static Route via Center Corridor (AD = 1)
  +-----------------------+     Backup: OSPF Dynamic Learning via Outer Ring (AD = 110)
         |                      Static Route (AD 1) wins; traffic binds to R1 -> R3 -> R5.
         v
  +-----------------------+

  | Gate 2 & 3: Failure   | --> CRITICAL FAILURE: Center link drops.
  +-----------------------+     Static Route interface drops. Prefix is purged from RIB.
         |                      Re-evaluation: Only the OSPF route (AD 110) remains.
         v
  +-----------------------+

  | Gate 4: Convergence   | --> Result: Traffic swings automatically to Outer Ring (R2/R4).
  +-----------------------+     Zero manual intervention required.
```

## 🛠️ Repository File Structure

```text
├── .github/workflows/
│   └── netdevops-ci.yaml     # GitHub Actions continuous integration pipeline
├── data/
│   └── network_inventory.yaml # Structured node data bindings & schema variables
├── scripts/
│   ├── deploy_configs.py     # RESTCONF payload enforcement engine
│   ├── backup_routes.py      # NAPALM state verification & routing table snapshots
│   └── deploy_base.py        # NAPALM golden configuration standard implementation
├── tests/
│   └── test_topology.py      # Pytest validation test definitions
├── .env.example              # Environment variables template for security masking
├── .gitignore                # Production file exclusion filter rules
├── pyproject.toml            # Black linter & code style configurations
└── requirements.txt          # Python production application dependencies
```

## 🔒 Security & Credential Management
This repository implements strict environment separation guidelines. Plaintext credentials are explicitly barred from the source tracking trees. System authorization relies on local environment bindings:
- `NET_DEV_USER`: Production/Sandbox administrative username string.
- `NET_DEV_PASS`: Production/Sandbox cryptographic password payload.
