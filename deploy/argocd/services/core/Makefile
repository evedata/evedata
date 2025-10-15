# Makefile for ArgoCD common services deployment
# Run from repository root: make -C deploy/argocd/common <target>

.PHONY: help lint template-default template-hzl template-stg template-prd \
        deploy-hzl deploy-stg deploy-prd diff-hzl diff-stg diff-prd \
        validate clean

# Default target
help:
	@echo "ArgoCD Common Services Deployment"
	@echo ""
	@echo "Validation targets:"
	@echo "  lint              - Validate Helm chart syntax and structure"
	@echo "  validate          - Run all validation checks"
	@echo ""
	@echo "Template targets (dry-run):"
	@echo "  template-default  - Generate manifests with default values"
	@echo "  template-hzl      - Generate manifests for hzl cluster"
	@echo "  template-stg      - Generate manifests for stg cluster"
	@echo "  template-prd      - Generate manifests for prd cluster"
	@echo ""
	@echo "Diff targets (compare with cluster):"
	@echo "  diff-hzl          - Show what would change in hzl cluster"
	@echo "  diff-stg          - Show what would change in stg cluster"
	@echo "  diff-prd          - Show what would change in prd cluster"
	@echo ""
	@echo "Deployment targets:"
	@echo "  deploy-hzl        - Deploy to hzl cluster"
	@echo "  deploy-stg        - Deploy to stg cluster"
	@echo "  deploy-prd        - Deploy to prd cluster"
	@echo ""
	@echo "Cleanup targets:"
	@echo "  clean             - Remove generated files"

lint:
	@echo "==> Linting Helm chart..."
	@helm lint bootstrap
	@echo "==> Lint successful!"

template-test:
	@echo "==> Testing template rendering..."
	@helm template test bootstrap --namespace argocd --debug > /dev/null
	@echo "==> Template test successful!"

validate: lint template-test
	@echo "==> All validation checks passed!"

template-default:
	@echo "==> Generating manifests with default values..."
	@helm template bootstrap bootstrap \
		--namespace argocd \
		--values bootstrap/values.yaml

template-hzl:
	@echo "==> Generating manifests for hzl cluster..."
	@helm template bootstrap bootstrap \
		--namespace argocd \
		--values bootstrap/values.yaml \
		--values bootstrap/values-hzl.yaml

template-stg:
	@echo "==> Generating manifests for stg cluster..."
	@helm template bootstrap bootstrap \
		--namespace argocd \
		--values bootstrap/values.yaml \
		--values bootstrap/values-stg.yaml

template-prd:
	@echo "==> Generating manifests for prd cluster..."
	@helm template bootstrap bootstrap \
		--namespace argocd \
		--values bootstrap/values.yaml \
		--values bootstrap/values-prd.yaml

diff-hzl:
	@echo "==> Comparing with hzl cluster..."
	@helm template bootstrap bootstrap \
		--namespace argocd \
		--values bootstrap/values.yaml \
		--values bootstrap/values-hzl.yaml \
		| kubectl diff -f - || true

diff-stg:
	@echo "==> Comparing with stg cluster..."
	@helm template bootstrap bootstrap \
		--namespace argocd \
		--values bootstrap/values.yaml \
		--values bootstrap/values-stg.yaml \
		| kubectl diff -f - || true

diff-prd:
	@echo "==> Comparing with prd cluster..."
	@helm template bootstrap bootstrap \
		--namespace argocd \
		--values bootstrap/values.yaml \
		--values bootstrap/values-prd.yaml \
		| kubectl diff -f - || true

clean:
	@echo "==> Cleaning generated files..."
	@rm -f bootstrap-*.yaml
	@echo "==> Clean complete!"
