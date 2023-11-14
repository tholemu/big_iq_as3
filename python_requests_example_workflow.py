# BIG-IQ AS3 Workflow via Requests

import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

endpoint            = os.getenv("ENDPOINT")
username            = os.getenv("USERNAME")
password            = os.getenv("PASSWORD")
global_app_name     = "Juice_Shop"
uri_auth            = "/mgmt/shared/authn/login"
uri_device_stats    = "/mgmt/shared/diagnostics/device-stats"
uri_as3_declare     = "/mgmt/shared/appsvcs/declare"
uri_config_sets     = "/mgmt/cm/global/config-sets/"
uri_merge_move      = "/mgmt/cm/global/global-apps-merge-move"
auth_data           = {"username":username,"password":password,"loginProviderName":"tmos"}

### Authorization

r_auth = requests.post("https://" + endpoint + uri_auth,
                       data=json.dumps(auth_data), verify=False)
auth_token = r_auth.json()["token"]["token"]
headers = {"X-F5-Auth-Token": auth_token}

### Stats Collection

# r_stats = requests.get("https://" + endpoint + uri_device_stats,
#                        headers=headers, verify=False)

# for stat in r_stats.json()["entries"]:
#     print(f"{stat}: {r_stats.json()['entries'][stat]}")

###

input("Press enter to deploy Juice Shop")

### Deploy Juice Shop to BIG-IP instance 02a

with open("juice-shop/juice-shop_02a.json") as file:
    juice_shop_02a = file.read()
    juice_shop_02a = json.loads(juice_shop_02a)

# Get the configSetName value from the AS3 declaration
#
# The declaration object has a number of keys we know
# will always exist, and one key which is the dynamic
# name for the tenant. The pre-existing keys are populated
# within the declaration_exemptions list. Iterating over the
# declaration object and looking for a key which does not
# match anything in declaration_exemptions will provide us
# with the dynamic tenant name.
declaration_exemptions = ["class","schemaVersion","id","label","remark","target"]
for key in juice_shop_02a["declaration"]:
    if key not in declaration_exemptions:
        tenant_name = key

# We then do something similar within the tenant object,
# but it should only have two keys: 'class' and the
# application object, whose key value is the application name.
for key in juice_shop_02a["declaration"][tenant_name]:
    if key != "class":
        application_name = key

# Set the configSetName
# Format: {tenant_name}_{application_name}
config_set_name = f"{tenant_name}_{application_name}"

# Make the POST request to deploy the AS3 declaration to instance 02a
r_juice_shop_02a = requests.post("https://" + endpoint + uri_as3_declare,
                                 data=json.dumps(juice_shop_02a), headers=headers, verify=False)
print(f"r_juice_shop_02a: {r_juice_shop_02a.json()}")

### Deploy Juice Shop to BIG-IP instance 02b

with open("juice-shop/juice-shop_02b.json") as file:
    juice_shop_02b = file.read()
    juice_shop_02b = json.loads(juice_shop_02b)

r_juice_shop_02b = requests.post("https://" + endpoint + uri_as3_declare,
                                 data=json.dumps(juice_shop_02b), headers=headers, verify=False)
print(f"r_juice_shop_02b: {r_juice_shop_02b.json()}")

### Get the app config set

uri_config_set_query = f"?$filter=configSetName eq '{config_set_name}'"
config_sets = requests.get("https://" + endpoint + uri_config_sets + uri_config_set_query,
                           headers=headers, verify=False)
if len(config_sets.json()["items"]) > 0:
    config_set_self_link = config_sets.json()["items"][0]["selfLink"]
app_move_content = {}
app_move_content["componentAppReferencesToMove"] = [{"link": config_set_self_link}]
app_move_content["targetGlobalAppName"] = global_app_name
app_move_content["deleteEmptyGlobalAppsWhenDone"] = False
app_move_content["requireNewGlobalApp"] = True
print(f"app_move_content: {app_move_content}")
r_juice_shop_move = requests.post("https://" + endpoint + uri_merge_move,
                                  data=json.dumps(app_move_content), headers=headers, verify=False)

###

input("Press enter to delete Juice Shop from BIG-IP 02A")

### Delete Juice Shop from BIG-IP instance 02a

with open("juice-shop/juice-shop_delete_02a.json") as file:
    juice_shop_delete_02a = file.read()
    juice_shop_delete_02a = json.loads(juice_shop_delete_02a)

r_juice_shop_delete_02a = requests.post("https://" + endpoint + uri_as3_declare,
                                        data=json.dumps(juice_shop_delete_02a), headers=headers, verify=False)
print(f"r_juice_shop_02a: {r_juice_shop_delete_02a.json()}")

###

input("Press enter to delete Juice Shop from BIG-IP 02B")

### Delete Juice Shop from BIG-IP instance 02b

with open("juice-shop/juice-shop_delete_02b.json") as file:
    juice_shop_delete_02b = file.read()
    juice_shop_delete_02b = json.loads(juice_shop_delete_02b)

r_juice_shop_delete_02b = requests.post("https://" + endpoint + uri_as3_declare,
                                        data=json.dumps(juice_shop_delete_02b),headers=headers, verify=False)
print(f"r_juice_shop_02b: {r_juice_shop_delete_02b.json()}")

###

### Testing

# big_data = ""
# for i in range(0,20):
#     big_data += juice_shop_02a
# for i in range(0,100):
#     r = requests.post("http://10.1.10.200", data=json.dumps(big_data))

# to watch traffic on the BIG-IP: tcpdump -X -nni 0.0 host 10.1.10.200