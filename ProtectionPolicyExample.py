#!/usr/bin/env python3

import requests
import json

username = "admin"
password = "*********"
prism_central = "IP or FQDN"
payload = '{"kind":"vm"}'
headers = {"content-type": "application/json"}

requests.packages.urllib3.disable_warnings()

response = requests.post('https://' + prism_central + ':9440/api/nutanix/v3/vms/list',
    verify = False,
    auth = (username, password),
    data = payload,
    headers = headers)

output = json.loads(response.text)

nvm = output["metadata"]["total_matches"]

vm = [item for item in output["entities"]
    if item["metadata"]["kind"] == "vm"]

x = 0

print('{0:25} : {1:26} : {2:17}'.format('Virtual Machine', 'Protection Status', 'Cluster'))
print('-'*74)

while x < nvm:
    print('{0:25} : {1:26} : {2:17}'.format(vm[x]["status"]["name"],
        vm[x]["status"]["resources"]["protection_type"],
	vm[x]["spec"]["cluster_reference"]["name"]))
    x = x+1
