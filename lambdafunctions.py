#! /usr/bin/env python3
import boto3
import arrow
from config import REGIONS


def scan(showEverything=False):
    for region in REGIONS:
        client = boto3.client("lambda", region_name=region)

        response = client.list_functions()
        functions = response["Functions"]

        if not functions:
            print("Found no lambda functions in {}".format(region))
            continue

        print("Found {} lambda functions in {}".format(len(functions), region))
        for f in functions:
            last_modified = arrow.get(f["LastModified"]).humanize()
            print(
                "  - {:<50} (Last modified: {})".format(f["FunctionName"], last_modified))


if __name__ == "__main__":
    scan()
