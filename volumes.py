#! /usr/bin/env python3
from helper import get_all_volumes
import crayons


def scan():
    volumes = get_all_volumes()
    print("Found {} volumes accross all regions".format(len(volumes)))
    available = [v for v in volumes if v["State"] == "available"]
    if len(available):
        print("{} of them are not in use".format(crayons.red(len(available))))
        for v in available:
            print("  - {} ({})".format(v["VolumeId"], v["AvailabilityZone"]))
    else:
        print("All are in use")


if __name__ == "__main__":
    scan()
