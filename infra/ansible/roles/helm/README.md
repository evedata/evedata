# Ansible Role: Helm

An Ansible role to install Helm package manager for Kubernetes on Ubuntu 24.04 LTS.

## Description

This role installs Helm, the package manager for Kubernetes, using the official APT repository method. It follows the official Helm installation guide for Debian/Ubuntu systems and ensures the installation is secure, idempotent, and follows Ansible best practices.

## Requirements

- **Operating System**: Ubuntu 24.04 LTS (Noble Numbat)
- **Ansible Version**: >= 2.15
- **Privileges**: Root or sudo access required for package installation

## Role Variables

### Default Variables

The following variables are defined in `defaults/main.yml` and can be overridden:

```yaml
# Helm GPG key URL
helm_gpg_key_url: "https://packages.buildkite.com/helm-linux/helm-debian/gpgkey"

# Helm APT repository URL
helm_repository_url: "https://packages.buildkite.com/helm-linux/helm-debian/any/"

# Helm package state (present, latest)
helm_package_state: present

# Helm version specification (empty string for latest available)
# Examples: "=3.13.*" for specific minor version, "=3.13.2-1" for specific version
helm_version_spec: ""
```

### Variable Usage Examples

To install a specific version of Helm:
```yaml
helm_version_spec: "=3.13.*"  # Install latest 3.13.x version
helm_version_spec: "=3.13.2-1"  # Install exact version
```

To always install the latest version:
```yaml
helm_package_state: latest
```

## Dependencies

This role has no dependencies on other Ansible roles.

## Installation Process

The role performs the following steps:

1. **Install Prerequisites**: Installs required packages (`curl`, `gpg`, `apt-transport-https`)
2. **Download GPG Key**: Fetches the official Helm GPG key
3. **Process GPG Key**: Dearmors the GPG key and stores it in `/usr/share/keyrings/helm.gpg`
4. **Add Repository**: Adds the official Helm APT repository with proper signing
5. **Install Helm**: Installs the Helm package from the repository
6. **Verify Installation**: Confirms Helm is installed and displays the version

## Example Playbook

### Basic Usage

```yaml
---
- name: Install Helm on Kubernetes nodes
  hosts: kubernetes
  become: true
  roles:
    - role: helm
```

### With Custom Variables

```yaml
---
- name: Install specific Helm version
  hosts: kubernetes
  become: true
  roles:
    - role: helm
      vars:
        helm_version_spec: "=3.13.*"
        helm_package_state: present
```

### Using with Group Variables

In `group_vars/kubernetes.yml`:
```yaml
helm_package_state: latest
```

In your playbook:
```yaml
---
- name: Configure Kubernetes cluster
  hosts: kubernetes
  become: true
  roles:
    - role: helm
```

## Tags

The role supports the following tags for selective execution:

- `helm`: Run all Helm-related tasks
- `helm-dependencies`: Install prerequisite packages only
- `helm-repository`: Configure APT repository only
- `helm-install`: Install Helm package only
- `helm-verify`: Verify installation only

### Tag Usage Examples

Install only prerequisites:
```bash
ansible-playbook playbooks/helm.yml --tags helm-dependencies
```

Configure repository and install:
```bash
ansible-playbook playbooks/helm.yml --tags helm-repository,helm-install
```

## Security Considerations

- **GPG Key Verification**: The role downloads and properly verifies the official Helm GPG key
- **Signed Repository**: The APT repository is configured with GPG signing for package integrity
- **No Hardcoded Credentials**: All URLs are configurable via variables
- **Proper Permissions**: Files are created with appropriate ownership and permissions

## Idempotency

This role is fully idempotent. Running it multiple times will:
- Only download the GPG key if it has changed
- Only update the repository if needed
- Only install/upgrade Helm if the desired state differs from current state

## Troubleshooting

### Common Issues

1. **GPG Key Download Fails**
   - Check network connectivity
   - Verify the `helm_gpg_key_url` is accessible
   - Check proxy settings if behind a corporate firewall

2. **Repository Addition Fails**
   - Ensure `/etc/apt/sources.list.d/` directory exists
   - Check for conflicting Helm repositories
   - Verify DNS resolution for the repository URL

3. **Helm Installation Fails**
   - Check available disk space
   - Verify no package conflicts exist
   - Review APT cache status

### Debug Mode

Run the playbook in verbose mode for detailed output:
```bash
ansible-playbook playbooks/helm.yml -vvv
```

## Testing

### Manual Testing

After running the role, verify the installation:

```bash
# Check Helm version
helm version

# Verify Helm is in PATH
which helm

# Test Helm functionality
helm repo add stable https://charts.helm.sh/stable
helm repo update
```

### Automated Testing

Use molecule or ansible-test for automated testing:

```bash
# Run ansible-lint
ansible-lint roles/helm/

# Run yamllint
yamllint roles/helm/
```

## License

MIT

## Author Information

EVEData Infrastructure Team

## References

- [Official Helm Installation Guide](https://helm.sh/docs/intro/install/#from-apt-debianubuntu)
- [Helm Documentation](https://helm.sh/docs/)
- [Ansible APT Module](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/apt_module.html)
- [Ansible Best Practices](https://docs.ansible.com/ansible/latest/user_guide/playbooks_best_practices.html)
