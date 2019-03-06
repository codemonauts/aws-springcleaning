#! /usr/bin/env python3
import crayons
import helper
import config
import timeit

import ami
import ec2_snapshots
import ec2
import rds_snapshots
import securitygroups
import volumes

print("Starting full account scan for these Regions: {}".format(",".join(config.REGIONS)))
print("Account: {}".format(helper.get_account_id()))
input("Press return to start ...")

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


stop = timeit.default_timer()
runtime = int(stop-start)
print("Scan finished after {} seconds".format(crayons.yellow(runtime)))
