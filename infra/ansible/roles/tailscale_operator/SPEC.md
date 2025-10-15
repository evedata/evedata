# Tailscale Operator Ansible Role Specification

## Overview

This Ansible role automates the deployment and configuration of the Tailscale Kubernetes Operator using Helm charts on Ubuntu 24.04 LTS systems with MicroK8s. The role configures the API server proxy in auth mode, enabling secure access to the Kubernetes control plane over the Tailscale network with impersonation-based authentication.

## Purpose

The role provides a declarative, idempotent deployment of the Tailscale Operator that:

- Exposes the Kubernetes API server securely over the Tailscale network
- Enables tailnet-based authentication and authorization using Kubernetes RBAC
- Supports OAuth-based authentication for enhanced security
- Provides a foundation for zero-trust network access to Kubernetes clusters

## Prerequisites

### System Requirements

- Ubuntu 24.04 LTS
- MicroK8s installed and configured (via `microk8s` role)
- Helm package manager installed (via `helm` role)
- Active Tailscale network with HTTPS enabled

### Tailscale Requirements

- Tailscale OAuth application configured with:
  - Valid OAuth client ID
  - OAuth client secret
  - Appropriate scopes for Kubernetes operator functionality
- Access control policies configured to allow devices to access the operator on port 443

### Ansible Collections

```yaml
collections:
  - name: kubernetes.core
    version: ">=6.1.0"
  - name: ansible.builtin
    version: ">=2.19.0"
```

## Variables

### Required Variables

| Variable | Description | Type | Vault |
|----------|-------------|------|-------|
| `tailscale_operator_oauth_client_id` | Tailscale OAuth application client ID | string | No |
| `tailscale_operator_oauth_client_secret` | Tailscale OAuth application client secret | string | **Yes** |
| `tailscale_operator_hostname` | Hostname for the Tailscale operator (e.g., `k8s-operator`) | string | No |

### Optional Variables

#### Helm Configuration

| Variable | Description | Type | Default |
|----------|-------------|------|---------|
| `helm_kubeconfig` | Path to kubeconfig file for Helm operations | string | `/var/snap/microk8s/current/credentials/client.config` |
| `tailscale_operator_namespace` | Kubernetes namespace for the operator | string | `tailscale` |
| `tailscale_operator_chart_version` | Specific Helm chart version to install | string | `""` (latest) |
| `tailscale_operator_helm_repo_name` | Name for the Tailscale Helm repository | string | `tailscale` |
| `tailscale_operator_helm_repo_url` | URL of the Tailscale Helm repository | string | `https://pkgs.tailscale.com/helmcharts` |
| `tailscale_operator_release_name` | Helm release name for the operator | string | `tailscale-operator` |
| `tailscale_operator_create_namespace` | Create namespace if it doesn't exist | boolean | `true` |

#### API Server Proxy Configuration

| Variable | Description | Type | Default |
|----------|-------------|------|---------|
| `tailscale_operator_api_server_proxy_mode` | API server proxy mode (auth/noauth) | string | `true` (auth mode) |
| `tailscale_operator_extra_values` | Additional Helm values to pass to the chart | dict | `{}` |

#### Operator Configuration

| Variable | Description | Type | Default |
|----------|-------------|------|---------|
| `tailscale_operator_replica_count` | Number of operator replicas (single replica for in-process proxy) | integer | `1` |
| `tailscale_operator_image_pull_policy` | Image pull policy for operator pods | string | `IfNotPresent` |
| `tailscale_operator_log_level` | Logging level for the operator | string | `info` |

#### Image Configuration

| Variable | Description | Type | Default |
|----------|-------------|------|---------|
| `tailscale_operator_image_tag` | Operator container image tag | string | `v1.88.4` |
| `tailscale_operator_image_digest` | Operator container image digest (SHA256) | string | `sha256:9a35d316344e4d6f85733848e79947566132d16abdb5fefb60adc49e04b9745c` |
| `tailscale_operator_proxy_image_tag` | Proxy container image tag | string | `v1.88.4` |
| `tailscale_operator_proxy_image_digest` | Proxy container image digest (SHA256) | string | `sha256:734c960048d9f0441cf0998d3c61b804ee8a7bebbdc607aa7df18bc460712ac7` |

## Task Flow

The role executes the following high-level tasks:

