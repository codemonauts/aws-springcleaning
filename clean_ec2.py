#! /usr/bin/env python3
import arrow
from config import REGIONS, EC2_OLD_DAYS
from datetime import timedelta
from helper import get_all_instances


def clean_ec2():
    now = arrow.utcnow()
    limit = timedelta(days=EC2_OLD_DAYS)

    for region in REGIONS:
        instances = get_all_instances([region])

        if instances:
            print("> Found {} instances in {}".format(len(instances), region))
        else:
            continue  # to next region

        stopped = []
        old = []
        for i in instances:
            if i["State"]["Name"] == "stopped":
                stopped.append(i)
                continue

            age = now - i["LaunchTime"]
            if age > limit:
                old.append(i)

        if len(stopped):
            print("  {} instances are stopped:".format(len(stopped)))
            for i in stopped:
                name = [t["Value"] for t in i["Tags"] if t["Key"] == "Name"][0]
                launch_time = arrow.get(i["LaunchTime"]).humanize()
                print("    - {}".format(name))

        if len(old):
            print("  {} old instances are still running:".format(len(old)))
            for i in old:
                name = [t["Value"] for t in i["Tags"] if t["Key"] == "Name"][0]
                launch_time = arrow.get(i["LaunchTime"]).humanize()
                print("    - {} (Started {})".format(name, launch_time))


if __name__ == "__main__":
    clean_ec2()
