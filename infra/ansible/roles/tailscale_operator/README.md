# Tailscale Operator Ansible Role

This Ansible role deploys and configures the Tailscale Kubernetes Operator on Ubuntu 24.04 LTS systems running MicroK8s. The operator enables secure access to your Kubernetes API server over the Tailscale network with authentication and authorization.

## Features

- **Automated Deployment**: Fully automated installation using Helm charts
- **API Server Proxy**: Exposes Kubernetes API server securely over Tailscale
- **Auth Mode**: Impersonation-based authentication with Kubernetes RBAC
- **OAuth Integration**: Secure authentication using Tailscale OAuth
- **Idempotent Operations**: Safe to run multiple times
- **Comprehensive Validation**: Built-in health checks and status reporting

## Requirements

### System Requirements

- Ubuntu 24.04 LTS
- MicroK8s installed (via `microk8s` role)
- Helm package manager (via `helm` role)
- Sufficient resources for operator pod(s)

### Tailscale Prerequisites

Before deploying, you need:

1. **Tailscale OAuth Application**
   - Go to [Tailscale Admin Console](https://login.tailscale.com/admin/settings/oauth)
   - Create a new OAuth application
   - Note the Client ID and Client Secret
   - Configure appropriate scopes for Kubernetes operator

2. **Tailscale Network Configuration**
   - HTTPS must be enabled for your tailnet
   - Access control policies configured for port 443 access

### Ansible Requirements

```bash
# Install required collections
ansible-galaxy collection install kubernetes.core
```

## Role Variables

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `tailscale_operator_oauth_client_id` | OAuth application client ID | `k8VxY3...` |
| `tailscale_operator_oauth_client_secret` | OAuth application client secret | `tskey-client-...` |
| `tailscale_operator_hostname` | Hostname for the operator | `k8s-operator` |

### Common Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `tailscale_operator_namespace` | Kubernetes namespace | `tailscale` |
| `tailscale_operator_chart_version` | Helm chart version | Latest |
| `tailscale_operator_log_level` | Logging level | `info` |
| `tailscale_operator_api_server_proxy_mode` | Proxy mode (true=auth, "noauth"=noauth) | `true` |

### Image Configuration

The role explicitly pins container image versions for reproducible deployments:

| Variable | Description | Default |
|----------|-------------|---------|
| `tailscale_operator_image_tag` | Operator container image tag | `v1.88.4` |
| `tailscale_operator_image_digest` | Operator image SHA256 digest | `sha256:9a35d316...` |
| `tailscale_operator_proxy_image_tag` | Proxy container image tag | `v1.88.4` |
| `tailscale_operator_proxy_image_digest` | Proxy image SHA256 digest | `sha256:734c9600...` |

**Note**: Using both tag and digest ensures immutable deployments and prevents unexpected image updates.

For a complete list of variables, see [defaults/main.yml](defaults/main.yml).

## Quick Start

### Step 1: Configure Variables

Create or update your inventory variables:

```yaml
# group_vars/vault.yml (encrypt with ansible-vault)
tailscale_operator_oauth_client_id: "your-client-id"
tailscale_operator_oauth_client_secret: "your-client-secret"

# group_vars/hzl.yml
tailscale_operator_hostname: "k8s-hzl"
```

### Step 2: Create Playbook

```yaml
---
- name: Deploy Tailscale Operator
  hosts: hzl
  become: true
  vars:
    tailscale_operator_oauth_client_id: "{{ tailscale_operator_oauth_client_id }}"
    tailscale_operator_oauth_client_secret: "{{ tailscale_operator_oauth_client_secret }}"
  roles:
    - tailscale_operator
```

### Step 3: Run Playbook

```bash
cd /Users/tony/Code/github.com/evedata/evedata/infra/ansible
ansible-playbook playbooks/tailscale-operator.yml -e @group_vars/vault.yml
```

## Usage Examples

### Basic Deployment

Deploy with minimal configuration:

```yaml
---
- name: Deploy Tailscale Operator
  hosts: hzl
  become: true
  vars:
    tailscale_operator_oauth_client_id: "{{ vault_tailscale_operator_oauth_client_id }}"
    tailscale_operator_oauth_client_secret: "{{ vault_tailscale_operator_oauth_client_secret }}"
    tailscale_operator_hostname: "k8s-operator"
  roles:
    - tailscale_operator
```

### Production Deployment

Deploy with custom configuration and resource limits:

```yaml
---
- name: Deploy Tailscale Operator for Production
  hosts: prd
  become: true
  vars:
    tailscale_operator_oauth_client_id: "{{ vault_tailscale_operator_oauth_client_id }}"
    tailscale_operator_oauth_client_secret: "{{ vault_tailscale_operator_oauth_client_secret }}"
    tailscale_operator_hostname: "k8s-prod"
    tailscale_operator_chart_version: "1.66.0"  # Pin version
    tailscale_operator_log_level: "warn"
    tailscale_operator_extra_values:
      resources:
        limits:
          cpu: "500m"
          memory: "256Mi"
        requests:
          cpu: "100m"
          memory: "128Mi"
  roles:
    - tailscale_operator
```

### Debug Deployment

Deploy with verbose logging for troubleshooting:

```yaml
---
- name: Deploy Tailscale Operator with Debug Logging
  hosts: stg
  become: true
  vars:
    tailscale_operator_oauth_client_id: "{{ vault_tailscale_operator_oauth_client_id }}"
    tailscale_operator_oauth_client_secret: "{{ vault_tailscale_operator_oauth_client_secret }}"
    tailscale_operator_hostname: "k8s-staging"
    tailscale_operator_log_level: "debug"
  roles:
    - tailscale_operator
```

## Tags

Use tags to run specific parts of the role:

```bash
# Deploy everything
ansible-playbook playbooks/tailscale-operator.yml --tags tailscale-operator

# Only configure Helm repository
ansible-playbook playbooks/tailscale-operator.yml --tags tailscale-operator-helm-repo

# Only install/upgrade operator
ansible-playbook playbooks/tailscale-operator.yml --tags tailscale-operator-install

# Only run validation
ansible-playbook playbooks/tailscale-operator.yml --tags tailscale-operator-validate
```

## Post-Deployment Configuration

### Configure kubectl

After successful deployment, configure kubectl to use the API server proxy:

```bash
# Get your tailnet name
TAILNET_NAME="your-tailnet.ts.net"
OPERATOR_HOSTNAME="k8s-operator"

# Add cluster configuration
kubectl config set-cluster tailscale-cluster \
  --server=https://${OPERATOR_HOSTNAME}.${TAILNET_NAME}

# Add context
kubectl config set-context tailscale \
  --cluster=tailscale-cluster \
  --user=$(whoami)

# Use context
kubectl config use-context tailscale

# Test connection
kubectl get nodes
```

### Configure RBAC

Grant access to tailnet users/groups:

```yaml
# rbac-example.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: tailnet-admins
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin
subjects:
- apiGroup: rbac.authorization.k8s.io
  kind: Group
  name: tag:k8s-admins  # Tailscale tag/group
```

Apply RBAC configuration:

```bash
kubectl apply -f rbac-example.yaml
```

## Troubleshooting

### Common Issues

#### OAuth Authentication Fails

```bash
# Check operator logs
kubectl logs -n tailscale deployment/operator

# Verify OAuth credentials
# Ensure client ID and secret are correct in vault
```

#### Helm Installation Fails

```bash
# Check MicroK8s status
microk8s status

# Verify Helm is working
helm version

# List Helm repositories
helm repo list
```

#### API Server Proxy Not Accessible

```bash
# Check operator status
kubectl get all -n tailscale

# Verify Tailscale device
kubectl exec -n tailscale deployment/operator -- tailscale status

# Check ACLs in Tailscale admin console
```

### Debug Commands

```bash
# Get operator status
kubectl get deployment -n tailscale operator -o yaml

# View operator logs
kubectl logs -n tailscale deployment/operator -f

# Check Helm release
helm get values tailscale-operator -n tailscale

# Test API server proxy
curl -k https://<operator-hostname>.<tailnet-name>.ts.net/healthz
```

## Security Best Practices

1. **OAuth Credentials**
   - Always store in Ansible Vault
   - Use separate OAuth apps per environment
   - Rotate credentials regularly

2. **Network Security**
   - Configure Tailscale ACLs appropriately
   - Limit access to necessary devices/users
   - Enable audit logging

3. **Kubernetes RBAC**
   - Follow principle of least privilege
   - Map tailnet groups to Kubernetes roles
   - Regularly audit permissions

## Dependencies

This role depends on:

- `microk8s` - MicroK8s installation
- `helm` - Helm package manager

## License

MIT

## Author Information

EVEData Infrastructure Team

## Additional Resources

- [Full Specification](SPEC.md)
- [Tailscale Kubernetes Operator Documentation](https://tailscale.com/kb/1236/kubernetes-operator)
- [API Server Proxy Guide](https://tailscale.com/kb/1437/kubernetes-operator-api-server-proxy)
- [Kubernetes RBAC Documentation](https://kubernetes.io/docs/reference/access-authn-authz/rbac/)
