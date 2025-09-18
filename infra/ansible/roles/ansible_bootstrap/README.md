# Ansible Bootstrap Role

This role bootstraps Ubuntu 24.04 LTS hosts for Ansible management by creating a dedicated ansible user, configuring UFW (Uncomplicated Firewall), and hardening SSH.

## Requirements

- Ubuntu 24.04 LTS (Noble Numbat)
- Root or sudo access for initial bootstrap
- SSH public key for the ansible user

## Role Variables

### Required Variables

- `ansible_user_public_key`: SSH public key for the ansible management user (required)

### Optional Variables

- `ansible_bootstrap_ssh_port`: SSH port number (default: 22)

## What This Role Does

1. **Creates Ansible User**:
   - Username: `ansible`
   - Home directory: `/home/ansible`
   - Shell: `/bin/bash`
   - Passwordless sudo access
   - No password expiration
   - SSH key authentication only

2. **Configures UFW Firewall**:
   - Allows SSH traffic on configured port with automatic rate limiting (6 connections per 30 seconds)
   - Default policy: deny incoming, allow outgoing, deny routed
   - Logging level set to low
   - Provides protection against brute force attacks via built-in rate limiting

3. **Hardens SSH Configuration**:
   - Disables root login
   - Disables password authentication
   - Enforces public key authentication
   - Sets connection timeouts
   - Limits authentication attempts

## Example Playbook

```yaml
---
- name: Bootstrap hosts for Ansible management
  hosts: new_hosts
  become: true
  vars:
    ansible_user_public_key: "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAAB... ansible@management"

  roles:
    - ansible_bootstrap
```

## Usage

1. Ensure you have initial SSH access to the target host (as root or a sudo user)

2. Set the `ansible_user_public_key` variable in your inventory or playbook

3. Run the bootstrap playbook:
   ```bash
   ansible-playbook -i inventory/production/hosts.yml playbooks/ansible_bootstrap.yml \
     --limit new_host \
     --user initial_user \
     --ask-become-pass
   ```

4. After successful bootstrap, update your inventory to use the ansible user:
   ```yaml
   new_host:
     ansible_user: ansible
     ansible_become: true
   ```

5. Test connectivity with the new ansible user:
   ```bash
   ansible new_host -m ping -u ansible
   ```

## Security Considerations

- The ansible user has passwordless sudo access - protect the SSH private key
- SSH root login is disabled after bootstrap
- Password authentication is disabled - ensure you have key access before running
- The firewall drops all unexpected incoming traffic
- SSH connections are automatically rate-limited by UFW to prevent brute force attacks (6 connections per 30 seconds)

## License

MIT
