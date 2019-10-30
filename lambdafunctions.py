#! /usr/bin/env python3
import boto3
import arrow
import crayons
from config import REGIONS

OUTDATED = ["nodejs8.10", "python2.7", "python3.6"]


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
            if f["Runtime"] in OUTDATED:
                runtime = crayons.red(f["Runtime"])
            else:
                runtime = f["Runtime"]
            print(
                "  - {:<50} (Last modified: {}, {})".format(f["FunctionName"], last_modified, runtime))


if __name__ == "__main__":
    scan()
