#! /usr/bin/env python3
import boto3
import arrow
import crayons
from config import REGIONS

LATEST = [
    "dotnetcore3.1",
    "java11",
    "go1.x",
    "nodejs14.x",
    "python3.8",
    "ruby2.7",
]

OTHER = [
    "dotnetcore2.1",
    "java8",
    "java8.al2",
    "nodejs10.x",
    "nodejs12.x",
    "python3.7",
    "python3.6",
    "ruby2.5",
]


def scan():
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
            if f["Runtime"] in LATEST:
                runtime = f["Runtime"]
            elif f["Runtime"] in OTHER:
                runtime = crayons.yellow(f["Runtime"])
            else:
                runtime = crayons.red(f["Runtime"])
            print("  - {:<50} (Last modified: {}, {})".format(f["FunctionName"], last_modified, runtime))


if __name__ == "__main__":
    scan()
