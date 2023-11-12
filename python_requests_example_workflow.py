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
print(f"r_auth: {r_auth.json()}")
auth_token = r_auth.json()["token"]["token"]

headers = {"X-F5-Auth-Token": auth_token}

r_stats = requests.get(endpoint + uri_device_stats, headers=headers, verify=False)

for stat in r_stats.json()["entries"]:
    print(f"{stat}: {r_stats.json()['entries'][stat]}")

input("Press enter to deploy Juice Shop to BIG-IP 02A the declaration")

# with open("west-app-22.json") as file:
with open("juice-shop/juice-shop_02a.json") as file:
    juice_shop_02a = file.read()
    juice_shop_02a = json.loads(juice_shop_02a)

r_juice_shop_02a = requests.post(endpoint + uri_as3_declare, data=json.dumps(juice_shop_02a), headers=headers, verify=False)
print(f"r_juice_shop_02: {r_juice_shop_02a.json()}")

input("Press enter to deploy Juice Shop to BIG-IP 02B")

with open("juice-shop/juice-shop_02b.json") as file:
    juice_shop_02b = file.read()
    juice_shop_02b = json.loads(juice_shop_02b)

r_juice_shop_02b = requests.post(endpoint + uri_as3_declare, data=json.dumps(juice_shop_02b), headers=headers, verify=False)
print(f"r_juice_shop_02: {r_juice_shop_02b.json()}")

input("Press enter to delete Juice Shop from BIG-IP 02A")

with open("juice-shop/juice-shop_delete_02a.json") as file:
    juice_shop_delete_02a = file.read()
    juice_shop_delete_02a = json.loads(juice_shop_delete_02a)

r_as3_declare = requests.post(endpoint + uri_as3_declare, data=json.dumps(juice_shop_delete_02a), headers=headers, verify=False)

input("Press enter to delete Juice Shop from BIG-IP 02B")

with open("juice-shop/juice-shop_delete_02b.json") as file:
    juice_shop_delete_02b = file.read()
    juice_shop_delete_02b = json.loads(juice_shop_delete_02a)

r_as3_declare = requests.post(endpoint + uri_as3_declare, data=json.dumps(juice_shop_delete_02b), headers=headers, verify=False)
