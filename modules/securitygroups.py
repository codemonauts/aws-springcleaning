#! /usr/bin/env python3
from helper import get_all_instances, get_all_rds, get_all_sg, get_elb_sg
import crayons


def scan():
    used_groups = []

    for instance in get_all_instances():
        attached = [sg["GroupId"] for sg in instance["SecurityGroups"]]
        used_groups.extend(attached)

    for db in get_all_rds():
        attached = [sg["VpcSecurityGroupId"] for sg in db["VpcSecurityGroups"]]
        used_groups.extend(attached)

    all_sg = get_all_sg()
    elb_sg = get_elb_sg()
    print("Found {} security groups".format(len(all_sg)))

    not_used = []
    for group in all_sg:
        id = group["GroupId"]
        if id not in used_groups:
            if len(elb_sg) > 0:
                if id not in elb_sg:
                    not_used.append(group)
            else:
                not_used.append(group)

    for sg in all_sg:
        flags = []
        if sg in not_used:
            flags.append(crayons.yellow(" Not used"))
        if world_open(group):
            flags.append(crayons.red(" World Open"))
        if sg["GroupName"].find("launch-wizard") != -1:
            flags.append(crayons.red(" DefaultName"))
        if sg["GroupName"].startswith("packer_"):
            flags.append(crayons.red(" Packer"))
        if len(flags) > 0:
            suffix = ",".join([str(f) for f in flags])
            print("  - {} ({}) {}".format(sg["GroupId"], sg["GroupName"], suffix))


def world_open(group):
    rules = group["IpPermissions"]
    for r in rules:
        cidr = [x["CidrIp"] for x in r["IpRanges"]]
        cidr6 = [x["CidrIp"] for x in r["Ipv6Ranges"]]
        if "0.0.0.0/0" in cidr or "::/0" in cidr6:
            return True

    return False


if __name__ == "__main__":
    scan()
