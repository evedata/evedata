# MicroK8s Non-HA Ansible Role Specification

## Overview

This Ansible role automates the installation and configuration of MicroK8s in non-HA (single-node) mode on Ubuntu 24.04 LTS systems. The role provides a secure, production-ready MicroK8s deployment with CIS hardening enabled by default, essential addons pre-configured, and proper multi-user access controls.

## Purpose

The role is designed specifically for non-HA MicroK8s deployments where high availability is not required. It leverages MicroK8s launch configurations to provide a declarative, repeatable deployment process with security hardening and essential addons enabled from the start.

## Variables

### Required Variables

None - all variables have sensible defaults for a secure single-node deployment.

### Optional Variables

#### Core Configuration

| Variable | Description | Type | Default |
|----------|-------------|------|---------|
| `microk8s_channel` | MicroK8s snap channel to install from | string | `"1.32/stable"` |
| `microk8s_config_version` | Launch configuration version (0.1.0 or 0.2.0) | string | `"0.2.0"` |
| `microk8s_users` | Additional users to add to the microk8s group (beyond ANSIBLE_USER) | list[string] | `[]` |
| `microk8s_persistent_cluster_token` | Optional persistent token for future cluster joins (32 chars) | string | `""` |

#### Kubernetes Component Arguments

| Variable | Description | Type | Default |
|----------|-------------|------|---------|
| `microk8s_extra_kube_apiserver_args` | Additional kube-apiserver arguments | dict | `{}` |
| `microk8s_extra_kubelet_args` | Additional kubelet arguments | dict | `{}` |
| `microk8s_extra_kube_proxy_args` | Additional kube-proxy arguments | dict | `{}` |
| `microk8s_extra_kube_controller_manager_args` | Additional kube-controller-manager arguments | dict | `{}` |
| `microk8s_extra_kube_scheduler_args` | Additional kube-scheduler arguments | dict | `{}` |
| `microk8s_extra_kubelite_env` | Environment variables for Kubernetes services (kubelite) | dict | `{}` |

#### Networking Configuration

| Variable | Description | Type | Default |
|----------|-------------|------|---------|
| `microk8s_extra_sans` | Additional Subject Alternative Names for API server certificates | list[string] | `[]` |
| `microk8s_dns_nameservers` | Custom upstream DNS servers for CoreDNS addon | list[string] | `["1.1.1.1", "1.0.0.1"]` |
| `microk8s_extra_cni_env` | CNI configuration (IPv4/IPv6 cluster and service CIDRs) | dict | `{}` |
| `microk8s_extra_flanneld_args` | Additional flanneld arguments | dict | `{}` |
| `microk8s_extra_flanneld_env` | Environment variables for flanneld | dict | `{}`

#### Container Runtime Configuration

| Variable | Description | Type | Default |
|----------|-------------|------|---------|
| `microk8s_registry_mirrors` | Container registry mirror configurations (containerdRegistryConfigs) | dict | `{}` |
| `microk8s_extra_containerd_args` | Additional containerd arguments | dict | `{}` |
| `microk8s_extra_containerd_env` | Environment variables for containerd (e.g., proxy settings) | dict | `{}` |

#### Storage Backend Configuration

| Variable | Description | Type | Default |
|----------|-------------|------|---------|
| `microk8s_extra_dqlite_args` | Additional k8s-dqlite arguments (when using dqlite backend) | dict | `{}` |
| `microk8s_extra_dqlite_env` | Environment variables for k8s-dqlite | dict | `{}` |
| `microk8s_extra_etcd_args` | Additional etcd arguments (when using etcd backend) | dict | `{}` |
| `microk8s_extra_etcd_env` | Environment variables for etcd | dict | `{}` |

#### MicroK8s Services Configuration

| Variable | Description | Type | Default |
|----------|-------------|------|---------|
| `microk8s_extra_cluster_agent_args` | Additional cluster-agent arguments | dict | `{}` |
| `microk8s_extra_cluster_agent_env` | Environment variables for cluster-agent | dict | `{}` |
| `microk8s_extra_apiserver_proxy_args` | Additional apiserver-proxy arguments (worker nodes) | dict | `{}` |
| `microk8s_extra_apiserver_proxy_env` | Environment variables for apiserver-proxy | dict | `{}` |

#### Security Configuration

