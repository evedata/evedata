# ArgoCD Ansible Role Specification

## Overview

This Ansible role automates the deployment and configuration of ArgoCD using the official Helm chart on Ubuntu 24.04 LTS systems with Kubernetes. The role configures ArgoCD in non-HA mode by default and exposes the ArgoCD dashboard and API via Tailscale ingress for secure, zero-trust network access.

## Purpose

The role provides a declarative, idempotent deployment of ArgoCD that:

- Deploys ArgoCD for GitOps-based continuous delivery
- Exposes the ArgoCD UI and API securely over the Tailscale network
- Configures appropriate security settings for Tailscale ingress compatibility
- Provides a foundation for declarative application management in Kubernetes

## Prerequisites

### System Requirements

- Ubuntu 24.04 LTS
- Kubernetes cluster (MicroK8s or other distributions)
- Helm package manager installed (via `helm` role)
- Tailscale Operator deployed and configured (via `tailscale_operator` role)

### Tailscale Requirements

- Active Tailscale network with HTTPS and MagicDNS enabled
- Tailscale ingress class available in the Kubernetes cluster
- Appropriate ACL policies configured for ArgoCD access

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
| `argo_cd_hostname` | Hostname for ArgoCD on Tailscale network (e.g., `argocd`) | string | No |

### Optional Variables

#### Helm Configuration

| Variable | Description | Type | Default |
|----------|-------------|------|---------|
| `helm_kubeconfig` | Path to kubeconfig file for Helm operations | string | `/var/snap/microk8s/current/credentials/client.localhost.config` |
| `argo_cd_namespace` | Kubernetes namespace for ArgoCD | string | `argocd` |
| `argo_cd_chart_version` | Specific Helm chart version to install | string | `""` (latest) |
| `argo_cd_helm_repo_name` | Name for the ArgoCD Helm repository | string | `argo` |
| `argo_cd_helm_repo_url` | URL of the ArgoCD Helm repository | string | `https://argoproj.github.io/argo-helm` |
| `argo_cd_release_name` | Helm release name for ArgoCD | string | `argocd` |
| `argo_cd_create_namespace` | Create namespace if it doesn't exist | boolean | `true` |

#### ArgoCD Configuration

| Variable | Description | Type | Default |
|----------|-------------|------|---------|
| `argo_cd_insecure` | Run ArgoCD server in insecure mode (required for Tailscale ingress) | boolean | `true` |
| `argo_cd_admin_enabled` | Enable the admin user | boolean | `true` |
| `argo_cd_redis_ha_enabled` | Enable Redis high availability | boolean | `false` |
| `argo_cd_controller_replicas` | Number of application controller replicas | integer | `1` |
| `argo_cd_server_replicas` | Number of ArgoCD server replicas | integer | `1` |
| `argo_cd_repo_server_replicas` | Number of repository server replicas | integer | `1` |
| `argo_cd_applicationset_replicas` | Number of ApplicationSet controller replicas | integer | `1` |

#### Ingress Configuration

| Variable | Description | Type | Default |
|----------|-------------|------|---------|
| `argo_cd_ingress_enabled` | Enable Tailscale ingress for ArgoCD | boolean | `true` |
| `argo_cd_ingress_class` | Ingress class to use | string | `tailscale` |
| `argo_cd_ingress_path_type` | Path type for ingress rules | string | `Prefix` |
| `argo_cd_grpc_ingress_enabled` | Enable separate ingress for gRPC API | boolean | `true` |
| `argo_cd_grpc_hostname` | Hostname for ArgoCD gRPC API (e.g., `argocd-grpc`) | string | `"{{ argo_cd_hostname }}-grpc"` |

#### Resource Configuration

| Variable | Description | Type | Default |
|----------|-------------|------|---------|
| `argo_cd_server_resources` | Resource limits and requests for server pods | dict | `{}` |
| `argo_cd_controller_resources` | Resource limits and requests for controller pods | dict | `{}` |
| `argo_cd_repo_server_resources` | Resource limits and requests for repo server pods | dict | `{}` |
| `argo_cd_redis_resources` | Resource limits and requests for Redis pods | dict | `{}` |
| `argo_cd_applicationset_resources` | Resource limits and requests for ApplicationSet controller pods | dict | `{}` |

#### Additional Configuration

| Variable | Description | Type | Default |
|----------|-------------|------|---------|
| `argo_cd_extra_values` | Additional Helm values to pass to the chart | dict | `{}` |
| `argo_cd_server_extra_args` | Additional arguments for ArgoCD server | list | `[]` |
| `argo_cd_controller_extra_args` | Additional arguments for application controller | list | `[]` |
| `argo_cd_repo_server_extra_env` | Additional environment variables for repo server | list | `[]` |

## Task Flow

The role executes the following high-level tasks:

