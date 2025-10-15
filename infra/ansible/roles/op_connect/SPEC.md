# 1Password Connect Operator Ansible Role Specification

## Overview

This Ansible role automates the deployment and configuration of the 1Password Connect server and Kubernetes Operator using Helm charts on Ubuntu 24.04 LTS systems with MicroK8s. The role provides secure secrets management for Kubernetes workloads by integrating 1Password's enterprise-grade password manager with native Kubernetes secret resources.

## Purpose

The role provides a declarative, idempotent deployment of the 1Password Connect infrastructure that:

- Deploys the 1Password Connect server for API-based secret access
- Installs the 1Password Kubernetes Operator for automatic secret synchronization
- Enables secure credential management across Kubernetes workloads
- Provides a foundation for centralized secrets management with 1Password vaults

## Prerequisites

### System Requirements

- Ubuntu 24.04 LTS
- MicroK8s installed and configured (via `microk8s` role)
- Helm package manager installed (via `helm` role)
- Active 1Password Business or Enterprise account

### 1Password Requirements

- 1Password Secrets Automation workflow configured with:
  - Valid Connect server credentials JSON file
  - Operator token generated for Kubernetes integration
  - Appropriate vault access permissions configured
- 1Password CLI installed (optional, for credential generation)

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
| `op_connect_credentials_file` | Path to 1Password Connect credentials JSON file (relative to `infra/ansible/files/`) | string | No |
| `op_connect_operator_token` | 1Password Operator authentication token | string | **Yes** |

### Optional Variables

#### Helm Configuration

| Variable | Description | Type | Default |
|----------|-------------|------|---------|
| `helm_kubeconfig` | Path to kubeconfig file for Helm operations | string | `/var/snap/microk8s/current/credentials/client.config` |
| `op_connect_namespace` | Kubernetes namespace for 1Password components | string | `onepassword` |
| `op_connect_chart_version` | Specific Helm chart version to install | string | `""` (latest) |
| `op_connect_helm_repo_name` | Name for the 1Password Helm repository | string | `1password` |
| `op_connect_helm_repo_url` | URL of the 1Password Helm repository | string | `https://1password.github.io/connect-helm-charts` |
| `op_connect_release_name` | Helm release name for 1Password Connect | string | `onepassword-connect` |
| `op_connect_create_namespace` | Create namespace if it doesn't exist | boolean | `true` |

#### Connect Server Configuration

| Variable | Description | Type | Default |
|----------|-------------|------|---------|
| `op_connect_server_create` | Deploy Connect server | boolean | `true` |
| `op_connect_server_replica_count` | Number of Connect server replicas | integer | `1` |
| `op_connect_server_version` | Connect server container image version | string | `""` (chart default) |
| `op_connect_server_resources` | Resource requests/limits for Connect server API | dict | `{}` |
| `op_connect_server_node_selector` | Node selector for Connect server pods | dict | `{}` |

#### Operator Configuration

| Variable | Description | Type | Default |
|----------|-------------|------|---------|
| `op_connect_operator_create` | Deploy Kubernetes Operator | boolean | `true` |
| `op_connect_operator_replica_count` | Number of operator replicas | integer | `1` |
| `op_connect_operator_version` | Operator container image version | string | `""` (chart default) |
| `op_connect_operator_log_level` | Logging level for the operator | string | `info` |
| `op_connect_operator_polling_interval` | Secret sync polling interval in seconds | integer | `600` |
| `op_connect_operator_auto_restart` | Auto-restart deployments on secret changes | boolean | `false` |
| `op_connect_operator_watch_namespace` | Namespaces to monitor (empty list for all) | list | `[]` |
| `op_connect_operator_resources` | Resource requests/limits for Operator | dict | `{}` |

#### Advanced Configuration

| Variable | Description | Type | Default |
|----------|-------------|------|---------|
| `op_connect_extra_values` | Additional Helm values to pass to the chart | dict | `{}` |
| `op_connect_cleanup_credentials` | Remove credentials file after deployment | boolean | `true` |
| `op_connect_credentials_upload_path` | Remote path for temporary credentials file | string | `/tmp/op_connect_operator_credentials.json` |

## Task Flow

The role executes the following high-level tasks:

1. **Namespace Management**
   - Creates the 1Password namespace if it doesn't exist
   - Configures appropriate labels and annotations

2. **Credentials Handling**
   - Uploads encrypted credentials JSON file to target host
   - Ensures proper file permissions (600)
   - Stores file path for Helm deployment

3. **Helm Repository Configuration**
   - Adds the official 1Password Helm repository
   - Updates repository metadata to ensure latest charts are available

4. **Chart Deployment**
   - Installs or upgrades the 1Password Connect Helm chart
   - Configures Connect server with uploaded credentials
   - Configures Operator with provided token
   - Applies any custom values specified in variables

5. **Cleanup**
   - Removes uploaded credentials file from target host
   - Ensures no sensitive data remains on the system

