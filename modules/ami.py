#! /usr/bin/env python3
import boto3
import crayons
from config import REGIONS
from helper import get_all_instances, get_account_id


def scan():
    account_id = get_account_id()

    for region in REGIONS:
        # Filter only for our own images
        ec2_client = boto3.client("ec2", region_name=region)
        ami_list = ec2_client.describe_images(Owners=[account_id])["Images"]
        if len(ami_list):
            print("Found {} AMIs in {}".format(len(ami_list), region))
        else:
            print("Found no AMIs in {}".format(len(ami_list), region))
            continue

        used_images = []

        # Get all running instances
        instances = get_all_instances([region])
        for i in instances:
            used_images.append(i["ImageId"])

        # Get all launch templates
        resp = ec2_client.describe_launch_templates()
        templates = resp.get("LaunchTemplates")
        for t in templates:
            resp = ec2_client.describe_launch_template_versions(LaunchTemplateName=t["LaunchTemplateName"])
            try:
                used_images += [v["LaunchTemplateData"]["ImageId"] for v in resp["LaunchTemplateVersions"]]
            except KeyError:
                # Launchtemplates does not need to have a preconfigured AMI
                pass

        unused_images = []
        for ami in ami_list:
            if ami["ImageId"] not in used_images:
                unused_images.append(ami)

        if len(unused_images) > 0:
            print("{} of them are not in use:".format(crayons.red(len(unused_images))))
            for ami in unused_images:
                print("  - {:<22} ({})".format(ami["ImageId"], ami["Name"]))


if __name__ == "__main__":
    scan()
