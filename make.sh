#!/bin/bash

export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
export UNAME=$(uname -s)
export ANSIBLE_COLLECTIONS_PATH=./
export AXONOPS_URL=${AXONOPS_URL:-https://dash.axonops.cloud}

# Default to use pipenv unless disabled
if [[ "${PIPENV}" == "true" ]]; then
  PIPENVCMD=${PIPENVCMD:-pipenv run}
else
  PIPENVCMD=
fi

case $1 in
  endpoints)
    ${PIPENVCMD} ansible-playbook -i localhost, setup_alert_endpoints.yml --diff ${EXTRA}
    ;;
  routes)
	${PIPENVCMD} ansible-playbook -i localhost, setup_alert_routes.yml --diff ${EXTRA}
    ;;
  metrics-alerts)
	${PIPENVCMD} ansible-playbook -i localhost, setup_metrics_alerts.yml --diff ${EXTRA}
    ;;
  log-alerts)
	${PIPENVCMD} ansible-playbook -i localhost, setup_log_alerts.yml --diff ${EXTRA}
    ;;
  service-checks)
	${PIPENVCMD} ansible-playbook -i localhost, setup_service_checks.yml --diff ${EXTRA}
    ;;
  backups)
	${PIPENVCMD} ansible-playbook -i localhost, setup_backups.yml --diff ${EXTRA}
    ;;
  *)
    echo "Usage: $(basename $0) <endpoints|routes|metrics-alerts|log-alerts|service-checks|backups>"
    ;;
esac
