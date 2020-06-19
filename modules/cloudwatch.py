#! /usr/bin/env python3
import boto3
import crayons
from config import REGIONS


def scan():

    for region in REGIONS:
        client = boto3.client("logs", region_name=region)

        response = client.describe_log_groups()
        log_groups = response["logGroups"]

        if not log_groups:
            print("Found no log groups in {}".format(region))
            return
        else:
            print("Found {} log groups in {}".format(len(log_groups), region))

        for group in log_groups:
            show = False
            if group.get("retentionInDays"):
                retention = "{}d".format(group["retentionInDays"])
            else:
                show = True
                retention = crayons.red("Never")

            if group.get("storedBytes"):
                size = "{} bytes".format(group["storedBytes"])
            else:
                show = True
                size = crayons.yellow("Empty")

            if show:
                print("  - {:<50} (Expire: {}, Size: {})".format(group["logGroupName"], retention, size))


if __name__ == "__main__":
    scan()
