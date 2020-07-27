import requests
import json
import os

from requests.packages.urllib3.exceptions import InsecureRequestWarning

vmanage_host = os.environ.get("vmanage_host")
vmanage_port = os.environ.get("vmanage_port")
username = os.environ.get("username")
password = os.environ.get("password")

if vmanage_host is None or vmanage_port is None or username is None or password is None:
    print("For Windows Workstation, vManage details must be set via environment variables using below commands")
    print("set vmanage_host=198.18.1.10")
    print("set vmanage_port=443")
    print("set username=admin")
    print("set password=admin")
    print("For MAC OSX Workstation, vManage details must be set via environment variables using below commands")
    print("export vmanage_host=198.18.1.10")
    print("export vmanage_port=443")
    print("export username=admin")
    print("export password=admin")
    exit()

requests.packages.urllib3.disable_warnings()

class rest_api_lib:
    def __init__(self, vmanage_host,vmanage_port, username, password):
        self.vmanage_host = vmanage_host
        self.vmanage_port = vmanage_port
        self.session = {}
        self.login()

    def login(self):

        """Login to vmanage"""

        base_url = 'https://%s:%s/'%(vmanage_host,vmanage_port)

        login_action = 'j_security_check'

        #Format data for loginForm
        login_data = {'j_username' : username, 'j_password' : password}

        #URL for posting login data
        login_url = base_url + login_action
        
        #URL for retrieving client token
        token_url = base_url + 'dataservice/client/token'
        
        sess = requests.session()

        #If the vmanage has a certificate signed by a trusted authority change verify to True

        login_response = sess.post(url=login_url, data=login_data, verify=False)

        if b'<html>' in login_response.content:
            print ("Login Failed")
            exit(0)

        login_token  = sess.get(url=token_url, verify=False)

        if login_token.status_code == 200:
            if b'<html>' in login_token.content:
                print ("Login Token Failed")
                exit(0)

        #update token to session headers
        sess.headers['X-XSRF-TOKEN'] = login_token.content

        self.session[vmanage_host] = sess

    def get_request(self, mount_point):
        """GET request"""
        url = "https://%s:%s/dataservice/%s"%(self.vmanage_host, self.vmanage_port, mount_point)      
        response = self.session[self.vmanage_host].get(url, verify=False)
        
        return response

    def post_request(self, mount_point, payload, headers={'Content-type': 'application/json', 'Accept': 'application/json'}):
        """POST request"""
        url = "https://%s:%s/dataservice/%s"%(self.vmanage_host, self.vmanage_port, mount_point)
        payload = json.dumps(payload)
        response = self.session[self.vmanage_host].post(url=url, data=payload, headers=headers, verify=False)
        return response

vmanage_session = rest_api_lib(vmanage_host, vmanage_port, username, password)

acl_query_fields = vmanage_session.get_request("statistics/flowlog/fields")

print(json.dumps(acl_query_fields.json(), indent=4, sort_keys=True))

payload ={ "query" : {"condition": "AND", 
                      "rules":
                      [{"value":["24"],"field":"entry_time","type":"date","operator":"last_n_hours"},
                       {"value":["_vpn1_data"],"field":"policy_name","type":"string","operator":"in"},
                       {"value":["ge0/5"],"field":"egress_intf","type":"string","operator":"in"}]}}

acl_logs = vmanage_session.post_request("statistics/flowlog",payload)

print(json.dumps(acl_logs.json()['data'], indent=4, sort_keys=True))

