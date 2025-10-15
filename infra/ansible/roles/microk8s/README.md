# MicroK8s Non-HA Ansible Role

This Ansible role automates the installation and configuration of MicroK8s in non-HA (single-node) mode on Ubuntu 24.04 LTS systems. The role provides a secure, production-ready MicroK8s deployment with CIS hardening enabled by default, essential addons pre-configured, and proper multi-user access controls.

## Requirements

### System Requirements

- **Operating System**: Ubuntu 24.04 LTS (Noble Numbat)
- **Memory**: Minimum 2GB RAM
- **Disk Space**: Minimum 20GB available
- **CPU**: Minimum 2 CPU cores
- **Snap**: Pre-installed (default on Ubuntu)

### Ansible Requirements

- Ansible >= 2.19.0
- Collections:
  - `ansible.builtin`
  - `community.general` >= 11.4.0

## Role Variables

### Core Configuration

| Variable | Description | Type | Default |
|----------|-------------|------|---------|
| `microk8s_channel` | MicroK8s snap channel to install from | string | `"1.32/stable"` |
| `microk8s_config_version` | Launch configuration version (0.1.0 or 0.2.0) | string | `"0.2.0"` |
| `microk8s_users` | Additional users to add to the microk8s group (beyond ANSIBLE_USER) | list[string] | `[]` |
| `microk8s_persistent_cluster_token` | Optional persistent token for future cluster joins (32 chars) | string | `""` |
| `microk8s_force_recreate_localhost_kubeconfig` | Force recreation of localhost kubeconfig even if it exists | boolean | `false` |

### Kubernetes Component Arguments

| Variable | Description | Type | Default |
|----------|-------------|------|---------|
| `microk8s_extra_kube_apiserver_args` | Additional kube-apiserver arguments | dict | `{}` |
| `microk8s_extra_kubelet_args` | Additional kubelet arguments | dict | `{}` |
| `microk8s_extra_kube_proxy_args` | Additional kube-proxy arguments | dict | `{}` |
| `microk8s_extra_kube_controller_manager_args` | Additional kube-controller-manager arguments | dict | `{}` |
| `microk8s_extra_kube_scheduler_args` | Additional kube-scheduler arguments | dict | `{}` |
| `microk8s_extra_kubelite_env` | Environment variables for Kubernetes services (kubelite) | dict | `{}` |

### Networking Configuration

| Variable | Description | Type | Default |
|----------|-------------|------|---------|
| `microk8s_extra_sans` | Additional Subject Alternative Names for API server certificates | list[string] | `[]` |
| `microk8s_dns_nameservers` | Custom upstream DNS servers for CoreDNS addon | list[string] | `[]` |
| `microk8s_extra_cni_env` | CNI configuration (IPv4/IPv6 cluster and service CIDRs) | dict | `{}` |
| `microk8s_extra_flanneld_args` | Additional flanneld arguments | dict | `{}` |
| `microk8s_extra_flanneld_env` | Environment variables for flanneld | dict | `{}` |

### Container Runtime Configuration

| Variable | Description | Type | Default |
|----------|-------------|------|---------|
| `microk8s_registry_mirrors` | Container registry mirror configurations | dict | `{}` |
| `microk8s_extra_containerd_args` | Additional containerd arguments | dict | `{}` |
| `microk8s_extra_containerd_env` | Environment variables for containerd (e.g., proxy settings) | dict | `{}` |

### Storage Backend Configuration

| Variable | Description | Type | Default |
|----------|-------------|------|---------|
| `microk8s_extra_dqlite_args` | Additional k8s-dqlite arguments | dict | `{}` |
| `microk8s_extra_dqlite_env` | Environment variables for k8s-dqlite | dict | `{}` |
| `microk8s_extra_etcd_args` | Additional etcd arguments | dict | `{}` |
| `microk8s_extra_etcd_env` | Environment variables for etcd | dict | `{}` |

### Security Configuration

| Variable | Description | Type | Default |
|----------|-------------|------|---------|
| `microk8s_enable_cis_hardening` | Enable CIS hardening addon for security compliance | boolean | `true` |
| `microk8s_extra_fips_env` | FIPS mode configuration (e.g., GOFIPS=1) | dict | `{}` |

### Advanced Configuration

| Variable | Description | Type | Default |
|----------|-------------|------|---------|
| `microk8s_extra_config_files` | Additional configuration files to create | dict | `{}` |
| `microk8s_addon_repositories` | Custom addon repositories to configure | list[dict] | `[]` |
| `microk8s_enable_community_repo` | Enable the community addon repository | boolean | `true` |

### Addons Configuration

