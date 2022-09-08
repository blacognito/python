import requests
from getToken import getToken


def getAllEPG(tenant_name, ap_name):
    url = 'https://sandboxapicdc.cisco.com/api/node/mo/uni/tn-{}/ap-{}.json?query-target=subtree&target-subtree-class=fvAEPg'.format(tenant_name, ap_name)
    epgs = requests.get(url, cookies={ 'Apic-cookie': getToken() }, verify=False).json()
    return epgs   


def getEPG(epg_name, tenant_name, ap_name):
    epgs = getAllEPG(tenant_name, ap_name)
    targetEPG = []

    for epg in epgs["imdata"]:
        if epg["fvAEPg"]["attributes"]["name"] == epg_name:
            targetEPG.append(epg["fvAEPg"]["attributes"]["name"])
    
    if epg_name in targetEPG:
        print("Your EPG: '" + epg_name + "' is present on the APIC")
    else:
        print("Your EPG: '" + epg_name + "' is NOT present on the APIC")


def epg(epg_name, tenant_name, ap_name, status):
    url = "https://sandboxapicdc.cisco.com/api/node/mo/uni/tn-{}/ap-{}.json".format(tenant_name, ap_name)

    payload = {
        "fvAEPg": {
            "attributes": {
                "name": epg_name,
                "status": status                # Either created or deleted
            }
        }
    }

    requests.post(url, json=payload, cookies={ "Apic-cookie": getToken() }, verify=False)
    getEPG(epg_name, tenant_name, ap_name)