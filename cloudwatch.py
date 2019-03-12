#! /usr/bin/env python3
import boto3
from config import REGIONS


def scan(showEverything=False):

    for region in REGIONS:
        client = boto3.client("logs", region_name=region)

        response = client.describe_log_groups()
        log_groups = response["logGroups"]

        if not log_groups:
            print("Found no log groups in {}".format(region))
            return
        else:
            print("Found {} log groups in {}".format(len(log_groups), region))

        if showEverything:
            for group in log_groups:
                if group.get("retentionInDays"):
                    retention = "{}d".format(group["retentionInDays"])
                else:
                    retention = "Never"
                print(
                    "  - {:<50} (Expire: {})".format(group["logGroupName"], retention))


if __name__ == "__main__":
    scan()
