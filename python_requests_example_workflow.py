# BIG-IQ AS3 Workflow via Requests

''' Testing procedure

big_data = ""
for i in range(0,20):
    big_data += juice_shop_02a
for i in range(0,100):
    r = requests.post("http://10.1.10.200", data=json.dumps(big_data))

to watch traffic on the BIG-IP: tcpdump -X -nni 0.0 host 10.1.10.200

'''

import os
import requests
import json
from dotenv import load_dotenv

# Silence HTTPS verification warning messages
requests.packages.urllib3.disable_warnings()

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
uri_global_apps     = "/mgmt/cm/global/global-apps/"
uri_waf_policies    = "/mgmt/cm/asm/working-config/policies"
auth_data           = {"username":username,"password":password,"loginProviderName":"tmos"}

### Load AS3 declaration from file
def load_declaration(filename):
    with open(filename) as file:
        declaration = file.read()
        declaration = json.loads(declaration)
    return declaration

### Authorization
# def get_auth_token():
    # r_auth = requests.post("https://" + endpoint + uri_auth,
    #                     data=json.dumps(auth_data), verify=False)
    # r_auth = api_call("https://" + endpoint, "post", uri_auth, access_token=None,
    #                   data=json.dumps(auth_data))
    # auth_token = r_auth.json()["token"]["token"]
    # headers = {"X-F5-Auth-Token": auth_token}
    # return headers

### Stats Collection
# def get_device_stats():
#     r_stats = requests.get("https://" + endpoint + uri_device_stats,
#                         headers=headers, verify=False)

#     for stat in r_stats.json()["entries"]:
#         print(f"{stat}: {r_stats.json()['entries'][stat]}")


''' Perform BIG-IQ API Calls

Each workflow-specific function should leverage the api_call
function so that login / access token obtainment and REST 
method executions are handled consistently.

'''
def api_call(endpoint, method, uri, access_token, data=None):
    if method in ["get", "patch", "put", "post", "delete"]:
        headers = {"Content-Type": "application/json"}

        # If no access token is provided, attempt to obtain
        # one via the login process. Bail out if the login
        # attempt fails. Otherwise, continue on and perform
        # the respective REST method and return the
        # JSON response object
        if access_token != "":
            headers["Authorization"] = f"Bearer {access_token}"
        else:
            r = requests.post("https://" + endpoint + uri_auth,
                         data=json.dumps(auth_data), verify=False)
            if "token" in r.json().keys():
                auth_token = r.json()["token"]["token"]
                headers["X-F5-Auth-Token"] = auth_token
            else:
                status = r.json()["status"]
                return f"Authoriation failed with a {status} error"

        if method == "get":
            response = requests.get(f"https://{endpoint}{uri}", headers=headers, verify=False)
        elif method == "patch":
            response = requests.patch(f"https://{endpoint}{uri}", headers=headers, data=json.dumps(data), verify=False)
            print(response.json())
        elif method == "put":
            response = requests.put(f"https://{endpoint}{uri}", headers=headers, data=json.dumps(data), verify=False)
        elif method == "post":
            response = requests.post(f"https://{endpoint}{uri}", headers=headers, data=json.dumps(data), verify=False)
        elif method == "delete":
            response = requests.delete(f"https://{endpoint}{uri}", headers=headers, verify=False)

        return response.status_code, response.json()
    else:
        return 400, f"Invalid method '{method}'"

def post_declaration(declaration):
    status_code, r = api_call(endpoint=endpoint, method="post", uri=uri_as3_declare, access_token="",
                             data=declaration)
    
    print(f"post_declaration POST body: {r}")
    
    print(f"post_declaration POST status_code: {status_code}")

    if status_code == 200:
        return True, r["declaration"]["id"]
    else:
        return False, r

def get_config_sets(config_set_name):
    uri_config_set_query = f"?$filter=configSetName eq '{config_set_name}'"
    status_code, r = api_call(endpoint=endpoint, method="get", uri=uri_config_sets+uri_config_set_query,
                           access_token="")
    print(f"get_config_sets GET status_code: {status_code}")
    
    if len(r["items"]) > 0:
        config_set_self_link = r["items"][0]["selfLink"]

    app_move_content = {}
    app_move_content["componentAppReferencesToMove"] = [{"link": config_set_self_link}]
    app_move_content["targetGlobalAppName"] = global_app_name
    app_move_content["deleteEmptyGlobalAppsWhenDone"] = False
    app_move_content["requireNewGlobalApp"] = True

    if status_code == 200:
        return True, app_move_content
    else:
        return False, r

