#! /usr/bin/env python3
import arrow
import crayons
from config import REGIONS, EC2_OLD_DAYS
from datetime import timedelta
from helper import get_all_instances


def scan(showEverything=False):
    now = arrow.utcnow()
    limit = timedelta(days=EC2_OLD_DAYS)

    for region in REGIONS:
        instances = get_all_instances([region])

        if instances:
            print("Found {} EC2 instances in {}".format(len(instances), region))
        else:
            print("Found no EC2 instances in {}".format(len(instances), region))
            continue  # to next region

        if showEverything:
            for i in instances:
                name = [t["Value"] for t in i["Tags"] if t["Key"] == "Name"][0]
                if i["State"]["Name"] == "stopped":
                    print("  - {:<50} (Stopped)".format(name))
                else:
                    launch_time = arrow.get(i["LaunchTime"]).humanize()
                    print("  - {:<50} (Started {})".format(name, launch_time))
        else:
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
                print("{} instances are stopped:".format(crayons.red(len(stopped))))
                for i in stopped:
                    name = [t["Value"] for t in i["Tags"] if t["Key"] == "Name"][0]
                    print("  - {:<50}".format(name))

            if len(old):
                print("{} old instances are still running:".format(crayons.red(len(old))))
                for i in old:
                    name = [t["Value"] for t in i["Tags"] if t["Key"] == "Name"][0]
                    launch_time = arrow.get(i["LaunchTime"]).humanize()
                    print("  - {:<50} (Started {})".format(name, launch_time))


if __name__ == "__main__":
    scan()