6. **Validation**
   - Verifies Connect server deployment is running
   - Checks that operator pod(s) are ready
   - Validates API connectivity

## Usage Examples

### Basic Usage

```yaml
---
- name: Deploy 1Password Connect
  hosts: hzl
  become: true
  vars:
    op_connect_credentials_file: "op_connect_operator_credentials.json"
    op_connect_operator_token: "{{ op_connect_operator_token }}"
  roles:
    - op_connect
```

### Advanced Configuration

```yaml
---
- name: Deploy 1Password Connect with Custom Configuration
  hosts: prd
  become: true
  vars:
    # Credentials Configuration (from vault)
    op_connect_credentials_file: "op_connect_operator_credentials.json"
    op_connect_operator_token: "{{ op_connect_operator_token }}"

    # Deployment Configuration
    op_connect_namespace: "secrets-management"
    op_connect_chart_version: "1.15.0"
    op_connect_server_replica_count: 2
    op_connect_operator_replica_count: 2

    # Operator Configuration
    op_connect_operator_log_level: "debug"
    op_connect_operator_polling_interval: 300
    op_connect_operator_auto_restart: true
    op_connect_operator_watch_namespace:
      - "default"
      - "production"

    # Resource Configuration
    op_connect_extra_values:
      connect:
        resources:
          limits:
            cpu: "500m"
            memory: "512Mi"
          requests:
            cpu: "200m"
            memory: "256Mi"
      operator:
        resources:
          limits:
            cpu: "250m"
            memory: "256Mi"
          requests:
            cpu: "100m"
            memory: "128Mi"
      nodeSelector:
        kubernetes.io/hostname: "htz-eu-fsn-prd-srv01"
  roles:
    - op_connect
```

### Multi-Environment Deployment

In `group_vars/all.yml`:

```yaml
helm_kubeconfig: /var/snap/microk8s/current/credentials/client.config
op_connect_namespace: onepassword
op_connect_operator_create: true
op_connect_server_create: true
op_connect_cleanup_credentials: true
```

In `group_vars/stg.yml`:

```yaml
op_connect_credentials_file: "stg/op_connect_operator_credentials.json"
op_connect_operator_log_level: "debug"
op_connect_operator_auto_restart: false
```

In `group_vars/prd.yml`:

```yaml
op_connect_credentials_file: "prd/op_connect_operator_credentials.json"
op_connect_chart_version: "1.15.0"  # Pin version for production
op_connect_server_replica_count: 2
op_connect_operator_replica_count: 2
op_connect_operator_polling_interval: 300
```

In `group_vars/vault.yml` (encrypted):

```yaml
op_connect_operator_token: "your-operator-token-here"
```

Directory structure for credentials:

```
infra/ansible/files/
├── hzl/
│   └── op_connect_operator_credentials.json  # Encrypted with ansible-vault
├── stg/
│   └── op_connect_operator_credentials.json  # Encrypted with ansible-vault
└── prd/
    └── op_connect_operator_credentials.json  # Encrypted with ansible-vault
```

Playbook:

```yaml
---
- name: Deploy 1Password Connect Across Environments
  hosts: all
  become: true
  vars:
    op_connect_operator_token: "{{ op_connect_operator_token }}"
  roles:
    - op_connect
```

## Dependencies

### Role Dependencies

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

- `op-connect`: Run all 1Password Connect tasks
- `op-connect-namespace`: Manage namespace only
- `op-connect-credentials`: Handle credentials upload/cleanup only
- `op-connect-helm-repo`: Configure Helm repository only
- `op-connect-install`: Install/upgrade 1Password Connect only
- `op-connect-cleanup`: Run cleanup tasks only
- `op-connect-validate`: Run validation tasks only

### Tag Usage Examples

Upload credentials and install:

```bash
ansible-playbook playbooks/op-connect.yml --tags op-connect-credentials,op-connect-install
```

Install and validate without cleanup:

```bash
ansible-playbook playbooks/op-connect.yml --skip-tags op-connect-cleanup
```

## Security Considerations

### Credential Management

- **ALWAYS** encrypt `op_connect_operator_credentials.json` files with Ansible Vault
- **ALWAYS** store operator tokens in Ansible Vault
- Never commit plaintext credentials to version control
- Use separate credentials for different environments
- Ensure credentials file is removed after deployment (`op_connect_cleanup_credentials: true`)

### File Permissions

- Credentials file is uploaded with 600 permissions (read/write owner only)
- Temporary files are stored in `/tmp` and removed after deployment
- Ensure target hosts have secure `/tmp` mounting (noexec not required)

### Network Security

- Connect server exposes API on port 8080 (ClusterIP by default)
- Operator communicates with Connect server internally
- No external network exposure by default
- Configure NetworkPolicies for additional isolation if required

### Kubernetes RBAC

- Operator requires cluster-wide permissions for secret management
- Connect server uses service account for authentication
- Follow principle of least privilege for vault access
- Regularly audit operator permissions and secret access

### Vault Configuration

After deployment, configure 1Password vaults for Kubernetes access:

