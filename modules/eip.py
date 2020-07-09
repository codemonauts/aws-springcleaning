#! /usr/bin/env python3
import arrow
import crayons
from config import REGIONS
import boto3
from pprint import pprint


def scan():

    for region in REGIONS:
        client = boto3.client("ec2", region_name=region)
        resp = client.describe_addresses()
        addresses = resp.get("Addresses")
        if len(addresses):
            print("Found {} elastic IPs in {}".format(len(addresses), region))
        else:
            print("Found no elastic IPs in {}".format(region))
            continue

        for addr in addresses:
            if "AssociationId" not in addr:
                print(f"  - {addr['AllocationId']} ({addr['PublicIp']}) {crayons.red('not in use')}")