| Variable | Description | Type | Default |
|----------|-------------|------|---------|
| `microk8s_enable_ha_cluster` | Enable HA cluster addon for future scalability | boolean | `true` |
| `microk8s_addons` | List of addons to enable/disable during deployment | list[dict] | See defaults/main.yml |

## Dependencies

None. This role is self-contained.

## Example Playbooks

### Basic Usage

```yaml
---
- name: Deploy MicroK8s in Non-HA Mode
  hosts: target_servers
  become: true
  roles:
    - microk8s
```

### Advanced Configuration

```yaml
---
- name: Deploy MicroK8s with Custom Configuration
  hosts: staging_server
  become: true
  vars:
    microk8s_channel: "1.31/stable"
    microk8s_users:
      - developer
      - operator
    microk8s_extra_sans:
      - k8s.example.com
      - api.k8s.example.com
    microk8s_dns_nameservers:
      - 1.1.1.1
      - 8.8.8.8
    microk8s_registry_mirrors:
      docker.io: |
        [host."http://registry-mirror.internal:5000"]
        capabilities = ["pull", "resolve"]
    microk8s_extra_containerd_env:
      http_proxy: "http://proxy.internal:3128"
      https_proxy: "http://proxy.internal:3128"
      no_proxy: "10.0.0.0/8,127.0.0.1,192.168.0.0/16"
    microk8s_addons:
      - name: dns
        enabled: true
        args: []
      - name: rbac
        enabled: true
        args: []
      - name: hostpath-storage
        enabled: true
        args: []
      - name: ha-cluster
        enabled: true
        args: []
      - name: cis-hardening
        enabled: true
        args: []
      - name: ingress
        enabled: true
        args: []
      - name: cert-manager
        enabled: true
        args: []
  roles:
    - microk8s
```

### Network Customization

```yaml
---
- name: Deploy MicroK8s with Custom Network Configuration
  hosts: kubernetes_nodes
  become: true
  vars:
    # Custom pod and service CIDRs
    microk8s_extra_cni_env:
      IPv4_SUPPORT: "true"
      IPv4_CLUSTER_CIDR: "10.2.0.0/16"
      IPv4_SERVICE_CIDR: "10.94.0.0/24"
      IPv6_SUPPORT: "false"
    # Additional API server SANs
    microk8s_extra_sans:
      - "10.94.0.1"
      - "k8s.internal.example.com"
    # Custom DNS configuration
    microk8s_dns_nameservers:
      - "10.0.0.53"
      - "10.0.0.54"
    # Flannel network configuration
    microk8s_extra_flanneld_args:
      --iface: "eth1"
      --public-ip: "10.0.1.10"
  roles:
    - microk8s
```

### Security Hardening

```yaml
---
- name: Deploy MicroK8s with Enhanced Security
  hosts: production_server
  become: true
  vars:
    microk8s_enable_cis_hardening: true
    # Enable FIPS mode for supported components
    microk8s_extra_fips_env:
      GOFIPS: "1"
    # Configure encryption at rest
    microk8s_extra_config_files:
      encryption-config.yaml: |
        apiVersion: apiserver.config.k8s.io/v1
        kind: EncryptionConfiguration
        resources:
          - resources:
              - secrets
              - configmaps
            providers:
              - aescbc:
                  keys:
                    - name: key1
                      secret: "{{ lookup('password', '/dev/null length=32 chars=ascii_letters,digits') | b64encode }}"
              - identity: {}
      audit-policy.yaml: |
        apiVersion: audit.k8s.io/v1
        kind: Policy
        omitStages:
          - "RequestReceived"
        rules:
          - level: RequestResponse
            resources:
            - group: ""
              resources: ["secrets", "configmaps"]
          - level: Metadata
            resources:
            - group: ""
              resources: ["pods/log", "pods/status"]
    microk8s_extra_kube_apiserver_args:
      --encryption-provider-config: "$SNAP_DATA/args/encryption-config.yaml"
      --audit-policy-file: "$SNAP_DATA/args/audit-policy.yaml"
      --audit-log-path: "-"
      --audit-log-maxage: "30"
      --audit-log-maxbackup: "10"
      --audit-log-maxsize: "100"
      --enable-admission-plugins: "NodeRestriction,ResourceQuota,ServiceAccount"
    # Enhanced kubelet security
    microk8s_extra_kubelet_args:
      --protect-kernel-defaults: "true"
      --read-only-port: "0"
      --streaming-connection-idle-timeout: "5m"
      --tls-cipher-suites: "TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256,TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256"
  roles:
    - microk8s
```

### Air-Gapped Environment

