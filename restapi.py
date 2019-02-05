import requests
import sys
import json
import os
import tabulate

vmanage_host = os.environ.get("vmanage_host")
vmanage_port = os.environ.get("vmanage_port")
username = os.environ.get("username")
password = os.environ.get("password")


if vmanage_host is None or vmanage_port is None or username is None or password is None:
    print("vManage details must be set via environment variables. For example: ")
    print("export vmanage_host=sdwandemo.cisco.com")
    print("export vmanage_port=8443")
    print("export username=demo")
    print("export password=demo")
    exit()

requests.packages.urllib3.disable_warnings()

class rest_api_lib:
    def __init__(self, vmanage_host,vmanage_port, username, password):
        self.vmanage_host = vmanage_host
        self.vmanage_port = vmanage_port
        self.session = {}
        self.login(self.vmanage_host, username, password)

    def login(self, vmanage_host, username, password):
        
        """Login to vmanage"""

        base_url = 'https://%s:%s/'%(self.vmanage_host, self.vmanage_port)

        login_action = '/j_security_check'

        #Format data for loginForm
        login_data = {'j_username' : username, 'j_password' : password}

        #Url for posting login data
        login_url = base_url + login_action
        url = base_url + login_url

        sess = requests.session()

        #If the vmanage has a certificate signed by a trusted authority change verify to True
        login_response = sess.post(url=login_url, data=login_data, verify=False)

    
        if b'<html>' in login_response.content:
            print ("Login Failed")
            sys.exit(0)

        self.session[vmanage_host] = sess

    def get_request(self, mount_point):
        """GET request"""
        url = "https://%s:%s/dataservice/%s"%(self.vmanage_host, self.vmanage_port, mount_point)
      
        response = self.session[self.vmanage_host].get(url, verify=False)
        data = response.content
        return data

    def post_request(self, mount_point, payload, headers={'Content-type': 'application/json', 'Accept': 'application/json'}):
        """POST request"""
        url = "https://%s:%s/dataservice/%s"%(self.vmanage_host, self.vmanage_port, mount_point)
        payload = json.dumps(payload)
        print (payload)

        response = self.session[self.vmanage_host].post(url=url, data=payload, headers=headers, verify=False)
        data = response.json()
        return data


#Create session with vmanage 

vmanage_session = rest_api_lib(vmanage_host, vmanage_port, username, password)

#print(vmanage_session)

#application and vpn id

application_name = 'office365'
vpn_id = '1'

response = json.loads(vmanage_session.get_request("template/cloudx/status?appName=%s&vpnId=%s"%(application_name,vpn_id)))


items = response['data']

# fetch table headers using the items dictionary keys. 

if items:
    headers = list(items[0].keys())
else:
    headers = list()

table = list()

for item in items:
    tr = list(item.values())
    table.append(tr)

try:
    print(tabulate.tabulate(table, headers, tablefmt="fancy_grid"))
except UnicodeEncodeError:
    print(tabulate.tabulate(table, headers, tablefmt="grid"))


