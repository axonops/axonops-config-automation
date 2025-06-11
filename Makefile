#
#
#
.ONESHELL:
.SHELL := /bin/bash
.PHONY: common
.EXPORT_ALL_VARIABLES:
CURRENT_FOLDER=$(shell basename "$$(pwd)")
# Bug running on OSX
OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
UNAME=$(shell uname -s)
ANSIBLE_COLLECTIONS_PATH=./

# Default to use pipenv unless disabled
PIPENV ?= false
ifeq ($(PIPENV),true)
PIPENVCMD=pipenv run
else
PIPENVCMD=
endif

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

check-env:
	@echo $(ANSIBLE_COLLECTIONS_PATH)
	@if [ ! "$(AXONOPS_ORG)" ]; then echo "$(BOLD)$(RED)AXONOPS_ORG is not set$(RESET)"; exit 1;fi

check: ## run pre-commit tests
	@${PIPENVCMD} pre-commit run --all-files

endpoints: check-env ## Create alert endpoints and integrations
	@${PIPENVCMD} ansible-playbook -i localhost, setup_alert_endpoints.yml --diff ${EXTRA}

routes: check-env ## Create alert routes
	@${PIPENVCMD} ansible-playbook -i localhost, setup_alert_routes.yml --diff ${EXTRA}

metrics-alerts: check-env ## Create alerts based on metrics
	@${PIPENVCMD} ansible-playbook -i localhost, setup_metrics_alerts.yml --diff ${EXTRA}

log-alerts: check-env ## Create alerts based on logs
	@${PIPENVCMD} ansible-playbook -i localhost, setup_log_alerts.yml --diff ${EXTRA}

service-checks: check-env ## Create alerts for TCP and shell connections
	@${PIPENVCMD} ansible-playbook -i localhost, setup_service_checks.yml --diff ${EXTRA}

backups: check-env ## Create backup
	@${PIPENVCMD} ansible-playbook -i localhost, setup_backups.yml --diff ${EXTRA}

commitlog: check-env ### Create commitlog archive
	@${PIPENVCMD} ansible-playbook -i localhost, setup_commitlogs_archive.yml --diff ${EXTRA}

dashboard: check-env ## Create custom dashboard
	@${PIPENVCMD} ansible-playbook -i localhost, setup_dashboards.yml --diff ${EXTRA}

validate: ## Validate YAML config
	@${PIPENVCMD} python validate_yaml.py
