import requests
import http.client
import json

from requests_futures.sessions import FuturesSession

session = FuturesSession()


def onboard_application(ott):
    url = f"http://10.212.135.3:8561/api-invoker-management/v1/onboardedInvokers"
    headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer {ott}"
    }
    data = {
    "description": "Smart Glasses",
    "direction": "DL",
    "traffic": "TCP",
    "ipv4": "10.212.135.3",
    "port": 2222
    }

    response_data = session.post(url, headers=headers, json = data).json()
    client_id = response_data["apiInvokerId"]
    client_secret = response_data["onboardingInformation"]["onboardingSecret"]
    return (client_id, client_secret)

def get_token(client_id, client_secret):
    url = "http://10.212.135.3:31002/security/v1/token"
    headers = {
    "Content-Type": "application/json"
    }
    data = {
    "client_id": client_id,
    "client_secret": client_secret
    }

    response_data = requests.post(url, headers=headers, json=data).json()
    token = response_data["access_token"]
    return token
    
def get_access_token():
   conn = http.client.HTTPConnection("192.168.3.18", 31002)
   payload = json.dumps({
      "client_id": "7692ed28-9d0f-4a53-bf02-62f93ae51fd6",
      "client_secret": "zjvWd5iYm5r_rO0iz9mtg_XX5WMP1c2-rHbBLhHUiG0"
   })
   headers = {
      "Content-Type": "application/json"
   }
   conn.request("POST", "/security/v1/token", payload, headers)
   res = conn.getresponse()
   data = res.read()
   token_data = json.loads(data.decode("utf-8"))
   access_token = token_data.get("access_token")
   conn.close()
   return access_token
   
def invocation_bw(access_token):
    conn = http.client.HTTPConnection("192.168.3.18", 7999)
    payload = json.dumps({
        "device": {
            "deviceId": {device_id}
        },
        "maxBitRate": 400,
        "direction": "uplink",
        "duration": 10000
    })
    headers = {
        'Content-type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    conn.request("POST", "/qos/v1/bandwidth", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))
    conn.close()
   
   
def invocation_sw(access_token):
    conn = http.client.HTTPConnection("192.168.3.18", 7999)
    payload = json.dumps({
        "device": {
            "deviceId": {device_id}
        },
        "maxBitRate": 400,
        "direction": "uplink",
        "duration": 10000
    })
    headers = {
        'Content-type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    conn.request("POST", "/qos/v1/simswap", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))
    conn.close()
    
    
print(get_access_token())