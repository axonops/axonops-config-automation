import argparse
import os
import sys

from src.axonops import AxonOps


def main():
    parser = argparse.ArgumentParser(description='AxonOps Adaptive Repair CLI')

    parser.add_argument('--org', type=str, required=False, default=os.getenv('AXONOPS_ORG'),
                        help='Name of your organisation')
    parser.add_argument('--cluster', type=str, required=False, default=os.getenv('AXONOPS_CLUSTER'),
                        help='Name of your cluster')
    parser.add_argument('--token', type=str, required=False, default=os.getenv('AXONOPS_TOKEN'),
                        help='AUTH_TOKEN used to authenticate with the API in SaaS')
    parser.add_argument('--api_token', type=str, required=False, default=os.getenv('AXONOPS_API_TOKEN'),
                        help='AXONOPS_API_TOKEN key')
    parser.add_argument('--username', type=str, required=False, default=os.getenv('AXONOPS_USERNAME'),
                        help='Username used for on-prem deployments when authentication is enabled')
    parser.add_argument('--password', type=str, required=False, default=os.getenv('AXONOPS_PASSWORD'),
                        help='Password used for on-prem deployments when authentication is enabled')
    parser.add_argument('--url', type=str, default=os.getenv('AXONOPS_URL'),
                        help='Specify the AxonOps URL if not using the SaaS production environment')

    parser.add_argument('--enabled', action='store_true',
                        help='If present, enables AxonOps Adaptive Repair; if absent, disables it')

    args = parser.parse_args()

    if not args.org or not args.cluster:
        print("The org and the cluster are mandatory")
        sys.exit(1)

    adaptive_repair_url = f"/api/v1/adaptiveRepair/{args.org}/cassandra/{args.cluster}"

    payload = {
        'Active': args.enabled,
        # 'GcGraceThreshold': requested_setting['gc_grace'],
        # 'TableParallelism': requested_setting['parallelism'],
        # 'BlacklistedTables': requested_setting['blacklisted'],
        # 'FilterTWCSTables': requested_setting['filter_twcs'],
        # 'SegmentRetries': requested_setting['retries']
    }

    axonops = AxonOps(args.org,
                      auth_token=args.token,
                      base_url=args.url,
                      username=args.username,
                      password=args.password,
                      cluster_type=args.cluster,
                      api_token=args.api_token)

    axonops.do_request(
        url=adaptive_repair_url,
        method='POST',
        json_data=payload,
    )


if __name__ == '__main__':
    main()