1. **Namespace Management**
   - Creates the Tailscale namespace if it doesn't exist
   - Configures appropriate labels and annotations

2. **Helm Repository Configuration**
   - Adds the official Tailscale Helm repository
   - Updates repository metadata to ensure latest charts are available

3. **Chart Deployment**
   - Installs or upgrades the tailscale-operator Helm chart
   - Configures OAuth authentication parameters
   - Enables API server proxy in auth mode
   - Applies any custom values specified in variables

4. **Validation**
   - Verifies the operator deployment is running
   - Checks that the operator pod(s) are ready
   - Validates API server proxy configuration

## Usage Examples

### Basic Usage

```yaml
---
- name: Deploy Tailscale Operator
  hosts: hzl
  become: true
  vars:
    tailscale_operator_oauth_client_id: "{{ vault_tailscale_operator_oauth_client_id }}"
    tailscale_operator_oauth_client_secret: "{{ vault_tailscale_operator_oauth_client_secret }}"
    tailscale_operator_hostname: "k8s-hzl"
  roles:
    - tailscale_operator
```

### Advanced Configuration

```yaml
---
- name: Deploy Tailscale Operator with Custom Configuration
  hosts: prd
  become: true
  vars:
    # OAuth Configuration (from vault)
    tailscale_operator_oauth_client_id: "{{ vault_tailscale_operator_oauth_client_id }}"
    tailscale_operator_oauth_client_secret: "{{ vault_tailscale_operator_oauth_client_secret }}"

    # Operator Configuration
    tailscale_operator_hostname: "k8s-prod"
    tailscale_operator_namespace: "tailscale-system"
    tailscale_operator_chart_version: "1.66.0"
    tailscale_operator_log_level: "debug"

    # Custom Helm values
    tailscale_operator_extra_values:
      resources:
        limits:
          cpu: "500m"
          memory: "256Mi"
        requests:
          cpu: "100m"
          memory: "128Mi"
      nodeSelector:
        kubernetes.io/hostname: "htz-eu-fsn-prd-srv01"
  roles:
    - tailscale_operator
```

### Multi-Environment Deployment

In `group_vars/all.yml`:

```yaml
helm_kubeconfig: /var/snap/microk8s/current/credentials/client.config
tailscale_operator_namespace: tailscale
tailscale_operator_api_server_proxy_mode: true
```

In `group_vars/stg.yml`:

```yaml
tailscale_operator_hostname: "k8s-staging"
tailscale_operator_log_level: "debug"
```

In `group_vars/prd.yml`:

```yaml
tailscale_operator_hostname: "k8s-production"
tailscale_operator_chart_version: "1.66.0"  # Pin version for production
```

In `group_vars/vault.yml` (encrypted):

```yaml
tailscale_operator_oauth_client_id: "your-client-id-here"
tailscale_operator_oauth_client_secret: "your-client-secret-here"
```

Playbook:

```yaml
---
- name: Deploy Tailscale Operator Across Environments
  hosts: all
  become: true
  vars:
    tailscale_operator_oauth_client_id: "{{ tailscale_operator_oauth_client_id }}"
    tailscale_operator_oauth_client_secret: "{{ tailscale_operator_oauth_client_secret }}"
  roles:
    - tailscale_operator
```

## Dependencies

### Role Dependencies

- `microk8s`: MicroK8s must be installed and configured
- `helm`: Helm package manager must be installed

### Collection Dependencies

The role requires the `kubernetes.core` collection for Helm module functionality. Ensure it's installed via `requirements.yml`:

```yaml
collections:
  - name: kubernetes.core
    version: ">=6.1.0"
```

Install collections:

```bash
ansible-galaxy collection install -r requirements.yml
```

## Tags

The role supports the following tags for selective execution:

- `tailscale-operator`: Run all Tailscale Operator tasks
- `tailscale-operator-namespace`: Manage namespace only
- `tailscale-operator-helm-repo`: Configure Helm repository only
- `tailscale-operator-install`: Install/upgrade operator only
- `tailscale-operator-validate`: Run validation tasks only

### Tag Usage Examples

Configure repository only:

```bash
ansible-playbook playbooks/tailscale-operator.yml --tags tailscale-operator-helm-repo
```

Install and validate:

```bash
ansible-playbook playbooks/tailscale-operator.yml --tags tailscale-operator-install,tailscale-operator-validate
```

