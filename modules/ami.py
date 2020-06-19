#! /usr/bin/env python3
import boto3
import crayons
from config import REGIONS
from helper import get_all_instances, get_account_id


def scan():
    account_id = get_account_id()

    for region in REGIONS:
        # Filter only for our own images
        ami_list = boto3.client("ec2", region_name=region).describe_images(Owners=[account_id])["Images"]
        print("Found {} AMIs in {}".format(len(ami_list), region))

        used_images = []
        if len(ami_list):
            instances = get_all_instances([region])
            for i in instances:
                used_images.append(i["ImageId"])

        unused_images = []
        for ami in ami_list:
            if ami["ImageId"] not in used_images:
                unused_images.append(ami)
        if len(unused_images):
            print("{} of them are not in use:".format(crayons.red(len(unused_images))))
            for ami in unused_images:
                print("  - {:<30} ({})".format(ami["ImageId"], ami["Name"]))


if __name__ == "__main__":
    scan()