```yaml
# Example OnePasswordItem resource
apiVersion: onepassword.com/v1
kind: OnePasswordItem
metadata:
  name: database-credentials
  namespace: default
spec:
  itemPath: "vaults/Production/items/Database"
```

## Idempotency

The role is fully idempotent and can be run multiple times safely:

- Helm repository addition is idempotent
- Chart installation uses `present` state by default
- Namespace creation checks for existence
- Credentials upload overwrites existing file
- Cleanup tasks handle missing files gracefully
- Validation tasks are read-only

## Troubleshooting

### Common Issues

1. **Credentials File Not Found**
   - Verify file exists in `infra/ansible/files/<environment>/`
   - Check file is encrypted with ansible-vault
   - Ensure correct environment group is targeted

2. **Operator Token Invalid**
   - Regenerate token in 1Password Secrets Automation
   - Verify token is correctly stored in vault
   - Check token has appropriate permissions

3. **Helm Chart Installation Fails**
   - Verify kubeconfig path is correct
   - Check MicroK8s is running: `microk8s status`
   - Ensure Helm is installed: `helm version`
   - Review logs: `kubectl logs -n onepassword -l app=onepassword-connect`

4. **Connect Server Not Accessible**
   - Verify Connect server pods are running: `kubectl get pods -n onepassword`
   - Check service endpoints: `kubectl get svc -n onepassword`
   - Review Connect logs: `kubectl logs -n onepassword -l app=onepassword-connect`

5. **Secret Synchronization Issues**
   - Check operator logs: `kubectl logs -n onepassword -l app=onepassword-operator`
   - Verify polling interval configuration
   - Ensure vault permissions are correct in 1Password
   - Check OnePasswordItem resource status

### Debug Commands

```bash
# Check 1Password components status
kubectl get all -n onepassword

# View Connect server logs
kubectl logs -n onepassword deployment/onepassword-connect

# View operator logs
kubectl logs -n onepassword deployment/onepassword-connect-operator

# Describe Connect deployment
kubectl describe deployment -n onepassword onepassword-connect

# Check Helm release status
helm list -n onepassword

# Get Helm values
helm get values onepassword-connect -n onepassword

# Test Connect server API (from within cluster)
kubectl run test-pod --rm -it --image=curlimages/curl -- \
  curl http://onepassword-connect.onepassword.svc.cluster.local:8080/health

# Check OnePasswordItem resources
kubectl get onepassworditems -A

# Describe specific OnePasswordItem
kubectl describe onepassworditem <item-name> -n <namespace>
```

## Configuration After Deployment

### Creating OnePasswordItem Resources

After successful deployment, create OnePasswordItem resources to sync secrets:

```yaml
---
apiVersion: onepassword.com/v1
kind: OnePasswordItem
metadata:
  name: app-secrets
  namespace: default
spec:
  itemPath: "vaults/Production/items/ApplicationSecrets"
```

### Verifying Secret Creation

```bash
# Check if secret was created
kubectl get secret app-secrets -n default

# View secret data (base64 encoded)
kubectl get secret app-secrets -n default -o yaml
```

### Using Secrets in Deployments

```yaml
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
spec:
  template:
    spec:
      containers:
      - name: app
        env:
        - name: API_KEY
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: api_key
```

### Configuring Auto-Restart

To enable automatic pod restarts when secrets change:

```yaml
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
  annotations:
    operator.1password.io/auto-restart: "true"
spec:
  # ... deployment spec
```

## Notes

### High Availability Considerations

For production deployments, consider:

- Running multiple Connect server replicas for redundancy
- Running multiple operator replicas for availability
- Configuring pod anti-affinity rules for distribution
- Implementing proper resource limits and requests

### Performance Tuning

- Adjust `op_connect_operator_polling_interval` based on secret change frequency
- Lower values increase API calls but provide faster updates
- Consider vault structure for optimal performance
- Monitor Connect server resource usage

### Version Compatibility

- 1Password Connect: Latest stable version recommended
- Kubernetes: 1.27+ (MicroK8s 1.32)
- Helm: 3.x
- 1Password Business or Enterprise account required

### Backup and Recovery

- Credentials file should be backed up securely
- Operator token should be stored in multiple secure locations
- Regular testing of credential rotation procedures
- Document recovery procedures for credential compromise

## References

- [1Password Connect Documentation](https://developer.1password.com/docs/connect)
- [1Password Kubernetes Operator Documentation](https://developer.1password.com/docs/k8s/operator)
- [1Password Connect Helm Chart](https://github.com/1Password/connect-helm-charts)
- [1Password Secrets Automation](https://developer.1password.com/docs/connect/get-started)
- [Kubernetes Secret Management Best Practices](https://kubernetes.io/docs/concepts/configuration/secret/)
- [Ansible Helm Module](https://docs.ansible.com/ansible/latest/collections/kubernetes/core/helm_module.html)
- [Ansible Vault Documentation](https://docs.ansible.com/ansible/latest/user_guide/vault.html)
