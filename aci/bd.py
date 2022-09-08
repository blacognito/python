import requests
from getToken import getToken


def getAllBD(tenant_name):
    url = "https://sandboxapicdc.cisco.com/api/node/mo/uni/tn-{}.json?query-target=subtree&target-subtree-class=fvBD".format(tenant_name)
    bds = requests.get(url, cookies={ "Apic-cookie": getToken() }, verify= False).json()
    return bds

def getBD(tenant_name, bd_name):
    bds = getAllBD(tenant_name)
    targetBD = []

    for bd in bds["imdata"]:
        if bd["fvBD"]["attributes"]["name"] == bd_name:
            targetBD.append(bd["fvBD"]["attributes"]["name"])
    
    if bd_name in targetBD:
        print("Your BD: '" + bd_name + "' is present on the APIC")
    else:
        print("Your BD: '" + bd_name + "' is NOT present on the APIC")


def bd(tenant_name, bd_name, status):
    url = "https://sandboxapicdc.cisco.com/api/node/mo/uni/tn-{}.json".format(tenant_name)

    payload = {
        "fvBD": {
            "attributes": {
                "name": bd_name,
                "status": status                # Either created or deleted
            }
        }
    }

    requests.post(url, json=payload, cookies={ "Apic-cookie": getToken() }, verify= False).json()
    getBD(tenant_name, bd_name)