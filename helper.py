#! /usr/bin/env python3
import boto3
import config


def get_all_instances(region=None):
    if not region:
        region = config.REGIONS

    instances = []
    for region in config.REGIONS:
        client = boto3.client('ec2', region_name=region)
        data = client.describe_instances()
        for res in data["Reservations"]:
            instances.extend(res["Instances"])

    return instances


def get_all_rds(region=None):
    if not region:
        region = config.REGIONS

    databases = []
    for region in config.REGIONS:
        client = boto3.client('rds', region_name=region)
        data = client.describe_db_instances()
        databases.extend(data["DBInstances"])

    return databases


def get_all_sg(region=None):
    if not region:
        region = config.REGIONS

    groups = []
    for region in config.REGIONS:
        client = boto3.client('ec2', region_name=region)
        data = client.describe_security_groups()
        groups.extend(data["SecurityGroups"])

    return groups