| Variable | Description | Type | Default |
|----------|-------------|------|---------|
| `microk8s_enable_cis_hardening` | Enable CIS hardening addon for security compliance | boolean | `true` |
| `microk8s_extra_fips_env` | FIPS mode configuration (e.g., GOFIPS=1) | dict | `{}` |

#### Advanced Configuration

| Variable | Description | Type | Default |
|----------|-------------|------|---------|
| `microk8s_extra_config_files` | Additional configuration files to create in $SNAP_DATA/args/ | dict | `{}` |
| `microk8s_addon_repositories` | Custom addon repositories to configure | list[dict] | `[]` |
| `microk8s_enable_community_repo` | Enable the community addon repository | boolean | `true` |

#### Addons Configuration

| Variable | Description | Type | Default |
|----------|-------------|------|---------|
| `microk8s_enable_ha_cluster` | Enable HA cluster addon for future scalability | boolean | `true` |
| `microk8s_addons` | List of addons to enable/disable during deployment | list[dict] | See below |

##### Default Addons Configuration

```yaml
microk8s_addons:
  - name: dns
    enabled: true
    args: []  # Uses Cloudflare DNS (1.1.1.1, 1.0.0.1) by default via microk8s_dns_nameservers
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
  - name: trivy
    enabled: true
    args: []
```

## Playbook Usage

### Basic Usage

```yaml
---
- name: Deploy MicroK8s in Non-HA Mode
  hosts: target_servers
  become: true
  roles:
    - microk8s
```

### Advanced Configuration Example

```yaml
---
- name: Deploy MicroK8s with Custom Configuration
  hosts: staging_server
  become: true
  vars:
    microk8s_channel: "1.31/stable"
    microk8s_config_version: "0.2.0"
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
      - name: trivy
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

### Network Customization Example

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
      - "10.94.0.1"  # First IP of service CIDR
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

### Security Hardening Example

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

### Performance Optimization Example

```yaml
---
- name: Deploy MicroK8s with Performance Optimizations
  hosts: high_performance_server
  become: true
  vars:
    # Optimize Kubernetes component performance
    microk8s_extra_kube_apiserver_args:
      --max-requests-inflight: "800"
      --max-mutating-requests-inflight: "400"
      --watch-cache-sizes: "deployments#1000,configmaps#1000"
      --default-watch-cache-size: "500"
    microk8s_extra_kubelet_args:
      --max-pods: "250"
      --pod-max-pids: "4096"
      --image-gc-high-threshold: "85"
      --image-gc-low-threshold: "80"
      --eviction-hard: "memory.available<500Mi,nodefs.available<10%"
      --system-reserved: "cpu=1,memory=2Gi"
      --kube-reserved: "cpu=500m,memory=1Gi"
    microk8s_extra_kube_controller_manager_args:
      --concurrent-deployment-syncs: "10"
      --concurrent-endpoint-syncs: "10"
      --concurrent-service-syncs: "5"
    # Optimize containerd
    microk8s_extra_containerd_args:
      --config: "$SNAP_DATA/args/containerd-config.toml"
    microk8s_extra_config_files:
      containerd-config.toml: |
        [plugins."io.containerd.grpc.v1.cri".containerd]
          default_runtime_name = "runc"
          snapshotter = "overlayfs"
        [plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runc]
          runtime_type = "io.containerd.runc.v2"
        [plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runc.options]
          SystemdCgroup = true
    # Storage backend optimization
    microk8s_extra_dqlite_args:
      --disk-mode: "true"
      --network-latency: "20ms"
  roles:
    - microk8s
```

### Air-Gapped Environment Example

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

### Group-Specific Deployment

```yaml
---
- name: Deploy MicroK8s to Staging Environment
  hosts: stg
  become: true
  roles:
    - microk8s
