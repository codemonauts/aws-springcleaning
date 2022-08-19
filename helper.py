#! /usr/bin/env python3
import boto3
import config


def get_all_instances(region_list=None):
    if not region_list:
        region_list = config.REGIONS

    instances = []
    for region in region_list:
        client = boto3.client("ec2", region_name=region)
        data = client.describe_instances()
        for res in data["Reservations"]:
            instances.extend(res["Instances"])

    return instances


def get_all_rds(region=None):
    if not region:
        region = config.REGIONS

    databases = []
    for region in config.REGIONS:
        client = boto3.client("rds", region_name=region)
        data = client.describe_db_instances()
        databases.extend(data["DBInstances"])

    return databases


def get_all_sg(region=None):
    if not region:
        region = config.REGIONS

    groups = []
    for region in config.REGIONS:
        client = boto3.client("ec2", region_name=region)
        data = client.describe_security_groups()
        groups.extend(data["SecurityGroups"])

    return groups


def get_all_volumes(region=None):
    if not region:
        region = config.REGIONS

    volumes = []
    for region in config.REGIONS:
        client = boto3.client("ec2", region_name=region)
        data = client.describe_volumes()
        volumes.extend(data["Volumes"])

    return volumes


def get_account_id():
    return boto3.client("sts").get_caller_identity().get("Account")


def get_all_regions():
    ec2 = boto3.client("ec2")
    response = ec2.describe_regions()
    regions = response["Regions"]
    return [r["RegionName"] for r in regions]


def get_elb_sg(region=None):
    if not region:
        region = config.REGIONS
    elb_sg = []
    for region in config.REGIONS:
        client = boto3.client("elb", region_name=region)
        data = client.describe_load_balancers()
        for elbDesc in data["LoadBalancerDescriptions"]:
            elb_sg.extend(elbDesc["SecurityGroups"])
    return elb_sg


def get_all_elbs(region=None):
    if not region:
        region = config.REGIONS
    data = ""
    for region in config.REGIONS:
        client = boto3.client("elb", region_name=region)
        data = client.describe_load_balancers()
    return data
