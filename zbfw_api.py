#!/usr/bin/env python

import requests
import sys
import json
import os

from requests.packages.urllib3.exceptions import InsecureRequestWarning

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

        #print(sess.cookies)
    
        if b'<html>' in login_response.content:
            print ("Login Failed")
            sys.exit(0)

        self.session[vmanage_host] = sess

    def get_request(self, mount_point):
        """GET request"""
        url = "https://%s:%s/dataservice/%s"%(self.vmanage_host, self.vmanage_port, mount_point)
      
        response = self.session[self.vmanage_host].get(url, verify=False)
        
        return response

    def post_request(self, mount_point, payload, headers={'Content-type': 'application/json', 'Accept': 'application/json'}):
        """POST request"""
        url = "https://%s:%s/dataservice/%s"%(self.vmanage_host, self.vmanage_port, mount_point)
        #print(url)
        payload = json.dumps(payload)

        response = self.session[self.vmanage_host].post(url=url, data=payload, headers=headers, verify=False)

        return response


#Create session with vmanage 

vmanage_session = rest_api_lib(vmanage_host, vmanage_port, username, password)

fw_inspect_payload = {"aggregation":{"metrics":[{"property":"fw_total_insp_count","type":"sum","order":"desc"}],"histogram":{"property":"entry_time","type":"minute","interval":30,"order":"asc"}},"query":{"condition":"AND","rules":[{"value":["24"],"field":"entry_time","type":"date","operator":"last_n_hours"},{"value":["total"],"field":"type","type":"string","operator":"in"}]}}

fw_drop_payload = {"aggregation":{"metrics":[{"property":"fw_total_drop_count","type":"sum","order":"desc"}],"histogram":{"property":"entry_time","type":"minute","interval":30,"order":"asc"}},"query":{"condition":"AND","rules":[{"value":["24"],"field":"entry_time","type":"date","operator":"last_n_hours"},{"value":["total"],"field":"type","type":"string","operator":"in"}]}}

fw_inspect_response = vmanage_session.post_request("statistics/fwall/aggregation",fw_inspect_payload)

fw_drop_response = vmanage_session.post_request("statistics/fwall/aggregation",fw_drop_payload)

inspect_count = fw_inspect_response.json()['data']

print("\nFirewall Inspect count\n\n")
print(inspect_count)

drop_count = fw_drop_response.json()['data']

print("\nFirewall Drop count\n\n")
print(drop_count)