1. **Namespace Management**
   - Creates the ArgoCD namespace if it doesn't exist
   - Configures appropriate labels and annotations

2. **Helm Repository Configuration**
   - Adds the official ArgoCD Helm repository
   - Updates repository metadata to ensure latest charts are available

3. **Chart Deployment**
   - Installs or upgrades the ArgoCD Helm chart
   - Configures insecure mode for Tailscale ingress compatibility
   - Sets appropriate replica counts for non-HA deployment
   - Applies any custom values specified in variables

4. **Ingress Configuration**
   - Creates Tailscale ingress for ArgoCD UI
   - Optionally creates separate ingress for gRPC API
   - Configures TLS with appropriate hostnames

5. **Validation**
   - Verifies ArgoCD pods are running
   - Checks ingress resources are created
   - Validates connectivity via Tailscale network

## Usage Examples

### Basic Usage

```yaml
---
- name: Deploy ArgoCD
  hosts: hzl
  become: true
  vars:
    argo_cd_hostname: "argocd"
  roles:
    - argo_cd
```

### Advanced Configuration

```yaml
---
- name: Deploy ArgoCD with Custom Configuration
  hosts: prd
  become: true
  vars:
    # Hostname Configuration
    argo_cd_hostname: "argocd-prod"
    argo_cd_grpc_hostname: "argocd-grpc-prod"

    # ArgoCD Configuration
    argo_cd_namespace: "gitops"
    argo_cd_chart_version: "7.6.8"
    argo_cd_admin_enabled: false

    # Resource Configuration
    argo_cd_server_resources:
      limits:
        cpu: "1"
        memory: "1Gi"
      requests:
        cpu: "250m"
        memory: "512Mi"
    argo_cd_controller_resources:
      limits:
        cpu: "2"
        memory: "2Gi"
      requests:
        cpu: "500m"
        memory: "1Gi"
    argo_cd_repo_server_resources:
      limits:
        cpu: "1"
        memory: "1Gi"
      requests:
        cpu: "250m"
        memory: "256Mi"

    # Custom Helm values
    argo_cd_extra_values:
      server:
        config:
          url: "https://argocd-prod.{{ tailscale_tailnet }}.ts.net"
          "application.instanceLabelKey": "argocd.argoproj.io/instance"
      controller:
        metrics:
          enabled: true
          serviceMonitor:
            enabled: true
  roles:
    - argo_cd
```

### High Availability Configuration

```yaml
---
- name: Deploy ArgoCD in HA Mode
  hosts: prd
  become: true
  vars:
    argo_cd_hostname: "argocd-ha"

    # Enable HA components
    argo_cd_redis_ha_enabled: true
    argo_cd_controller_replicas: 3
    argo_cd_server_replicas: 2
    argo_cd_repo_server_replicas: 2
    argo_cd_applicationset_replicas: 2

    # Anti-affinity rules for HA
    argo_cd_extra_values:
      controller:
        affinity:
          podAntiAffinity:
            preferredDuringSchedulingIgnoredDuringExecution:
              - weight: 100
                podAffinityTerm:
                  labelSelector:
                    matchLabels:
                      app.kubernetes.io/name: argocd-application-controller
                  topologyKey: kubernetes.io/hostname
      server:
        affinity:
          podAntiAffinity:
            preferredDuringSchedulingIgnoredDuringExecution:
              - weight: 100
                podAffinityTerm:
                  labelSelector:
                    matchLabels:
                      app.kubernetes.io/name: argocd-server
                  topologyKey: kubernetes.io/hostname
  roles:
    - argo_cd
```

### Multi-Environment Deployment

In `group_vars/all.yml`:

```yaml
helm_kubeconfig: /var/snap/microk8s/current/credentials/client.localhost.config
argo_cd_namespace: argocd
argo_cd_insecure: true
argo_cd_ingress_enabled: true
```

In `group_vars/stg.yml`:

```yaml
argo_cd_hostname: "argocd-staging"
argo_cd_admin_enabled: true
```

In `group_vars/prd.yml`:

```yaml
argo_cd_hostname: "argocd-production"
argo_cd_chart_version: "7.6.8"  # Pin version for production
argo_cd_admin_enabled: false
argo_cd_controller_replicas: 2
```

Playbook:

```yaml
---
- name: Deploy ArgoCD Across Environments
  hosts: all
  become: true
  roles:
    - argo_cd
```

## Dependencies

### Role Dependencies

- `microk8s` or equivalent: Kubernetes cluster must be installed and configured
- `helm`: Helm package manager must be installed
- `tailscale_operator`: Tailscale Operator must be deployed for ingress functionality

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

- `argo-cd`: Run all ArgoCD tasks
- `argo-cd-namespace`: Manage namespace only
- `argo-cd-helm-repo`: Configure Helm repository only
- `argo-cd-install`: Install/upgrade ArgoCD only
- `argo-cd-ingress`: Configure ingress resources only
- `argo-cd-validate`: Run validation tasks only

