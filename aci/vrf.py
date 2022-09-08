import requests
from getToken import getToken


def getAllVRF(tenant_name):
    url = "https://sandboxapicdc.cisco.com/api/node/mo/uni/tn-{}.json?query-target=subtree&target-subtree-class=fvCtx".format(tenant_name)
    vrfs = requests.get(url, cookies={ "Apic-cookie": getToken()}, verify=False).json()
    return vrfs


def getVRF(tenant_name, vrf_name):
    vrfs = getAllVRF(tenant_name)
    targetVRF = []

    for vrf in vrfs["imdata"]:
        if vrf["fvCtx"]["attributes"]["name"] == vrf_name:
            targetVRF.append(vrf["fvCtx"]["attributes"]["name"])
    
    if vrf_name in targetVRF:
        print("Your VRF: '" + vrf_name + "' is present on the APIC")
    else:
        print("Your VRF: '" + vrf_name + "' cannot be found on the APIC")


def vrf(tenant_name, vrf_name, status):
    url = "https://sandboxapicdc.cisco.com/api/node/mo/uni/tn-{}.json".format(tenant_name)

    payload = {
        "fvCtx": {
            "attributes": {
                "name": vrf_name,
                "status": status                # Either created or deleted
            }
        }
    }

    requests.post(url, json=payload, cookies={ "Apic-cookie": getToken() }, verify= False).json()
    getVRF(tenant_name, vrf_name)