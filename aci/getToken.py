import requests, urllib3

def getToken():
    urllib3.disable_warnings()
    url = "https://sandboxapicdc.cisco.com/api/aaaLogin.json"

    payload = {
        "aaaUser" : {
            "attributes" : {
                "name" : "admin",
                "pwd" : "!v3G@!4@Y"
            }
        }
    }

    headers = { "Accept": "application/json" }

    resp = requests.post(url, json=payload, headers=headers, verify=False).json()
    return resp["imdata"][0]["aaaLogin"]["attributes"]["token"]