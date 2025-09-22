import argparse
from axonopscli.axonops import AxonOps

class AdaptiveRepair:
    """
    This class manages the logic for the adaptive repair.
    """
    adaptive_repair_url = "/api/v1/adaptiveRepair"

    def __init__(self, args: argparse.Namespace, axonops: AxonOps):
        self.args = args
        self.axonops = axonops
        self.repair_data = None
        self.full_url = f"{self.adaptive_repair_url}/{args.org}/cassandra/{args.cluster}"

    def get_actual_repair(self):
        if self.repair_data is None:
            if self.args.v:
                print("Getting actual repair")
                print("GET", self.full_url)

            self.repair_data = self.axonops.do_request(
            url=self.full_url,
            method='GET',
        )
        return self.repair_data

    def check_repair_status(self):
        """ Check if the repair is failing and why"""
        if not  self.repair_data['Ready']:
            print("The repair is not ready")
            if self.repair_data['NotReadyReason']:
                print("Reason:",self.repair_data['NotReadyReason'])

    def check_repair_active(self):
        """ Check if the repair needs to be enabled/disabled"""
        if self.args.v:
            print("Actual", self.repair_data['Active']) 
            print("Enabled", self.args.enabled)
            print("Disabled", self.args.disabled)

        if not self.repair_data['Active'] and self.args.enabled:
            print("The repair is currently disabled, it needs to be enabled. Enabling it")
            self.repair_data['Active'] = True

        if self.repair_data['Active'] and self.args.disabled:
            print("The repair is currently enabled, it needs to be disabled. Disabling it")
            self.repair_data['Active'] = False

    def set_repair(self):
        # payload = {
        #     'Active': self.args.enabled,
        #     'Ready': self.repair_data['Ready'],
        #     'NotReadyReason': self.repair_data['NotReadyReason'],
        #     'GcGraceThreshold': self.repair_data['GcGraceThreshold'],
        #     'SegmentsPerVnode': self.repair_data['SegmentsPerVnode'],
        #     'TableParallelism': self.repair_data['TableParallelism'],
        #     'SegmentRetries': self.repair_data['SegmentRetries'],
        #     'BlacklistedTables': self.repair_data['BlacklistedTables'],
        #     'FilterTWCSTables': self.repair_data['FilterTWCSTables'],
        #     'SegmentTargetSizeMB': self.repair_data['SegmentTargetSizeMB'],
        #     'SkipPaxos': self.repair_data['SkipPaxos'],
        #     'PaxosOnly': self.repair_data['PaxosOnly'],
        #     'OptimiseStreams': self.repair_data['OptimiseStreams'],
        #     'MaxSegmentsPerTable': self.repair_data['MaxSegmentsPerTable'],
        # }
        # print(self.repair_data)

        if self.args.v:
            print("POST", self.full_url, self.repair_data)

        self.axonops.do_request(
            url=self.full_url,
            method='POST',
            json_data=self.repair_data,
        )

    