# 1Password Connect Ansible Role

This Ansible role automates the deployment and configuration of the 1Password Connect server and Kubernetes Operator on Ubuntu 24.04 LTS systems with MicroK8s.

## Documentation

For complete documentation, including prerequisites, variables, usage examples, and troubleshooting, please refer to [SPEC.md](./SPEC.md).

## Quick Start

### Basic Usage

```yaml
---
- name: Deploy 1Password Connect
  hosts: hzl
  become: true
  vars:
    op_connect_credentials_file: "op_connect_operator_credentials.json"
    op_connect_operator_token: "{{ vault_op_connect_operator_token }}"
  roles:
    - op_connect
```

### Required Variables

- `op_connect_credentials_file`: Path to 1Password Connect credentials JSON file (relative to `infra/ansible/files/`)
- `op_connect_operator_token`: 1Password Operator authentication token (should be stored in Ansible Vault)

### Role Structure

```
op_connect/
├── defaults/
│   └── main.yml          # Default variables
├── handlers/
│   └── main.yml          # Handlers (currently empty)
├── meta/
│   └── main.yml          # Role metadata and dependencies
├── tasks/
│   ├── main.yml          # Main task orchestration
│   ├── namespace.yml     # Namespace management
│   ├── credentials.yml   # Credentials handling
│   ├── helm-repo.yml     # Helm repository configuration
│   ├── install.yml       # Helm chart installation
│   └── validate.yml      # Validation checks
├── README.md             # This file
└── SPEC.md               # Complete specification and documentation
```

## Dependencies

- `helm` role (for Helm package manager)
- MicroK8s installed and configured
- Active 1Password Business or Enterprise account

## License

MIT

## Author

EVEData Infrastructure Team
