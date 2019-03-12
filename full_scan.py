#! /usr/bin/env python3
import crayons
import helper
import config
import timeit
from datetime import datetime

import ami
import ec2_snapshots
import ec2
import rds_snapshots
import securitygroups
import volumes
import lambdafunctions
import cloudwatch


print("Starting full account scan for these Regions: {}".format(",".join(config.REGIONS)))
print("Account: {}".format(helper.get_account_id()))
print("Start date: {}".format(datetime.now()))

start = timeit.default_timer()

print(crayons.yellow('Scanning AMIs'))
ami.scan()

print(crayons.yellow('Scanning EC2 instances'))
ec2.scan()

print(crayons.yellow('Scanning EC2 volumes'))
volumes.scan()

print(crayons.yellow('Scanning EC2 snapshots'))
ec2_snapshots.scan()

print(crayons.yellow('Scanning RDS snapshots'))
rds_snapshots.scan()

print(crayons.yellow('Scanning security groups'))
securitygroups.scan()

print(crayons.yellow('Scanning CloudWatch loggroups'))
cloudwatch.scan()

print(crayons.yellow('Scanning Lambda functions'))
lambdafunctions.scan()


stop = timeit.default_timer()
runtime = int(stop-start)
print("Scan finished after {} seconds".format(crayons.yellow(runtime)))
