import requests
from getToken import getToken


def getAllAP(tenant_name):
    url = "https://sandboxapicdc.cisco.com/api/node/mo/uni/tn-{}.json?query-target=subtree&target-subtree-class=fvAp".format(tenant_name)
    aps = requests.get(url, cookies={ "Apic-cookie": getToken() }, verify=False).json()
    return aps


def getAP(tenant_name, ap_name):
    aps = getAllAP(tenant_name)
    targetAP = []

    for ap in aps["imdata"]:
        if ap["fvAp"]["attributes"]["name"] == ap_name:
            targetAP.append(ap["fvAp"]["attributes"]["name"])
    
    if ap_name in targetAP:
        print("Your Application Profile: '" + ap_name + "' is present on the APIC")
    else:
        print("Your Application Profile: '" + ap_name + "' cannot be found on the APIC")


def ap(tenant_name, ap_name, status):
    url = "https://sandboxapicdc.cisco.com/api/node/mo/uni/tn-{}/ap-{}.json".format(tenant_name, ap_name)

    payload = {
        "fvAp": {
            "attributes": {
                "name": ap_name,
                "status": status            # Either created or deleted
            }
        }
    }

    requests.post(url, json=payload, cookies={ "Apic-cookie": getToken() }, verify=False)
    getAP(tenant_name, ap_name)