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
AXONOPS_URL ?= https://dash.axonops.cloud

# Default to use pipenv unless disabled
PIPENV ?= false
ifeq ($(PIPENV),true)
PIPENVCMD=pipenv run
else
PIPENVCMD=
endif

check-env:
	@echo $(ANSIBLE_COLLECTIONS_PATH)
	@if [ ! "$(AXONOPS_TOKEN)" ]; then echo "$(BOLD)$(RED)AXONOPS_TOKEN is not set$(RESET)"; exit 1;fi


check: ## run pre-commit tests
	@${PIPENVCMD} pre-commit run --all-files

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

endpoints: check-env ## Create alert endpoints and integrations
	@${PIPENVCMD} ansible-playbook -i localhost, setup_alert_endpoints.yml --diff ${EXTRA}

routes: check-env ## Create alert routes
	@${PIPENVCMD} ansible-playbook -vvv -i localhost, setup_alert_routes.yml --diff ${EXTRA}

metrics-alerts: check-env ## Create alerts based on metrics
	@${PIPENVCMD} ansible-playbook -vvv -i localhost, setup_metrics_alerts.yml --diff ${EXTRA}

log-alerts: check-env ## Create alerts based on logs
	@${PIPENVCMD} ansible-playbook -i localhost, setup_log_alerts.yml --diff ${EXTRA}

service-checks: check-env ## Create alerts for TCP and shell connections
	@${PIPENVCMD} ansible-playbook -i localhost, setup_service_checks.yml --diff ${EXTRA}
