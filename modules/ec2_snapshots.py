#! /usr/bin/env python3
from helper import get_all_volumes, get_account_id
from config import EC2_SNAPSHOT_OLD_DAYS, REGIONS
from datetime import timedelta
import boto3
import arrow
import crayons


def scan():
    account_id = get_account_id()
    limit = timedelta(days=EC2_SNAPSHOT_OLD_DAYS)
    now = arrow.utcnow()

    for region in REGIONS:

        volumes = get_all_volumes([region])
        available_volume_ids = [v["VolumeId"] for v in volumes]

        snapshot_list = boto3.client("ec2", region_name=region).describe_snapshots(OwnerIds=[account_id])["Snapshots"]
        print("Found {} snapshots in {}".format(len(snapshot_list), region))

        old = []
        no_vol = []
        for snap in snapshot_list:
            source_volume = snap["VolumeId"]
            if source_volume not in available_volume_ids:
                no_vol.append(snap)

            age = now - snap["StartTime"]
            if age > limit:
                old.append(snap)

        if len(no_vol):
            print("{} snapshots exist for non-existing volumes:".format(crayons.red(len(no_vol))))
            for i in no_vol:
                print("    - {}".format(i["SnapshotId"]))

        if len(old):
            print("{} are older than {} days".format(crayons.red(len(old)), EC2_SNAPSHOT_OLD_DAYS))
            for i in old:
                create_time = arrow.get(i["StartTime"]).humanize()
                print("  - {:<22} (Created {})".format(i["SnapshotId"], create_time))


if __name__ == "__main__":
    scan()
