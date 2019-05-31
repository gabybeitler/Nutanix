#!/usr/bin/env python3

import requests
import json

username = "admin"
password = PASSWORD
payload = '{"kind":"vm"}'
headers = {"content-type": "application/json"}

requests.packages.urllib3.disable_warnings()

response = requests.post('https://aaa.bbb.ccc.ddd:9440/api/nutanix/v3/vms/list',
    verify = False,
    auth = (username, password),
    data = payload,
    headers = headers)

output = json.loads(response.text)

nvm = output["metadata"]["total_matches"]

vm = [item for item in output["entities"]
    if item["metadata"]["kind"] == "vm"]

x = 0

print('{0:15} : {1:36} : {2:17}'.format('Virtual Machine', 'UUID', 'MAC'))
print('-'*74)

while x < nvm:
    print('{0:15} : {1:36} : {2:17}'.format(vm[x]["spec"]["name"],
        vm[x]["metadata"]["uuid"],
	vm[x]["spec"]["resources"]["nic_list"][0]["mac_address"]))
    x = x+1