### Tag Usage Examples

Configure repository only:

```bash
ansible-playbook playbooks/argo-cd.yml --tags argo-cd-helm-repo
```

Install and configure ingress:

```bash
ansible-playbook playbooks/argo-cd.yml --tags argo-cd-install,argo-cd-ingress
```

## Security Considerations

### Insecure Mode

- The role configures ArgoCD server with `insecure: true` by default
- This is required for Tailscale ingress as TLS termination happens at the Tailscale level
- The connection remains secure as it's only accessible via the Tailscale network

### Admin User

- The admin user is enabled by default for initial setup
- Consider disabling it in production and using SSO/OIDC instead
- Store the initial admin password securely

### Network Security

- ArgoCD is only accessible via the Tailscale network
- Access control must be properly configured in Tailscale ACLs
- Consider implementing RBAC policies within ArgoCD

### Secret Management

- Use Kubernetes secrets or external secret management solutions
- Never commit sensitive data to Git repositories
- Consider using tools like Sealed Secrets or External Secrets Operator

## Idempotency

The role is fully idempotent and can be run multiple times safely:

- Helm repository addition is idempotent
- Chart installation uses `present` state by default
- Namespace creation checks for existence
- Ingress resources are managed declaratively

## Troubleshooting

### Common Issues

1. **ArgoCD Server Not Starting**
   - Check pod logs: `kubectl logs -n argocd deployment/argocd-server`
   - Verify resource limits are adequate
   - Ensure namespace exists and has proper permissions

2. **Ingress Not Accessible**
   - Verify Tailscale Operator is running
   - Check ingress resource: `kubectl get ingress -n argocd`
   - Ensure MagicDNS and HTTPS are enabled in Tailscale
   - Verify hostname resolution: `nslookup <hostname>.<tailnet>.ts.net`

3. **Helm Chart Installation Fails**
   - Verify kubeconfig path is correct
   - Check Helm repository is accessible
   - Review Helm release status: `helm list -n argocd`

### Debug Commands

```bash
# Check ArgoCD pods status
kubectl get pods -n argocd

# View ArgoCD server logs
kubectl logs -n argocd deployment/argocd-server

# Check ingress configuration
kubectl describe ingress -n argocd

# Get Helm release values
helm get values argocd -n argocd

# Test ArgoCD API access
curl -k https://<argo-cd-hostname>.<tailnet>.ts.net/api/v1/session

# Get initial admin password
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
```

## Configuration After Deployment

### Accessing ArgoCD UI

After successful deployment, access ArgoCD via:

```
https://<argo-cd-hostname>.<tailnet-name>.ts.net
```

### Initial Admin Password

Retrieve the initial admin password:

```bash
kubectl -n argocd get secret argocd-initial-admin-secret \
  -o jsonpath="{.data.password}" | base64 -d
```

### CLI Configuration

Configure ArgoCD CLI:

```bash
# Login to ArgoCD
argocd login <argo-cd-hostname>.<tailnet-name>.ts.net \
  --username admin \
  --password <initial-password> \
  --insecure

# Add cluster (if needed)
argocd cluster add <context-name>

# Create first application
argocd app create <app-name> \
  --repo <git-repo-url> \
  --path <path> \
  --dest-server https://kubernetes.default.svc \
  --dest-namespace <namespace>
```

## Notes

### Non-HA vs HA Deployment

This role defaults to non-HA configuration suitable for:

- Development and staging environments
- Single-node Kubernetes clusters
- Cost-conscious deployments

For production HA deployments:

- Enable Redis HA
- Increase replica counts for all components
- Configure pod anti-affinity rules
- Consider using external Redis/database

### Tailscale Ingress Limitations

- TLS is mandatory for Tailscale ingress
- Only `Prefix` path type is supported
- First connection may be slow due to certificate provisioning
- Exposed only on port 443

### Version Compatibility

- ArgoCD: 2.12+ recommended
- Kubernetes: 1.27+ (MicroK8s 1.32)
- Helm: 3.x
- Tailscale Operator: Latest stable version

## References

- [ArgoCD Documentation](https://argo-cd.readthedocs.io/)
- [ArgoCD Helm Chart](https://github.com/argoproj/argo-helm/tree/main/charts/argo-cd)
- [ArgoCD Helm Chart Values](https://github.com/argoproj/argo-helm/blob/main/charts/argo-cd/values.yaml)
- [Tailscale Kubernetes Ingress](https://tailscale.com/kb/1439/kubernetes-operator-cluster-ingress)
- [Ansible Helm Module](https://docs.ansible.com/ansible/latest/collections/kubernetes/core/helm_module.html)
- [ArgoCD Best Practices](https://argo-cd.readthedocs.io/en/stable/user-guide/best_practices/)
