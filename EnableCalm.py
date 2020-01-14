#!/usr/bin/env python3

import requests as r
import json as j
import getpass

PE = input("Prism Element: ")
username = input("Username: ")
password = getpass.getpass(prompt="Password: ")
headers = {"content-type": "application/json"}

r.packages.urllib3.disable_warnings()

response = r.get('https://' + PE + ':9440/PrismGateway/services/rest/v2.0/vms/',
    verify = False,
    auth = (username, password),
    headers = headers)

output = j.loads(response.text)
nvm = output["metadata"]["count"]
x = 0

while x < nvm:
    vmname = output["entities"][x]["name"]
    vmpowerstate = output["entities"][x]["power_state"]

    # Get PC address
    if output["entities"][x]["name"] == "RXAutomationPC":
        pc_uuid = output["entities"][x]["uuid"]
        pc_json = j.loads(r.get('https://' + PE + '\
        :9440/PrismGateway/services/rest/v2.0/vms/' + pc_uuid + '\
        ?include_vm_nic_config=true',
            verify = False,
            auth = (username, password),
            headers = headers).text)
        pc_ip = pc_json["vm_nics"][0]["ip_address"]

    x = x + 1

PC = pc_ip

# Enable CALM on Prism Central IP
# Currently commented out to not clutter PC events

payload = dict(state='ENABLE', enable_nutanix_apps=True)

r.post('https://' + PC + ':9440/api/nutanix/v3/services/nucalm',
    verify = False,
    auth = (username, password),
    json = payload,
    headers = headers)
