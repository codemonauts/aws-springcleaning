#! /usr/bin/env python3
import boto3
import arrow
from config import REGIONS
from pprint import pprint


def scan():
    for region in REGIONS:
        client = boto3.client("cloudformation", region_name=region)

        response = client.describe_stacks()
        stacks = response["Stacks"]

        if not stacks:
            print("Found no CF stacks in {}".format(region))
            continue

        print("Found {} CF stacks in {}".format(len(stacks), region))
        for s in stacks:
            last_updated = arrow.get(s["LastUpdatedTime"]).humanize()
            print("  - {:<50} (Last updated: {}, State: {})".format(s["StackName"], last_updated, s["StackStatus"]))


if __name__ == "__main__":
    scan()
