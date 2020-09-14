#! /usr/bin/env python3
import boto3
import arrow
from config import REGIONS, CF_STACK_OLD_DAYS
from pprint import pprint
from datetime import timedelta


def scan():
    limit = timedelta(days=CF_STACK_OLD_DAYS)
    now = arrow.utcnow()

    for region in REGIONS:
        client = boto3.client("cloudformation", region_name=region)

        response = client.describe_stacks()
        stacks = response["Stacks"]

        if not stacks:
            print("Found no CF stacks in {}".format(region))
            continue

        print("Found {} CF stacks in {}".format(len(stacks), region))
        old = []
        for s in stacks:
            # Stacks without a 'LastUpdatedTime' key are new and therefore
            # now-now generates a ago of 0
            age = now - s.get("LastUpdatedTime", now)
            if age > limit:
                last_updated = "Never"
                if s.get("LastUpdatedTime"):
                    last_updated = arrow.get(s["LastUpdatedTime"]).humanize()
                print("  - {:<50} (Last updated: {}, State: {})".format(s["StackName"], last_updated, s["StackStatus"]))


if __name__ == "__main__":
    scan()
