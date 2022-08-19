#! /usr/bin/env python3
from helper import get_all_instances, get_all_rds, get_all_sg, get_all_elbs
import crayons
import boto3
import config


def scan():
    not_used = []
    flags = []

    response = get_all_elbs()
    for ELB in response['LoadBalancerDescriptions']:
        if len(ELB['Instances']) == 0:
            not_used.append(ELB['LoadBalancerName'])
            flags.append(crayons.yellow(" Not used"))

    for elb in not_used:
        if len(flags) > 0:
            suffix = ",".join([str(f) for f in flags])
            print("  - {} {}".format(elb, suffix))


if __name__ == "__main__":
    scan()

