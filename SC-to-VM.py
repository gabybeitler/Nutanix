#!/usr/bin/env python3


import requests
import json
import re

username = "admin"
password = ""
headers = {"content-type": "application/json"}
requests.packages.urllib3.disable_warnings()

# Let's get the Stoage Container Information for the API
response_sc = requests.get('https://<PE_IP>:9440/PrismGateway/services/rest/v2.0/storage_containers/',
    verify = False,
    auth = (username, password),
    headers = headers)

output_sc = json.loads(response_sc.text)

# Let's load the virtual disks from the API
response_vd = requests.get('https://<PE_IP>:9440/PrismGateway/services/rest/v2.0/virtual_disks/',
    verify = False,
    auth = (username, password),
    headers = headers)

output_vd = json.loads(response_vd.text)

# First let's see how many Storage Containers and virtual disks we have
nsc = output_sc["metadata"]["total_entities"]
nvd = output_vd["metadata"]["total_entities"]

# Loop through every Storage Container and assemble an array
sc = [item_sc for item_sc in output_sc["entities"]
    if item_sc["storage_container_uuid"] is not None]

# Create an empty disctionary and set the counter to zero
scs = {}
z = 0

# Loop through the Stoage Containers and populate the dictionary with
# key = container UUID and value = container name
while z < nsc:
    scs.update({sc[z]["storage_container_uuid"]:sc[z]["name"]})
    print(str(z + 1) + ". " + sc[z]["name"])
    z = z+1

# Ask the user to select which container to search
container = input("Please select a Storage Container [1-" + str(z) + "]: ")

# If the user chooses an entry that is higher than the choices force a choice
# TODO: trap non numeric values

while int(container) > int(z): #or bool(re.match("^([A-Z]+)+$", str(z))):
    container = input("Please select a Storage Container [1-" + str(z) + "]: ")

# hold the container UUID for the value the user selected
if int(container) <= int(z):
    container_id = list(scs.items())[int(container) - 1][0]

vd = [item_vd for item_vd in output_vd["entities"]
    if item_vd["uuid"] is not None]

# Create and empty list for virtual disks
vds = list()
y = 0

# Popluate the list with the virtual disks
while y < nvd:
    vds.append(tuple([vd[y]["storage_container_uuid"],vd[y]["attached_vmname"]]))
    y = y+1

# search for the contaniner ID in the list of virtual disks
matching = [s for s in vds if container_id in s]
x = 0

matching_vms = {}
# Loop through all the matching VMs in a contaniner and display the name of the VM
if len(matching) == 0:
    print("Sorry no vdisks exist in select container.")
else:
    while x < len(matching):
        matching_vms.update({matching[x][1]:x})
        x = x + 1

print(','.join([k for k in matching_vms.keys()]))
