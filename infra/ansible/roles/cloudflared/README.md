# Ansible Role: cloudflared

An Ansible role to deploy and manage Cloudflare Tunnel (cloudflared) on Kubernetes clusters. This role creates a secure tunnel between your Kubernetes services and Cloudflare's edge network, enabling secure exposure of internal services without opening inbound ports.

## Features

- Automated deployment of cloudflared in Kubernetes
- Integration with 1Password for secure credential management
- Configurable ingress rules for service routing
- Built-in health checks and metrics endpoint
- Support for multiple replicas for high availability
- Namespace isolation with proper labeling
- Comprehensive validation and status reporting

## Requirements

### Prerequisites

1. **Kubernetes Cluster**: A working Kubernetes cluster (tested with MicroK8s)
2. **1Password Operator**: Must be installed in the cluster (use the `op_connect` role)
3. **Cloudflare Account**: Active Cloudflare account with a configured tunnel
4. **Ansible Collections**:
   - `kubernetes.core` >= 3.0.0
   - `ansible.builtin` >= 2.15.0

### Cloudflare Setup

Before using this role, you need to:

1. Create a Cloudflare Tunnel in your Cloudflare dashboard
2. Generate a tunnel token
3. Store the tunnel token in 1Password
4. Configure DNS records to point to your tunnel

## Role Variables

### Required Variables

These variables must be defined in your playbook or inventory:

```yaml
# Kubernetes configuration
helm_kubeconfig: /path/to/kubeconfig

# 1Password configuration
cloudflared_onepassword_vault: "Infrastructure"  # Vault containing the token
cloudflared_onepassword_item: "Cloudflared Tunnel Token"  # Item name in vault

# Ingress rules (at least one rule required, last must be catch-all)
cloudflared_ingress_rules:
  - hostname: app.example.com
    service: http://app-service:80
  - hostname: api.example.com
    service: http://api-service:8080
  - service: http_status:404  # Required catch-all rule
```

### Optional Variables

```yaml
# Namespace configuration
cloudflared_namespace: cloudflared
cloudflared_create_namespace: true

# Deployment configuration
cloudflared_deployment_name: cloudflared
cloudflared_replica_count: 1
cloudflared_image_repository: cloudflare/cloudflared
cloudflared_image_tag: "2025.10.0"
cloudflared_image_pull_policy: IfNotPresent

# Resource limits
cloudflared_resources:
  limits:
    cpu: "200m"
    memory: "256Mi"
  requests:
    cpu: "100m"
    memory: "128Mi"

# Metrics configuration
cloudflared_metrics_enabled: true
cloudflared_metrics_port: 2000
cloudflared_metrics_address: "0.0.0.0"

# Tunnel configuration
cloudflared_tunnel_name: "k8s-tunnel"  # Optional tunnel name
```

For a complete list of variables, see `defaults/main.yml`.

## Dependencies

This role depends on the 1Password Operator being installed in your cluster. You can install it using the `op_connect` role:

```yaml
- name: Install 1Password Operator
  ansible.builtin.include_role:
    name: op_connect
```

## Example Playbook

### Basic Usage

```yaml
---
- name: Deploy Cloudflare Tunnel
  hosts: hzl
  become: true
  vars:
    helm_kubeconfig: /var/snap/microk8s/current/credentials/client.config
    cloudflared_onepassword_vault: "Infrastructure"
    cloudflared_onepassword_item: "Cloudflared Tunnel Token"
    cloudflared_ingress_rules:
      - hostname: app.example.com
        service: http://my-app-service:80
      - hostname: api.example.com
        service: http://my-api-service:8080
      - service: http_status:404

  tasks:
    - name: Deploy cloudflared
      ansible.builtin.include_role:
        name: cloudflared
```

### Advanced Configuration

