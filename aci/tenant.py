import requests
from getToken import getToken


def getAllTenants():
    url = "https://sandboxapicdc.cisco.com/api/node/class/fvTenant.json"
    tenants = requests.get(url, cookies={ "Apic-cookie": getToken() }, verify=False).json()
    return tenants


def getTenant(tenant_name):
    tenants = getAllTenants()
    targetTenant = []

    for tenant in tenants["imdata"]:
        targetTenant.append(tenant["fvTenant"]["attributes"]["name"])
    
    if tenant_name in targetTenant:
        print("Your tenant: '" + tenant_name + "' is present on the APIC")
    else:
        print("Your tenant: '" + tenant_name + "' is not present on the APIC")


def tenant(tenant_name, status):
    url = "https://sandboxapicdc.cisco.com/api/mo/uni.json"

    payload = {
        "fvTenant": {
            "attributes": {
                "name": tenant_name,
                "status": status        # Either 'created' or 'deleted'
            }
        }
    }

    requests.post(url, json=payload, cookies={"Apic-cookie": getToken()}, verify=False).json()
    getTenant(tenant_name)