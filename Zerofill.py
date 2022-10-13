import datetime
import os
import sys
import subprocess

list_blcks = subprocess.Popen(["lsblk"], stdout=subprocess.PIPE)  ## Run lsblk in bash
list_blcks = list_blcks.stdout.readlines()  ## Read lsblk from bash
print("Available Blocks: \n %d", list_blcks)  ## Print list_blcks +...
for line in list_blcks:  ## ...per line lsblk
    print(line.decode().strip())

print(
    "Zerofill block or partition\n\nEx: Input: sda1 \n\nBlock or partition input: "
)  ## Ask input block
blck = input()  ## Grab input for blck
print(f"\nIs {blck} correct? [y/n]\n")  ## Print question
valid = input()  ## Grab input for valid
if (
    valid == "n" or valid == "no" or valid == "N" or valid == "NO"
):  ## Simple filters for typos
    sys.exit(1)  ## End process with EC 1
    
lin = f"date:{datetime.date.today()}, user:{os.path.expanduser('~')}, block:sd{blck}\n"
    
with open(f"./Log-{datetime.date.today()}",mode="w") as temp:
    var = temp.write(lin)

zerofill = subprocess.Popen(
    [
        "sudo",
        "dd",
        "if=/dev/zero",
        "of=/dev/sd{}",
        "status=progress",
        "bs=16M".format(blck),
    ],
    stdout=subprocess.PIPE,
    stdin=subprocess.PIPE,
)  ## Runs dd in bash with given args
zerofill.wait()  ## Wait for termination of zerofill
sync = subprocess.Popen(["sync"], stdout=subprocess.PIPE)  ## Run sync in bash

print("\n------------------------\n         END\n------------------------\n")