```yaml
---
- name: Deploy Cloudflare Tunnel with Advanced Configuration
  hosts: hzl
  become: true
  vars:
    helm_kubeconfig: /var/snap/microk8s/current/credentials/client.config
    cloudflared_namespace: cloudflare-tunnels
    cloudflared_replica_count: 3

    # 1Password configuration
    op_connect_vault: "prd"
    cloudflared_secret_name: "cloudflared-tunnel-token"

    # Custom resource limits
    cloudflared_resources:
      limits:
        cpu: "500m"
        memory: "512Mi"
      requests:
        cpu: "250m"
        memory: "256Mi"

    # Ingress configuration
    cloudflared_ingress_rules:
      - hostname: www.example.com
        service: http://frontend-service:80
      - hostname: api.example.com
        service: http://backend-service:8080
      - hostname: admin.example.com
        service: http://admin-service:3000
      - service: http_status:404

    # Node placement
    cloudflared_node_selector:
      node-role.kubernetes.io/worker: "true"

    # Pod annotations
    cloudflared_pod_annotations:
      prometheus.io/scrape: "true"
      prometheus.io/port: "2000"

  tasks:
    - name: Deploy cloudflared with custom configuration
      ansible.builtin.include_role:
        name: cloudflared
```

## Directory Structure

```
cloudflared/
├── README.md
├── defaults/
│   └── main.yml      # Default variables
├── meta/
│   └── main.yml      # Role metadata and dependencies
├── tasks/
│   ├── main.yml      # Main task orchestration
│   ├── namespace.yml # Namespace creation and management
│   ├── secret.yml    # OnePasswordItem and secret creation
│   ├── configmap.yml # ConfigMap for cloudflared configuration
│   ├── deployment.yml # Deployment creation and management
│   └── validate.yml  # Validation and health checks
├── handlers/
│   └── main.yml      # Handlers (if needed)
├── templates/        # Jinja2 templates (if needed)
├── files/           # Static files (if needed)
└── vars/            # Role variables (if needed)
```

## Task Execution Flow

1. **Variable Validation**: Ensures all required variables are defined
2. **Namespace Management**: Creates or verifies the namespace exists
3. **Secret Creation**: Creates OnePasswordItem to fetch credentials from 1Password
4. **ConfigMap Creation**: Generates cloudflared configuration
5. **Deployment**: Creates the cloudflared deployment with specified replicas
6. **Validation**: Verifies all resources are created and pods are running

## Monitoring and Troubleshooting

### Check Deployment Status

```bash
kubectl get all -n cloudflared
kubectl describe deployment cloudflared -n cloudflared
```

### View Logs

```bash
kubectl logs -n cloudflared -l app=cloudflared
```

### Access Metrics

The cloudflared pods expose metrics on port 2000:

```bash
kubectl port-forward -n cloudflared deployment/cloudflared 2000:2000
curl http://localhost:2000/metrics
```

### Health Check

```bash
kubectl port-forward -n cloudflared deployment/cloudflared 2000:2000
curl http://localhost:2000/ready
```

## Security Considerations

1. **Credential Management**: Tunnel tokens are stored securely in 1Password and never exposed in plain text
2. **Network Isolation**: Cloudflared runs in its own namespace with appropriate RBAC
3. **Pod Security**: Runs as non-root user with read-only root filesystem
4. **No Auto-Updates**: Auto-updates are disabled to ensure consistent behavior

## Common Issues and Solutions

### Issue: OnePasswordItem CRD not found

**Solution**: Ensure the 1Password Operator is installed:

```yaml
- name: Install 1Password Operator first
  ansible.builtin.include_role:
    name: op_connect
```

### Issue: Pods not starting

**Solution**: Check the logs for authentication issues:

```bash
kubectl logs -n cloudflared -l app=cloudflared
kubectl describe secret -n cloudflared cloudflared-tunnel-token
```

### Issue: Ingress rules not working

**Solution**: Verify the catch-all rule is present as the last rule:

```yaml
cloudflared_ingress_rules:
  - hostname: example.com
    service: http://service:80
  - service: http_status:404  # This must be the last rule
```

## Tags

The role supports the following tags for selective execution:

- `cloudflared`: Run all cloudflared tasks
- `cloudflared-validate`: Run validation tasks only
- `cloudflared-namespace`: Manage namespace
- `cloudflared-secret`: Manage secrets
- `cloudflared-configmap`: Manage ConfigMap
- `cloudflared-deployment`: Manage deployment

Example usage with tags:

```bash
ansible-playbook playbook.yml --tags cloudflared-deployment
```

## License

MIT

## Author Information

Created by the EVEData Team for managing Cloudflare Tunnels in Kubernetes environments.

## Contributing

Contributions are welcome! Please ensure:

1. All tasks are properly named and tagged
2. Variables follow the naming convention
3. Documentation is updated for new features
4. Code passes ansible-lint and yamllint checks