```

## Role Behavior

### Installation Process

1. **Pre-flight Checks**: Validates Ubuntu 24.04 LTS target system
2. **Launch Configuration**: Creates MicroK8s launch configuration from Jinja2 template at `/var/snap/microk8s/common/.microk8s.yaml`
3. **Installation**: Installs MicroK8s snap from specified channel
4. **User Management**: Adds ANSIBLE_USER and any specified additional users to the microk8s group
5. **Addon Repository**: Enables community addon repository if configured
6. **Validation**: Waits for cluster to be ready and validates addon status

### Launch Configuration Template

The role uses a Jinja2 template to generate the launch configuration file that includes:

- **Version Control**: Support for launch config versions 0.1.0 and 0.2.0
- **Addon Management**: Enablement/disabling with proper ordering and custom arguments
- **Kubernetes Components**: Custom arguments and environment variables for all core components
  - kube-apiserver, kubelet, kube-proxy, kube-controller-manager, kube-scheduler
  - kubelite environment variables for unified Kubernetes services
- **Container Runtime**: Full containerd configuration including:
  - Registry mirrors and pull-through cache settings
  - Proxy configuration for air-gapped environments
  - Custom runtime arguments and environment variables
- **Networking**: Comprehensive network configuration
  - Custom pod and service CIDRs via CNI environment
  - Additional SANs for API server certificates
  - Flannel configuration for overlay networking
  - DNS configuration with custom nameservers
- **Storage Backends**: Support for both dqlite and etcd
  - Custom arguments and environment for each backend
  - Performance tuning options
- **MicroK8s Services**: Configuration for cluster-specific services
  - cluster-agent for node management
  - apiserver-proxy for worker node communication
- **Security Features**:
  - CIS hardening configuration
  - FIPS mode support via environment variables
  - Custom configuration files for encryption at rest, audit policies, etc.
- **Addon Repositories**: Custom repository support for private/local addons

### Security Features

- CIS hardening enabled by default following CIS Kubernetes Benchmark v1.24
- RBAC enabled by default for proper access control
- HA cluster addon for consistent cluster management
- Support for custom API server SANs
- Proxy configuration support for air-gapped environments
- Registry mirror support for private registries

## Dependencies

### System Requirements

- Ubuntu 24.04 LTS
- Snap package manager (pre-installed on Ubuntu)
- Sufficient system resources for Kubernetes workloads

### Ansible Collections

```yaml
collections:
  - name: ansible.builtin
    version: ">=2.19.0"
  - name: community.general
    version: ">=11.4.0"
```

## Target Platform

This role is designed exclusively for Ubuntu 24.04 LTS (Noble Numbat) and has been optimized for this specific distribution. The role leverages Ubuntu-specific features and the snap packaging system.

## Notes

### Non-HA Limitation

This role is explicitly designed for single-node, non-HA deployments. For high availability requirements, a different role or configuration approach would be needed.

### HA Cluster Addon

Despite being a non-HA deployment, the ha-cluster addon is enabled by default. This provides:

- Preparation for future cluster expansion without reconfiguration
- Consistent API endpoints and cluster management features
- Simplified migration path to multi-node deployments if requirements change
- No performance overhead for single-node operations

### Launch Configuration

The role utilizes MicroK8s launch configurations (available since v1.27) to provide a declarative deployment model. The configuration is applied during installation, ensuring addons are enabled and configured correctly from the start.

### User Access

The role automatically adds the Ansible user to the microk8s group, allowing kubectl commands to be run without sudo. Additional users can be specified via the `microk8s_users` variable.

### Community Addons

When the community addon repository is enabled, additional addons become available including the Trivy security scanner. The repository is maintained by the MicroK8s community and provides extended functionality beyond core addons.

### Idempotency

The role is designed to be idempotent - running it multiple times will not cause unintended changes. However, modifying the launch configuration after initial installation requires specific handling as documented in the MicroK8s documentation.

## Version Compatibility

- MicroK8s: 1.32+ (required for launch configuration support)
- Recommended: 1.32+ (for latest features and security updates)
- Default: 1.32/stable (latest stable release at time of specification)

## References

- [MicroK8s Launch Configurations Documentation](https://microk8s.io/docs/add-launch-config)
- [MicroK8s Launch Configurations Reference](https://microk8s.io/docs/ref-launch-config)
- [MicroK8s Launch Configurations Full Example](https://raw.githubusercontent.com/canonical/microk8s-cluster-agent/refs/heads/main/pkg/k8sinit/testdata/schema/full.yaml)
- [MicroK8s Multi-User Setup](https://microk8s.io/docs/multi-user)
- [MicroK8s CIS Hardening](https://microk8s.io/docs/how-to-cis-harden)
- [MicroK8s Community Addons](https://github.com/canonical/microk8s-community-addons)
