#! /usr/bin/env python3
from helper import get_all_volumes
import crayons


def scan(showEverything=False):
    volumes = get_all_volumes()
    print("Found {} volumes accross all regions".format(len(volumes)))
    if showEverything:
        for v in volumes:
            print("  - {} ({})".format(v["VolumeId"], v["AvailabilityZone"]))
    else:
        available = [v for v in volumes if v["State"] == "available"]
        if len(available):
            print("{} of them are not in use".format(crayons.red(len(available))))
            for v in available:
                print("  - {} ({})".format(v["VolumeId"], v["AvailabilityZone"]))
        else:
            print("All are in use")


if __name__ == "__main__":
    scan()
