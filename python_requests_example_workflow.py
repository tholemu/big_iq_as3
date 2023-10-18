# BIG-IQ AS3 Workflow via Requests

import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

endpoint = os.getenv("ENDPOINT")
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")

uri_auth = "mgmt/shared/authn/login"
uri_device_stats = "mgmt/shared/diagnostics/device-stats"
uri_as3_declare = "mgmt/shared/appsvcs/declare"
auth_data = {"username":username, "password":password, "loginProviderName":"tmos"}

r_auth = requests.post(endpoint + uri_auth, data=json.dumps(auth_data), verify=False)
auth_token = r_auth.json()["token"]["token"]

headers = {"X-F5-Auth-Token": auth_token}

r_stats = requests.get(endpoint + uri_device_stats, headers=headers, verify=False)

for stat in r_stats.json()["entries"]:
    print(f"{stat}: {r_stats.json()['entries'][stat]}")

with open("west-app-22.json") as file:
    declaration = file.read()
    declaration = json.loads(declaration)

r_as3_declare = requests.post(endpoint + uri_as3_declare, data=json.dumps(declaration), headers=headers, verify=False)

input("press enter to delete the declaration")

with open("west-app-22-delete.json") as file:
    declaration = file.read()
    declaration = json.loads(declaration)

r_as3_declare = requests.post(endpoint + uri_as3_declare, data=json.dumps(declaration), headers=headers, verify=False)