# Get the configSetName value from the AS3 declaration
#
# The declaration object has a number of keys we know
# will always exist, and one key which is the dynamic
# name for the tenant. The pre-existing keys are populated
# within the declaration_exemptions list. Iterating over the
# declaration object and looking for a key which does not
# match anything in declaration_exemptions will provide us
# with the dynamic tenant name.
def get_config_set_name(declaration):
    declaration_exemptions = ["class","schemaVersion","id","label","remark","target"]
    for key in declaration["declaration"]:
        if key not in declaration_exemptions:
            tenant_name = key

    # We then do something similar within the tenant object,
    # but it should only have two keys: 'class' and the
    # application object, whose key value is the application name.
    for key in declaration["declaration"][tenant_name]:
        if key != "class":
            application_name = key

    # Set the configSetName
    # Format: {tenant_name}_{application_name}
    config_set_name = f"{tenant_name}_{application_name}"
    return config_set_name

def move_application(app_move_content):
    status_code, r = api_call(endpoint=endpoint, method="post", uri=uri_merge_move, access_token="", data=app_move_content)
    print(f"move_application POST status code: {status_code}")

    if status_code == 200:
        return True, r
    else:
        return False, r

def get_global_app_id():
    status_code, r = api_call(endpoint=endpoint, method="get", uri="//mgmt/cm/global/global-apps", access_token="")
    print(f"get_global_app_id status code: {status_code}")
    for item in r["items"]:
        if item["name"] == global_app_name:
            global_app_id = item["id"]

    if status_code == 200:
        print(f"global_app_id: {global_app_id}")
        return True, global_app_id
    else:
        return False, r

def delete_global_app(id):
    status_code, r = api_call(endpoint=endpoint, method="delete", uri=uri_global_apps + id, access_token="")
    print(f"delete_global_app DELETE status code: {status_code}")

    if status_code == 200:
        return True, r
    else:
        return False, r

def main():

    input("Press enter to deploy Juice Shop\n")

    print("Loading Juice Shop 02 deployment declaration")
    juice_shop_02_dec = load_declaration("juice-shop/juice-shop_02a.json")
    print("Loading Juice Shop 02 deployment declaration")
    juice_shop_02_waf_dec = load_declaration("juice-shop/juice-juice-shop_02_waf.json")

    print("Deploying Juice Shop 02 deployment declaration")
    juice_shop_02_created, juice_shop_02 = post_declaration(juice_shop_02_dec)
    print(f"juice_shop_02_created: {juice_shop_02_created}\n")

    print("Getting configSetName")
    config_set_name = get_config_set_name(juice_shop_02_dec)
    print(f"config_set_name: {config_set_name}\n")

    print("Generating app move content")
    app_moved, app_move_content = get_config_sets(config_set_name)

    print("Moving Juice Shop to dedicated application space\n")
    move_application(app_move_content)

    input("Press enter to deploy Juice Shop with a WAF policy\n")

    print("Deploying Juice Shop 02 WAF declaration")
    juice_shop_02_waf_created, juice_shop_02_waf = post_declaration(juice_shop_02_waf_dec)
    print(f"juice_shop_02_waf_created: {juice_shop_02_waf_created}\n")

    input("Press enter to delete Juice Shop deployment\n")

    print("Loading Juice Shop 02 deletion declaration")
    juice_shop_02_delete_dec = load_declaration("juice-shop/juice-shop_delete_02a.json")

    print("Deleting Juice Shop 02a")
    juice_shop_02_deleted, juice_shop_02_delete = post_declaration(juice_shop_02_delete_dec)
    print(f"juice_shop_02_deleted: {juice_shop_02_deleted}\n")

    print("Getting global app ID")
    global_app_id_retrieved, global_app_id = get_global_app_id()

    print(f"Deleting global app '{global_app_name}'")
    delete_global_app(global_app_id)


main()