## Security Considerations

### OAuth Credentials

- **ALWAYS** store OAuth credentials in Ansible Vault
- Never commit plaintext OAuth secrets to version control
- Use separate OAuth applications for different environments
- Regularly rotate OAuth credentials

### Network Security

- The operator exposes the Kubernetes API server on port 443 over Tailscale
- Access control policies must be properly configured in Tailscale ACLs
- Only authorized devices should be able to reach the operator

### Kubernetes RBAC

- The operator uses impersonation for auth mode
- Configure appropriate Kubernetes RBAC policies for tailnet users/groups
- Follow the principle of least privilege for access grants
- Regularly audit RBAC configurations

### Example RBAC Configuration

After deployment, configure RBAC for tailnet access:

```yaml
# Grant read-only access to tailnet group
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: tailnet-readers
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: view
subjects:
- apiGroup: rbac.authorization.k8s.io
  kind: Group
  name: tag:k8s-readers
```

## Idempotency

The role is fully idempotent and can be run multiple times safely:

- Helm repository addition is idempotent
- Chart installation uses `present` state by default
- Namespace creation checks for existence
- Validation tasks are read-only

## Troubleshooting

### Common Issues

1. **OAuth Authentication Fails**
   - Verify OAuth client ID and secret are correct
   - Check Tailscale OAuth application configuration
   - Ensure OAuth scopes are properly configured

2. **Helm Chart Installation Fails**
   - Verify kubeconfig path is correct
   - Check MicroK8s is running: `microk8s status`
   - Ensure Helm is installed: `helm version`
   - Review operator logs: `kubectl logs -n tailscale -l app=operator`

3. **API Server Proxy Not Accessible**
   - Verify Tailscale ACLs allow access on port 443
   - Check operator hostname resolution
   - Ensure HTTPS is enabled for the tailnet
   - Validate operator is running: `kubectl get pods -n tailscale`

### Debug Commands

```bash
# Check operator status
kubectl get all -n tailscale

# View operator logs
kubectl logs -n tailscale deployment/operator

# Describe operator deployment
kubectl describe deployment -n tailscale operator

# Check Helm release status
helm list -n tailscale

# Get Helm values
helm get values tailscale-operator -n tailscale

# Test API server proxy connection
curl -k https://<operator-hostname>.<tailnet-name>.ts.net/api/v1/namespaces
```

## Configuration After Deployment

### Configuring kubectl

After successful deployment, configure kubectl to use the API server proxy:

```bash
# Add cluster configuration
kubectl config set-cluster tailscale-cluster \
  --server=https://<operator-hostname>.<tailnet-name>.ts.net

# Add context
kubectl config set-context tailscale \
  --cluster=tailscale-cluster \
  --user=<your-tailnet-user>

# Use context
kubectl config use-context tailscale
```

### Verifying Access

```bash
# Test API server access
kubectl get nodes

# Check your permissions
kubectl auth can-i --list
```

## Notes

### API Server Proxy Modes

This role configures the operator in **auth mode** by default, which:

- Impersonates requests using tailnet identity
- Integrates with Kubernetes RBAC
- Provides zero-trust access control

For noauth mode deployment, set:

```yaml
tailscale_operator_api_server_proxy_mode: "noauth"
```

### High Availability

The specification assumes single-replica deployment with in-process proxy. For HA deployments using ProxyGroup, additional configuration would be required (currently in alpha).

### Version Compatibility

- Tailscale Operator: Latest stable version recommended
- Kubernetes: 1.27+ (MicroK8s 1.32)
- Helm: 3.x

## References

- [Tailscale Kubernetes Operator Documentation](https://tailscale.com/kb/1236/kubernetes-operator)
- [API Server Proxy Configuration](https://tailscale.com/kb/1437/kubernetes-operator-api-server-proxy)
- [Tailscale Helm Chart](https://github.com/tailscale/tailscale/tree/main/cmd/k8s-operator/charts)
- [Kubernetes RBAC Documentation](https://kubernetes.io/docs/reference/access-authn-authz/rbac/)
- [Ansible Helm Module](https://docs.ansible.com/ansible/latest/collections/kubernetes/core/helm_module.html)
- [Ansible Helm Repository Module](https://docs.ansible.com/ansible/latest/collections/kubernetes/core/helm_repository_module.html)
