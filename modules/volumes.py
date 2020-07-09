#! /usr/bin/env python3
from helper import get_all_volumes
from config import REGIONS
import boto3
import crayons


def scan():
    for region in REGIONS:
        client = boto3.client("ec2", region_name=region)
        response = client.describe_volumes()
        if "Volumes" in response and len(response["Volumes"]) > 0:
            print("Found {} volumes in {}".format(len(response["Volumes"]), region))
        else:
            print("Found no volumes in {}".format(region))

        available = [v for v in response["Volumes"] if v["State"] == "available"]
        if len(available):
            print("{} of them are not in use".format(crayons.red(len(available))))
            for v in available:
                print("  - {} ({})".format(v["VolumeId"], v["AvailabilityZone"]))
        else:
            print("All are in use")


if __name__ == "__main__":
    scan()
