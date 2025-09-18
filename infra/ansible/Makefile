.PHONY: help
help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-20s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: lint
lint: lint-yaml lint-ansible ## Lint all files

.PHONY: lint-ansible
lint-ansible: ## Lint with ansible-lint
	@echo "Running ansible-lint..."
	@ansible-lint --profile production

.PHONY: lint-yaml
lint-yaml: ## Lint YAML files with yamllint
	@echo "Running yamllint..."
	@yamllint -c .yamllint .

.PHONY: test
test: test-syntax test-sanity ## Run all tests

.PHONY: test-sanity
test-sanity: ## Run ansible-test sanity checks
	@echo "Running ansible-test sanity checks..."
	@cd roles && \
	for role in */; do \
		echo "Testing role: $$role"; \
		cd "$$role" && \
		ansible-test sanity 2>/dev/null || true; \
		cd ..; \
	done

.PHONY: test-syntax
test-syntax: ## Check Ansible playbook syntax
	@echo "Checking Ansible playbook syntax..."
	@for playbook in playbooks/*.yml; do \
		echo "Checking: $$playbook"; \
		ansible-playbook --syntax-check -i hosts.yml "$$playbook"; \
	done

.PHONY: clean
clean: ## Clean temporary files
	@echo "Cleaning temporary files..."
	@find . -name "*.retry" -delete
	@find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
	@find . -name "*.pyc" -delete

# Ansible-specific commands
.PHONY: bootstrap
bootstrap: ## Bootstrap hosts (use LIMIT=hostname)
	@if [ -z "$(LIMIT)" ]; then \
		echo "Error: LIMIT variable not set. Usage: make bootstrap LIMIT=hostname"; \
		exit 1; \
	fi
	@echo "Running bootstrap playbook on $(LIMIT)..."
	@ansible-playbook -i hosts.yml playbooks/ansible_bootstrap.yml \
		--limit "$(LIMIT)" \
		--vault-password-file .vault-pass \
		-e @group_vars/vault.yml \
		-u root

.PHONY: ping
ping: ## Test ansible connectivity to all hosts
	@echo "Testing ansible connectivity..."
	@ansible -i hosts.yml all -m ping -u ansible

.PHONY: encrypt
encrypt: ## Encrypt a file with ansible-vault (use FILE=filename)
	@if [ -z "$(FILE)" ]; then \
		echo "Error: FILE variable not set. Usage: make encrypt FILE=filename"; \
		exit 1; \
	fi
	@ansible-vault encrypt --vault-password-file .vault-pass "$(FILE)"

.PHONY: decrypt
decrypt: ## Decrypt a file with ansible-vault (use FILE=filename)
	@if [ -z "$(FILE)" ]; then \
		echo "Error: FILE variable not set. Usage: make decrypt FILE=filename"; \
		exit 1; \
	fi
	@ansible-vault decrypt --vault-password-file .vault-pass "$(FILE)"

.PHONY: edit-vault
edit-vault: ## Edit vault file (use FILE=filename)
	@if [ -z "$(FILE)" ]; then \
		echo "Error: FILE variable not set. Usage: make edit-vault FILE=filename"; \
		exit 1; \
	fi
	@ansible-vault edit --vault-password-file .vault-pass "$(FILE)"

.PHONY: install
install: ## Install Ansible Galaxy requirements
	@echo "Installing Ansible Galaxy requirements..."
	@[ -f requirements.yml ] && ansible-galaxy install -r requirements.yml --force || echo "No requirements.yml found"
	@[ -f collections/requirements.yml ] && ansible-galaxy collection install -r collections/requirements.yml --force || echo "No collections/requirements.yml found"

.PHONY: validate
validate: lint test ## Run all validation checks (lint + tests)
