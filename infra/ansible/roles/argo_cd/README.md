# ArgoCD Ansible Role

This Ansible role automates the deployment and configuration of ArgoCD using the official Helm chart on Ubuntu 24.04 LTS systems with Kubernetes.

## Documentation

For complete documentation, configuration options, and usage examples, please refer to the [SPEC.md](SPEC.md) file.

## Quick Start

### Prerequisites

- Ubuntu 24.04 LTS
- Kubernetes cluster (e.g., MicroK8s)
- Helm package manager installed
- Tailscale Operator deployed (for ingress)

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

### Required Variables

- `argo_cd_hostname`: Hostname for ArgoCD on the Tailscale network (e.g., "argocd")

## Tags

- `argo-cd`: Run all ArgoCD tasks
- `argo-cd-namespace`: Manage namespace only
- `argo-cd-helm-repo`: Configure Helm repository only
- `argo-cd-install`: Install/upgrade ArgoCD only
- `argo-cd-ingress`: Configure ingress resources only
- `argo-cd-validate`: Run validation tasks only

## License

MIT

## Author

EVEData Platform
