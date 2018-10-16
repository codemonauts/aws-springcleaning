#! /usr/bin/env python3
from helper import get_all_instances, get_all_rds, get_all_sg


def clean_securitygroups():
    used_groups = []

    for instance in get_all_instances():
        attached = [sg["GroupId"] for sg in instance["SecurityGroups"]]
        used_groups.extend(attached)

    for db in get_all_rds():
        attached = [sg["VpcSecurityGroupId"] for sg in db["VpcSecurityGroups"]]
        used_groups.extend(attached)

    all_sg = get_all_sg()

    print("Found {} security groups".format(len(all_sg)))

    not_used = []
    for group in all_sg:
        id = group["GroupId"]
        if id not in used_groups:
            not_used.append(group)

    if len(not_used):
        print("{} of them seem to be not in use".format(len(not_used)))
        for sg in not_used:
            print("    - {} ({})".format(sg["GroupId"], sg["GroupName"]))
    else:
        print("All of them appear to be in use")


if __name__ == "__main__":
    clean_securitygroups()
