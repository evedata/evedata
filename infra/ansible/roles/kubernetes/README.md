# Ansible Role: kubernetes

## Description

This role installs Python dependencies required for the `kubernetes.core` Ansible collection to work on Ubuntu 24.04 LTS systems. It ensures that the necessary Python libraries are installed system-wide, enabling Ansible to interact with Kubernetes clusters using the kubernetes.core collection modules.

## Purpose

The kubernetes.core Ansible collection requires specific Python libraries to function properly. This role automates the installation of these dependencies, ensuring:

- Consistent environment setup across all managed hosts
- Proper version management of Python dependencies
- Verification of successful installation
- Idempotent operations

## Requirements

- **Operating System**: Ubuntu 24.04 LTS (Noble Numbat)
- **Ansible Version**: 2.15 or higher
- **Privileges**: Root or sudo access (for package installation)
- **Python**: Python 3.x (comes pre-installed with Ubuntu 24.04)

## What It Installs

This role installs the following components:

1. **python3-pip**: The Python package installer
   - Installed via apt package manager
   - Required to install Python libraries system-wide

2. **kubernetes Python library**: Official Python client for Kubernetes
   - Installed via pip
   - Provides programmatic access to Kubernetes API
   - Required by kubernetes.core collection modules

3. **PyYAML Python library**: YAML parser and emitter for Python
   - Installed via pip
   - Required for parsing Kubernetes YAML manifests
   - Dependency of the kubernetes Python library

## Role Variables

### defaults/main.yml

| Variable | Default | Description |
|----------|---------|-------------|
| `kubernetes_python_version` | `""` (latest) | Specific version of kubernetes Python library to install |
| `kubernetes_pyyaml_version` | `""` (latest) | Specific version of PyYAML library to install |

### Example: Pinning Versions

```yaml
# Install specific versions for stability
kubernetes_python_version: "30.1.0"
kubernetes_pyyaml_version: "6.0.2"
```

## Dependencies

This role has no dependencies on other Ansible roles.

## Tags

The following tags are available:

- `kubernetes`: Apply all tasks in this role
- `kubernetes-deps`: Install Python dependencies
- `kubernetes-verify`: Run verification tasks only

## Usage Examples

### Basic Usage in a Playbook

```yaml
---
- name: Install Kubernetes Python dependencies
  hosts: all
  become: true
  roles:
    - kubernetes
```

### With Version Pinning

```yaml
---
- name: Install Kubernetes Python dependencies with specific versions
  hosts: all
  become: true
  roles:
    - role: kubernetes
      vars:
        kubernetes_python_version: "30.1.0"
        kubernetes_pyyaml_version: "6.0.2"
```

### As a Dependency for Another Role

In your role's `meta/main.yml`:

```yaml
dependencies:
  - role: kubernetes
    tags:
      - kubernetes-deps
```

### Using with kubernetes.core Collection

After running this role, you can use kubernetes.core modules:

```yaml
---
- name: Deploy application to Kubernetes
  hosts: localhost
  tasks:
    - name: Create a namespace
      kubernetes.core.k8s:
        name: my-namespace
        api_version: v1
        kind: Namespace
        state: present
```

## Verification

The role includes verification tasks that:

1. Check if the kubernetes Python library is installed correctly
2. Display the installed version of the kubernetes library
3. Check if PyYAML is installed correctly
4. Display the installed version of PyYAML

These verification tasks can be run independently using the `kubernetes-verify` tag:

```bash
ansible-playbook playbooks/kubernetes.yml --tags kubernetes-verify
```

## Troubleshooting

### Common Issues

1. **pip3 not found**: Ensure python3-pip is installed via apt
2. **Permission denied**: Ensure the playbook runs with `become: true`
3. **Version conflicts**: Consider pinning specific versions if you encounter compatibility issues

### Debug Output

To see more detailed output during execution:

```bash
ansible-playbook playbooks/kubernetes.yml -vv
```

## Integration with kubernetes.core

This role is a prerequisite for using the kubernetes.core Ansible collection. After installing these dependencies, you can:

- Manage Kubernetes resources declaratively
- Deploy applications to Kubernetes clusters
- Configure Kubernetes RBAC
- Manage ConfigMaps and Secrets
- Handle Kubernetes networking resources

## Testing

To test this role:

1. Create a test playbook
2. Run it against a test Ubuntu 24.04 system
3. Verify the libraries are installed:

```bash
python3 -c "import kubernetes; print(kubernetes.__version__)"
python3 -c "import yaml; print(yaml.__version__)"
```

## License

MIT

## Author Information

Created by the EVEData Team for managing Kubernetes dependencies on Ubuntu 24.04 LTS systems.
