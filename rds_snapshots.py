#! /usr/bin/env python3
from config import REGIONS
import boto3
import crayons
import arrow
from datetime import timedelta
from config import RDS_SNAPSHOT_OLD_DAYS


def scan(showEverything=False):
    limit = timedelta(days=RDS_SNAPSHOT_OLD_DAYS)
    now = arrow.utcnow()

    for region in REGIONS:
        client = boto3.client("rds", region_name=region)
        snapshot_list = client.describe_db_snapshots()["DBSnapshots"]

        if len(snapshot_list):
            print("Found {} RDS snapshots in {}".format(len(snapshot_list), region))

        if showEverything:
            for i in snapshot_list:
                create_time = arrow.get(i["SnapshotCreateTime"]).humanize()
                print("  - {:<30} (Created {})".format(i["DBSnapshotIdentifier"], create_time))
        else:
            old = []
            for snap in snapshot_list:
                age = now - snap["SnapshotCreateTime"]
                if age > limit:
                    old.append(snap)

            if len(old):
                print("{} are old".format(crayons.red(len(old))))
                for i in old:
                    create_time = arrow.get(i["SnapshotCreateTime"]).humanize()
                    print("  - {:<30} (Created {})".format(i["DBSnapshotIdentifier"], create_time))


if __name__ == "__main__":
    scan()
