#! /usr/bin/env python3
import boto3
from pprint import pprint


def scan():
    client = boto3.client("s3")

    response = client.list_buckets()
    buckets = response["Buckets"]

    if not buckets:
        print("Found no S3 buckets")
        return

    print("Found {} S3 buckets".format(len(buckets)))

    for b in buckets:
        name = b["Name"]
        list_of_files = []
        try:
            r = client.list_objects_v2(Bucket=name, MaxKeys=1)
            list_of_files = r.get("Contents", [])
        except:
            print("ERROR")
            pprint(r)

        if len(list_of_files) == 0:
            print("  - {:<50} (Empty)".format(name))


if __name__ == "__main__":
    scan()