```yaml
---
- name: Deploy MicroK8s in Air-Gapped Environment
  hosts: airgapped_server
  become: true
  vars:
    # Configure proxy for external access
    microk8s_extra_containerd_env:
      http_proxy: "http://proxy.internal:3128"
      https_proxy: "http://proxy.internal:3128"
      no_proxy: "10.0.0.0/8,172.16.0.0/12,192.168.0.0/16,127.0.0.1,localhost,.internal"
    # Configure local registry mirrors
    microk8s_registry_mirrors:
      docker.io: |
        [host."http://registry.internal:5000"]
        capabilities = ["pull", "resolve"]
        skip_verify = true
      registry.k8s.io: |
        [host."http://registry.internal:5000"]
        capabilities = ["pull", "resolve"]
        skip_verify = true
      ghcr.io: |
        [host."http://registry.internal:5000"]
        capabilities = ["pull", "resolve"]
        skip_verify = true
    # Use custom addon repository from local path
    microk8s_addon_repositories:
      - name: local-addons
        url: "/opt/microk8s-addons"
    microk8s_enable_community_repo: false
  roles:
    - microk8s
```

## Role Behavior

### Installation Process

1. **Pre-flight Checks**: Validates Ubuntu 24.04 LTS target system and resources
2. **Launch Configuration**: Creates MicroK8s launch configuration from Jinja2 template at `/var/snap/microk8s/common/.microk8s.yaml`
3. **Installation**: Installs MicroK8s snap from specified channel
4. **User Management**: Adds ANSIBLE_USER and any specified additional users to the microk8s group
5. **Addon Repository**: Enables community addon repository if configured
6. **Validation**: Waits for cluster to be ready and validates addon status

### Files Created

- `/var/snap/microk8s/common/.microk8s.yaml` - Launch configuration file
- `/var/snap/microk8s/current/credentials/client.config` - Original kubeconfig with public IP
- `/var/snap/microk8s/current/credentials/client.localhost.config` - Localhost kubeconfig (127.0.0.1:16443)
- `/root/.kube/config` - Root user kubeconfig (localhost version)
- `/home/<user>/.kube/config` - Kubeconfig for each configured user (localhost version)
- `/etc/bash.bashrc` - Updated with kubectl and helm aliases

### Localhost Kubeconfig Feature

The role automatically creates a localhost-friendly kubeconfig that uses `127.0.0.1:16443` instead of the public IP address. This feature is essential when:

- Port 16443 is blocked on the public interface by firewall rules
- You need to access the cluster from the local machine
- Tools like Helm or kubectl require local kubeconfig access
- You want to avoid exposing the API server on the public interface

The original kubeconfig is preserved, and the localhost version is distributed to all users automatically.

### Security Features

- CIS hardening enabled by default following CIS Kubernetes Benchmark v1.24
- RBAC enabled by default for proper access control
- HA cluster addon for consistent cluster management
- Support for custom API server SANs
- Proxy configuration support for air-gapped environments
- Registry mirror support for private registries
- Localhost kubeconfig to avoid exposing API server publicly

## Important Notes

### Non-HA Limitation

This role is explicitly designed for single-node, non-HA deployments. For high availability requirements, a different role or configuration approach would be needed.

### HA Cluster Addon

Despite being a non-HA deployment, the ha-cluster addon is enabled by default. This provides:

- Preparation for future cluster expansion without reconfiguration
- Consistent API endpoints and cluster management features
- Simplified migration path to multi-node deployments if requirements change
- No performance overhead for single-node operations

### User Access

The role automatically adds the Ansible user to the microk8s group, allowing kubectl commands to be run without sudo. Users may need to log out and back in for group membership to take effect, or run `newgrp microk8s`.

### Idempotency

The role is designed to be idempotent - running it multiple times will not cause unintended changes. However, modifying the launch configuration after initial installation requires specific handling as documented in the MicroK8s documentation.

## Troubleshooting

### Check MicroK8s Status

```bash
microk8s status
microk8s kubectl get nodes
microk8s kubectl get pods -A
```

### View Logs

```bash
sudo journalctl -u snap.microk8s.daemon-kubelite -f
sudo journalctl -u snap.microk8s.daemon-containerd -f
```

### Reset MicroK8s

```bash
microk8s reset
```

### Common Issues

1. **DNS not working**: DNS addon might take a few minutes to be fully operational after installation
2. **Group membership not active**: Users need to log out and back in or run `newgrp microk8s`
3. **Snap refresh**: If MicroK8s auto-updates, you may need to re-run the role to ensure configuration consistency

## License

MIT

## Author Information

EVEData Infrastructure Team

## References

- [MicroK8s Documentation](https://microk8s.io/docs)
- [MicroK8s Launch Configurations](https://microk8s.io/docs/add-launch-config)
- [MicroK8s CIS Hardening](https://microk8s.io/docs/how-to-cis-harden)
- [MicroK8s Community Addons](https://github.com/canonical/microk8s-community-addons)
