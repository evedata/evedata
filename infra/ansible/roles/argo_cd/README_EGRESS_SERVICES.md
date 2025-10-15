# ArgoCD Egress Services for Remote Clusters

This feature enables ArgoCD to connect to remote Kubernetes clusters via Tailscale egress services.

## Overview

When managing multiple Kubernetes clusters with ArgoCD, you need to establish secure connectivity between the ArgoCD controller and remote clusters. Using Tailscale Kubernetes Operator, we can create egress services that route traffic through the Tailscale network (tailnet) to reach remote clusters securely.

## Configuration

### Required Variables

The following variables must be defined to enable egress services:

1. **`tailscale_dns_name`** - Your Tailscale network's DNS name (e.g., `example.ts.net`)
2. **`argo_cd_remote_cluster_hostnames`** - List of remote cluster hostnames to create egress services for

### Example Configuration

#### In `group_vars/all.yml` or `group_vars/<group>.yml`

```yaml
# Tailnet DNS configuration
tailscale_dns_name: "mycompany.ts.net"

# Remote cluster hostnames for ArgoCD
argo_cd_remote_cluster_hostnames:
  - "k8s-cluster-stg"
  - "k8s-cluster-prd"
  - "k8s-cluster-dev"
```

#### In `group_vars/vault.yml` (encrypted with ansible-vault)

```yaml
# If your tailnet DNS name is sensitive
tailscale_dns_name: "mycompany.ts.net"
```

## How It Works

1. **Service Creation**: For each hostname in `argo_cd_remote_cluster_hostnames`, an egress service is created in the ArgoCD namespace.

2. **FQDN Composition**: Each service is annotated with the full Tailscale FQDN by combining:
   - The cluster hostname (e.g., `k8s-cluster-stg`)
   - The tailnet DNS name (e.g., `mycompany.ts.net`)
   - Result: `k8s-cluster-stg.mycompany.ts.net`

3. **Tailscale Routing**: The Tailscale Kubernetes Operator automatically:
   - Detects services with the `tailscale.com/tailnet-fqdn` annotation
   - Routes traffic through the tailnet to the specified FQDN
   - Handles TLS and authentication transparently

## Generated Resources

For each remote cluster, the following Kubernetes Service is created:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: k8s-cluster-stg
  namespace: argocd
  annotations:
    tailscale.com/tailnet-fqdn: "k8s-cluster-stg.mycompany.ts.net"
  labels:
    app.kubernetes.io/name: egress-service
    app.kubernetes.io/instance: k8s-cluster-stg
    app.kubernetes.io/component: remote-cluster
    app.kubernetes.io/part-of: argocd
    app.kubernetes.io/managed-by: ansible
spec:
  type: ExternalName
  externalName: placeholder
  ports:
    - name: https
      port: 443
      protocol: TCP
```

## Usage in ArgoCD

Once the egress services are created, you can add remote clusters to ArgoCD using the service names as the cluster endpoints:

```bash
# Add a remote cluster to ArgoCD
argocd cluster add k8s-cluster-stg \
  --server https://k8s-cluster-stg.argocd.svc.cluster.local:443 \
  --name staging-cluster
```

Or in ArgoCD Application manifests:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: my-app
  namespace: argocd
spec:
  destination:
    server: https://k8s-cluster-stg.argocd.svc.cluster.local:443
    namespace: default
```

## Prerequisites

1. **Tailscale Kubernetes Operator** must be installed and configured in the cluster
2. **Remote clusters** must be accessible via Tailscale with appropriate hostnames
3. **ArgoCD** must be installed (handled by this role)

## Playbook Execution

The egress services are automatically created when running the ArgoCD playbook with proper variables:

```bash
# Deploy with egress services
ansible-playbook playbooks/argo-cd.yml -e @group_vars/vault.yml -l hzl

# Deploy to specific host
ansible-playbook playbooks/argo-cd.yml -e @group_vars/vault.yml -l htz-eu-fsn-hzl-srv01
```

## Troubleshooting

### Verify Service Creation

```bash
# List egress services
kubectl get services -n argocd -l app.kubernetes.io/component=remote-cluster

# Check service details
kubectl describe service k8s-cluster-stg -n argocd
```

### Check Tailscale Annotations

```bash
# Verify FQDN annotation
kubectl get service k8s-cluster-stg -n argocd -o jsonpath='{.metadata.annotations.tailscale\.com/tailnet-fqdn}'
```

### Test Connectivity

```bash
# From within the ArgoCD pod
kubectl exec -it deploy/argocd-server -n argocd -- curl -k https://k8s-cluster-stg:443
```

## Security Considerations

1. **Network Isolation**: Traffic flows only through the Tailscale network
2. **Authentication**: Tailscale handles device authentication and authorization
3. **Encryption**: All traffic is encrypted end-to-end via WireGuard
4. **No Public Exposure**: Remote clusters don't need public endpoints

## References

- [Tailscale Kubernetes Operator Documentation](https://tailscale.com/kb/1486/kubernetes-operator-multi-cluster-argocd)
- [ArgoCD Multi-Cluster Management](https://argo-cd.readthedocs.io/en/stable/user-guide/clusters/)
