import argparse
import os
import sys
from typing import Sequence

from .axonops import AxonOps

class Application:
    adaptive_repair_url = "/api/v1/adaptiveRepair"

    def __init__(self):
        """
        This object represents the main application
        """
        # the option taken from the files and argv parameter
        #self.options:dict[str, str] = {}

    def run(self, argv: Sequence):

        parser = argparse.ArgumentParser(description='AxonOps Adaptive Repair CLI')

        parser.add_argument('--org', type=str, required=False, default=os.getenv('AXONOPS_ORG'),
                            help='Name of your organisation')
        parser.add_argument('--cluster', type=str, required=False, default=os.getenv('AXONOPS_CLUSTER'),
                            help='Name of your cluster')
        parser.add_argument('--token', type=str, required=False, default=os.getenv('AXONOPS_TOKEN'),
                            help='AUTH_TOKEN used to authenticate with the API in SaaS')
        parser.add_argument('--username', type=str, required=False, default=os.getenv('AXONOPS_USERNAME'),
                            help='Username used for AxonOps Self-Hosted when authentication is enabled')
        parser.add_argument('--password', type=str, required=False, default=os.getenv('AXONOPS_PASSWORD'),
                            help='Password used for AxonOps Self-Hosted when authentication is enabled')
        parser.add_argument('--url', type=str, default=os.getenv('AXONOPS_URL'),
                            help='Specify the AxonOps URL if not using the AxonOps Cloud environment')

        parser.add_argument("-v", action='count', default=0, help="Verbosity")

        commands_subparser = parser.add_subparsers(help="commands")

        adaptive_repair_parser = commands_subparser.add_parser(
            "repair",
            help="Manage the Adaptive Repair in AxonOps")
        adaptive_repair_parser.set_defaults(func=self.run_adaptive_repair)

        adaptive_repair_parser.add_argument('--enabled', action='store_true',
                            help='Enables AxonOps Adaptive Repair')

        adaptive_repair_parser.add_argument('--disabled', action='store_true',
                            help='Disable AxonOps Adaptive Repair')

        parsed_result: argparse.Namespace = parser.parse_args(args=argv)

        # if func() is not present it means that no command was inserted
        if hasattr(parsed_result, 'func'):
            parsed_result.func(parsed_result)
        else:
            parser.print_help()

    def run_adaptive_repair(self, args):
        if args.v:
            print(f"Running repairs on {args.org}")
            print(args)

        if not args.org or not args.cluster:
            print("The org and the cluster are mandatory")
            sys.exit(1)

        if args.enabled and args.disabled:
            print("The option enabled and disabled are mutually exclusive, you can't choose both at the same time.")
            sys.exit(1)

        if not args.enabled and not args.disabled:
            print("At least one option enabled or disabled should be present.")
            sys.exit(1)

        url = f"{Application.adaptive_repair_url}/{args.org}/cassandra/{args.cluster}"

        payload = {
            'Active': args.enabled,
            # 'GcGraceThreshold': requested_setting['gc_grace'],
            # 'TableParallelism': requested_setting['parallelism'],
            # 'BlacklistedTables': requested_setting['blacklisted'],
            # 'FilterTWCSTables': requested_setting['filter_twcs'],
            # 'SegmentRetries': requested_setting['retries']
        }

        if args.v:
            print("POST", url, payload)

        axonops = AxonOps(args.org,
                          api_token=args.token,
                          base_url=args.url,
                          username=args.username,
                          password=args.password,
                          cluster_type=args.cluster)

        axonops.do_request(
            url=url,
            method='POST',
            json_data=payload,
        )