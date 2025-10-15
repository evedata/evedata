# Ansible Role: hostname

## Description

This role manages the system hostname on Ubuntu 24.04 LTS systems. It provides a consistent and idempotent way to set the hostname across your infrastructure, ensuring proper configuration in both systemd and traditional hostname files.

## Features

- Sets the system hostname using systemd
- Updates `/etc/hostname` file
- Updates `/etc/hosts` with the new hostname
- Validates hostname format according to RFC 1123
- Creates backups of modified files
- Verifies the hostname was set correctly

## Requirements

- Ubuntu 24.04 LTS (Noble Numbat)
- Ansible 2.15 or higher
- Sudo/root privileges on the target system

## Role Variables

### Optional Variables

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `hostname` | The desired system hostname | `{{ inventory_hostname }}` | `htz-eu-fsn-hzl-srv01` |

By default, the role uses the inventory hostname from Ansible. You can override this by setting the `hostname` variable in your playbook, host_vars, or group_vars.

## Dependencies

This role has no dependencies on other Ansible roles.

## Example Playbook

### Basic Usage (using inventory hostname)

The simplest usage - the role will automatically use the inventory hostname:

```yaml
---
- name: Configure system hostname
  hosts: all
  become: true
  roles:
    - hostname
```

### Override with Custom Hostname

You can override the default by setting the hostname variable:

```yaml
---
- name: Configure system hostname
  hosts: all
  become: true
  vars:
    hostname: "custom-server-name"
  roles:
    - hostname
```

### Using with Host Variables

Create a host_vars file for your server:

```yaml
# host_vars/htz-eu-fsn-hzl-srv01.yml
hostname: htz-eu-fsn-hzl-srv01
```

Then use in your playbook:

```yaml
---
- name: Configure hostnames from host_vars
  hosts: all
  become: true
  roles:
    - hostname
```

### Using with Group Variables

```yaml
# group_vars/hzl.yml
hostname_prefix: htz-eu-fsn-hzl
```

```yaml
---
- name: Configure hostnames with prefix
  hosts: hzl
  become: true
  vars:
    hostname: "{{ hostname_prefix }}-{{ inventory_hostname_short }}"
  roles:
    - hostname
```

## Hostname Format Requirements

The hostname must comply with RFC 1123:

- Must start and end with an alphanumeric character
- May contain hyphens (-) in the middle
- Maximum length of 63 characters
- No underscores, spaces, or special characters

Valid examples:

- `web-server-01`
- `htz-eu-fsn-hzl-srv01`
- `ubuntu-24`

Invalid examples:

- `_server` (starts with underscore)
- `server_` (ends with underscore)
- `web server` (contains space)
- `web.server` (contains period)

## Files Modified

This role modifies the following system files:

- `/etc/hostname` - Contains the system hostname
- `/etc/hosts` - Updates the 127.0.1.1 entry with the new hostname

Backups are automatically created for both files.

## Error Handling

The role includes validation to ensure:

1. The hostname variable is defined and not empty
2. The hostname format is valid according to RFC 1123
3. The hostname was successfully applied

If any validation fails, the role will stop execution with a descriptive error message.

## Testing

To test this role in a development environment:

```bash
# Run ansible-lint
cd $ANSIBLE_HOME
ansible-lint roles/hostname/

# Test with ansible-playbook in check mode
ansible-playbook playbooks/test-hostname.yml --check -e hostname=test-server

# Run the playbook
ansible-playbook playbooks/test-hostname.yml -e hostname=test-server
```

## License

MIT

## Author Information

Created and maintained by the EVEData Team for managing Ubuntu 24.04 LTS infrastructure.
