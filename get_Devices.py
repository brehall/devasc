import requests
from requests.auth import HTTPBasicAuth
#from dnac_config import DNAC, DNAC_PORT, DNAC_USER, DNAC_PASSWORD

def get_auth_token():
    """
    Used to get Auth Token from DNAC
    """
    url = "https://sandboxdnac.cisco.com/dna/system/api/v1/auth/token"
    username = "devnetuser"
    password = "Cisco123!"
    resp = requests.post(url, auth=HTTPBasicAuth(username, password))
    token = resp.json()['Token']
    #print("Token Retrieved: {}".format(token))
    return token

def get_device_list():
    """
    Building out function to retrieve list of devices. Using requests.get to make a call to the network device Endpoint
    """
    token = get_auth_token() # Get Token
    url = "https://sandboxdnac.cisco.com/api/v1/network-device"
    hdr = {'x-auth-token': token, 'content-type' : 'application/json'}
    querystring = {"macAddress":"f8:7b:20:67:62:80", "managementIpAddress":"10.10.22.66"}
    resp = requests.get(url, headers=hdr)  # Make the Get Request.  If a filter is required, add params=querystring
    device_list = resp.json()
    print_device_list(device_list)

def print_device_list(device_json):
    print("{0:42}{1:17}{2:12}{3:18}{4:12}{5:16}{6:15}".
          format("hostname", "mgmt IP", "serial","platformId", "SW Version", "role", "Uptime"))
    for device in device_json['response']:
        uptime = "N/A" if device['upTime'] is None else device['upTime']
        if device['serialNumber'] is not None and "," in device['serialNumber']:
            serialPlatformList = zip(device['serialNumber'].split(","), device['platformId'].split(","))
        else:
            serialPlatformList = [(device['serialNumber'], device['platformId'])]
        for (serialNumber, platformId) in serialPlatformList:
            print("{0:42}{1:17}{2:12}{3:18}{4:12}{5:16}{6:15}".
                  format(device['hostname'],
                         device['managementIpAddress'],
                         serialNumber,
                         platformId,
                         device['softwareVersion'],
                         device['role'], uptime))

if __name__ == "__main__":
    get_device_list()

#token = get_auth_token()
#url = "https://sandboxdnac.cisco.com/dna/intent/api/v1/network-device/"
#header = {'x-auth-token': token, 'content-type': 'application/json'}
#resp = requests.get(url, headers=header)
#device_list = resp.json()
#print_device_list(device_list)

